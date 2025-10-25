# Multi-Calendar Dimension Library

A comprehensive Python library for Persian (Jalali), Gregorian, and Hijri calendar operations including date conversion, dimension generation, and current date information.

## Features

### 📅 Multi-Calendar Support
- **Persian (Jalali) Calendar**: Complete support with leap year calculations
- **Gregorian Calendar**: Standard Western calendar
- **Hijri (Islamic) Calendar**: Islamic lunar calendar with astronomical calculations

### 🔄 Date Conversion
- Convert between all calendar types (6 conversion combinations)
- Accurate astronomical calculations for Hijri calendar
- Support for leap years in all calendars

### 📊 Date Dimension Generation
- Generate comprehensive date dimension tables
- Include events, holidays, and weekend information
- Support for annual and monthly ranges
- Export to Excel, CSV, or DataFrame formats

### 📍 Current Date Information
- Get today's date in all calendars
- Event and holiday information
- Weekend and holiday status
- Multiple formatting options

### 🎉 Events & Holidays
- **Persian Events**: 176+ Persian events and holidays
- **Gregorian Events**: 488+ international events (English & Persian)
- **Hijri Events**: Complete Islamic calendar events
- **Variable Holidays**: Easter, Thanksgiving, and other calculated holidays

## Installation

```bash
pip install multi-calendar-dimension
```

## Quick Start

### Basic Date Conversion

```python
from multi_calendar_dimension import jalali_to_gregorian, gregorian_to_hijri

# Convert Persian to Gregorian
gy, gm, gd = jalali_to_gregorian(1403, 1, 1)
print(f"1 Farvardin 1403 = {gy}-{gm:02d}-{gd:02d}")

# Convert Gregorian to Hijri
hy, hm, hd = gregorian_to_hijri(2024, 3, 20)
print(f"20 March 2024 = {hd}/{hm}/{hy} Hijri")
```

### Generate Date Dimension Table

```python
from multi_calendar_dimension import DateDimensionGenerator, DateDimensionConfig

# Create configuration
config = DateDimensionConfig(
    start_year=1400,
    end_year=1410,
    include_events=True,
    include_holidays=True
)

# Generate table
generator = DateDimensionGenerator(config)
df = generator.to_dataframe()

# Export to Excel
filename = generator.to_excel("my_date_dimension.xlsx")
print(f"Generated: {filename}")
```

### Monthly Range Generation

```python
from multi_calendar_dimension import DateRangeGenerator, DateRangeConfig, CalendarType

# Generate Persian calendar range
config = DateRangeConfig(
    calendar_type=CalendarType.JALALI,
    start_year=1403,
    start_month=1,
    end_year=1403,
    end_month=6
)

generator = DateRangeGenerator(config)
df = generator.to_dataframe()
print(f"Generated {len(df)} days for Persian calendar range")
```

### Current Date Information

```python
from multi_calendar_dimension import CurrentDate

# Get today's information
current = CurrentDate()
today = current.now()

print(f"Persian: {today.jalali.date_string}")
print(f"Gregorian: {today.gregorian.date_string}")
print(f"Hijri: {today.hijri.date_string}")

# Check if today is a holiday
if today.jalali.is_holiday:
    print("Today is a holiday!")
    print(f"Events: {today.jalali.events}")
```

## API Reference

### Converters

#### Jalali (Persian) Calendar
- `jalali_to_gregorian(jy, jm, jd)` - Convert Persian to Gregorian
- `gregorian_to_jalali(gy, gm, gd)` - Convert Gregorian to Persian
- `is_leap_year_persian(year)` - Check if Persian year is leap

#### Hijri Calendar
- `gregorian_to_hijri(gy, gm, gd)` - Convert Gregorian to Hijri
- `hijri_to_gregorian(hy, hm, hd)` - Convert Hijri to Gregorian
- `is_hijri_leap(year)` - Check if Hijri year is leap

