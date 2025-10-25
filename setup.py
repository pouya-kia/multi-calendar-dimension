"""
Setup script for multi-calendar-dimension library
"""

from setuptools import setup, find_packages

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    # Fallback requirements if requirements.txt is not found
    requirements = [
        "pandas>=2.0.0",
        "openpyxl>=3.1.0", 
        "skyfield>=1.46",
        "numpy>=1.21.0",
    ]

setup(
    name="multi-calendar-dimension",
    version="1.0.0",
    author="Pouya Kia",
    author_email="kiaa.pouya@gmail.com",
    description="A comprehensive library for Persian (Jalali), Gregorian, and Hijri calendar operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pouya-kia/multi-calendar-dimension",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "multi_calendar_dimension": ["events/*.py"],
    },
    entry_points={
        "console_scripts": [
            "multi-calendar=multi_calendar_dimension.cli:main",
        ],
    },
)
