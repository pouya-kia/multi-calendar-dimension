# Deployment Guide

This guide explains how to deploy and distribute the Multi-Calendar Dimension Library.

## Prerequisites

Before deploying, ensure you have:

- Python 3.8 or higher
- pip and setuptools
- build and twine packages
- Git configured with your credentials
- PyPI account (for publishing)

## Local Development Setup

### 1. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install build twine
```

### 2. Run Tests

```bash
python -m pytest tests/
```

### 3. Check Code Quality

```bash
# Run linting (if you have flake8 or similar)
flake8 multi_calendar_dimension/

# Run type checking (if you have mypy)
mypy multi_calendar_dimension/
```

## Building the Package

### 1. Clean Previous Builds

```bash
rm -rf build/ dist/ *.egg-info/
```

### 2. Build Source Distribution

```bash
python -m build
```

This creates:
- `dist/multi_calendar_dimension-1.0.0.tar.gz` (source distribution)
- `dist/multi_calendar_dimension-1.0.0-py3-none-any.whl` (wheel)

### 3. Verify the Build

```bash
twine check dist/*
```

## Publishing to PyPI

### 1. Test on Test PyPI First

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ multi-calendar-dimension
```

### 2. Publish to Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

## Version Management

### Updating Version

1. Update version in `pyproject.toml`:
```toml
[project]
version = "1.0.1"  # or appropriate version
```

2. Update `CHANGELOG.md` with new changes

3. Commit and tag the version:
```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Bump version to 1.0.1"
git tag v1.0.1
git push origin main --tags
```

### Semantic Versioning

Follow semantic versioning (SemVer):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.0.1): Bug fixes (backward compatible)

## GitHub Releases

### 1. Create Release on GitHub

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Choose tag version (e.g., v1.0.0)
4. Add release title and description
5. Upload distribution files from `dist/` folder

### 2. Automated Release (Optional)

You can set up GitHub Actions for automated releases:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## Docker Deployment (Optional)

### 1. Create Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

CMD ["python", "-c", "import multi_calendar_dimension; print('Library installed successfully')"]
```

### 2. Build and Run

```bash
docker build -t multi-calendar-dimension .
docker run multi-calendar-dimension
```

## Documentation Deployment

### 1. Sphinx Documentation (Optional)

If you want to create Sphinx documentation:

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs/
```

### 2. GitHub Pages

1. Enable GitHub Pages in repository settings
2. Choose source branch (usually `gh-pages`)
3. Push documentation files

## Monitoring and Maintenance

### 1. Monitor Downloads

- Check PyPI download statistics
- Monitor GitHub repository activity
- Track issue reports and feature requests

### 2. Regular Updates

- Update dependencies regularly
- Monitor security vulnerabilities
- Keep documentation current

## Troubleshooting

### Common Issues

1. **Build fails**: Check `pyproject.toml` syntax
2. **Upload fails**: Verify PyPI credentials
3. **Import errors**: Check package structure
4. **Test failures**: Run tests locally first

### Getting Help

- Check existing issues on GitHub
- Create new issue with detailed description
- Contact maintainers if needed

## Security Considerations

- Never commit API keys or passwords
- Use environment variables for sensitive data
- Keep dependencies updated
- Monitor for security vulnerabilities

## Backup Strategy

- Regular Git pushes to remote repository
- Backup important configuration files
- Keep multiple copies of distribution files
