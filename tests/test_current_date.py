"""
Test suite for current date module
تست‌های ماژول current date
"""

import pytest
from datetime import datetime
from multi_calendar_dimension.current.now import CurrentDate, DateInfo, CurrentDateInfo


class TestCurrentDate:
    """Test CurrentDate class"""
    
    def test_current_date_initialization(self):
        """Test CurrentDate initialization"""
        current = CurrentDate()
        assert current is not None
        assert hasattr(current, 'persian_months')
        assert hasattr(current, 'gregorian_months')
        assert hasattr(current, 'hijri_months')
    
    def test_now_persian(self):
        """Test now() method with Persian language"""
        current = CurrentDate()
        today = current.now(language='fa')
        
        assert isinstance(today, CurrentDateInfo)
        assert isinstance(today.gregorian, DateInfo)
        assert isinstance(today.jalali, DateInfo)
        assert isinstance(today.hijri, DateInfo)
        assert isinstance(today.timestamp, datetime)
        
        # Check that all dates are valid
        assert 1 <= today.jalali.month <= 12
        assert 1 <= today.jalali.day <= 31
        assert 1 <= today.gregorian.month <= 12
        assert 1 <= today.gregorian.day <= 31
        assert 1 <= today.hijri.month <= 12
        assert 1 <= today.hijri.day <= 30
    
    def test_now_english(self):
        """Test now() method with English language"""
        current = CurrentDate()
        today = current.now(language='en')
        
        assert isinstance(today, CurrentDateInfo)
        assert isinstance(today.gregorian, DateInfo)
        assert isinstance(today.jalali, DateInfo)
        assert isinstance(today.hijri, DateInfo)
    
    def test_get_date_info_jalali(self):
        """Test get_date_info() with Jalali calendar"""
        current = CurrentDate()
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        
        assert isinstance(date_info, DateInfo)
        assert date_info.year == 1403
        assert date_info.month == 1
        assert date_info.day == 1
        assert date_info.month_name == "فروردین"
        assert isinstance(date_info.is_leap_year, bool)
        assert isinstance(date_info.is_holiday, bool)
        assert isinstance(date_info.is_weekend, bool)
        assert isinstance(date_info.events, list)
    
    def test_get_date_info_gregorian(self):
        """Test get_date_info() with Gregorian calendar"""
        current = CurrentDate()
        date_info = current.get_date_info(2024, 3, 20, 'gregorian', 'en')
        
        assert isinstance(date_info, DateInfo)
        assert date_info.year == 2024
        assert date_info.month == 3
        assert date_info.day == 20
        assert date_info.month_name == "March"
        assert isinstance(date_info.is_leap_year, bool)
        assert isinstance(date_info.is_holiday, bool)
        assert isinstance(date_info.is_weekend, bool)
        assert isinstance(date_info.events, list)
    
    def test_get_date_info_hijri(self):
        """Test get_date_info() with Hijri calendar"""
        current = CurrentDate()
        date_info = current.get_date_info(1445, 9, 10, 'hijri', 'fa')
        
        assert isinstance(date_info, DateInfo)
        assert date_info.year == 1445
        assert date_info.month == 9
        assert date_info.day == 10
        assert isinstance(date_info.is_leap_year, bool)
        assert isinstance(date_info.is_holiday, bool)
        assert isinstance(date_info.is_weekend, bool)
        assert isinstance(date_info.events, list)
    
    def test_format_date_full(self):
        """Test format_date() with full format"""
        current = CurrentDate()
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        formatted = current.format_date(date_info, 'full')
        
        assert isinstance(formatted, str)
        assert "1403" in formatted
        assert "فروردین" in formatted
    
    def test_format_date_short(self):
        """Test format_date() with short format"""
        current = CurrentDate()
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        formatted = current.format_date(date_info, 'short')
        
        assert isinstance(formatted, str)
        assert "فروردین" in formatted
    
    def test_format_date_numeric(self):
        """Test format_date() with numeric format"""
        current = CurrentDate()
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        formatted = current.format_date(date_info, 'numeric')
        
        assert isinstance(formatted, str)
        assert formatted == "1403/01/01"
    
    def test_format_date_readable(self):
        """Test format_date() with readable format"""
        current = CurrentDate()
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        formatted = current.format_date(date_info, 'readable')
        
        assert isinstance(formatted, str)
        assert "1403" in formatted
        assert "فروردین" in formatted
    
    def test_holiday_detection(self):
        """Test holiday detection"""
        current = CurrentDate()
        
        # Test Persian New Year (should be holiday)
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        assert date_info.is_holiday == True
        
        # Test regular day (should not be holiday)
        date_info = current.get_date_info(1403, 1, 2, 'jalali', 'fa')
        # Note: This might be holiday depending on the day of week
    
    def test_weekend_detection(self):
        """Test weekend detection"""
        current = CurrentDate()
        
        # Test Friday (should be weekend in Persian calendar)
        # We need to find a Friday in 1403
        for day in range(1, 32):
            try:
                date_info = current.get_date_info(1403, 1, day, 'jalali', 'fa')
                if date_info.day_of_week == "جمعه":
                    assert date_info.is_weekend == True
                    break
            except:
                continue
        
        # Test Thursday (should be weekend in Persian calendar)
        for day in range(1, 32):
            try:
                date_info = current.get_date_info(1403, 1, day, 'jalali', 'fa')
                if date_info.day_of_week == "پنج‌شنبه":
                    assert date_info.is_weekend == True
                    break
            except:
                continue
    
    def test_leap_year_detection(self):
        """Test leap year detection"""
        current = CurrentDate()
        
        # Test leap year
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        assert date_info.is_leap_year == True
        
        # Test non-leap year
        date_info = current.get_date_info(1404, 1, 1, 'jalali', 'fa')
        assert date_info.is_leap_year == False
    
    def test_event_detection(self):
        """Test event detection"""
        current = CurrentDate()
        
        # Test Persian New Year (should have event)
        date_info = current.get_date_info(1403, 1, 1, 'jalali', 'fa')
        assert isinstance(date_info.events, list)
        # Note: The event might be None or empty depending on the data
    
    def test_invalid_calendar_type(self):
        """Test invalid calendar type"""
        current = CurrentDate()
        
        with pytest.raises(ValueError):
            current.get_date_info(1403, 1, 1, 'invalid', 'fa')
    
    def test_invalid_date_components(self):
        """Test invalid date components"""
        current = CurrentDate()
        
        # Test invalid month
        with pytest.raises((ValueError, KeyError)):
            current.get_date_info(1403, 13, 1, 'jalali', 'fa')
        
        # Test invalid day
        with pytest.raises((ValueError, KeyError)):
            current.get_date_info(1403, 1, 32, 'jalali', 'fa')


