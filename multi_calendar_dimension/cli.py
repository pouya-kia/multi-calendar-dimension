"""
Command Line Interface for multi-calendar-dimension
رابط خط فرمان برای کتابخانه چند تقویمی
"""

import argparse
import sys
from datetime import datetime
from multi_calendar_dimension import (
    DateDimensionGenerator, DateRangeGenerator, CurrentDate,
    jalali_to_gregorian, gregorian_to_jalali, gregorian_to_hijri,
    CalendarType
)
from multi_calendar_dimension.generator.dimension import DateDimensionConfig
from multi_calendar_dimension.generator.range_generator import DateRangeConfig


def convert_date(args):
    """Convert date between calendars"""
    if args.from_calendar == 'jalali':
        gy, gm, gd = jalali_to_gregorian(args.year, args.month, args.day)
        hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        
        print(f"Persian: {args.year}/{args.month:02d}/{args.day:02d}")
        print(f"Gregorian: {gy}-{gm:02d}-{gd:02d}")
        print(f"Hijri: {hd}/{hm:02d}/{hy}")
    
    elif args.from_calendar == 'gregorian':
        jy, jm, jd = gregorian_to_jalali(args.year, args.month, args.day)
        hy, hm, hd = gregorian_to_hijri(args.year, args.month, args.day)
        
        print(f"Gregorian: {args.year}-{args.month:02d}-{args.day:02d}")
        print(f"Persian: {jy}/{jm:02d}/{jd:02d}")
        print(f"Hijri: {hd}/{hm:02d}/{hy}")
    
    elif args.from_calendar == 'hijri':
        # This would require hijri_to_gregorian function
        print("Hijri to other calendars conversion not implemented in CLI yet")


def current_date(args):
    """Show current date in all calendars"""
    current = CurrentDate()
    today = current.now(language=args.language)
    
    print(f"Current Date Information:")
    print(f"Persian: {today.jalali.date_string} ({today.jalali.month_name})")
    print(f"Gregorian: {today.gregorian.date_string} ({today.gregorian.month_name})")
    print(f"Hijri: {today.hijri.date_string} ({today.hijri.month_name})")
    
    if today.jalali.events:
        print(f"Persian Events: {', '.join(today.jalali.events)}")
    if today.gregorian.events:
        print(f"Gregorian Events: {', '.join(today.gregorian.events)}")
    if today.hijri.events:
        print(f"Hijri Events: {', '.join(today.hijri.events)}")


def generate_dimension(args):
    """Generate date dimension table"""
    config = DateDimensionConfig(
        start_year=args.start_year,
        end_year=args.end_year,
        include_events=args.include_events,
        include_holidays=args.include_holidays
    )
    
    generator = DateDimensionGenerator(config)
    
    if args.output_format == 'excel':
        filename = generator.to_excel(args.output_file)
        print(f"Generated Excel file: {filename}")
    elif args.output_format == 'csv':
        filename = generator.to_csv(args.output_file)
        print(f"Generated CSV file: {filename}")
    else:
        df = generator.to_dataframe()
        print(f"Generated DataFrame with {len(df):,} rows and {len(df.columns)} columns")
        print(df.head())


def generate_range(args):
    """Generate date range table"""
    calendar_type = CalendarType.JALALI if args.calendar == 'jalali' else \
                   CalendarType.GREGORIAN if args.calendar == 'gregorian' else \
                   CalendarType.HIJRI
    
    config = DateRangeConfig(
        calendar_type=calendar_type,
        start_year=args.start_year,
        start_month=args.start_month,
        end_year=args.end_year,
        end_month=args.end_month,
        include_events=args.include_events,
        include_holidays=args.include_holidays
    )
    
    generator = DateRangeGenerator(config)
    
    if args.output_format == 'excel':
        filename = generator.to_excel(args.output_file)
        print(f"Generated Excel file: {filename}")
    elif args.output_format == 'csv':
        filename = generator.to_csv(args.output_file)
        print(f"Generated CSV file: {filename}")
    else:
        df = generator.to_dataframe()
        summary = generator.get_summary()
        print(f"Generated {summary['total_days']} days")
        print(f"Date range: {summary['start_date']} to {summary['end_date']}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Multi-Calendar Dimension Library CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show current date
  multi-calendar current
  
  # Convert Persian date
  multi-calendar convert --from jalali --year 1403 --month 1 --day 1
  
  # Generate date dimension for 5 years
  multi-calendar generate-dimension --start-year 1400 --end-year 1404 --output excel
  
  # Generate monthly range
  multi-calendar generate-range --calendar jalali --start-year 1403 --start-month 1 --end-year 1403 --end-month 6
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert date between calendars')
    convert_parser.add_argument('--from', dest='from_calendar', 
                               choices=['jalali', 'gregorian', 'hijri'],
                               required=True, help='Source calendar')
    convert_parser.add_argument('--year', type=int, required=True, help='Year')
    convert_parser.add_argument('--month', type=int, required=True, help='Month')
    convert_parser.add_argument('--day', type=int, required=True, help='Day')
    
    # Current date command
    current_parser = subparsers.add_parser('current', help='Show current date in all calendars')
    current_parser.add_argument('--language', choices=['fa', 'en'], default='fa', 
                               help='Language for events (default: fa)')
    
    # Generate dimension command
    dim_parser = subparsers.add_parser('generate-dimension', help='Generate date dimension table')
    dim_parser.add_argument('--start-year', type=int, required=True, help='Start year')
    dim_parser.add_argument('--end-year', type=int, required=True, help='End year')
    dim_parser.add_argument('--include-events', action='store_true', default=True, 
                           help='Include events')
    dim_parser.add_argument('--include-holidays', action='store_true', default=True, 
                           help='Include holidays')
    dim_parser.add_argument('--output-format', choices=['excel', 'csv', 'dataframe'], 
                           default='dataframe', help='Output format')
    dim_parser.add_argument('--output-file', help='Output filename')
    
    # Generate range command
    range_parser = subparsers.add_parser('generate-range', help='Generate date range table')
    range_parser.add_argument('--calendar', choices=['jalali', 'gregorian', 'hijri'], 
                             required=True, help='Calendar type')
    range_parser.add_argument('--start-year', type=int, required=True, help='Start year')
    range_parser.add_argument('--start-month', type=int, required=True, help='Start month')
    range_parser.add_argument('--end-year', type=int, required=True, help='End year')
    range_parser.add_argument('--end-month', type=int, required=True, help='End month')
    range_parser.add_argument('--include-events', action='store_true', default=True, 
                             help='Include events')
    range_parser.add_argument('--include-holidays', action='store_true', default=True, 
                             help='Include holidays')
    range_parser.add_argument('--output-format', choices=['excel', 'csv', 'dataframe'], 
                             default='dataframe', help='Output format')
    range_parser.add_argument('--output-file', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'convert':
            convert_date(args)
        elif args.command == 'current':
            current_date(args)
        elif args.command == 'generate-dimension':
            generate_dimension(args)
        elif args.command == 'generate-range':
            generate_range(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
