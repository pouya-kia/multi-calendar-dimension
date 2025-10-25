"""
Date Range Generator for monthly date ranges
تولید کننده بازه‌های ماهانه تاریخ
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Union, List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

from .dimension import DateDimensionGenerator, DateDimensionConfig
from ..converters.jalali import jalali_to_gregorian, gregorian_to_jalali, is_leap_year_persian
from ..converters.hijri import gregorian_to_hijri, hijri_to_gregorian
from ..converters.cross import jalali_to_hijri, hijri_to_jalali


class CalendarType(Enum):
    """Supported calendar types"""
    JALALI = "jalali"
    GREGORIAN = "gregorian"
    HIJRI = "hijri"


@dataclass
class DateRangeConfig:
    """Configuration for date range generation"""
    calendar_type: CalendarType
    start_year: int
    start_month: int
    end_year: int
    end_month: int
    include_events: bool = True
    include_holidays: bool = True
    include_week_calculations: bool = True
    output_format: str = 'dataframe'  # 'dataframe', 'excel', 'csv'


class DateRangeGenerator:
    """
    Generator for monthly date ranges across different calendars
    
    Supports generating date dimension tables for specific month ranges
    in Persian (Jalali), Gregorian, or Hijri calendars.
    """
    
    def __init__(self, config: DateRangeConfig):
        """
        Initialize the date range generator
        
        Args:
            config: Configuration object with range parameters
        """
        self.config = config
        self._validate_config()
    
    def _validate_config(self):
        """Validate the configuration parameters"""
        if self.config.start_year > self.config.end_year:
            raise ValueError("Start year cannot be greater than end year")
        
        if (self.config.start_year == self.config.end_year and 
            self.config.start_month > self.config.end_month):
            raise ValueError("Start month cannot be greater than end month when years are equal")
        
        if not (1 <= self.config.start_month <= 12):
            raise ValueError("Start month must be between 1 and 12")
        
        if not (1 <= self.config.end_month <= 12):
            raise ValueError("End month must be between 1 and 12")
    
    def _convert_to_jalali_range(self) -> Tuple[int, int, int, int]:
        """
        Convert the configured range to Jalali calendar range
        
        Returns:
            Tuple of (start_year, start_month, end_year, end_month) in Jalali
        """
        if self.config.calendar_type == CalendarType.JALALI:
            return (self.config.start_year, self.config.start_month,
                    self.config.end_year, self.config.end_month)
        
        elif self.config.calendar_type == CalendarType.GREGORIAN:
            # Convert Gregorian start date to Jalali
            start_jy, start_jm, start_jd = gregorian_to_jalali(
                self.config.start_year, self.config.start_month, 1
            )
            
            # Convert Gregorian end date to Jalali
            # Get last day of the month
            if self.config.end_month in [1, 3, 5, 7, 8, 10, 12]:
                last_day = 31
            elif self.config.end_month in [4, 6, 9, 11]:
                last_day = 30
            else:  # February
                last_day = 29 if self.config.end_year % 4 == 0 else 28
            
            end_jy, end_jm, end_jd = gregorian_to_jalali(
                self.config.end_year, self.config.end_month, last_day
            )
            
            return (start_jy, start_jm, end_jy, end_jm)
        
        elif self.config.calendar_type == CalendarType.HIJRI:
            # Convert Hijri start date to Jalali
            start_jy, start_jm, start_jd = hijri_to_jalali(
                self.config.start_year, self.config.start_month, 1
            )
            
            # Convert Hijri end date to Jalali
            # Hijri months have 29 or 30 days
            last_day = 30  # Use 30 as default for Hijri months
            end_jy, end_jm, end_jd = hijri_to_jalali(
                self.config.end_year, self.config.end_month, last_day
            )
            
            return (start_jy, start_jm, end_jy, end_jm)
        
        else:
            raise ValueError(f"Unsupported calendar type: {self.config.calendar_type}")
    
    def _get_month_range(self) -> List[Tuple[int, int]]:
        """
        Get list of (year, month) tuples for the configured range
        
        Returns:
            List of (year, month) tuples
        """
        start_jy, start_jm, end_jy, end_jm = self._convert_to_jalali_range()
        
        months = []
        current_year = start_jy
        current_month = start_jm
        
        while (current_year < end_jy or 
               (current_year == end_jy and current_month <= end_jm)):
            
            months.append((current_year, current_month))
            
            # Move to next month
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        
        return months
    
    def generate(self) -> pd.DataFrame:
        """
        Generate the date dimension table for the specified range
        
        Returns:
            DataFrame with date dimension data for the specified range
        """
        months = self._get_month_range()
        
        if not months:
            return pd.DataFrame()
        
        # Get the full year range
        start_year = months[0][0]
        end_year = months[-1][0]
        
        # Create a temporary config for the full year range
        temp_config = DateDimensionConfig(
            start_year=start_year,
            end_year=end_year,
            include_events=self.config.include_events,
            include_holidays=self.config.include_holidays,
            include_week_calculations=self.config.include_week_calculations,
            output_format=self.config.output_format
        )
        
        # Generate the full table
        generator = DateDimensionGenerator(temp_config)
        df = generator.generate()
        
        # Filter to only include the specified months
        month_filters = []
        for year, month in months:
            month_filters.append(
                (df['shamsi_year_id'] == year) & (df['shamsi_month_of_year_id'] == month)
            )
        
        if month_filters:
            # Combine all filters with OR
            combined_filter = month_filters[0]
            for filter_condition in month_filters[1:]:
                combined_filter = combined_filter | filter_condition
            
            df = df[combined_filter]
        
        return df
    
    def to_excel(self, filename: Optional[str] = None) -> str:
        """
        Export date range to Excel file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to created Excel file
        """
        df = self.generate()
        
        if filename is None:
            calendar_name = self.config.calendar_type.value
            filename = f"date_range_{calendar_name}_{self.config.start_year}_{self.config.start_month}_{self.config.end_year}_{self.config.end_month}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Date_Range', index=False)
        
        return filename
    
    def to_csv(self, filename: Optional[str] = None) -> str:
        """
        Export date range to CSV file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to created CSV file
        """
        df = self.generate()
        
        if filename is None:
            calendar_name = self.config.calendar_type.value
            filename = f"date_range_{calendar_name}_{self.config.start_year}_{self.config.start_month}_{self.config.end_year}_{self.config.end_month}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        return filename
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Get date range as DataFrame
        
        Returns:
            DataFrame with date range data
        """
        return self.generate()
    
    def get_summary(self) -> Dict[str, any]:
        """
        Get summary information about the date range
        
        Returns:
            Dictionary with summary statistics
        """
        df = self.generate()
        
        if df.empty:
            return {
                'total_days': 0,
                'start_date': None,
                'end_date': None,
                'calendar_type': self.config.calendar_type.value,
                'years_covered': 0,
                'months_covered': 0
            }
        
        return {
            'total_days': len(df),
            'start_date': df['shamsi_date_title'].iloc[0],
            'end_date': df['shamsi_date_title'].iloc[-1],
            'calendar_type': self.config.calendar_type.value,
            'years_covered': df['shamsi_year_id'].nunique(),
            'months_covered': df['shamsi_month_id'].nunique(),
            'holidays_count': df['shamsi_is_holiday'].sum() if 'shamsi_is_holiday' in df.columns else 0,
            'weekends_count': df['shamsi_is_weekend'].sum() if 'shamsi_is_weekend' in df.columns else 0
        }