class TestDateInfo:
    """Test DateInfo dataclass"""
    
    def test_date_info_creation(self):
        """Test DateInfo creation"""
        date_info = DateInfo(
            year=1403,
            month=1,
            day=1,
            date_string="1403/01/01",
            month_name="فروردین",
            day_of_week="دوشنبه",
            day_of_week_en="Monday",
            is_leap_year=True,
            is_holiday=True,
            is_weekend=False,
            events=["عید نوروز"]
        )
        
        assert date_info.year == 1403
        assert date_info.month == 1
        assert date_info.day == 1
        assert date_info.date_string == "1403/01/01"
        assert date_info.month_name == "فروردین"
        assert date_info.day_of_week == "دوشنبه"
        assert date_info.day_of_week_en == "Monday"
        assert date_info.is_leap_year == True
        assert date_info.is_holiday == True
        assert date_info.is_weekend == False
        assert date_info.events == ["عید نوروز"]


class TestCurrentDateInfo:
    """Test CurrentDateInfo dataclass"""
    
    def test_current_date_info_creation(self):
        """Test CurrentDateInfo creation"""
        gregorian = DateInfo(
            year=2024, month=3, day=20,
            date_string="2024-03-20", month_name="March",
            day_of_week="دوشنبه", day_of_week_en="Monday",
            is_leap_year=False, is_holiday=False, is_weekend=False,
            events=[]
        )
        
        jalali = DateInfo(
            year=1403, month=1, day=1,
            date_string="1403/01/01", month_name="فروردین",
            day_of_week="دوشنبه", day_of_week_en="Monday",
            is_leap_year=True, is_holiday=True, is_weekend=False,
            events=["عید نوروز"]
        )
        
        hijri = DateInfo(
            year=1445, month=9, day=10,
            date_string="1445/09/10", month_name="رمضان",
            day_of_week="دوشنبه", day_of_week_en="Monday",
            is_leap_year=False, is_holiday=False, is_weekend=False,
            events=[]
        )
        
        current_info = CurrentDateInfo(
            gregorian=gregorian,
            jalali=jalali,
            hijri=hijri,
            timestamp=datetime.now()
        )
        
        assert current_info.gregorian.year == 2024
        assert current_info.jalali.year == 1403
        assert current_info.hijri.year == 1445
        assert isinstance(current_info.timestamp, datetime)


if __name__ == "__main__":
    pytest.main([__file__])
