"""
Test suite for main module
تست‌های ماژول اصلی
"""

import pytest
from multi_calendar_dimension import (
    DateDimensionGenerator, DateRangeGenerator, CurrentDate,
    jalali_to_gregorian, gregorian_to_jalali, is_leap_year_persian,
    gregorian_to_hijri, hijri_to_gregorian, is_hijri_leap,
    jalali_to_hijri, hijri_to_jalali
)


class TestMainModuleImports:
    """Test main module imports"""
    
    def test_main_classes_imported(self):
        """Test that main classes are imported"""
        assert DateDimensionGenerator is not None
        assert DateRangeGenerator is not None
        assert CurrentDate is not None
    
    def test_converter_functions_imported(self):
        """Test that converter functions are imported"""
        assert jalali_to_gregorian is not None
        assert gregorian_to_jalali is not None
        assert is_leap_year_persian is not None
        assert gregorian_to_hijri is not None
        assert hijri_to_gregorian is not None
        assert is_hijri_leap is not None
        assert jalali_to_hijri is not None
        assert hijri_to_jalali is not None
    
    def test_all_functions_callable(self):
        """Test that all imported functions are callable"""
        functions = [
            jalali_to_gregorian, gregorian_to_jalali, is_leap_year_persian,
            gregorian_to_hijri, hijri_to_gregorian, is_hijri_leap,
            jalali_to_hijri, hijri_to_jalali
        ]
        
        for func in functions:
            assert callable(func)
    
    def test_all_classes_instantiable(self):
        """Test that all imported classes can be instantiated"""
        # Test DateDimensionGenerator
        from multi_calendar_dimension.generator.dimension import DateDimensionConfig
        config = DateDimensionConfig(start_year=1403, end_year=1403)
        generator = DateDimensionGenerator(config)
        assert generator is not None
        
        # Test DateRangeGenerator
        from multi_calendar_dimension.generator.range_generator import DateRangeConfig, CalendarType
        range_config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403, start_month=1,
            end_year=1403, end_month=1
        )
        range_generator = DateRangeGenerator(range_config)
        assert range_generator is not None
        
        # Test CurrentDate
        current = CurrentDate()
        assert current is not None


class TestMainModuleFunctionality:
    """Test main module functionality"""
    
    def test_basic_conversion_workflow(self):
        """Test basic conversion workflow"""
        # Persian to Gregorian
        gy, gm, gd = jalali_to_gregorian(1403, 1, 1)
        assert gy == 2024
        assert gm == 3
        assert gd == 20
        
        # Gregorian to Hijri
        hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        assert isinstance(hy, int)
        assert isinstance(hm, int)
        assert isinstance(hd, int)
        
        # Persian to Hijri (cross conversion)
        hy2, hm2, hd2 = jalali_to_hijri(1403, 1, 1)
        assert isinstance(hy2, int)
        assert isinstance(hm2, int)
        assert isinstance(hd2, int)
    
    def test_leap_year_functions(self):
        """Test leap year functions"""
        # Persian leap year
        assert is_leap_year_persian(1403) == True
        assert is_leap_year_persian(1404) == False
        
        # Hijri leap year
        assert isinstance(is_hijri_leap(1445), bool)
        assert isinstance(is_hijri_leap(1446), bool)
    
    def test_generator_workflow(self):
        """Test generator workflow"""
        from multi_calendar_dimension.generator.dimension import DateDimensionConfig
        
        config = DateDimensionConfig(
            start_year=1403,
            end_year=1403,
            include_events=True,
            include_holidays=True
        )
        
        generator = DateDimensionGenerator(config)
        df = generator.to_dataframe()
        
        assert len(df) > 0
        assert 'shamsi_date' in df.columns
        assert 'miladi_date' in df.columns
        assert 'hijri_date' in df.columns
    
    def test_range_generator_workflow(self):
        """Test range generator workflow"""
        from multi_calendar_dimension.generator.range_generator import DateRangeConfig, CalendarType
        
        config = DateRangeConfig(
            calendar_type=CalendarType.JALALI,
            start_year=1403,
            start_month=1,
            end_year=1403,
            end_month=3
        )
        
        generator = DateRangeGenerator(config)
        df = generator.to_dataframe()
        
        assert len(df) > 0
        assert 'shamsi_date' in df.columns
    
    def test_current_date_workflow(self):
        """Test current date workflow"""
        current = CurrentDate()
        today = current.now()
        
        assert today.gregorian.year > 2000
        assert today.jalali.year > 1300
        assert today.hijri.year > 1400
        
        assert 1 <= today.gregorian.month <= 12
        assert 1 <= today.jalali.month <= 12
        assert 1 <= today.hijri.month <= 12


class TestModuleIntegration:
    """Test module integration"""
    
    def test_end_to_end_workflow(self):
        """Test end-to-end workflow"""
        # 1. Get current date
        current = CurrentDate()
        today = current.now()
        
        # 2. Convert current date
        gy, gm, gd = jalali_to_gregorian(today.jalali.year, today.jalali.month, today.jalali.day)
        hy, hm, hd = gregorian_to_hijri(gy, gm, gd)
        
        # 3. Generate dimension table for current year
        from multi_calendar_dimension.generator.dimension import DateDimensionConfig
        
        config = DateDimensionConfig(
            start_year=today.jalali.year,
            end_year=today.jalali.year,
            include_events=True,
            include_holidays=True
        )
        
        generator = DateDimensionGenerator(config)
        df = generator.to_dataframe()
        
        # 4. Find today in the generated data
        today_in_data = df[df['shamsi_date_title'] == today.jalali.date_string]
        assert len(today_in_data) == 1
        
        # 5. Verify consistency
        row = today_in_data.iloc[0]
        assert row['shamsi_year_id'] == today.jalali.year
        assert row['shamsi_month_of_year_id'] == today.jalali.month
        assert row['shamsi_day_of_month_id'] == today.jalali.day
    
    def test_cross_calendar_consistency(self):
        """Test cross-calendar consistency"""
        # Test that conversions are consistent
        original_jalali = (1403, 1, 1)
        
        # Jalali -> Gregorian -> Jalali
        gy, gm, gd = jalali_to_gregorian(*original_jalali)
        jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
        assert (jy, jm, jd) == original_jalali
        
        # Jalali -> Hijri -> Gregorian -> Jalali
        hy, hm, hd = jalali_to_hijri(*original_jalali)
        gy2, gm2, gd2 = hijri_to_gregorian(hy, hm, hd)
        jy2, jm2, jd2 = gregorian_to_jalali(gy2, gm2, gd2)
        
        # Should be close (within a few days due to calendar differences)
        assert abs(jy2 - original_jalali[0]) <= 1
        assert abs(jm2 - original_jalali[1]) <= 1
        assert abs(jd2 - original_jalali[2]) <= 1


if __name__ == "__main__":
    pytest.main([__file__])
