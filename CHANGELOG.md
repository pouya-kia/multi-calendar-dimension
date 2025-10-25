# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
