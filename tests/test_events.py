"""
Test suite for events module
تست‌های ماژول events
"""

import pytest
from multi_calendar_dimension.events import (
    persian_events, persian_holidays, hijri_official_holidays,
    gregorian_events_en, gregorian_events_fa, gregorian_holidays,
    hijri_events, hijri_events_en, hijri_holidays
)


class TestPersianEvents:
    """Test Persian events and holidays"""
    
    def test_persian_events_structure(self):
        """Test Persian events data structure"""
        assert isinstance(persian_events, dict)
        assert len(persian_events) > 0
        
        # Check that keys are tuples of (month, day)
        for key in persian_events.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 31
    
    def test_persian_holidays_structure(self):
        """Test Persian holidays data structure"""
        assert isinstance(persian_holidays, dict)
        assert len(persian_holidays) > 0
        
        # Check that keys are tuples of (month, day)
        for key in persian_holidays.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 31
        
        # Check that values are 0 or 1
        for value in persian_holidays.values():
            assert value in [0, 1]
    
    def test_persian_new_year_event(self):
        """Test Persian New Year event"""
        # Persian New Year is on 1/1
        assert (1, 1) in persian_events
        assert (1, 1) in persian_holidays
        assert persian_holidays[(1, 1)] == 1
    
    def test_persian_events_content(self):
        """Test Persian events content"""
        # Check that events are strings
        for event in persian_events.values():
            assert isinstance(event, str)
            assert len(event) > 0
    
    def test_hijri_official_holidays_structure(self):
        """Test Hijri official holidays structure"""
        assert isinstance(hijri_official_holidays, dict)
        assert len(hijri_official_holidays) > 0
        
        # Check that keys are tuples of (month, day)
        for key in hijri_official_holidays.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 30
        
        # Check that values are 0 or 1
        for value in hijri_official_holidays.values():
            assert value in [0, 1]


class TestGregorianEvents:
    """Test Gregorian events and holidays"""
    
    def test_gregorian_events_en_structure(self):
        """Test English Gregorian events structure"""
        assert isinstance(gregorian_events_en, dict)
        assert len(gregorian_events_en) > 0
        
        # Check that keys are tuples of (month, day)
        for key in gregorian_events_en.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 31
    
    def test_gregorian_events_fa_structure(self):
        """Test Persian Gregorian events structure"""
        assert isinstance(gregorian_events_fa, dict)
        assert len(gregorian_events_fa) > 0
        
        # Check that keys are tuples of (month, day)
        for key in gregorian_events_fa.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 31
    
    def test_gregorian_holidays_structure(self):
        """Test Gregorian holidays structure"""
        assert isinstance(gregorian_holidays, dict)
        assert len(gregorian_holidays) > 0
        
        # Check that keys are tuples of (month, day)
        for key in gregorian_holidays.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 31
        
        # Check that values are 0 or 1
        for value in gregorian_holidays.values():
            assert value in [0, 1]
    
    def test_new_years_day(self):
        """Test New Year's Day"""
        # New Year's Day is on 1/1
        assert (1, 1) in gregorian_events_en
        assert (1, 1) in gregorian_events_fa
        assert (1, 1) in gregorian_holidays
        assert gregorian_holidays[(1, 1)] == 1
    
    def test_christmas_day(self):
        """Test Christmas Day"""
        # Christmas is on 12/25
        assert (12, 25) in gregorian_events_en
        assert (12, 25) in gregorian_events_fa
        assert (12, 25) in gregorian_holidays
        assert gregorian_holidays[(12, 25)] == 1
    
    def test_gregorian_events_content(self):
        """Test Gregorian events content"""
        # Check that English events are strings
        for event in gregorian_events_en.values():
            assert isinstance(event, str)
            assert len(event) > 0
        
        # Check that Persian events are strings
        for event in gregorian_events_fa.values():
            assert isinstance(event, str)
            assert len(event) > 0


