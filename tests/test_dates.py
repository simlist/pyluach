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


class TestComparisons(object):
    """In ComparisonTests, comparisons are tested.

    Every function tests one test case comparing a date from each
    calendar type to another date from each calendar type.
    """

    def test_gt(self, setup):
        """Test all comparers when one date is greater."""
        for cal in setup['caltypes']:
            today = cal.today()
            for cal2 in setup['caltypes']:
                yesterday = cal2.today() - 1
                for comp in [gt, ge, ne]:
                    assert comp(today, yesterday)
                for comp in [eq, lt, le]:
                    assert comp(today, yesterday) is False

    def test_lt(self, setup):
        """Test all comparers when one date is less than another."""
        for cal in setup['caltypes']:
            today = cal.today()
            for cal2 in setup['caltypes']:
                tomorrow = cal2.today() + 1
                for comp in [lt, le, ne]:
                    assert comp(today, tomorrow)
                for comp in [gt, ge, eq]:
                    assert comp(today, tomorrow) is False

    def test_eq(self, setup):
        """Test all comparers when the dates are equal."""
        for cal in setup['caltypes']:
            today = cal.today()
            for cal2 in setup['caltypes']:
                today2 = cal2.today()
                for comp in [eq, ge, le]:
                    assert comp(today, today2)
                for comp in [gt, lt, ne]:
                    assert comp(today, today2) is False


class TestErrors(object):

    def test_too_low_heb(self):
        with pytest.raises(ValueError):
            dates.HebrewDate(0, 7, 1)
        with pytest.raises(ValueError):
            dates.HebrewDate(-1, 7, 1)

    def test_comparer_errors(self):
        day1 = dates.HebrewDate(5777, 12, 10)
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
        jd = JulianDay.today()
        assert eval(repr(jd)) == jd

def test_jd_str():
    assert str(JulianDay(550.5)) == '550.5'
    assert str(JulianDay(1008)) == '1007.5'

def test_weekday():
    assert GregorianDate(2017, 8, 7).weekday() == 2
    assert HebrewDate(5777, 6, 1).weekday() == 4

class TestMixinMethods():

    @pytest.fixture
    def date(self):
        return dates.GregorianDate(2017, 10, 31)

    def test_str(self, date):
        assert str(date) == '2017-10-31'

    def test_dict(self, date):
        assert date.dict() == {'year': 2017, 'month': 10, 'day': 31}

    def test_iter(self, date):
        assert list(date) == [date.year, date.month, date.day]
