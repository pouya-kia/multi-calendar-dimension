#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 8: Check Iranian Holidays (Persian + Hijri)
Shows how to check if a Persian date is an official holiday in Iran
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_calendar_dimension import (
    is_iranian_holiday,
    get_all_holidays_for_jalali_date,
    gregorian_to_hijri,
    get_hijri_month_name
)

def main():
    print("=" * 70)
    print("Iranian Official Holidays Checker")
    print("Includes both Persian (Shamsi) and Hijri holidays")
    print("=" * 70)
    
    # Test dates - mix of Persian and Hijri holidays
    test_dates = [
        (1403, 1, 1, "Nowruz - Persian New Year"),
        (1403, 1, 13, "Nature Day - Persian holiday"),
        (1403, 3, 14, "Imam Khomeini demise - Persian holiday"),
        (1403, 11, 22, "Islamic Revolution - Persian holiday"),
        # Add some dates that might have Hijri holidays
        (1403, 1, 10, "Check for potential Muharram 10"),
    ]
    
    print("\nChecking Official Holidays:")
    print("-" * 70)
    
    for jy, jm, jd, description in test_dates:
        result = is_iranian_holiday(jy, jm, jd)
        status = "HOLIDAY" if result['is_holiday'] else "Working Day"
        
        print(f"\n{jy}/{jm:02d}/{jd:02d} - {description}")
        print(f"  Status: {status}")
        if result['is_holiday']:
            print(f"  Type: {result['holiday_type']}")
            print(f"  Reason: {result['reason']}")
    
    # Comprehensive check
    print("\n" + "=" * 70)
    print("Comprehensive Holiday Information:")
    print("-" * 70)
    
    comprehensive_dates = [
        (1403, 1, 1),
        (1403, 11, 22),
    ]
    
    for jy, jm, jd in comprehensive_dates:
        info = get_all_holidays_for_jalali_date(jy, jm, jd)
        
        print(f"\nJalali Date: {info['jalali_date']}")
        print(f"Gregorian: {info['gregorian_date']}")
        print(f"Hijri: {info['hijri_date']}")
        print(f"Official Holiday: {'YES' if info['is_official_holiday'] else 'NO'}")
        
        if info['is_persian_holiday']:
            print(f"  - Persian Holiday")
        if info['is_hijri_holiday']:
            print(f"  - Hijri Holiday")
        if info['persian_event']:
            print(f"  - Persian Event: {info['persian_event']}")
        if info['hijri_event']:
            print(f"  - Hijri Event: {info['hijri_event']}")
    
    # Show all Persian holidays
    print("\n" + "=" * 70)
    print("Note: Iranian holidays include:")
    print("-" * 70)
    print("1. Fixed Persian (Shamsi) holidays:")
    print("   - Nowruz (1-4 Farvardin)")
    print("   - Islamic Republic Day (12 Farvardin)")
    print("   - Nature Day (13 Farvardin)")
    print("   - Imam Khomeini demise (14 Khordad)")
    print("   - 15 Khordad uprising (15 Khordad)")
    print("   - Islamic Revolution (22 Bahman)")
    print("   - Oil Nationalization (29 Esfand)")
    print("\n2. Variable Hijri holidays (change each year):")
    print("   - Tasua & Ashura (9-10 Muharram)")
    print("   - Arbaeen (20 Safar)")
    print("   - Prophet's demise (28 Safar)")
    print("   - Imam Reza martyrdom (29 Safar)")
    print("   - Prophet's birth (17 Rabi I)")
    print("   - Fatimah's birth (20 Jumada II)")
    print("   - Imam Ali's birth (13 Rajab)")
    print("   - Mab'ath (27 Rajab)")
    print("   - Imam Mahdi's birth (15 Sha'ban)")
    print("   - Imam Ali's martyrdom (21 Ramadan)")
    print("   - Eid al-Fitr (1-2 Shawwal)")

if __name__ == "__main__":
    main()

