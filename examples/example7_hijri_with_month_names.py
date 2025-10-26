#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 7: Hijri Conversion with Month Names
Convert Gregorian dates to Hijri with full month names
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_calendar_dimension import (
    gregorian_to_hijri,
    hijri_to_gregorian, 
    get_hijri_month_name,
    HIJRI_MONTH_NAMES_EN
)

def main():
    print("=" * 60)
    print("Hijri Calendar Converter with Month Names")
    print("=" * 60)
    
    # Sample Gregorian dates
    test_dates = [
        (2023, 7, 19, "Islamic New Year 1445"),
        (2024, 3, 20, "Nowruz 1403 / Ramadan"),
        (2025, 10, 26, "Today"),
        (2024, 6, 17, "Eid al-Adha (approx)"),
    ]
    
    print("\nGregorian to Hijri Conversion:")
    print("-" * 60)
    
    for gy, gm, gd, description in test_dates:
        hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        month_name_en = get_hijri_month_name(hm, english=True)
        
        print(f"\n{description}:")
        print(f"  Gregorian: {gy}-{gm:02d}-{gd:02d}")
        print(f"  Hijri: {hd} {month_name_en} {hy}")
        print(f"  Hijri (numeric): {hd}/{hm}/{hy}")
    
    # Reverse conversion test
    print("\n" + "=" * 60)
    print("Hijri to Gregorian Conversion:")
    print("-" * 60)
    
    hijri_dates = [
        (1445, 1, 1, "Muharram 1 (New Year)"),
        (1445, 9, 1, "Ramadan 1"),
        (1445, 10, 1, "Shawwal 1 (Eid al-Fitr)"),
    ]
    
    for hy, hm, hd, description in hijri_dates:
        gy, gm, gd = hijri_to_gregorian(hy, hm, hd)
        month_name = get_hijri_month_name(hm, english=True)
        
        print(f"\n{description}:")
        print(f"  Hijri: {hd} {month_name} {hy}")
        print(f"  Gregorian: {gy}-{gm:02d}-{gd:02d}")
    
    # All Hijri months
    print("\n" + "=" * 60)
    print("All Hijri Months:")
    print("-" * 60)
    
    for month_num in range(1, 13):
        name_en = get_hijri_month_name(month_num, english=True)
        print(f"{month_num:2d}. {name_en}")

if __name__ == "__main__":
    main()