class TestHijriEvents:
    """Test Hijri events and holidays"""
    
    def test_hijri_events_structure(self):
        """Test Hijri events structure"""
        assert isinstance(hijri_events, dict)
        assert len(hijri_events) > 0
        
        # Check that keys are tuples of (month, day)
        for key in hijri_events.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 30
    
    def test_hijri_events_en_structure(self):
        """Test English Hijri events structure"""
        assert isinstance(hijri_events_en, dict)
        assert len(hijri_events_en) > 0
        
        # Check that keys are tuples of (month, day)
        for key in hijri_events_en.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 30
    
    def test_hijri_holidays_structure(self):
        """Test Hijri holidays structure"""
        assert isinstance(hijri_holidays, dict)
        assert len(hijri_holidays) > 0
        
        # Check that keys are tuples of (month, day)
        for key in hijri_holidays.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], int)  # month
            assert isinstance(key[1], int)  # day
            assert 1 <= key[0] <= 12
            assert 1 <= key[1] <= 30
        
        # Check that values are 0 or 1
        for value in hijri_holidays.values():
            assert value in [0, 1]
    
    def test_ashura_holiday(self):
        """Test Ashura holiday"""
        # Ashura is on 1/10 (Muharram 10th)
        assert (1, 10) in hijri_events
        assert (1, 10) in hijri_events_en
        assert (1, 10) in hijri_holidays
        assert hijri_holidays[(1, 10)] == 1
    
    def test_eid_al_fitr(self):
        """Test Eid al-Fitr"""
        # Eid al-Fitr is on 10/1 (Shawwal 1st)
        assert (10, 1) in hijri_events
        assert (10, 1) in hijri_events_en
        assert (10, 1) in hijri_holidays
        assert hijri_holidays[(10, 1)] == 1
    
    def test_hijri_events_content(self):
        """Test Hijri events content"""
        # Check that Persian events are strings
        for event in hijri_events.values():
            assert isinstance(event, str)
            assert len(event) > 0
        
        # Check that English events are strings
        for event in hijri_events_en.values():
            assert isinstance(event, str)
            assert len(event) > 0


class TestEventsConsistency:
    """Test consistency between different event types"""
    
    def test_holiday_event_consistency(self):
        """Test that holidays have corresponding events"""
        # Check Persian holidays
        for (month, day) in persian_holidays.keys():
            if persian_holidays[(month, day)] == 1:
                # Holiday should have an event
                assert (month, day) in persian_events
        
        # Check Gregorian holidays
        for (month, day) in gregorian_holidays.keys():
            if gregorian_holidays[(month, day)] == 1:
                # Holiday should have an event
                assert (month, day) in gregorian_events_en
                assert (month, day) in gregorian_events_fa
        
        # Check Hijri holidays
        for (month, day) in hijri_holidays.keys():
            if hijri_holidays[(month, day)] == 1:
                # Holiday should have an event
                assert (month, day) in hijri_events
                assert (month, day) in hijri_events_en
    
    def test_event_language_consistency(self):
        """Test that events exist in both languages"""
        # Check Gregorian events
        for (month, day) in gregorian_events_en.keys():
            assert (month, day) in gregorian_events_fa
        
        for (month, day) in gregorian_events_fa.keys():
            assert (month, day) in gregorian_events_en
        
        # Check Hijri events
        for (month, day) in hijri_events.keys():
            assert (month, day) in hijri_events_en
        
        for (month, day) in hijri_events_en.keys():
            assert (month, day) in hijri_events
    
    def test_month_day_validity(self):
        """Test that all month/day combinations are valid"""
        # Persian calendar: months 1-6 have 31 days, 7-11 have 30 days, 12 has 29/30 days
        persian_month_days = {1: 31, 2: 31, 3: 31, 4: 31, 5: 31, 6: 31,
                             7: 30, 8: 30, 9: 30, 10: 30, 11: 30, 12: 30}
        
        for (month, day) in persian_events.keys():
            assert 1 <= month <= 12
            assert 1 <= day <= persian_month_days[month]
        
        for (month, day) in persian_holidays.keys():
            assert 1 <= month <= 12
            assert 1 <= day <= persian_month_days[month]
        
        # Gregorian calendar: standard month lengths
        gregorian_month_days = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                               7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        
        for (month, day) in gregorian_events_en.keys():
            assert 1 <= month <= 12
            assert 1 <= day <= gregorian_month_days[month]
        
        # Hijri calendar: all months have 29 or 30 days
        for (month, day) in hijri_events.keys():
            assert 1 <= month <= 12
            assert 1 <= day <= 30


if __name__ == "__main__":
    pytest.main([__file__])
