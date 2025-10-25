"""
Cross-calendar conversion functions
تبدیل مستقیم بین تقویم‌های شمسی و قمری
"""

from typing import Tuple
from .jalali import jalali_to_gregorian, gregorian_to_jalali
from .hijri import gregorian_to_hijri, hijri_to_gregorian


def jalali_to_hijri(jy: int, jm: int, jd: int) -> Tuple[int, int, int]:
    """
    Convert Jalali (Persian) date to Hijri date
    
    Args:
        jy: Jalali year
        jm: Jalali month (1-12)
        jd: Jalali day (1-31)
        
    Returns:
        Tuple of (Hijri year, Hijri month, Hijri day)
        
    Example:
        >>> jalali_to_hijri(1403, 1, 1)
        (1445, 9, 10)
    """
    # Convert Jalali to Gregorian first
    gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
    
    # Convert Gregorian to Hijri
    hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
    
    return hy, hm, hd


def hijri_to_jalali(hy: int, hm: int, hd: int) -> Tuple[int, int, int]:
    """
    Convert Hijri date to Jalali (Persian) date
    
    Args:
        hy: Hijri year
        hm: Hijri month (1-12)
        hd: Hijri day (1-30)
        
    Returns:
        Tuple of (Jalali year, Jalali month, Jalali day)
        
    Example:
        >>> hijri_to_jalali(1445, 9, 10)
        (1403, 1, 1)
    """
    # Convert Hijri to Gregorian first
    gy, gm, gd = hijri_to_gregorian(hy, hm, hd)
    
    # Convert Gregorian to Jalali
    jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
    
    return jy, jm, jd
