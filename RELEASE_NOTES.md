# Release Notes

## Version 1.0.5 - Complete Export Fix (2025-10-28)

### 🐛 Bug Fixes

#### Missing Export Fix
- **Fixed**: `DateDimensionConfig` was not exported in `__init__.py`
- **Added**: Complete export of all Config classes
- **Impact**: Users can now import all necessary classes without errors

### 📝 Changes

```python
# Now all Config classes work correctly:
from multi_calendar_dimension import (
    DateDimensionGenerator,
    DateDimensionConfig,      # ✅ Now exported!
    DateRangeGenerator,
    DateRangeConfig,
    CalendarType
)
```

### ✅ Verified

- All imports tested and working
- Complete guide notebook updated
- Test suite passes (11/13 tests)

---

## Version 1.0.4 - Bug Fix Release (2025-10-28)

### 🐛 Bug Fixes

#### Import Error Fix
- **Fixed**: `DateRangeGenerator` import error that prevented users from importing the class
- **Changed**: Converted lazy imports to direct imports in `__init__.py`
- **Added**: `DateRangeConfig` and `CalendarType` to public API exports
- **Impact**: Users can now successfully import and use `DateRangeGenerator`

### 📝 Changes

```python
# Now works correctly:
from multi_calendar_dimension import DateRangeGenerator, DateRangeConfig, CalendarType
```

### ✨ Improvements

- Enhanced public API accessibility
- Better module initialization
- More intuitive import structure

### 🔧 Technical Details

Before this fix, attempting to import `DateRangeGenerator` would result in:
```
ImportError: cannot import name 'DateRangeGenerator' from 'multi_calendar_dimension'
```

This version resolves the issue by properly exposing all generator classes and their dependencies.

---

## Version 1.0.3 - Maintenance Release (2024-10-26)

### 🔧 Minor Updates
- Documentation improvements
- Code quality enhancements

---

## Version 1.0.0 - Initial Release (2024-10-25)

### 🎉 First Public Release

This is the initial release of the Multi-Calendar Dimension Library, a comprehensive Python library for multi-calendar date operations.

### ✨ Features

#### Calendar Systems Support
- **Persian (Jalali) Calendar**: Complete support with leap year calculations
- **Gregorian Calendar**: Standard international calendar
- **Hijri Calendar**: Islamic calendar with astronomical calculations

#### Date Conversion Functions
- `jalali_to_gregorian()` - Convert Persian dates to Gregorian
- `gregorian_to_jalali()` - Convert Gregorian dates to Persian
- `gregorian_to_hijri()` - Convert Gregorian dates to Hijri (astronomical)
- `hijri_to_gregorian()` - Convert Hijri dates to Gregorian
- `jalali_to_hijri()` - Convert Persian dates to Hijri
- `hijri_to_jalali()` - Convert Hijri dates to Persian

#### Date Dimension Generator
- `DateDimensionGenerator` - Generate comprehensive date dimension tables
- Support for Persian, Gregorian, and Hijri calendars
- Excel export with formatting
- CSV export support
- Customizable date ranges

#### Current Date Information
- `CurrentDate` - Get current date across all calendars
- Event and holiday information
- Weekend and holiday detection
- Multiple output formats

#### Events and Holidays
- **Persian Events**: 166 events in Persian and English
- **Gregorian Events**: Comprehensive international events
- **Hijri Events**: Islamic holidays and events
- Official holiday detection
- Event name translations

#### Additional Features
- Leap year detection for all calendars
- Day of week calculations
- Week numbering systems
- Season and quarter calculations
- Comprehensive test suite
- Multiple usage examples

### 📦 Package Structure

```
multi_calendar_dimension/
├── converters/          # Date conversion functions
├── generator/           # Date dimension generation
├── current/            # Current date information
├── events/             # Events and holidays data
└── utils/              # Utility functions
```

### 🚀 Installation

```bash
pip install multi-calendar-dimension
```

### 📖 Quick Start

```python
from multi_calendar_dimension import jalali_to_gregorian, persian_events_en

# Convert Persian date to Gregorian
gregorian_date = jalali_to_gregorian(1403, 1, 1)
print(gregorian_date)  # (2024, 3, 20)

# Get Persian events in English
from multi_calendar_dimension import persian_events_en
event = persian_events_en[(1, 1)]
print(event)  # "Nowruz (Persian New Year)"
```

### 🧪 Testing

The library includes comprehensive tests:
- Unit tests for all conversion functions
- Integration tests for generators
- Event data validation tests
- Cross-calendar consistency tests

### 📚 Documentation

- Complete API documentation
- Usage examples for all features
- Contributing guidelines
- Security policy
- Code of conduct

### 🔧 Requirements

- Python 3.8+
- pandas (for generators)
- openpyxl (for Excel export)
- skyfield (for astronomical calculations)
- numpy (for calculations)

### 🌍 Internationalization

- Persian events available in both Persian and English
- Gregorian events in English and Persian
- Hijri events in Arabic and English
- Unicode support throughout

### 🛡️ Security

- Input validation for all functions
- Safe date range handling
- No external network dependencies for core functions
- Secure file handling for exports

### 📈 Performance

- Optimized conversion algorithms
- Lazy loading for large datasets
- Memory-efficient data structures
- Fast lookup for events and holidays

### 🤝 Community

- Open source under MIT License
- Community-driven development
- Comprehensive contribution guidelines
- Issue templates and pull request templates

### 🔮 Future Roadmap

- Additional calendar systems support
- More event databases
- Enhanced astronomical calculations
- Performance optimizations
- Extended language support

### 📞 Support

- GitHub Issues for bug reports
- GitHub Discussions for questions
- Comprehensive documentation
- Example code and tutorials

---

**Thank you for using Multi-Calendar Dimension Library!**

For more information, visit: https://github.com/pouya-kia/multi-calendar-dimension
