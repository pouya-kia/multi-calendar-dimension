"""
Hijri (Islamic) calendar conversion functions using Umm al-Qura algorithm
"""

import math
from typing import Tuple
from .ummalqura_data import UMMALQURA_DATA, get_index


HIJRI_MONTH_NAMES = {
    1: "محرم",
    2: "صفر",
    3: "ربیع‌الاول",
    4: "ربیع‌الثانی",
    5: "جمادی‌الاول",
    6: "جمادی‌الثانی",
    7: "رجب",
    8: "شعبان",
    9: "رمضان",
    10: "شوال",
    11: "ذی‌قعده",
    12: "ذی‌حجه"
}

HIJRI_MONTH_NAMES_EN = {
    1: "Muharram",
    2: "Safar",
    3: "Rabi' al-Awwal",
    4: "Rabi' al-Thani",
    5: "Jumada al-Ula",
    6: "Jumada al-Thani",
    7: "Rajab",
    8: "Sha'ban",
    9: "Ramadan",
    10: "Shawwal",
    11: "Dhu al-Qa'dah",
    12: "Dhu al-Hijjah"
}


def is_hijri_leap(year: int) -> bool:
    """
    Check if a Hijri year is leap year
    """
    return ((11 * year + 14) % 30) < 11


def hijri_year_days(year: int) -> int:
    """
    Get number of days in Hijri year
    """
    return 355 if is_hijri_leap(year) else 354


def gregorian_to_hijri(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert Gregorian date to Hijri date using Umm al-Qura algorithm.
    
    Args:
        year: Gregorian year
        month: Gregorian month (1-12)
        day: Gregorian day (1-31)
        
    Returns:
        Tuple of (Hijri year, Hijri month, Hijri day)
        
    Example:
        >>> gregorian_to_hijri(2023, 7, 19)
        (1445, 1, 1)
    """
    day = int(day)
    m = int(month)
    y = int(year)

    if m < 3:
        y -= 1
        m += 12

    a = math.floor(y / 100.)
    jgc = a - math.floor(a / 4.) - 2

    cjdn = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + day - jgc - 1524

    mcjdn = cjdn - 2400000

    index = get_index(mcjdn)

    iln = index + 16260
    ii = math.floor((iln - 1) / 12)
    iy = ii + 1
    im = iln - 12 * ii
    id_ = mcjdn - UMMALQURA_DATA[index - 1] + 1
    
    return int(iy), int(im), int(id_)


def hijri_to_gregorian(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    Convert Hijri date to Gregorian date using Umm al-Qura algorithm.
    
    Args:
        year: Hijri year
        month: Hijri month (1-12)
        day: Hijri day (1-30)
        
    Returns:
        Tuple of (Gregorian year, Gregorian month, Gregorian day)
        
    Example:
        >>> hijri_to_gregorian(1445, 1, 1)
        (2023, 7, 19)
    """
    year = int(year)
    month = int(month)
    day = int(day)
    
    iy = year
    im = month
    id_ = day
    ii = iy - 1
    iln = (ii * 12) + 1 + (im - 1)
    i = iln - 16260
    mcjdn = id_ + UMMALQURA_DATA[i - 1] - 1
    cjdn = mcjdn + 2400000
    
    return julian_to_gregorian(cjdn)


def julian_to_gregorian(julian_date: float) -> Tuple[int, int, int]:
    """
    Convert Julian Day Number to Gregorian date.
    
    Args:
        julian_date: Julian Day Number
        
    Returns:
        Tuple of (Gregorian year, Gregorian month, Gregorian day)
    """
    z = math.floor(julian_date + 0.5)
    a = math.floor((z - 1867216.25) / 36524.25)
    a = z + 1 + a - math.floor(a / 4)
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(e * 30.6001)

    if e > 13.5:
        month = e - 13
    else:
        month = e - 1
    if month > 2.5:
        year = c - 4716
    else:
        year = c - 4715
    if year <= 0:
        year -= 1
        
    return int(year), int(month), int(day)


def get_hijri_month_name(month: int, english: bool = False) -> str:
    """
    Get Hijri month name in Persian or English.
    
    Args:
        month: Hijri month number (1-12)
        english: If True, return English name, otherwise Persian
        
    Returns:
        Month name string
        
    Example:
        >>> get_hijri_month_name(1)
        'محرم'
        >>> get_hijri_month_name(1, english=True)
        'Muharram'
    """
    if english:
        return HIJRI_MONTH_NAMES_EN.get(month, "")
    return HIJRI_MONTH_NAMES.get(month, "")
