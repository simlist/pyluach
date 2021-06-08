import datetime
from copy import copy

from pytest import fixture, raises
from pyluach import dates, hebrewcal
from pyluach.hebrewcal import Year, Month, holiday, festival, fast_day


class TestYear:

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
        with raises(TypeError):
            year + year
        with raises(TypeError):
            year + 'str'

    def test_subtractintfromyear(self):
        year = Year(5777)
        assert year - 0 == year
        assert year - 3 == Year(5774)
        with raises(TypeError):
            year - 'str'

    def test_subtractyearfromyear(self):
        year = Year(5777)
        assert year - year == 0
        assert year - (year - 1) == 1
        assert year - (year + 2) == 2

    def test_iterdays(self):
        year = Year(5778)
        yearlist = list(year.iterdays())
        assert len(yearlist) == len(year)
        assert yearlist[0] == 1
        assert yearlist[-1] == len(year)

    def test_iterdates(self):
        year = 5778
        workingdate = dates.HebrewDate(year, 7, 1)
        for date in Year(year).iterdates():
            assert workingdate == date
            workingdate += 1

    def test_errors(self):
        with raises(ValueError):
            Year(0)

    def test_year_string(self):
        year = Year(5781)
        assert year.year_string() == 'תשפ״א'
        assert year.year_string(True) == 'ה׳תשפ״א'

    def test_from_date(self):
        date = dates.GregorianDate(2021, 6, 7)
        year = Year.from_date(date)
        assert year == Year(date.to_heb().year)

    def test_from_pydate(self):
        pydate = datetime.date(2021, 6, 7)
        date = dates.HebrewDate.from_pydate(pydate)
        assert Year.from_pydate(pydate) == Year(date.year)


@fixture
def years():
    year1 = Year(5778)
    year2 = Year(5780)
    return {1: year1, 2: year2}


class TestYearComparisons:

    def test_year_equals(self, years):
        assert years[1] == copy(years[1])
        assert (years[1] == years[2]) is False
        assert years[2] != years[1]
        assert (copy(years[2]) != years[2]) is False

    def test_year_gt(self, years):
        assert years[2] > years[1]
        assert (years[1] > years[1]) is False

    def test_years_ge(self, years):
        assert copy(years[1]) >= years[1]
        assert years[2] >= years[1]
        assert (years[1] >= years[2]) is False

    def test_years_lt(self, years):
        assert years[1] < years[2]
        assert (copy(years[2]) < years[2]) is False
        assert (years[2] < years[1]) is False

    def test_years_le(self, years):
        assert copy(years[1]) <= years[1]
        assert years[1] <= years[2]
        assert (years[2] <= years[1]) is False

