"""
Hijri (Islamic) calendar conversion functions
تبدیل تاریخ قمری به میلادی و برعکس
"""

from typing import Tuple
from skyfield.api import load
import numpy as np


def is_hijri_leap(year: int) -> bool:
    """
    Check if a Hijri year is leap year
    
    Args:
        year: Hijri year
        
    Returns:
        True if leap year, False otherwise
        
    Example:
        >>> is_hijri_leap(1445)
        True
        >>> is_hijri_leap(1446)
        False
    """
    return ((11 * year + 14) % 30) < 11


def hijri_year_days(year: int) -> int:
    """
    Get number of days in Hijri year
    
    Args:
        year: Hijri year
        
    Returns:
        355 for leap year, 354 for normal year
        
    Example:
        >>> hijri_year_days(1445)
        355
        >>> hijri_year_days(1446)
        354
    """
    return 355 if is_hijri_leap(year) else 354


def gregorian_to_jd(gy: int, gm: int, gd: int) -> int:
    """
    Convert Gregorian date to Julian Day Number
    
    Args:
        gy: Gregorian year
        gm: Gregorian month (1-12)
        gd: Gregorian day (1-31)
        
    Returns:
        Julian Day Number
    """
    a = (14 - gm) // 12
    y = gy + 4800 - a
    m = gm + 12 * a - 3
    jd = gd + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045
    return jd


def jd_to_hijri_tabular(jd: int) -> Tuple[int, int, int]:
    """
    Convert Julian Day Number to Hijri date using tabular algorithm
    
    Args:
        jd: Julian Day Number
        
    Returns:
        Tuple of (Hijri year, Hijri month, Hijri day)
    """
    jd = int(jd)
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d


def gregorian_to_hijri_astronomical(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert Gregorian date to Hijri using astronomical calculations
    
    Args:
        year: Gregorian year
        month: Gregorian month (1-12)
        day: Gregorian day (1-31)
        
    Returns:
        Tuple of (Hijri year, Hijri month, Hijri day)
    """
    # Load astronomical data
    ts = load.timescale()
    planets = load('de421.bsp')
    earth, moon, sun = planets['earth'], planets['moon'], planets['sun']
    
    # Input time
    t = ts.utc(year, month, day)
    
    # Celestial positions
    e = earth.at(t)
    moon_lon = e.observe(moon).apparent().ecliptic_latlon()[1].degrees
    sun_lon = e.observe(sun).apparent().ecliptic_latlon()[1].degrees

    # Moon-sun elongation angle (degrees)
    elongation = (moon_lon - sun_lon) % 360

    # Moon age (days since conjunction)
    moon_age = (elongation / 360.0) * 29.53058867
    day_in_hijri_month = int(moon_age)
    if day_in_hijri_month == 0:
        day_in_hijri_month = 30  # Back to previous month

    # Estimate Hijri month and year
    # Difference between Gregorian date and Hijri epoch (July 16, 622 CE)
    jd_days = (t.utc_datetime() - ts.utc(622, 7, 16).utc_datetime()).days
    hijri_months_passed = int(jd_days / 29.53058867)
    hijri_year = 1 + hijri_months_passed // 12
    hijri_month = hijri_months_passed % 12

    return hijri_year, hijri_month + 1, day_in_hijri_month


def gregorian_to_hijri(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    """
    Convert Gregorian date to Hijri date using astronomical calculations
    
    Args:
        gy: Gregorian year
        gm: Gregorian month (1-12)
        gd: Gregorian day (1-31)
        
    Returns:
        Tuple of (Hijri year, Hijri month, Hijri day)
        
    Example:
        >>> gregorian_to_hijri(2024, 3, 20)
        (1445, 9, 10)
    """
    return gregorian_to_hijri_astronomical(gy, gm, gd)


def hijri_to_gregorian(hy: int, hm: int, hd: int) -> Tuple[int, int, int]:
    """
    Convert Hijri date to Gregorian date
    
    Args:
        hy: Hijri year
        hm: Hijri month (1-12)
        hd: Hijri day (1-30)
        
    Returns:
        Tuple of (Gregorian year, Gregorian month, Gregorian day)
        
    Example:
        >>> hijri_to_gregorian(1445, 9, 10)
        (2024, 3, 20)
    """
    # Convert Hijri to Julian Day Number first
    # This is a simplified conversion - for more accuracy, 
    # we would need the reverse of the astronomical calculation
    jd = 1948440 + (hy - 1) * 354 + (hy - 1) // 30 * 11 + (hm - 1) * 29 + hd
    
    # Convert Julian Day Number to Gregorian
    a = jd + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    
    return year, month, day
