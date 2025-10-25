#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example 6: Persian Events in Both Languages
مثال ۶: رویدادهای فارسی به دو زبان

This example demonstrates how to access Persian events
in both Persian and English languages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_calendar_dimension import persian_events, persian_events_en

def main():
    print("=" * 60)
    print("Persian Events in Both Languages")
    print("=" * 60)
    
    # Sample dates to demonstrate
    sample_dates = [
        (1, 1),   # Nowruz
        (1, 12),  # Islamic Republic Day
        (3, 14),  # Imam Khomeini's Demise
        (11, 22), # Islamic Revolution Victory
        (12, 29)  # Oil Nationalization Day
    ]
    
    print(f"\nTotal Persian Events: {len(persian_events)}")
    print(f"Total English Events: {len(persian_events_en)}")
    print("\nSample Events:")
    print("-" * 40)
    
    for month, day in sample_dates:
        persian_event = persian_events.get((month, day), "No event")
        english_event = persian_events_en.get((month, day), "No event")
        
        print(f"\nMonth {month}, Day {day}:")
        print(f"  English:  {english_event}")
    
    # Check if all events have English translations
    missing_translations = []
    for key in persian_events:
        if key not in persian_events_en:
            missing_translations.append(key)
    
    if missing_translations:
        print(f"\nMissing English translations: {len(missing_translations)}")
        for key in missing_translations[:5]:  # Show first 5
            print(f"  {key}: {persian_events[key]}")
    else:
        print("\nAll Persian events have English translations!")
    
    # Check for extra English events
    extra_translations = []
    for key in persian_events_en:
        if key not in persian_events:
            extra_translations.append(key)
    
    if extra_translations:
        print(f"\nExtra English events: {len(extra_translations)}")
        for key in extra_translations[:5]:  # Show first 5
            print(f"  {key}: {persian_events_en[key]}")
    else:
        print("No extra English events found!")

if __name__ == "__main__":
    main()
