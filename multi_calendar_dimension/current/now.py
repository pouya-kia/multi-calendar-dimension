"""
Current Date Information
اطلاعات تاریخ امروز در همه تقویم‌ها
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from ..converters.jalali import gregorian_to_jalali, is_leap_year_persian
from ..converters.hijri import gregorian_to_hijri, is_hijri_leap
from ..converters.cross import jalali_to_hijri, hijri_to_jalali
from ..events import (
    persian_events, persian_holidays, hijri_official_holidays,
    gregorian_events_en, gregorian_events_fa, gregorian_holidays,
    hijri_events, hijri_events_en, hijri_holidays
)


@dataclass
class DateInfo:
    """Information about a specific date"""
    year: int
    month: int
    day: int
    date_string: str
    month_name: str
    day_of_week: str
    day_of_week_en: str
    is_leap_year: bool
    is_holiday: bool
    is_weekend: bool
    events: List[str]


@dataclass
class CurrentDateInfo:
    """Complete information about current date in all calendars"""
    gregorian: DateInfo
    jalali: DateInfo
    hijri: DateInfo
    timestamp: datetime


class CurrentDate:
    """
    Get current date information in all supported calendars
    
    Provides comprehensive information about today's date including
    events, holidays, and weekend status in Persian, Gregorian, and Hijri calendars.
    """
    
    def __init__(self):
        """Initialize the current date handler"""
        self._setup_constants()
    
    def _setup_constants(self):
        """Setup constant dictionaries for month names"""
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
        
        self.persian_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
        self.english_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
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
        
        return self.persian_days[h], self.english_days[h], h + 1
    
    def _get_events(self, calendar_type: str, month: int, day: int, language: str = 'fa') -> List[str]:
        """
        Get events for a specific date
        
        Args:
            calendar_type: 'jalali', 'gregorian', or 'hijri'
            month: Month number
            day: Day number
            language: 'fa' for Persian, 'en' for English
            
        Returns:
            List of event names
        """
        events = []
        
        if calendar_type == 'jalali':
            event = persian_events.get((month, day))
            if event:
                events.append(event)
        
        elif calendar_type == 'gregorian':
            if language == 'fa':
                event = gregorian_events_fa.get((month, day))
            else:
                event = gregorian_events_en.get((month, day))
            if event:
                events.append(event)
        
        elif calendar_type == 'hijri':
            if language == 'fa':
                event = hijri_events.get((month, day))
            else:
                event = hijri_events_en.get((month, day))
            if event:
                events.append(event)
        
        return events
    
    def _is_holiday(self, calendar_type: str, month: int, day: int, day_of_week_id: int) -> bool:
        """
        Check if a date is a holiday
        
        Args:
            calendar_type: 'jalali', 'gregorian', or 'hijri'
            month: Month number
            day: Day number
            day_of_week_id: Day of week ID (1-7)
            
        Returns:
            True if holiday, False otherwise
        """
        if calendar_type == 'jalali':
            # Check Persian holidays
            is_persian_holiday = persian_holidays.get((month, day), 0) == 1
            # Friday is always a holiday in Persian calendar
            is_friday = day_of_week_id == 7
            return is_persian_holiday or is_friday
        
        elif calendar_type == 'gregorian':
            return gregorian_holidays.get((month, day), 0) == 1
        
        elif calendar_type == 'hijri':
            # Check Hijri holidays
            is_hijri_holiday = hijri_holidays.get((month, day), 0) == 1
            # Check official Iranian Hijri holidays
            is_official_holiday = hijri_official_holidays.get((month, day), 0) == 1
            return is_hijri_holiday or is_official_holiday
        
        return False
    
    def _is_weekend(self, calendar_type: str, day_of_week_id: int) -> bool:
        """
        Check if a date is a weekend
        
        Args:
            calendar_type: 'jalali', 'gregorian', or 'hijri'
            day_of_week_id: Day of week ID (1-7)
            
        Returns:
            True if weekend, False otherwise
        """
        if calendar_type == 'jalali':
            # Thursday (6) and Friday (7) are weekends in Persian calendar
            return day_of_week_id in [6, 7]
        
        elif calendar_type == 'gregorian':
            # Saturday (1) and Sunday (2) are weekends in Gregorian calendar
            return day_of_week_id in [1, 2]
        
        elif calendar_type == 'hijri':
            # Friday (7) is weekend in Hijri calendar
            return day_of_week_id == 7
        
        return False
    
    def now(self, language: str = 'fa') -> CurrentDateInfo:
        """
        Get current date information in all calendars
        
        Args:
            language: 'fa' for Persian, 'en' for English
            
        Returns:
            CurrentDateInfo object with complete date information
        """
        # Get current Gregorian date
        now = datetime.now()
        gy, gm, gd = now.year, now.month, now.day
        
        # Convert to Jalali
        jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
        
        # Convert to Hijri
        hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        
        # Get day of week information
        persian_day, english_day, day_id = self._day_of_week(gy, gm, gd)
        
        # Create DateInfo objects for each calendar
        gregorian_info = DateInfo(
            year=gy,
            month=gm,
            day=gd,
            date_string=f"{gy:04d}-{gm:02d}-{gd:02d}",
            month_name=self.gregorian_months[gm],
            day_of_week=persian_day,
            day_of_week_en=english_day,
            is_leap_year=gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0),
            is_holiday=self._is_holiday('gregorian', gm, gd, day_id),
            is_weekend=self._is_weekend('gregorian', day_id),
            events=self._get_events('gregorian', gm, gd, language)
        )
        
        jalali_info = DateInfo(
            year=jy,
            month=jm,
            day=jd,
            date_string=f"{jy:04d}/{jm:02d}/{jd:02d}",
            month_name=self.persian_months[jm],
            day_of_week=persian_day,
            day_of_week_en=english_day,
            is_leap_year=is_leap_year_persian(jy),
            is_holiday=self._is_holiday('jalali', jm, jd, day_id),
            is_weekend=self._is_weekend('jalali', day_id),
            events=self._get_events('jalali', jm, jd, language)
        )
        
        hijri_info = DateInfo(
            year=hy,
            month=hm,
            day=hd,
            date_string=f"{hy:04d}/{hm:02d}/{hd:02d}",
            month_name=self.hijri_months[hm],
            day_of_week=persian_day,
            day_of_week_en=english_day,
            is_leap_year=is_hijri_leap(hy),
            is_holiday=self._is_holiday('hijri', hm, hd, day_id),
            is_weekend=self._is_weekend('hijri', day_id),
            events=self._get_events('hijri', hm, hd, language)
        )
        
        return CurrentDateInfo(
            gregorian=gregorian_info,
            jalali=jalali_info,
            hijri=hijri_info,
            timestamp=now
        )
    
    def get_date_info(self, year: int, month: int, day: int, 
                     calendar_type: str = 'gregorian', language: str = 'fa') -> DateInfo:
        """
        Get information for a specific date
        
        Args:
            year: Year
            month: Month
            day: Day
            calendar_type: 'jalali', 'gregorian', or 'hijri'
            language: 'fa' for Persian, 'en' for English
            
        Returns:
            DateInfo object
        """
        if calendar_type == 'gregorian':
            gy, gm, gd = year, month, day
            jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
            hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        elif calendar_type == 'jalali':
            jy, jm, jd = year, month, day
            gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
            hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        elif calendar_type == 'hijri':
            hy, hm, hd = year, month, day
            gy, gm, gd = hijri_to_gregorian(hy, hm, hd)
            jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
        else:
            raise ValueError(f"Unsupported calendar type: {calendar_type}")
        
        # Get day of week information
        persian_day, english_day, day_id = self._day_of_week(gy, gm, gd)
        
        # Get month name based on calendar type
        if calendar_type == 'jalali':
            month_name = self.persian_months[month]
            date_string = f"{year:04d}/{month:02d}/{day:02d}"
            is_leap = is_leap_year_persian(year)
        elif calendar_type == 'gregorian':
            month_name = self.gregorian_months[month]
            date_string = f"{year:04d}-{month:02d}-{day:02d}"
            is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        elif calendar_type == 'hijri':
            month_name = self.hijri_months[month]
            date_string = f"{year:04d}/{month:02d}/{day:02d}"
            is_leap = is_hijri_leap(year)
        
        return DateInfo(
            year=year,
            month=month,
            day=day,
            date_string=date_string,
            month_name=month_name,
            day_of_week=persian_day,
            day_of_week_en=english_day,
            is_leap_year=is_leap,
            is_holiday=self._is_holiday(calendar_type, month, day, day_id),
            is_weekend=self._is_weekend(calendar_type, day_id),
            events=self._get_events(calendar_type, month, day, language)
        )
    
    def format_date(self, date_info: DateInfo, format_type: str = 'full') -> str:
        """
        Format date information as string
        
        Args:
            date_info: DateInfo object
            format_type: 'full', 'short', 'numeric', or 'readable'
            
        Returns:
            Formatted date string
        """
        if format_type == 'full':
            return f"{date_info.day} {date_info.month_name} {date_info.year} ({date_info.day_of_week})"
        elif format_type == 'short':
            return f"{date_info.day} {date_info.month_name}"
        elif format_type == 'numeric':
            return date_info.date_string
        elif format_type == 'readable':
            return f"{date_info.day_of_week}، {date_info.day} {date_info.month_name} {date_info.year}"
        else:
            return date_info.date_string
