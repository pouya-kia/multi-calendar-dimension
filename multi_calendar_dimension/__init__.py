"""
Multi-Calendar Dimension Library
کتابخانه چند تقویمی برای تولید Date Dimension

A comprehensive library for Persian (Jalali), Gregorian, and Hijri calendar operations
including date conversion, dimension generation, and current date information.
"""

__version__ = "1.0.5"
__author__ = "Pouya Kia"
__email__ = "kiaa.pouya@gmail.com"

# Main classes
from .generator.dimension import DateDimensionGenerator, DateDimensionConfig
from .generator.range_generator import DateRangeGenerator, DateRangeConfig, CalendarType
from .current.now import CurrentDate

# Converter functions (these don't require pandas)
from .converters.jalali import (
    jalali_to_gregorian,
    gregorian_to_jalali,
    is_leap_year_persian
)

from .converters.hijri import (
    gregorian_to_hijri,
    hijri_to_gregorian,
    is_hijri_leap,
    get_hijri_month_name,
    HIJRI_MONTH_NAMES,
    HIJRI_MONTH_NAMES_EN
)

from .converters.cross import (
    jalali_to_hijri,
    hijri_to_jalali
)

# Events (these don't require pandas)
from .events import (
    persian_events, persian_events_en, persian_holidays, hijri_official_holidays,
    gregorian_events_en, gregorian_events_fa, gregorian_holidays,
    hijri_events, hijri_events_en, hijri_holidays
)

# Utilities
from .utils import is_iranian_holiday, get_all_holidays_for_jalali_date

__all__ = [
    # Main classes
    'DateDimensionGenerator',
    'DateDimensionConfig',
    'DateRangeGenerator',
    'DateRangeConfig',
    'CalendarType',
    'CurrentDate',
    
    # Jalali converters
    'jalali_to_gregorian',
    'gregorian_to_jalali',
    'is_leap_year_persian',
    
    # Hijri converters
    'gregorian_to_hijri',
    'hijri_to_gregorian',
    'is_hijri_leap',
    'get_hijri_month_name',
    'HIJRI_MONTH_NAMES',
    'HIJRI_MONTH_NAMES_EN',
    
    # Cross converters
    'jalali_to_hijri',
    'hijri_to_jalali',
    
    # Events
    'persian_events',
    'persian_events_en',
    'persian_holidays',
    'hijri_official_holidays',
    'gregorian_events_en',
    'gregorian_events_fa',
    'gregorian_holidays',
    'hijri_events',
    'hijri_events_en',
    'hijri_holidays',
    
    # Utilities
    'is_iranian_holiday',
    'get_all_holidays_for_jalali_date',
]
