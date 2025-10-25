"""
Example 4: Current Date Information
مثال ۴: اطلاعات تاریخ امروز
"""

from multi_calendar_dimension import CurrentDate

print("=== Current Date Information Example ===")
print()

# Initialize current date handler
current = CurrentDate()

# Get today's information in Persian
print("1. Today's Information (Persian):")
today_fa = current.now(language='fa')

print(f"   Persian Date: {today_fa.jalali.date_string}")
print(f"   Persian Month: {today_fa.jalali.month_name}")
print(f"   Persian Day: {today_fa.jalali.day_of_week}")
print(f"   Is Leap Year: {today_fa.jalali.is_leap_year}")
print(f"   Is Holiday: {today_fa.jalali.is_holiday}")
print(f"   Is Weekend: {today_fa.jalali.is_weekend}")

if today_fa.jalali.events:
    print(f"   Events: {', '.join(today_fa.jalali.events)}")
else:
    print("   Events: None")
print()

# Get today's information in English
print("2. Today's Information (English):")
today_en = current.now(language='en')

print(f"   Gregorian Date: {today_en.gregorian.date_string}")
print(f"   Gregorian Month: {today_en.gregorian.month_name}")
print(f"   Gregorian Day: {today_en.gregorian.day_of_week_en}")
print(f"   Is Leap Year: {today_en.gregorian.is_leap_year}")
print(f"   Is Holiday: {today_en.gregorian.is_holiday}")
print(f"   Is Weekend: {today_en.gregorian.is_weekend}")

if today_en.gregorian.events:
    print(f"   Events: {', '.join(today_en.gregorian.events)}")
else:
    print("   Events: None")
print()

# Get Hijri information
print("3. Hijri Information:")
print(f"   Hijri Date: {today_fa.hijri.date_string}")
print(f"   Hijri Month: {today_fa.hijri.month_name}")
print(f"   Is Leap Year: {today_fa.hijri.is_leap_year}")
print(f"   Is Holiday: {today_fa.hijri.is_holiday}")
print(f"   Is Weekend: {today_fa.hijri.is_weekend}")

if today_fa.hijri.events:
    print(f"   Events: {', '.join(today_fa.hijri.events)}")
else:
    print("   Events: None")
print()

# Get specific date information
print("4. Specific Date Information:")
# Persian New Year 1403
date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
print(f"   Persian New Year 1403:")
print(f"     Date: {date_info.date_string}")
print(f"     Month: {date_info.month_name}")
print(f"     Day: {date_info.day_of_week}")
print(f"     Is Holiday: {date_info.is_holiday}")
print(f"     Events: {', '.join(date_info.events) if date_info.events else 'None'}")
print()

# Format date examples
print("5. Date Formatting Examples:")
formatted_full = current.format_date(date_info, 'full')
formatted_short = current.format_date(date_info, 'short')
formatted_numeric = current.format_date(date_info, 'numeric')
formatted_readable = current.format_date(date_info, 'readable')

print(f"   Full format: {formatted_full}")
print(f"   Short format: {formatted_short}")
print(f"   Numeric format: {formatted_numeric}")
print(f"   Readable format: {formatted_readable}")
print()

print("=== Current Date Information Complete ===")