class TestMonth:

    def test_reprmonth(self):
        month = Month(5777, 10)
        assert eval(repr(month)) == month

    def test_equalmonth(self):
        month1 = hebrewcal.Month(5777, 12)
        month2 = hebrewcal.Month(5777, 12)
        assert month1 == month2
        assert not month1 == (month2 + 1)

    def test_addinttomonth(self):
        month = hebrewcal.Month(5777, 12)
        assert month + 0 == month
        assert month + 1 == hebrewcal.Month(5777, 1)
        assert month + 6 == hebrewcal.Month(5777, 6)
        assert month + 7 == hebrewcal.Month(5778, 7)
        assert month + 35 == hebrewcal.Month(5780, 10)
        with raises(TypeError):
            month + month
        with raises(TypeError):
            month + 'str'

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
        with raises(TypeError):
            month - 'str'

    def test_startingweekday(self):
        assert Month(5778, 8).starting_weekday() == 7
        assert Month(5778, 9).starting_weekday() == 1

    def test_iterdate(self):
        year = 5770
        workingdate = dates.HebrewDate(year, 7 ,1)
        for month in (list(range(7, 13)) + list(range(1, 7))):
            for date in Month(year, month).iterdates():
                assert date == workingdate
                workingdate += 1
    
    def test_molad(self):
        month = Month(5779, 7)
        assert month.molad() == {'weekday': 2, 'hours':14, 'parts': 316}
        month = Month(5779, 5)
        assert month.molad() == {'weekday':5, 'hours': 10, 'parts': 399}
    
    def test_molad_announcement(self):
        month = Month(5780, 3)
        assert month.molad_announcement() == {
            'weekday': 6, 'hour': 11, 'minutes':42, 'parts': 13
        }

        month = Month(5780, 2)
        assert month.molad_announcement() == {
            'weekday': 4, 'hour': 22, 'minutes': 58, 'parts': 12
        }
        month = Month(5780, 8)
        assert month.molad_announcement() == {
            'weekday': 2, 'hour': 18, 'minutes': 34, 'parts': 6
        }
        month = Month(5780, 12)
        assert month.molad_announcement() == {
            'weekday': 1, 'hour':21, 'minutes': 30, 'parts': 10
        }
        month = Month(5781, 1)
        assert month.molad_announcement() == {
            'weekday': 7, 'hour': 19, 'minutes': 3, 'parts': 5
        }
        month = Month(5781, 8)
        assert month.molad_announcement() == {
            'weekday': 7, 'hour': 3, 'minutes': 23, 'parts': 0
        }
    
    def test_month_name(self):
        month = Month(5781, 9)
        assert month.month_name() == 'Kislev'
        assert month.month_name(hebrew=True) == 'כסלו'
        adar = Month(5781, 12)
        assert adar.month_name() == 'Adar'
        adar_bais = Month(5782, 13)
        assert adar_bais.month_name() == 'Adar 2'

    def test_month_string(self):
        month = Month(5781, 3)
        assert month.month_string() == 'סיון תשפ״א'
        assert month.month_string(True) == 'סיון ה׳תשפ״א'

    def test_errors(self):
        with raises(ValueError):
            Month(-1, 1)
        with raises(ValueError):
            Month(5781, 13)

    def test_from_date(self):
        date = dates.HebrewDate(5781, 7, 10)
        assert Month.from_date(date) == Month(date.year, date.month)

    def test_from_pydate(self):
        pydate = datetime.date(2021, 6, 7)
        date = dates.HebrewDate.from_pydate(pydate)
        assert Month.from_pydate(pydate) == Month(date.year, date.month)

@fixture
def months():
    month1 = Month(5780, 3)
    month2 = Month(5780, 4)
    month3 = Month(5781, 3)
    return {1: month1, 2: month2, 3: month3}

class TestCompareMonth:

    def test_month_gt(self, months):
        assert months[2] > months[1]
        assert (months[1] > months[2]) is False
        assert months[3] > months[1]
        assert (months[2] > months[3]) is False

    def test_month_ge(self, months):
        assert copy(months[1]) >= months[1]
        assert months[2] >= months[1]
        assert (months[2] >= months[3]) is False

    def test_month_lt(self, months):
        assert (copy(months[2]) < months[2]) is False
        assert months[1] < months[2]
        assert months[2] < months[3]
        assert (months[3] < months[1]) is False
    
    def test_month_le(self, months):
        assert copy(months[2]) <= months[2]
        assert months[1] <= months[2]
        assert (months[3] <= months[2]) is False
    
    def rest_month_ne(self, months):
        assert months[2] != months[1]
        assert months[3] != months[1]
        assert (copy(months[1]) != months[1]) is False

