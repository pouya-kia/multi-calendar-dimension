"""
Utility functions for checking holidays across different calendars
"""

from typing import Tuple, Dict, Any
from ..converters.jalali import jalali_to_gregorian
from ..converters.hijri import gregorian_to_hijri
from ..events import persian_holidays, hijri_official_holidays, gregorian_holidays


def is_iranian_holiday(jalali_year: int, jalali_month: int, jalali_day: int) -> Dict[str, Any]:
    """
    Check if a Jalali (Persian) date is an official holiday in Iran.
    This includes both fixed Persian holidays and variable Hijri holidays.
    
    Args:
        jalali_year: Persian year
        jalali_month: Persian month (1-12)
        jalali_day: Persian day (1-31)
        
    Returns:
        Dictionary with holiday information:
        - is_holiday: bool
        - holiday_type: 'persian', 'hijri', 'friday', or None
        - reason: description of the holiday
        
    Example:
        >>> is_iranian_holiday(1403, 1, 1)
        {'is_holiday': True, 'holiday_type': 'persian', 'reason': 'Nowruz'}
    """
    result = {
        'is_holiday': False,
        'holiday_type': None,
        'reason': None
    }
    
    # Check Persian fixed holidays
    if (jalali_month, jalali_day) in persian_holidays:
        result['is_holiday'] = True
        result['holiday_type'] = 'persian'
        result['reason'] = f'Persian holiday on {jalali_month}/{jalali_day}'
        return result
    
    # Convert to Gregorian then to Hijri to check Hijri holidays
    try:
        greg_year, greg_month, greg_day = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)
        hijri_year, hijri_month, hijri_day = gregorian_to_hijri(greg_year, greg_month, greg_day)
        
        if (hijri_month, hijri_day) in hijri_official_holidays:
            result['is_holiday'] = True
            result['holiday_type'] = 'hijri'
            result['reason'] = f'Hijri holiday on {hijri_month}/{hijri_day}'
            return result
    except:
        pass
    
    # Check if it's Friday (day_of_week would need to be calculated)
    # For now, we don't check Friday here
    
    return result


def get_all_holidays_for_jalali_date(jalali_year: int, jalali_month: int, jalali_day: int) -> Dict[str, Any]:
    """
    Get comprehensive holiday information for a Persian date including events from all calendars.
    
    Args:
        jalali_year: Persian year
        jalali_month: Persian month (1-12)
        jalali_day: Persian day (1-31)
        
    Returns:
        Dictionary with all relevant information:
        - jalali_date: the input date
        - gregorian_date: converted Gregorian date
        - hijri_date: converted Hijri date  
        - is_persian_holiday: bool
        - is_hijri_holiday: bool
        - is_official_holiday: bool (either Persian or Hijri)
        - persian_event: Persian event name if any
        - hijri_event: Hijri event name if any
    """
    from ..events import persian_events, hijri_events
    
    # Convert to other calendars
    greg_year, greg_month, greg_day = jalali_to_gregorian(jalali_year, jalali_month, jalali_day)
    hijri_year, hijri_month, hijri_day = gregorian_to_hijri(greg_year, greg_month, greg_day)
    
    result = {
        'jalali_date': f'{jalali_year}/{jalali_month:02d}/{jalali_day:02d}',
        'gregorian_date': f'{greg_year}/{greg_month:02d}/{greg_day:02d}',
        'hijri_date': f'{hijri_year}/{hijri_month:02d}/{hijri_day:02d}',
        'is_persian_holiday': (jalali_month, jalali_day) in persian_holidays,
        'is_hijri_holiday': (hijri_month, hijri_day) in hijri_official_holidays,
        'is_official_holiday': False,
        'persian_event': persian_events.get((jalali_month, jalali_day)),
        'hijri_event': hijri_events.get((hijri_month, hijri_day))
    }
    
    result['is_official_holiday'] = result['is_persian_holiday'] or result['is_hijri_holiday']
    
    return result

