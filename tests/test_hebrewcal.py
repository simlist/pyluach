import pytest

from pyluach import dates, hebrewcal
from pyluach.hebrewcal import Year, Month, holiday


class TestHoliday(object):

    def test_holiday(self):
        years = [5777, 5770, 5781]
        for year in years:
            assert holiday(dates.HebrewDate(year, 7, 1)) == 'Rosh Hashana'
            assert holiday(dates.HebrewDate(year, 7, 10)) == 'Yom Kippur'


class TestYear(object):

    def test_repryear(self):
        year = Year(5777)
        assert eval(repr(year)) == year

    def test_iteryear(self):
        assert list(Year(5777)) == [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        assert list(Year(5776)) == [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]

    def test_equalyear(self):
        year1 = hebrewcal.Year(5777)
        year2 = hebrewcal.Year(5777)
        assert year1 == year2

    def test_addtoyear(self):
        year = Year(5777)
        assert year + 2 == Year(5779)
        assert year + 0 == year

    def test_subtractintfromyear(self):
        year = Year(5777)
        assert year - 0 == year
        assert year - 3 == Year(5774)

    def test_subtractyearfromyear(self):
        year = Year(5777)
        assert year - year == 0
        assert year - (year - 1) == 1
        assert year - (year + 2) == 2


class TestMonth(object):

    def test_reprmonth(self):
        month = Month(5777, 10)
        assert eval(repr(month)) == month

    def test_equalmonth(self):
        month1 = hebrewcal.Month(5777, 12)
        month2 = hebrewcal.Month(5777, 12)
        assert month1 == month2

    def test_addinttomonth(self):
        month = hebrewcal.Month(5777, 12)
        assert month + 0 == month
        assert month + 1 == hebrewcal.Month(5777, 1)
        assert month + 6 == hebrewcal.Month(5777, 6)
        assert month + 7 == hebrewcal.Month(5778, 7)
        assert month + 35 == hebrewcal.Month(5780, 10)

    def test_subtract_month(self):
        month1 = hebrewcal.Month(5775, 10)
        month2 = hebrewcal.Month(5776, 10)
        month3 = hebrewcal.Month(5777, 10)
        assert month1 - month2 == 12
        assert month3 - month1 == 25

    def test_subtractintfrommonth(self):
        month = hebrewcal.Month(5778, 9)
        assert month - 2 == hebrewcal.Month(5778, 7)
        assert month - 3 == hebrewcal.Month(5777, 6)
        assert month - 30 == hebrewcal.Month(5775, 4)

class TestHoliday(object):

    def test_succos(self):
        day = dates.HebrewDate(5778, 7, 18)
        assert holiday(day) == 'Succos'
        day2 = dates.HebrewDate(5778, 7, 23)
        assert holiday(day2, israel=True) is None

    def test_chanuka(self):
        chanuka = dates.HebrewDate(5778, 9, 25)
        for i in range(8):
            assert holiday(chanuka + i) == 'Chanuka'

    def test_tubshvat(self):
        assert holiday(dates.HebrewDate(5779, 11, 15)) == "Tu B'shvat"

    def test_purim(self):
        purims = [dates.HebrewDate(5778, 12, 14),
                  dates.HebrewDate(5779, 13, 14)]
        for purim in purims:
            assert holiday(purim) == 'Purim'
            assert holiday(purim + 1) == 'Shushan Purim'
        assert holiday(dates.HebrewDate(5779, 12, 14)) == 'Purim Katan'
