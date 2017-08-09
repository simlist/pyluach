#! python

import unittest
import pytest
from operator import gt, lt, eq, ne, ge, le, add, sub

from pyluach import dates
from pyluach.dates import HebrewDate, GregorianDate, JulianDay


KNOWN_VALUES = {(2009, 8, 21): (5769, 6, 1),
                (2009, 9, 30): (5770, 7, 12),
                (2009, 11, 13): (5770, 8, 26),
                (2010, 1, 21): (5770, 11, 6),
                (2010, 5, 26): (5770, 3, 13),
                (2013, 11, 17): (5774, 9, 14),
                (2014, 3, 12): (5774, 13, 10),
                (2014, 6, 10): (5774, 3, 12),
                (2016, 2, 10): (5776, 12, 1)
                }


@pytest.fixture(scope='module')
def datetypeslist():
    datetypes = [dates.HebrewDate, dates.GregorianDate]
    return datetypes


class TestClassesSanity(object):
    def test_greg_sanity(self):
        for i in range(347998, 2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_greg().to_jd()
            assert jd.day == conf.day

    def test_heb_sanity(self):
        for i in range(347998, 2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_heb().to_jd()
            assert jd.day == conf.day


class TestClassesConversion(object):
    def test_from_greg(self):
        for date in KNOWN_VALUES:
            heb = dates.GregorianDate(*date).to_heb().tuple()
            assert KNOWN_VALUES[date] == heb

    def test_from_heb(self):
        for date in KNOWN_VALUES:
            greg = dates.HebrewDate(*KNOWN_VALUES[date]).to_greg().tuple()
            assert date == greg

@pytest.fixture
def setup(scope='module'):
    caltypes = [GregorianDate, HebrewDate, JulianDay]
    deltas =  [0, 1, 29, 73, 1004]
    return  {'caltypes': caltypes, 'deltas': deltas}

class TestOperators(object):

    def test_add(self, setup):
        for cal in setup['caltypes']:
            for delta in setup['deltas']:
                date = cal.today()
                date2 = date + delta
                assert date.jd + delta == date2.jd

    def test_min_int(self, setup):
        '''Test subtracting a number from a date'''
        for cal in setup['caltypes']:
            for delta in setup['deltas']:
                date = cal.today()
                date2 = date - delta
                assert date.jd - delta == date2.jd

    def test_min_date(self, setup):
        '''Test subtracting one date from another

        This test loops through subtracting the current date of each
        calendar from a date of each calendar at intervals from the
        current date.
        '''
        for cal in setup['caltypes']:
            for cal2 in setup['caltypes']:
                for delta in setup['deltas']:
                    today = cal.today()
                    difference = (cal2.today() - delta) - today
                    assert delta == difference


class TestComparisons(unittest.TestCase):
    """In ComparisonTests, comparisons are tested.

    Every function tests one test case comparing a date from each
    calendar type to another date from each calendar type.
    """

    def setUp(self):
        self.caltypes = [dates.GregorianDate, dates.HebrewDate,
                         dates.JulianDay]

    def test_gt(self):
        """Test all comparers when one date is greater."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                yesterday = cal2.today() - 1
                for comp in [gt, ge, ne]:
                    self.assertTrue(comp(today, yesterday))
                for comp in [eq, lt, le]:
                    self.assertFalse(comp(today, yesterday))

    def test_lt(self):
        """Test all comparers when one date is less than another."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                tomorrow = cal2.today() + 1
                for comp in [lt, le, ne]:
                    self.assertTrue(comp(today, tomorrow))
                for comp in [gt, ge, eq]:
                    self.assertFalse(comp(today, tomorrow))

    def test_eq(self):
        """Test all comparers when the dates are equal."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                today2 = cal2.today()
                for comp in [eq, ge, le]:
                    self.assertTrue(comp(today, today2))
                for comp in [gt, lt, ne]:
                    self.assertFalse(comp(today, today2))


class TestErrors(object):

    def test_too_low_heb(self):
        with pytest.raises(ValueError):
            dates.HebrewDate(0, 7, 1)
        with pytest.raises(ValueError):
            dates.HebrewDate(-1, 7, 1)

    def test_comparer_errors(self):
        day1 = dates.HebrewDate(5777, 12, 10)
        day2 = dates.HebrewDate(5777, 12, 14)
        for comparer in [gt, lt, eq, ne, ge, le]:
            for value in [1, 0, 'hello', None, '']:
                with pytest.raises(TypeError):
                    comparer(day1, value)

    def test_operator_errors(self):
        day = dates.GregorianDate(2016, 11, 20)
        for operator in [add, sub]:
            for value in ['Hello', '', None]:
                with pytest.raises(TypeError):
                    operator(day, value)
                with pytest.raises(TypeError):
                    day + (day+1)


class TestReprandStr(object):
    def test_repr(self, datetypeslist):
        for datetype in datetypeslist:
            assert eval(repr(datetype.today())) == datetype.today()


if __name__ == '__main__':
    unittest.main()
