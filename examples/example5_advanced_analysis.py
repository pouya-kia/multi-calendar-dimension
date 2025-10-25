"""
Example 5: Advanced Usage - Custom Analysis
مثال ۵: استفاده پیشرفته - تحلیل سفارشی
"""

import pandas as pd
from multi_calendar_dimension import DateDimensionGenerator, DateDimensionConfig, CurrentDate

print("=== Advanced Usage Example ===")
print()

# Generate 2 years of data for analysis
config = DateDimensionConfig(
    start_year=1402,
    end_year=1403,
    include_events=True,
    include_holidays=True,
    include_week_calculations=True
)

generator = DateDimensionGenerator(config)
df = generator.to_dataframe()

print(f"Generated {len(df):,} days for analysis")
print()

# Analysis 1: Holiday Distribution
print("1. Holiday Distribution Analysis:")
persian_holidays = df[df['shamsi_is_holiday'] == 1]
gregorian_holidays = df[df['gregorian_is_holiday'] == 1]
hijri_holidays = df[df['hijri_is_holiday'] == 1]

print(f"   Persian holidays: {len(persian_holidays)}")
print(f"   Gregorian holidays: {len(gregorian_holidays)}")
print(f"   Hijri holidays: {len(hijri_holidays)}")
print()

# Analysis 2: Weekend Analysis
print("2. Weekend Analysis:")
persian_weekends = df[df['shamsi_is_weekend'] == 1]
gregorian_weekends = df[df['gregorian_is_weekend'] == 1]

print(f"   Persian weekends: {len(persian_weekends)}")
print(f"   Gregorian weekends: {len(gregorian_weekends)}")
print()

# Analysis 3: Event Analysis
print("3. Event Analysis:")
persian_events = df[df['shamsi_event_name'].notna()]
gregorian_events = df[df['gregorian_event_name_fa'].notna()]
hijri_events = df[df['hijri_event_name'].notna()]

print(f"   Days with Persian events: {len(persian_events)}")
print(f"   Days with Gregorian events: {len(gregorian_events)}")
print(f"   Days with Hijri events: {len(hijri_events)}")
print()

# Analysis 4: Monthly Statistics
print("4. Monthly Statistics:")
monthly_stats = df.groupby('shamsi_month_of_year_id').agg({
    'shamsi_is_holiday': 'sum',
    'shamsi_is_weekend': 'sum',
    'shamsi_event_name': lambda x: x.notna().sum()
}).rename(columns={
    'shamsi_is_holiday': 'holidays',
    'shamsi_is_weekend': 'weekends',
    'shamsi_event_name': 'events'
})

print("   Month | Holidays | Weekends | Events")
print("   ------|----------|----------|-------")
for month, row in monthly_stats.iterrows():
    print(f"   {month:5d} | {row['holidays']:8d} | {row['weekends']:8d} | {row['events']:6d}")
print()

# Analysis 5: Season Analysis
print("5. Season Analysis:")
season_stats = df.groupby('shamsi_season_title').agg({
    'shamsi_is_holiday': 'sum',
    'shamsi_is_weekend': 'sum',
    'shamsi_event_name': lambda x: x.notna().sum()
}).rename(columns={
    'shamsi_is_holiday': 'holidays',
    'shamsi_is_weekend': 'weekends',
    'shamsi_event_name': 'events'
})

for season, row in season_stats.iterrows():
    print(f"   {season}: {row['holidays']} holidays, {row['weekends']} weekends, {row['events']} events")
print()

# Analysis 6: Current Date Analysis
print("6. Current Date Analysis:")
current = CurrentDate()
today = current.now()

print(f"   Today's Persian date: {today.jalali.date_string}")
print(f"   Today's Gregorian date: {today.gregorian.date_string}")
print(f"   Today's Hijri date: {today.hijri.date_string}")
print()

# Find today in the generated data
today_in_data = df[df['shamsi_date_title'] == today.jalali.date_string]
if not today_in_data.empty:
    row = today_in_data.iloc[0]
    print(f"   Today's information from generated data:")
    print(f"     Persian holiday: {bool(row['shamsi_is_holiday'])}")
    print(f"     Persian weekend: {bool(row['shamsi_is_weekend'])}")
    print(f"     Persian event: {row['shamsi_event_name'] if pd.notna(row['shamsi_event_name']) else 'None'}")
    print(f"     Gregorian holiday: {bool(row['gregorian_is_holiday'])}")
    print(f"     Gregorian weekend: {bool(row['gregorian_is_weekend'])}")
    print(f"     Hijri holiday: {bool(row['hijri_is_holiday'])}")
else:
    print("   Today's date not found in generated data range")
print()

# Analysis 7: Export filtered data
print("7. Exporting Filtered Data:")
# Export only holidays
holidays_df = df[df['shamsi_is_holiday'] == 1]
holidays_df.to_excel("persian_holidays_1402_1403.xlsx", index=False)
print(f"   Exported {len(holidays_df)} Persian holidays to Excel")

# Export only days with events
events_df = df[df['shamsi_event_name'].notna()]
events_df.to_excel("persian_events_1402_1403.xlsx", index=False)
print(f"   Exported {len(events_df)} days with Persian events to Excel")
print()

print("=== Advanced Analysis Complete ===")
