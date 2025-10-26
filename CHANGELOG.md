# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2024-10-26

### Added
- Complete usage guide as Jupyter Notebook (`complete_guide.ipynb`)
- Comprehensive examples covering all library features
- Step-by-step tutorials for each functionality

### Documentation
- Added interactive notebook for easy learning
- 43 code cells with practical examples
- Covers conversions, holidays, events, and data generation

## [1.0.2] - 2024-10-26

### Added
- `is_iranian_holiday()` function to check if a Persian date is an official holiday
- `get_all_holidays_for_jalali_date()` for comprehensive holiday information
- Holiday checker utilities that recognize both Persian and Hijri holidays
- Example 8 showing Iranian holiday checking
- Support for checking Hijri holidays in Persian calendar context

### Improved
- Better integration of Hijri holidays with Persian calendar
- Comprehensive holiday detection across all calendar systems

## [1.0.1] - 2024-10-26

### Changed
- **BREAKING**: Replaced astronomical Hijri conversion with Umm al-Qura algorithm for improved accuracy
- Updated `gregorian_to_hijri()` to use official Saudi Umm al-Qura calendar data
- Updated `hijri_to_gregorian()` to use Umm al-Qura algorithm

### Added
- `get_hijri_month_name()` function for easy month name retrieval
- `HIJRI_MONTH_NAMES` dictionary with Persian month names
- `HIJRI_MONTH_NAMES_EN` dictionary with English month names
- `ummalqura_data.py` module with official lunar calendar data
- `persian_events_en` dictionary with English translations of Persian events

### Improved
- More accurate Hijri date conversion using official Saudi calendar
- Faster conversion without astronomical calculations
- Better month name handling for Hijri calendar
- Complete bilingual support for Persian events

### Removed
- Dependency on `skyfield` for Hijri calculations (still kept for potential future use)

## [1.0.0] - 2024-10-25

### Added
- Initial release of multi-calendar-dimension library
- Support for Persian (Jalali), Gregorian, and Hijri calendars
- Date conversion functions between all calendar types
- DateDimensionGenerator for creating comprehensive date dimension tables
- DateRangeGenerator for generating monthly date ranges
- CurrentDate class for getting today's information in all calendars
- Comprehensive event and holiday data:
  - 176+ Persian events and holidays
  - 488+ Gregorian events (English and Persian)
  - Complete Hijri calendar events
  - Variable date holidays (Easter, Thanksgiving, etc.)
- Astronomical calculations for accurate Hijri calendar conversion
- Export functionality (Excel, CSV, DataFrame)
- Command-line interface (CLI)
- Comprehensive test suite
- Complete documentation and examples

### Features
- **Multi-Calendar Support**: Persian, Gregorian, and Hijri calendars
- **Date Conversion**: 6 conversion combinations between all calendars
- **Date Dimension Generation**: Full-featured date dimension tables
- **Event & Holiday Data**: Comprehensive event and holiday information
- **Current Date Information**: Today's date in all calendars with events
- **Export Options**: Excel, CSV, and DataFrame formats
- **CLI Interface**: Command-line tool for common operations
- **Type Hints**: Full type annotation support
- **Documentation**: Comprehensive README and examples

### Technical Details
- Python 3.8+ support
- Dependencies: pandas, openpyxl, skyfield, numpy
- MIT License
- Comprehensive test coverage
- Type hints throughout
- Dataclass-based design
- Modular architecture
