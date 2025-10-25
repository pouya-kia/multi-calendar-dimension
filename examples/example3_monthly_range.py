"""
Example 3: Monthly Range Generation
مثال ۳: تولید بازه‌های ماهانه
"""

from multi_calendar_dimension import DateRangeGenerator, DateRangeConfig, CalendarType

print("=== Monthly Range Generation Example ===")
print()

# Example 1: Persian calendar range (6 months)
print("1. Persian Calendar Range (6 months):")
config1 = DateRangeConfig(
    calendar_type=CalendarType.JALALI,
    start_year=1403,
    start_month=1,
    end_year=1403,
    end_month=6,
    include_events=True,
    include_holidays=True
)

generator1 = DateRangeGenerator(config1)
df1 = generator1.to_dataframe()
summary1 = generator1.get_summary()

print(f"   Generated {summary1['total_days']} days")
print(f"   Date range: {summary1['start_date']} to {summary1['end_date']}")
print(f"   Holidays: {summary1['holidays_count']}")
print(f"   Weekends: {summary1['weekends_count']}")
print()

# Example 2: Gregorian calendar range (3 months)
print("2. Gregorian Calendar Range (3 months):")
config2 = DateRangeConfig(
    calendar_type=CalendarType.GREGORIAN,
    start_year=2024,
    start_month=1,
    end_year=2024,
    end_month=3,
    include_events=True,
    include_holidays=True
)

generator2 = DateRangeGenerator(config2)
df2 = generator2.to_dataframe()
summary2 = generator2.get_summary()

print(f"   Generated {summary2['total_days']} days")
print(f"   Date range: {summary2['start_date']} to {summary2['end_date']}")
print(f"   Holidays: {summary2['holidays_count']}")
print(f"   Weekends: {summary2['weekends_count']}")
print()

# Example 3: Hijri calendar range (2 months)
print("3. Hijri Calendar Range (2 months):")
config3 = DateRangeConfig(
    calendar_type=CalendarType.HIJRI,
    start_year=1445,
    start_month=9,
    end_year=1445,
    end_month=10,
    include_events=True,
    include_holidays=True
)

generator3 = DateRangeGenerator(config3)
df3 = generator3.to_dataframe()
summary3 = generator3.get_summary()

print(f"   Generated {summary3['total_days']} days")
print(f"   Date range: {summary3['start_date']} to {summary3['end_date']}")
print(f"   Holidays: {summary3['holidays_count']}")
print(f"   Weekends: {summary3['weekends_count']}")
print()

# Export examples
print("4. Exporting ranges to files:")
excel1 = generator1.to_excel("persian_range_6months.xlsx")
excel2 = generator2.to_excel("gregorian_range_3months.xlsx")
excel3 = generator3.to_excel("hijri_range_2months.xlsx")

print(f"   Persian range: {excel1}")
print(f"   Gregorian range: {excel2}")
print(f"   Hijri range: {excel3}")
print()

print("=== Range Generation Complete ===")
