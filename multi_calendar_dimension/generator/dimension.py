"""
Date Dimension Generator
تولید کننده جدول Date Dimension برای تقویم‌های شمسی، میلادی و قمری
"""

import pandas as pd
from datetime import datetime, timedelta
import calendar
from typing import Optional, Union, List, Tuple
from dataclasses import dataclass

from ..converters.jalali import jalali_to_gregorian, gregorian_to_jalali, is_leap_year_persian
from ..converters.hijri import gregorian_to_hijri, hijri_to_gregorian
from ..converters.cross import jalali_to_hijri, hijri_to_jalali
from ..events import (
    persian_events, persian_holidays, hijri_official_holidays,
    gregorian_events_en, gregorian_events_fa, gregorian_holidays,
    hijri_events, hijri_events_en, hijri_holidays
)


@dataclass
class DateDimensionConfig:
    """Configuration for date dimension generation"""
    start_year: int
    end_year: int
    include_events: bool = True
    include_holidays: bool = True
    include_week_calculations: bool = True
    output_format: str = 'dataframe'  # 'dataframe', 'excel', 'csv'


class DateDimensionGenerator:
    """
    Generator for multi-calendar date dimension tables
    
    Supports Persian (Jalali), Gregorian, and Hijri calendars with
    comprehensive event and holiday information.
    """
    
    def __init__(self, config: DateDimensionConfig):
        """
        Initialize the date dimension generator
        
        Args:
            config: Configuration object with generation parameters
        """
        self.config = config
        self._setup_constants()
    
    def _setup_constants(self):
        """Setup constant dictionaries for month names and seasons"""
        self.persian_months = {
            1: "فروردین", 2: "اردیبهشت", 3: "خرداد", 4: "تیر",
            5: "مرداد", 6: "شهریور", 7: "مهر", 8: "آبان",
            9: "آذر", 10: "دی", 11: "بهمن", 12: "اسفند"
        }
        
        self.gregorian_months = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        
        self.hijri_months = {
            1: "محرم", 2: "صفر", 3: "ربیع الاول", 4: "ربیع الثانی",
            5: "جمادی الاول", 6: "جمادی الثانی", 7: "رجب", 8: "شعبان",
            9: "رمضان", 10: "شوال", 11: "ذی القعده", 12: "ذی حجه"
        }
        
        self.seasons = {
            1: "بهار", 2: "بهار", 3: "بهار",
            4: "تابستان", 5: "تابستان", 6: "تابستان",
            7: "پاییز", 8: "پاییز", 9: "پاییز",
            10: "زمستان", 11: "زمستان", 12: "زمستان"
        }
        
        self.half_years = {
            1: "نیمسال اول", 2: "نیمسال اول", 3: "نیمسال اول",
            4: "نیمسال اول", 5: "نیمسال اول", 6: "نیمسال اول",
            7: "نیمسال دوم", 8: "نیمسال دوم", 9: "نیمسال دوم",
            10: "نیمسال دوم", 11: "نیمسال دوم", 12: "نیمسال دوم"
        }
    
    def _day_of_week(self, gy: int, gm: int, gd: int) -> Tuple[str, str, int]:
        """
        Calculate day of week using Zeller's congruence
        
        Args:
            gy: Gregorian year
            gm: Gregorian month
            gd: Gregorian day
            
        Returns:
            Tuple of (Persian day name, English day name, day ID)
        """
        if gm < 3:
            gm += 12
            gy -= 1
        K, J = gy % 100, gy // 100
        h = (gd + (13*(gm + 1))//5 + K + (K//4) + (J//4) + (5*J)) % 7
        
        persian_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
        english_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
        return persian_days[h], english_days[h], h + 1
    
    def _get_variable_holidays(self, year: int) -> dict:
        """
        Calculate variable date holidays for a given year
        
        Args:
            year: Gregorian year
            
        Returns:
            Dictionary of (month, day) -> holiday status
        """
        holidays = {}
        
        # Martin Luther King Jr. Day (3rd Monday of January)
        mlk_day = self._nth_weekday_of_month(year, 1, 0, 3)
        holidays[(1, mlk_day)] = 1
        
        # Washington's Birthday (3rd Monday of February)
        washington_day = self._nth_weekday_of_month(year, 2, 0, 3)
        holidays[(2, washington_day)] = 1
        
        # Memorial Day (Last Monday of May)
        memorial_day = self._last_weekday_of_month(year, 5, 0)
        holidays[(5, memorial_day)] = 1
        
        # Labor Day (1st Monday of September)
        labor_day = self._nth_weekday_of_month(year, 9, 0, 1)
        holidays[(9, labor_day)] = 1
        
        # Columbus Day (2nd Monday of October)
        columbus_day = self._nth_weekday_of_month(year, 10, 0, 2)
        holidays[(10, columbus_day)] = 1
        
        # Thanksgiving Day (4th Thursday of November)
        thanksgiving_day = self._nth_weekday_of_month(year, 11, 3, 4)
        holidays[(11, thanksgiving_day)] = 1
        
        # Easter calculations
        easter = self._calculate_easter(year)
        good_friday = easter - timedelta(days=2)
        easter_monday = easter + timedelta(days=1)
        
        holidays[(good_friday.month, good_friday.day)] = 1
        holidays[(easter_monday.month, easter_monday.day)] = 1
        
        # UK Bank Holidays
        early_may_day = self._nth_weekday_of_month(year, 5, 0, 1)
        holidays[(5, early_may_day)] = 1
        
        spring_bank_day = self._last_weekday_of_month(year, 5, 0)
        holidays[(5, spring_bank_day)] = 1
        
        summer_bank_day = self._last_weekday_of_month(year, 8, 0)
        holidays[(8, summer_bank_day)] = 1
        
        return holidays
    
    def _nth_weekday_of_month(self, year: int, month: int, weekday: int, n: int) -> int:
        """Find the nth occurrence of a weekday in a month"""
        first_day = datetime(year, month, 1)
        first_weekday = first_day.weekday()
        days_to_add = (weekday - first_weekday) % 7 + (n - 1) * 7
        target_date = first_day + timedelta(days=days_to_add)
        return target_date.day
    
    def _last_weekday_of_month(self, year: int, month: int, weekday: int) -> int:
        """Find the last occurrence of a weekday in a month"""
        last_day = calendar.monthrange(year, month)[1]
        last_date = datetime(year, month, last_day)
        last_weekday = last_date.weekday()
        days_to_subtract = (last_weekday - weekday) % 7
        target_date = last_date - timedelta(days=days_to_subtract)
        return target_date.day
    
    def _calculate_easter(self, year: int) -> datetime:
        """Calculate Easter date using the algorithm"""
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return datetime(year, month, day)
    
    def _assign_monthly_weeks(self, df_month: pd.DataFrame) -> pd.DataFrame:
        """Assign week numbers within each month"""
        df_month = df_month.sort_values('shamsi_date').copy()
        is_saturday = (df_month['shamsi_day_of_week_id'] == 1)
        week_break = is_saturday.astype(int)
        if len(week_break) > 0:
            week_break.iloc[0] = 0
        df_month['week_num_in_month'] = 1 + week_break.cumsum()
        df_month['shamsi_week_id'] = df_month['shamsi_month_id'].astype(str) + '_' + df_month['week_num_in_month'].astype(int).astype(str)
        return df_month
    
    def _assign_yearly_weeks(self, df_year: pd.DataFrame) -> pd.DataFrame:
        """Assign week numbers within each year"""
        df_year = df_year.sort_values(['shamsi_month_id', 'shamsi_date']).copy()
        is_saturday = (df_year['shamsi_day_of_week_id'] == 1)
        week_break = is_saturday.astype(int)
        if len(week_break) > 0:
            week_break.iloc[0] = 0
        df_year['week_num_in_year'] = 1 + week_break.cumsum()
        return df_year
    
    def generate(self) -> pd.DataFrame:
        """
        Generate the complete date dimension table
        
        Returns:
            DataFrame with all date dimension columns
        """
        data = []
        
        for year in range(self.config.start_year, self.config.end_year + 1):
            # Get variable holidays for this year
            variable_holidays = self._get_variable_holidays(year)
            
            for month in range(1, 13):
                days_in_month = 31 if month <= 6 else (30 if month <= 11 else (30 if is_leap_year_persian(year) else 29))
                
                for day in range(1, days_in_month + 1):
                    # Convert Jalali to Gregorian
                    gy, gm, gd = jalali_to_gregorian(year, month, day)
                    persian_day, english_day, day_id = self._day_of_week(gy, gm, gd)
                    greg_date = datetime(gy, gm, gd)
                    
                    # Convert to Hijri
                    hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
                    
                    # Check holiday status
                    is_variable_holiday = variable_holidays.get((gm, gd), 0)
                    gregorian_holiday_status = gregorian_holidays.get((gm, gd), 0) or is_variable_holiday
                    
                    persian_holiday_status = persian_holidays.get((month, day), 0)
                    if day_id == 7:  # Friday (جمعه) - always holiday
                        persian_holiday_status = 1
                    
                    hijri_holiday_status = hijri_holidays.get((hm, hd), 0)
                    hijri_official_status = hijri_official_holidays.get((hm, hd), 0)
                    hijri_holiday_status = hijri_holiday_status or hijri_official_status
                    
                    # Calculate day of year for Persian calendar
                    shamsi_day_of_year = sum([
                        31 if m <= 6 else (30 if m <= 11 else (30 if is_leap_year_persian(year) else 29))
                        for m in range(1, month)
                    ]) + day
                    
                    # Get season for Gregorian calendar
                    get_season = lambda m: "Winter" if m in [12, 1, 2] else ("Spring" if m in [3, 4, 5] else ("Summer" if m in [6, 7, 8] else "Autumn"))
                    
                    row_data = {
                        'shamsi_date': int(f"{year:04d}{month:02d}{day:02d}"),
                        'miladi_date': f"{gy:04d}-{gm:02d}-{gd:02d}",
                        'miladi_day_of_week_title': english_day,
                        'shamsi_date_title': f"{year:04d}/{month:02d}/{day:02d}",
                        'shamsi_next_date': int(f"{year:04d}{month:02d}{day+1:02d}") if day < days_in_month else (int(f"{year:04d}{month+1:02d}01") if month < 12 else int(f"{year+1:04d}0101")),
                        'shamsi_month_id': int(f"{year:04d}{month:02d}"),
                        'shamsi_month_title': f"{self.persian_months[month]} {year}",
                        'shamsi_month_of_year_title': self.persian_months[month],
                        'shamsi_season_id': int(f"{year:04d}{month:02d}"),
                        'shamsi_season_title': f"{self.seasons[month]} {year}",
                        'shamsi_half_year_id': int(f"{year:04d}{month:02d}"),
                        'shamsi_half_year_title': f"{self.half_years[month]} {year}",
                        'shamsi_year_id': year,
                        'shamsi_month_of_year_id': month,
                        'shamsi_day_of_month_id': day,
                        'shamsi_day_of_year_id': shamsi_day_of_year,
                        'shamsi_day_of_week_title': persian_day,
                        'shamsi_day_of_week_id': day_id,
                        'shamsi_is_holiday': persian_holiday_status,
                        'shamsi_is_happy_holiday': persian_holiday_status,
                        'shamsi_is_sad_holiday': 0,
                        'shamsi_is_weekend': 1 if day_id in [6, 7] else 0,  # Thursday and Friday are weekends
                        'gregorian_next_date': (greg_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                        'gregorian_month_id': int(f"{gy:04d}{gm:02d}"),
                        'gregorian_month_title': f"{self.gregorian_months[gm]} {gy}",
                        'gregorian_month_of_year_title': self.gregorian_months[gm],
                        'gregorian_season_id': int(f"{gy:04d}{gm:02d}"),
                        'gregorian_season_title': f"{get_season(gm)} {gy}",
                        'gregorian_half_year_id': int(f"{gy:04d}{gm:02d}"),
                        'gregorian_half_year_title': f"{'H1' if gm <= 6 else 'H2'} {gy}",
                        'gregorian_year_id': gy,
                        'gregorian_month_of_year_id': gm,
                        'gregorian_day_of_month_id': gd,
                        'gregorian_day_of_year_id': greg_date.timetuple().tm_yday,
                        'gregorian_day_of_week_title': english_day,
                        'gregorian_day_of_week_id': (greg_date.weekday() + 2) % 7 + 1,
                        'gregorian_is_holiday': gregorian_holiday_status,
                        'gregorian_is_happy_holiday': gregorian_holiday_status,
                        'gregorian_is_sad_holiday': 0,
                        'gregorian_is_weekend': 1 if greg_date.weekday() in [5, 6] else 0,
                        'hijri_date': int(f"{hy:04d}{hm:02d}{hd:02d}"),
                        'hijri_date_title': f"{hy:04d}/{hm:02d}/{hd:02d}",
                        'hijri_month_id': int(f"{hy:04d}{hm:02d}"),
                        'hijri_month_title': f"{self.hijri_months[hm]} {hy}",
                        'hijri_month_of_year_title': self.hijri_months[hm],
                        'hijri_year_id': hy,
                        'hijri_month_of_year_id': hm,
                        'hijri_day_of_month_id': hd,
                        'hijri_is_holiday': hijri_holiday_status,
                        'hijri_is_happy_holiday': hijri_holiday_status,
                        'hijri_is_sad_holiday': 0,
                    }
                    
                    # Add events if enabled
                    if self.config.include_events:
                        row_data.update({
                            'shamsi_event_name': persian_events.get((month, day)),
                            'gregorian_event_name_en': gregorian_events_en.get((gm, gd)),
                            'gregorian_event_name_fa': gregorian_events_fa.get((gm, gd)),
                            'hijri_event_name': hijri_events.get((hm, hd)),
                            'hijri_event_name_en': hijri_events_en.get((hm, hd)),
                        })
                    
                    data.append(row_data)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Add week calculations if enabled
        if self.config.include_week_calculations:
            df = df.sort_values(['shamsi_month_id', 'shamsi_date']).groupby('shamsi_month_id', group_keys=False).apply(self._assign_monthly_weeks)
            df = df.groupby('shamsi_year_id', group_keys=False).apply(self._assign_yearly_weeks)
            df['shamsi_week_title'] = df.apply(lambda row: f"هفته {int(row['week_num_in_year'])} سال {int(row['shamsi_year_id'])}", axis=1)
            df['shamsi_week_of_year_id'] = df.apply(lambda row: f"{int(row['shamsi_year_id']):04d}_{int(row['week_num_in_year']):02d}", axis=1)
            
            # Gregorian week calculations
            dates = pd.to_datetime(df['miladi_date'])
            iso = dates.dt.isocalendar()
            df['gregorian_week_id'] = iso['week'].astype(int)
            df['gregorian_week_title'] = df.apply(lambda row: f"Week {row['gregorian_week_id']} {row['gregorian_year_id']}", axis=1)
            df['gregorian_week_of_year_id'] = df.apply(lambda row: f"{int(row['gregorian_year_id']):04d}_{int(row['gregorian_week_id']):02d}", axis=1)
            df['miladi_week_id'] = iso['week'].astype(int)
            df['miladi_week_num_in_month'] = df.groupby(dates.dt.to_period('M').astype(str))['miladi_week_id'].transform(lambda s: s.rank(method='dense').astype(int))
        
        return df
    
    def to_excel(self, filename: Optional[str] = None) -> str:
        """
        Export date dimension to Excel file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to created Excel file
        """
        df = self.generate()
        
        if filename is None:
            filename = f"date_dimension_{self.config.start_year}_{self.config.end_year}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Date_Dimension', index=False)
        
        return filename
    
    def to_csv(self, filename: Optional[str] = None) -> str:
        """
        Export date dimension to CSV file
        
        Args:
            filename: Output filename (optional)
            
        Returns:
            Path to created CSV file
        """
        df = self.generate()
        
        if filename is None:
            filename = f"date_dimension_{self.config.start_year}_{self.config.end_year}.csv"
        
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        return filename
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Get date dimension as DataFrame
        
        Returns:
            DataFrame with date dimension data
        """
        return self.generate()
