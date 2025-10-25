"""
Jalali (Persian) calendar conversion functions
تبدیل تاریخ شمسی به میلادی و برعکس
"""

from typing import Tuple


def is_leap_year_persian(year: int) -> bool:
    """
    Check if a Persian year is leap year
    
    Args:
        year: Persian year
        
    Returns:
        True if leap year, False otherwise
        
    Example:
        >>> is_leap_year_persian(1403)
        True
        >>> is_leap_year_persian(1404)
        False
    """
    return (year % 33) in [1, 5, 9, 13, 17, 21, 25, 29]


def jalali_to_gregorian(jy: int, jm: int, jd: int) -> Tuple[int, int, int]:
    """
    Convert Jalali (Persian) date to Gregorian date
    
    Args:
        jy: Jalali year
        jm: Jalali month (1-12)
        jd: Jalali day (1-31)
        
    Returns:
        Tuple of (Gregorian year, Gregorian month, Gregorian day)
        
    Example:
        >>> jalali_to_gregorian(1403, 1, 1)
        (2024, 3, 20)
    """
    jy += 1595
    days = -355668 + (365*jy) + ((jy//33)*8) + (((jy%33)+3)//4) + (31*(jm-1) if jm < 7 else (186 + (jm-7)*30)) + jd
    gy = 400 * (days // 146097)
    days %= 146097
    leap = True
    if days > 36524:
        gy += 100*(days//36524)
        days %= 36524
        if days >= 365:
            days += 1
        else:
            leap = False
    gy += 4*(days//1461)
    days %= 1461
    if days > 365:
        gy += (days-1)//365
        days = (days-1)%365
        leap = False
    gd_m = [0,31,59,90,120,151,181,212,243,273,304,334]
    for i in range(1,13):
        v = gd_m[i-1] + (1 if i > 2 and leap else 0)
        if i == 12 or days < gd_m[i] + (1 if i+1 > 2 and leap else 0):
            return gy, i, days - v + 1


def gregorian_to_jalali(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    """
    Convert Gregorian date to Jalali (Persian) date
    
    Args:
        gy: Gregorian year
        gm: Gregorian month (1-12)
        gd: Gregorian day (1-31)
        
    Returns:
        Tuple of (Jalali year, Jalali month, Jalali day)
        
    Example:
        >>> gregorian_to_jalali(2024, 3, 20)
        (1403, 1, 1)
    """
    gy -= 1600
    gm -= 1
    gd -= 1
    
    g_day_no = 365*gy + (gy+3)//4 - (gy+99)//100 + (gy+399)//400
    g_day_no += [0,31,59,90,120,151,181,212,243,273,304,334][gm]
    if gm > 1 and ((gy%4 == 0 and gy%100 != 0) or (gy%400 == 0)):
        g_day_no += 1
    g_day_no += gd
    
    j_day_no = g_day_no - 79
    j_np = j_day_no // 12053
    j_day_no %= 12053
    
    jy = 979 + 33*j_np + 4*(j_day_no//1461)
    j_day_no %= 1461
    
    if j_day_no >= 366:
        jy += (j_day_no-1)//365
        j_day_no = (j_day_no-1)%365
    
    if j_day_no < 186:
        jm = 1 + j_day_no//31
        jd = 1 + j_day_no%31
    else:
        jm = 7 + (j_day_no-186)//30
        jd = 1 + (j_day_no-186)%30
    
    return jy, jm, jd
