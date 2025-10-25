# Contributing to Multi-Calendar Dimension Library

Thank you for your interest in contributing to the Multi-Calendar Dimension Library! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip or conda

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-calendar-dimension.git
cd multi-calendar-dimension
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

## Contributing Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write comprehensive docstrings for all public functions
- Keep functions focused and single-purpose

### Testing

- Write tests for all new functionality
- Ensure all existing tests pass
- Aim for high test coverage
- Use descriptive test names

### Documentation

- Update README.md for new features
- Add examples for new functionality
- Update CHANGELOG.md for significant changes
- Write clear commit messages

## Types of Contributions

### Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages or stack traces

### Feature Requests

For new features, please:
- Describe the use case
- Explain why it would be valuable
- Provide examples if possible
- Consider backward compatibility

### Code Contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `python -m pytest`
6. Commit changes: `git commit -m "Add feature-name"`
7. Push to your fork: `git push origin feature-name`
8. Create a Pull Request

## Calendar System Guidelines

### Persian (Jalali) Calendar
- Follow official Iranian calendar rules
- Use Persian month names in Persian text
- Include both Persian and English event names

### Gregorian Calendar
- Follow international standards
- Include major international holidays
- Support variable holidays (Easter, etc.)

### Hijri Calendar
- Use astronomical calculations for accuracy
- Include Islamic holidays and events
- Support both Sunni and Shia traditions where applicable

## Event and Holiday Data

When adding new events or holidays:
- Verify historical accuracy
- Include both Persian and English names
- Specify if it's a holiday or just an event
- Add appropriate metadata (year, significance)

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Run tests and ensure they pass
4. Create a release tag
5. Build and upload to PyPI

## Questions?

Feel free to open an issue for questions or discussions about the project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
