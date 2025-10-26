#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: How to get Hijri date with month name from Gregorian date
"""

from multi_calendar_dimension import (
    gregorian_to_hijri,
    get_hijri_month_name,
    HIJRI_MONTH_NAMES_EN
)

def convert_gregorian_to_hijri_with_month(year, month, day):
    """
    Convert Gregorian date to Hijri and return with month name.
    """
    hijri_year, hijri_month, hijri_day = gregorian_to_hijri(year, month, day)
    
    month_name_en = get_hijri_month_name(hijri_month, english=True)
    
    result = {
        'gregorian': f"{year}-{month:02d}-{day:02d}",
        'hijri_numeric': f"{hijri_day}/{hijri_month}/{hijri_year}",
        'hijri_formatted': f"{hijri_day} {month_name_en} {hijri_year}",
        'year': hijri_year,
        'month': hijri_month,
        'day': hijri_day,
        'month_name': month_name_en
    }
    
    return result


if __name__ == "__main__":
    # Example usage
    gregorian_date = (2023, 7, 19)
    result = convert_gregorian_to_hijri_with_month(*gregorian_date)
    
    print(f"Gregorian Date: {result['gregorian']}")
    print(f"Hijri Date: {result['hijri_formatted']}")
    print(f"Hijri (numeric): {result['hijri_numeric']}")
    print(f"\nDetails:")
    print(f"  Year: {result['year']}")
    print(f"  Month: {result['month']} ({result['month_name']})")
    print(f"  Day: {result['day']}")
    
    print("\n" + "=" * 60)
    print("More Examples:")
    print("=" * 60)
    
    dates = [
        (2024, 3, 20),
        (2025, 10, 26),
        (2024, 6, 17),
    ]
    
    for gdate in dates:
        result = convert_gregorian_to_hijri_with_month(*gdate)
        print(f"{result['gregorian']} -> {result['hijri_formatted']}")