#### Cross Conversions
- `jalali_to_hijri(jy, jm, jd)` - Convert Persian to Hijri
- `hijri_to_jalali(hy, hm, hd)` - Convert Hijri to Persian

### Generators

#### DateDimensionGenerator
```python
config = DateDimensionConfig(
    start_year=1400,
    end_year=1410,
    include_events=True,
    include_holidays=True,
    include_week_calculations=True
)

generator = DateDimensionGenerator(config)
df = generator.generate()
excel_file = generator.to_excel()
csv_file = generator.to_csv()
```

#### DateRangeGenerator
```python
config = DateRangeConfig(
    calendar_type=CalendarType.JALALI,
    start_year=1403,
    start_month=1,
    end_year=1403,
    end_month=12
)

generator = DateRangeGenerator(config)
df = generator.generate()
summary = generator.get_summary()
```

### Current Date

#### CurrentDate
```python
current = CurrentDate()

# Get today's information
today = current.now(language='fa')  # or 'en'

# Get specific date information
date_info = current.get_date_info(1403, 1, 1, 'jalali')

# Format date
formatted = current.format_date(date_info, 'full')
```

## Data Structure

The generated date dimension tables include the following columns:

### Persian (Jalali) Columns
- `shamsi_date` - Date as integer (YYYYMMDD)
- `shamsi_date_title` - Formatted date string
- `shamsi_month_id` - Month identifier
- `shamsi_month_title` - Month name with year
- `shamsi_season_title` - Season name
- `shamsi_day_of_week_title` - Day of week in Persian
- `shamsi_event_name` - Persian events
- `shamsi_is_holiday` - Holiday status
- `shamsi_is_weekend` - Weekend status

### Gregorian Columns
- `miladi_date` - Date as string (YYYY-MM-DD)
- `gregorian_month_title` - Month name with year
- `gregorian_season_title` - Season name
- `gregorian_day_of_week_title` - Day of week in English
- `gregorian_event_name_en` - English events
- `gregorian_event_name_fa` - Persian events
- `gregorian_is_holiday` - Holiday status
- `gregorian_is_weekend` - Weekend status

### Hijri Columns
- `hijri_date` - Date as integer (YYYYMMDD)
- `hijri_date_title` - Formatted date string
- `hijri_month_title` - Month name with year
- `hijri_event_name` - Hijri events
- `hijri_is_holiday` - Holiday status

## Examples

### Example 1: Generate 10 Years of Data
```python
from multi_calendar_dimension import DateDimensionGenerator, DateDimensionConfig

config = DateDimensionConfig(start_year=1400, end_year=1410)
generator = DateDimensionGenerator(config)
df = generator.to_dataframe()

print(f"Generated {len(df):,} days")
print(f"Columns: {len(df.columns)}")
print(df.head())
```

### Example 2: Convert Specific Dates
```python
from multi_calendar_dimension import jalali_to_gregorian, gregorian_to_hijri

# Persian New Year 1403
gy, gm, gd = jalali_to_gregorian(1403, 1, 1)
print(f"Persian New Year 1403 = {gy}-{gm:02d}-{gd:02d}")

# Convert to Hijri
hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
print(f"Same date in Hijri = {hd}/{hm}/{hy}")
```

### Example 3: Check Today's Events
```python
from multi_calendar_dimension import CurrentDate

current = CurrentDate()
today = current.now()

print(f"Today is {today.jalali.date_string}")
print(f"Persian month: {today.jalali.month_name}")
print(f"Day of week: {today.jalali.day_of_week}")

if today.jalali.events:
    print("Today's events:")
    for event in today.jalali.events:
        print(f"- {event}")

if today.jalali.is_holiday:
    print("Today is a holiday!")
```

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- skyfield >= 1.46
- numpy >= 1.21.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Persian calendar algorithms based on established astronomical calculations
- Hijri calendar conversion using Skyfield astronomical library
- Event and holiday data compiled from official sources
- Inspired by data warehousing date dimension best practices