class TestHoliday:

    def test_roshhashana(self):
        roshhashana = dates.HebrewDate(5779, 7, 1)
        assert all([holiday(day, location) == 'Rosh Hashana'
                    for day in[roshhashana, roshhashana + 1]
                    for location in [True, False]
                   ])

    def test_yomkippur(self):
        yom_kippur = dates.HebrewDate(5775, 7, 10)
        assert holiday(yom_kippur) == 'Yom Kippur'
        assert holiday(yom_kippur, hebrew=True) == 'יום כיפור'

    def test_succos(self):
        day = dates.HebrewDate(5778, 7, 18)
        assert festival(day) == 'Succos'
        day2 = dates.HebrewDate(5778, 7, 23)
        assert festival(day2, israel=True, hebrew=True) is None

    def test_shmini(self):
        shmini = dates.HebrewDate(5780, 7, 22)
        assert holiday(shmini, True) == 'Shmini Atzeres'
        assert holiday(shmini) == 'Shmini Atzeres'
        assert holiday(shmini + 1) == 'Simchas Torah'
        assert holiday(shmini + 1, True) is None

    def test_chanuka(self):
        for year in [5778, 5787]:
            chanuka = dates.HebrewDate(year, 9, 25)
            for i in range(8):
                assert holiday(chanuka + i) == 'Chanuka'
            assert holiday(chanuka + 8) is None

    def test_tubshvat(self):
        assert holiday(dates.HebrewDate(5779, 11, 15)) == "Tu B'shvat"

    def test_purim(self):
        purims = [dates.HebrewDate(5778, 12, 14),
                  dates.HebrewDate(5779, 13, 14)]
        for purim in purims:
            assert holiday(purim, hebrew=True) == 'פורים'
            assert holiday(purim + 1) == 'Shushan Purim'
        assert holiday(dates.HebrewDate(5779, 12, 14)) == 'Purim Katan'

    def test_pesach(self):
        pesach = dates.HebrewDate(5778, 1, 15)
        for i in range (6):
            assert (
                    holiday(pesach + i, True) == 'Pesach' and
                    holiday(pesach + i) == 'Pesach'
                   )
        eighth = pesach + 7
        assert holiday(eighth) == 'Pesach' and holiday(eighth, True) is None
        assert holiday(eighth + 1) is None

    def test_pesach_sheni(self):
        ps = dates.HebrewDate(5781, 2, 14)
        assert holiday(ps) == 'Pesach Sheni'
        assert holiday(ps + 1) is None

    def test_lagbaomer(self):
        lag_baomer = dates.GregorianDate(2018, 5, 3)
        assert festival(lag_baomer) == "Lag Ba'omer"
        assert festival(lag_baomer, hebrew=True) == 'ל״ג בעומר'

    def test_shavuos(self):
        shavuos = dates.HebrewDate(5778, 3, 6)
        assert all([holiday(day) == 'Shavuos' for day in [shavuos, shavuos + 1]])
        assert holiday(shavuos, True) == 'Shavuos'
        assert holiday(shavuos + 1, True) is None

    def test_tubeav(self):
        assert holiday(dates.HebrewDate(5779, 5, 15)) == "Tu B'av"

class TestFasts:

    def test_gedalia(self):
        assert fast_day(dates.HebrewDate(5779, 7, 3)) == 'Tzom Gedalia'
        assert holiday(dates.HebrewDate(5778, 7, 3)) is None
        assert holiday(dates.HebrewDate(5778, 7, 4), hebrew=True) == 'צום גדליה'

    def test_asara(self):
        ten_of_teves = dates.GregorianDate(2018, 12, 18)
        assert holiday(ten_of_teves) == '10 of Teves'
        assert fast_day(ten_of_teves, hebrew=True) == 'י׳ בטבת'

    def test_esther(self):
        fasts = [
            dates.HebrewDate(5778, 12, 13),
            dates.HebrewDate(5776, 13, 13),
            dates.HebrewDate(5777, 12, 11),  #nidche
            dates.HebrewDate(5784, 13, 11)  #ibbur and nidche
        ]
        for fast in fasts:
            assert holiday(fast)  == 'Taanis Esther'
        non_fasts = [
            dates.HebrewDate(5776, 12, 13),
            dates.HebrewDate(5777, 12, 13),
            dates.HebrewDate(5784, 12, 11),
            dates.HebrewDate(5784, 13, 13)
        ]
        for non in non_fasts:
            assert holiday(non) is None

    def test_tamuz(self):
        fasts = [dates.HebrewDate(5777, 4, 17), dates.HebrewDate(5778, 4, 18)]
        for fast in fasts:
            assert holiday(fast) == '17 of Tamuz'
        assert holiday(dates.HebrewDate(5778, 4, 17)) is None

    def test_av(self):
        fasts = [dates.HebrewDate(5777, 5, 9), dates.HebrewDate(5778, 5, 10)]
        for fast in fasts:
            assert holiday(fast) == '9 of Av'
        assert holiday(dates.HebrewDate(5778, 5, 9)) is None
