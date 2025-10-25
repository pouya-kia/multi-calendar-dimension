"""
Example 1: Basic Date Conversion
مثال ۱: تبدیل تاریخ‌های پایه
"""

from multi_calendar_dimension import (
    jalali_to_gregorian, gregorian_to_jalali,
    gregorian_to_hijri, hijri_to_gregorian,
    jalali_to_hijri, hijri_to_jalali,
    is_leap_year_persian, is_hijri_leap
)

print("=== Basic Date Conversion Examples ===")
print()

# Persian to Gregorian conversion
print("1. Persian to Gregorian:")
jy, jm, jd = 1403, 1, 1  # 1 Farvardin 1403
gy, gm, gd = jalali_to_gregorian(jy, jm, jd)
print(f"   {jy}/{jm:02d}/{jd:02d} Persian = {gy}-{gm:02d}-{gd:02d} Gregorian")
print()

# Gregorian to Persian conversion
print("2. Gregorian to Persian:")
gy, gm, gd = 2024, 3, 20  # March 20, 2024
jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
print(f"   {gy}-{gm:02d}-{gd:02d} Gregorian = {jy}/{jm:02d}/{jd:02d} Persian")
print()

# Gregorian to Hijri conversion
print("3. Gregorian to Hijri:")
gy, gm, gd = 2024, 3, 20
hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
print(f"   {gy}-{gm:02d}-{gd:02d} Gregorian = {hd}/{hm:02d}/{hy} Hijri")
print()

# Persian to Hijri conversion
print("4. Persian to Hijri:")
jy, jm, jd = 1403, 1, 1
hy, hm, hd = jalali_to_hijri(jy, jm, jd)
print(f"   {jy}/{jm:02d}/{jd:02d} Persian = {hd}/{hm:02d}/{hy} Hijri")
print()

# Leap year checks
print("5. Leap Year Checks:")
print(f"   Persian year 1403 is leap: {is_leap_year_persian(1403)}")
print(f"   Persian year 1404 is leap: {is_leap_year_persian(1404)}")
print(f"   Hijri year 1445 is leap: {is_hijri_leap(1445)}")
print(f"   Hijri year 1446 is leap: {is_hijri_leap(1446)}")
print()

print("=== Conversion Complete ===")
