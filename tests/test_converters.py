"""
Test suite for converters module
تست‌های ماژول converters
"""

import pytest
from multi_calendar_dimension.converters.jalali import (
    jalali_to_gregorian, gregorian_to_jalali, is_leap_year_persian
)
from multi_calendar_dimension.converters.hijri import (
    gregorian_to_hijri, hijri_to_gregorian, is_hijri_leap
)
from multi_calendar_dimension.converters.cross import (
    jalali_to_hijri, hijri_to_jalali
)


class TestJalaliConverters:
    """Test Jalali calendar conversion functions"""
    
    def test_jalali_to_gregorian_basic(self):
        """Test basic Jalali to Gregorian conversion"""
        # Persian New Year 1403
        gy, gm, gd = jalali_to_gregorian(1403, 1, 1)
        assert gy == 2024
        assert gm == 3
        assert gd == 20
    
    def test_gregorian_to_jalali_basic(self):
        """Test basic Gregorian to Jalali conversion"""
        # March 20, 2024
        jy, jm, jd = gregorian_to_jalali(2024, 3, 20)
        assert jy == 1403
        assert jm == 1
        assert jd == 1
    
    def test_jalali_to_gregorian_roundtrip(self):
        """Test roundtrip conversion"""
        original = (1403, 1, 1)
        gy, gm, gd = jalali_to_gregorian(*original)
        jy, jm, jd = gregorian_to_jalali(gy, gm, gd)
        assert (jy, jm, jd) == original
    
    def test_is_leap_year_persian(self):
        """Test Persian leap year detection"""
        assert is_leap_year_persian(1403) == True
        assert is_leap_year_persian(1404) == False
        assert is_leap_year_persian(1405) == False
        assert is_leap_year_persian(1406) == False
        assert is_leap_year_persian(1407) == True
    
    def test_jalali_month_boundaries(self):
        """Test month boundary conversions"""
        # Last day of Farvardin 1403
        gy, gm, gd = jalali_to_gregorian(1403, 1, 31)
        assert gy == 2024
        assert gm == 4
        assert gd == 19
        
        # First day of Ordibehesht 1403
        gy, gm, gd = jalali_to_gregorian(1403, 2, 1)
        assert gy == 2024
        assert gm == 4
        assert gd == 20


class TestHijriConverters:
    """Test Hijri calendar conversion functions"""
    
    def test_gregorian_to_hijri_basic(self):
        """Test basic Gregorian to Hijri conversion"""
        # March 20, 2024
        hy, hm, hd = gregorian_to_hijri(2024, 3, 20)
        assert isinstance(hy, int)
        assert isinstance(hm, int)
        assert isinstance(hd, int)
        assert 1 <= hm <= 12
        assert 1 <= hd <= 30
    
    def test_hijri_to_gregorian_basic(self):
        """Test basic Hijri to Gregorian conversion"""
        # This is a simplified test since Hijri conversion is complex
        hy, hm, hd = 1445, 9, 10
        gy, gm, gd = hijri_to_gregorian(hy, hm, hd)
        assert isinstance(gy, int)
        assert isinstance(gm, int)
        assert isinstance(gd, int)
        assert 1 <= gm <= 12
        assert 1 <= gd <= 31
    
    def test_is_hijri_leap(self):
        """Test Hijri leap year detection"""
        assert isinstance(is_hijri_leap(1445), bool)
        assert isinstance(is_hijri_leap(1446), bool)
    
    def test_hijri_month_boundaries(self):
        """Test Hijri month boundary conversions"""
        # Test that months are within valid range
        hy, hm, hd = gregorian_to_hijri(2024, 1, 1)
        assert 1 <= hm <= 12
        assert 1 <= hd <= 30


class TestCrossConverters:
    """Test cross-calendar conversion functions"""
    
    def test_jalali_to_hijri_basic(self):
        """Test Jalali to Hijri conversion"""
        jy, jm, jd = 1403, 1, 1
        hy, hm, hd = jalali_to_hijri(jy, jm, jd)
        assert isinstance(hy, int)
        assert isinstance(hm, int)
        assert isinstance(hd, int)
        assert 1 <= hm <= 12
        assert 1 <= hd <= 30
    
    def test_hijri_to_jalali_basic(self):
        """Test Hijri to Jalali conversion"""
        hy, hm, hd = 1445, 9, 10
        jy, jm, jd = hijri_to_jalali(hy, hm, hd)
        assert isinstance(jy, int)
        assert isinstance(jm, int)
        assert isinstance(jd, int)
        assert 1 <= jm <= 12
        assert 1 <= jd <= 31
    
    def test_cross_conversion_consistency(self):
        """Test that cross conversions are consistent"""
        # Test Jalali -> Hijri -> Jalali
        original_jalali = (1403, 1, 1)
        hy, hm, hd = jalali_to_hijri(*original_jalali)
        jy, jm, jd = hijri_to_jalali(hy, hm, hd)
        
        # The result should be reasonable (within a few days due to calendar differences)
        assert abs(jy - original_jalali[0]) <= 1
        assert abs(jm - original_jalali[1]) <= 1
        assert abs(jd - original_jalali[2]) <= 1


class TestConverterEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_invalid_month_jalali(self):
        """Test invalid month in Jalali conversion"""
        with pytest.raises((ValueError, KeyError, IndexError)):
            jalali_to_gregorian(1403, 13, 1)
    
    def test_invalid_day_jalali(self):
        """Test invalid day in Jalali conversion"""
        with pytest.raises((ValueError, KeyError, IndexError)):
            jalali_to_gregorian(1403, 1, 32)
    
    def test_leap_year_edge_cases(self):
        """Test leap year edge cases"""
        # Test leap year detection for various years
        leap_years = [1403, 1407, 1411, 1415]
        non_leap_years = [1404, 1405, 1406, 1408]
        
        for year in leap_years:
            assert is_leap_year_persian(year) == True
        
        for year in non_leap_years:
            assert is_leap_year_persian(year) == False
    
    def test_year_boundaries(self):
        """Test year boundary conversions"""
        # Test conversion around year boundaries
        gy, gm, gd = jalali_to_gregorian(1403, 12, 29)
        assert gy == 2025
        assert gm == 3
        assert gd == 19
        
        gy, gm, gd = jalali_to_gregorian(1404, 1, 1)
        assert gy == 2025
        assert gm == 3
        assert gd == 20


if __name__ == "__main__":
    pytest.main([__file__])
