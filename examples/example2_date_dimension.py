"""
Example 2: Generate Date Dimension Table
مثال ۲: تولید جدول Date Dimension
"""

from multi_calendar_dimension import DateDimensionGenerator, DateDimensionConfig

print("=== Date Dimension Generation Example ===")
print()

# Create configuration for 5 years of data
config = DateDimensionConfig(
    start_year=1400,
    end_year=1404,
    include_events=True,
    include_holidays=True,
    include_week_calculations=True,
    output_format='dataframe'
)

print(f"Configuration:")
print(f"  Start Year: {config.start_year}")
print(f"  End Year: {config.end_year}")
print(f"  Include Events: {config.include_events}")
print(f"  Include Holidays: {config.include_holidays}")
print(f"  Include Week Calculations: {config.include_week_calculations}")
print()

# Generate the date dimension table
print("Generating date dimension table...")
generator = DateDimensionGenerator(config)
df = generator.to_dataframe()

print(f"Generated successfully!")
print(f"  Total days: {len(df):,}")
print(f"  Total columns: {len(df.columns)}")
print(f"  Date range: {df['shamsi_date_title'].iloc[0]} to {df['shamsi_date_title'].iloc[-1]}")
print()

# Show sample data
print("Sample data (first 5 rows):")
print(df[['shamsi_date_title', 'miladi_date', 'shamsi_day_of_week_title', 
          'shamsi_is_holiday', 'shamsi_event_name']].head())
print()

# Show statistics
print("Statistics:")
print(f"  Total holidays: {df['shamsi_is_holiday'].sum()}")
print(f"  Total weekends: {df['shamsi_is_weekend'].sum()}")
print(f"  Days with events: {df['shamsi_event_name'].notna().sum()}")
print()

# Export to Excel
print("Exporting to Excel...")
excel_file = generator.to_excel("example_date_dimension.xlsx")
print(f"Excel file created: {excel_file}")
print()

# Export to CSV
print("Exporting to CSV...")
csv_file = generator.to_csv("example_date_dimension.csv")
print(f"CSV file created: {csv_file}")
print()

print("=== Generation Complete ===")
