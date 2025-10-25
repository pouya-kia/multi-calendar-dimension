"""
Test suite for generators module
تست‌های ماژول generators
"""

import pytest
import pandas as pd
from multi_calendar_dimension.generator.dimension import DateDimensionGenerator, DateDimensionConfig
from multi_calendar_dimension.generator.range_generator import DateRangeGenerator, DateRangeConfig, CalendarType


class TestDateDimensionGenerator:
    """Test DateDimensionGenerator class"""
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        config = DateDimensionConfig(
            start_year=1400,
            end_year=1401,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        assert generator.config.start_year == 1400
        assert generator.config.end_year == 1401
        assert generator.config.include_events == True
    
    def test_generate_basic(self):
        """Test basic generation"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'shamsi_date' in df.columns
        assert 'miladi_date' in df.columns
        assert 'hijri_date' in df.columns
    
    def test_generate_without_events(self):
        """Test generation without events"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=False,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_generate_without_holidays(self):
        """Test generation without holidays"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=False
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_generate_without_week_calculations(self):
        """Test generation without week calculations"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True,
            include_week_calculations=False
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_to_excel(self):
        """Test Excel export"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        filename = generator.to_excel("test_output.xlsx")
        
        assert filename == "test_output.xlsx"
        # Note: In a real test, you would check if the file exists
    
    def test_to_csv(self):
        """Test CSV export"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        filename = generator.to_csv("test_output.csv")
        
        assert filename == "test_output.csv"
        # Note: In a real test, you would check if the file exists
    
    def test_to_dataframe(self):
        """Test DataFrame export"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_leap_year_handling(self):
        """Test leap year handling"""
        config = DateDimensionConfig(
            start_year=1403,  # Leap year
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        # Check that Esfand has 30 days in leap year
        esfand_days = df[df['shamsi_month_of_year_id'] == 12]
        assert len(esfand_days) == 30
    
    def test_holiday_detection(self):
        """Test holiday detection"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        # Check that Persian New Year is marked as holiday
        new_year = df[df['shamsi_date_title'] == '1403/01/01']
        assert len(new_year) == 1
        assert new_year.iloc[0]['shamsi_is_holiday'] == 1
    
    def test_weekend_detection(self):
        """Test weekend detection"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        # Check that weekends are detected
        weekends = df[df['shamsi_is_weekend'] == 1]
        assert len(weekends) > 0
        
        # Check that Thursdays and Fridays are weekends
        thursdays = df[df['shamsi_day_of_week_id'] == 6]
        fridays = df[df['shamsi_day_of_week_id'] == 7]
        
        assert all(thursdays['shamsi_is_weekend'] == 1)
        assert all(fridays['shamsi_is_weekend'] == 1)


class TestDateRangeGenerator:
    """Test DateRangeGenerator class"""
    
    def test_range_generator_initialization(self):
        """Test range generator initialization"""
        config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403,
            start_month=1,
            end_year=1403,
            end_month=6
        )
        generator = DateRangeGenerator(config)
        assert generator.config.start_year == 1403
        assert generator.config.end_year == 1403
        assert generator.config.start_month == 1
        assert generator.config.end_month == 6
    
    def test_range_generator_validation(self):
        """Test range generator validation"""
        # Test invalid start year > end year
        with pytest.raises(ValueError):
            config = DateRangeConfig(
                calendar_type=CalendarType.JALALI,
                start_year=1404,
                start_month=1,
                end_year=1403,
                end_month=6
            )
            DateRangeGenerator(config)
        
        # Test invalid month
        with pytest.raises(ValueError):
            config = DateRangeConfig(
                calendar_type=CalendarType.JALALI,
                start_year=1403,
                start_month=13,
                end_year=1403,
                end_month=6
            )
            DateRangeGenerator(config)
    
    def test_generate_jalali_range(self):
        """Test Jalali range generation"""
        config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403,
            start_month=1,
            end_year=1403,
            end_month=3
        )
        generator = DateRangeGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Check that all months are within range
        months = df['shamsi_month_of_year_id'].unique()
        assert all(1 <= month <= 3 for month in months)
    
    def test_generate_gregorian_range(self):
        """Test Gregorian range generation"""
        config = DateRangeConfig(
            calendar_type=CalendarType.GREGORIAN,
            start_year=2024,
            start_month=1,
            end_year=2024,
            end_month=3
        )
        generator = DateRangeGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_generate_hijri_range(self):
        """Test Hijri range generation"""
        config = DateRangeConfig(
            calendar_type=CalendarType.HIJRI,
            start_year=1445,
            start_month=9,
            end_year=1445,
            end_month=10
        )
        generator = DateRangeGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
    
    def test_get_summary(self):
        """Test summary generation"""
        config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403,
            start_month=1,
            end_year=1403,
            end_month=3
        )
        generator = DateRangeGenerator(config)
        summary = generator.get_summary()
        
        assert isinstance(summary, dict)
        assert 'total_days' in summary
        assert 'start_date' in summary
        assert 'end_date' in summary
        assert 'calendar_type' in summary
        assert summary['calendar_type'] == 'jalali'
    
    def test_empty_range(self):
        """Test empty range handling"""
        config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403,
            start_month=1,
            end_year=1403,
            end_month=1
        )
        generator = DateRangeGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        # Should have at least one month of data
        assert len(df) > 0


class TestGeneratorEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_single_year_generation(self):
        """Test single year generation"""
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Check that all dates are from 1403
        years = df['shamsi_year_id'].unique()
        assert len(years) == 1
        assert years[0] == 1403
    
    def test_multiple_years_generation(self):
        """Test multiple years generation"""
        config = DateDimensionConfig(
            start_year=1400,
            end_year=1402,
            include_events=True,
            include_holidays=True
        )
        generator = DateDimensionGenerator(config)
        df = generator.generate()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Check that multiple years are included
        years = df['shamsi_year_id'].unique()
        assert len(years) == 3
        assert 1400 in years
        assert 1401 in years
        assert 1402 in years
    
    def test_column_consistency(self):
        """Test column consistency across different configurations"""
        config1 = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        
        config2 = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=False,
            include_holidays=False
        )
        
        generator1 = DateDimensionGenerator(config1)
        generator2 = DateDimensionGenerator(config2)
        
        df1 = generator1.generate()
        df2 = generator2.generate()
        
        # Both should have the same number of rows
        assert len(df1) == len(df2)
        
        # Both should have basic columns
        basic_columns = ['shamsi_date', 'miladi_date', 'hijri_date']
        for col in basic_columns:
            assert col in df1.columns
            assert col in df2.columns


if __name__ == "__main__":
    pytest.main([__file__])
