import datetime
from copy import copy
import calendar

from pytest import fixture, raises
from bs4 import BeautifulSoup

from pyluach import dates, hebrewcal
from pyluach.hebrewcal import Year, Month, holiday, festival, fast_day
from pyluach.hebrewcal import HebrewTextCalendar, HebrewHTMLCalendar


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

    def test_monthscount(self):
        year = Year(5782)
        assert year.monthscount() == 13
        assert (year + 1).monthscount() == 12

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
        assert years[1] != 5778

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

    def test_errors(self, years):
        with raises(TypeError):
            years[1] > 5778
        with raises(TypeError):
            years[1] >= 0
        with raises(TypeError):
            years[1] < '5778'
        with raises(TypeError):
            years[1] <= 10000


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
        workingdate = dates.HebrewDate(year, 7, 1)
        for month in (list(range(7, 13)) + list(range(1, 7))):
            for date in Month(year, month).iterdates():
                assert date == workingdate
                workingdate += 1

    def test_molad(self):
        month = Month(5779, 7)
        assert month.molad() == {'weekday': 2, 'hours': 14, 'parts': 316}
        month = Month(5779, 5)
        assert month.molad() == {'weekday': 5, 'hours': 10, 'parts': 399}

    def test_molad_announcement(self):
        month = Month(5780, 3)
        assert month.molad_announcement() == {
            'weekday': 6, 'hour': 11, 'minutes': 42, 'parts': 13
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
            'weekday': 1, 'hour': 21, 'minutes': 30, 'parts': 10
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
        with raises(ValueError):
            Month(5781, 14)

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
    month12 = Month(5781, 12)
    return {1: month1, 2: month2, 3: month3, 12: month12}


class TestCompareMonth:

    def test_month_gt(self, months):
        assert months[2] > months[1]
        assert not (months[1] > months[2])
        assert months[3] > months[1]
        assert not (months[2] > months[3])
        assert months[3] > months[12]
        assert not (months[12] > months[3])

    def test_month_ge(self, months):
        assert copy(months[1]) >= months[1]
        assert months[2] >= months[1]
        assert (months[2] >= months[3]) is False
        assert months[3] >= months[12]

    def test_month_lt(self, months):
        assert (copy(months[2]) < months[2]) is False
        assert months[1] < months[2]
        assert months[2] < months[3]
        assert (months[3] < months[1]) is False
        assert Month(5780, 12) < months[1]

    def test_month_le(self, months):
        assert copy(months[2]) <= months[2]
        assert months[1] <= months[2]
        assert (months[3] <= months[2]) is False
        assert months[12] <= months[3]

    def test_month_ne(self, months):
        assert months[2] != months[1]
        assert months[3] != months[1]
        assert (copy(months[1]) != months[1]) is False
        assert months[3] != 3

    def test_month_errors(self, months):
        with raises(TypeError):
            months[1] > 5
        with raises(TypeError):
            assert months[2] <= '5'
        with raises(TypeError):
            assert months[1] >= 0
        with raises(TypeError):
            assert months[3] < 100


class TestHoliday:

    def test_roshhashana(self):
        roshhashana = dates.HebrewDate(5779, 7, 1)
        assert all([
            holiday(day, location) == 'Rosh Hashana'
            for day in [roshhashana, roshhashana + 1]
            for location in [True, False]
        ])
        assert all((
            festival(
                day, location,
                include_working_days=included_days
            ) == 'Rosh Hashana'
            for day in [roshhashana, roshhashana + 1]
            for location in [True, False]
            for included_days in [True, False]
        ))

    def test_yomkippur(self):
        yom_kippur = dates.HebrewDate(5775, 7, 10)
        assert holiday(yom_kippur) == 'Yom Kippur'
        assert holiday(yom_kippur, hebrew=True) == 'יום כיפור'
        assert festival(yom_kippur, include_working_days=False) == 'Yom Kippur'

    def test_succos(self):
        second_day = dates.HebrewDate(5782, 7, 16)
        day = dates.HebrewDate(5778, 7, 18)
        assert festival(day) == 'Succos'
        day2 = dates.HebrewDate(5778, 7, 23)
        assert festival(day2, israel=True, hebrew=True) is None
        assert festival(day, include_working_days=False) is None
        assert (
            festival(second_day + 1, israel=True, include_working_days=False)
            is None
        )
        assert (
            festival(second_day, israel=False, include_working_days=False)
            == 'Succos'
        )

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
        chanuka = dates.HebrewDate(5782, 9, 25)
        assert festival(chanuka, include_working_days=False) is None

    def test_tubshvat(self):
        tubeshvat = dates.HebrewDate(5779, 11, 15)
        assert holiday(tubeshvat) == "Tu B'shvat"
        assert festival(tubeshvat, include_working_days=False) is None

    def test_purim(self):
        purims = [dates.HebrewDate(5778, 12, 14),
                  dates.HebrewDate(5779, 13, 14)]
        for purim in purims:
            assert holiday(purim, hebrew=True) == 'פורים'
            assert holiday(purim + 1) == 'Shushan Purim'
        assert holiday(dates.HebrewDate(5779, 12, 14)) == 'Purim Katan'
        for purim in purims:
            assert (
                festival(purim, israel=True, include_working_days=False)
                is None
            )

    def test_pesach(self):
        pesach = dates.HebrewDate(5778, 1, 15)
        for i in range(6):
            assert (
                holiday(pesach + i, True) == 'Pesach'
                and holiday(pesach + i) == 'Pesach'
            )
        eighth = pesach + 7
        assert holiday(eighth) == 'Pesach' and holiday(eighth, True) is None
        assert holiday(eighth + 1) is None
        chol_hamoed = [pesach + i for i in range(2, 6)]
        for day in chol_hamoed:
            assert festival(day, include_working_days=False) is None
        assert (
            festival(pesach + 1, israel=True, include_working_days=False)
            is None
        )

    def test_pesach_sheni(self):
        ps = dates.HebrewDate(5781, 2, 14)
        assert holiday(ps) == 'Pesach Sheni'
        assert holiday(ps + 1) is None
        assert festival(ps, include_working_days=False) is None

    def test_lagbaomer(self):
        lag_baomer = dates.GregorianDate(2018, 5, 3)
        assert festival(lag_baomer) == "Lag Ba'omer"
        assert festival(lag_baomer, hebrew=True) == 'ל״ג בעומר'
        assert (
            festival(lag_baomer, hebrew=True, include_working_days=False)
            is None
        )

    def test_shavuos(self):
        shavuos = dates.HebrewDate(5778, 3, 6)
        assert all(
            (holiday(day) == 'Shavuos' for day in [shavuos, shavuos + 1]))
        assert holiday(shavuos, True) == 'Shavuos'
        assert holiday(shavuos + 1, True) is None
        assert festival(shavuos + 1, include_working_days=False) == 'Shavuos'
        not_shavuos = dates.HebrewDate(5782, 4, 7)
        assert festival(not_shavuos) is None

    def test_tubeav(self):
        tubeav = dates.HebrewDate(5779, 5, 15)
        assert holiday(tubeav) == "Tu B'av"
        assert festival(tubeav, include_working_days=False) is None


class TestFasts:

    def test_gedalia(self):
        assert fast_day(dates.HebrewDate(5779, 7, 3)) == 'Tzom Gedalia'
        assert holiday(dates.HebrewDate(5778, 7, 3)) is None
        assert (
            holiday(dates.HebrewDate(5778, 7, 4), hebrew=True) == 'צום גדליה'
        )

    def test_asara(self):
        ten_of_teves = dates.GregorianDate(2018, 12, 18)
        assert holiday(ten_of_teves) == '10 of Teves'
        assert fast_day(ten_of_teves, hebrew=True) == 'י׳ בטבת'

    def test_esther(self):
        fasts = [
            dates.HebrewDate(5778, 12, 13),
            dates.HebrewDate(5776, 13, 13),
            dates.HebrewDate(5777, 12, 11),  # nidche
            dates.HebrewDate(5784, 13, 11)  # ibbur and nidche
        ]
        for fast in fasts:
            assert holiday(fast) == 'Taanis Esther'
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


def test_to_hebrew_numeral():
    assert hebrewcal.to_hebrew_numeral(5782) == 'תשפ״ב'


@fixture
def cal():
    return hebrewcal.HebrewCalendar()


class TestCalendar:

    def test_setfirstweekday(self, cal):
        cal.firstweekday = 2
        assert cal.firstweekday == 2
        assert cal._firstpyweekday == 0
        cal.firstweekday = 1

    def test_iterweekdays(self):
        for startingweekday in range(1, 8):
            cal = hebrewcal.HebrewCalendar(startingweekday)
            weekdays = list(cal.iterweekdays())
            assert len(weekdays) == 7
            assert weekdays[0] == startingweekday
            last = startingweekday - 1 or 7
            assert weekdays[-1] == last

    def test_first_month(self, cal):
        list(cal.itermonthdates(1, 7))

    def test_itermonthdates(self, cal):
        adar2 = list(cal.itermonthdates(5782, 13))
        assert adar2[0] == dates.HebrewDate(5782, 12, 26)
        assert adar2[-1] == dates.HebrewDate(5782, 1, 1)

    def test_minyear(self, cal):
        list(cal.itermonthdates(1, 1))

    def test_itermonthdays4(self, cal):
        nissan = list(cal.itermonthdays4(5782, 1))
        assert nissan[0] == (5782, 13, 24, 1)
        assert nissan[-1] == (5782, 2, 6, 7)

    def test_itermonthdays(self):
        for firstweekday in range(1, 8):
            cal = hebrewcal.HebrewCalendar(firstweekday)
            for y, m in [(1, 7), (6000, 12)]:
                days = list(cal.itermonthdays(y, m))
                assert len(days) in [35, 42]

    def test_itermonthdays2(self, cal):
        tishrei = list(cal.itermonthdays2(5783, 7))
        assert tishrei[0] == (0, 1)
        assert tishrei[-1] == (0, 7)

    def test_yeardatescalendar(self, cal):
        year = cal.yeardatescalendar(5783, 4)
        assert len(year) == 3
        assert len(year[1]) == 4
        assert year[2][3][4][6] == dates.HebrewDate(5784, 7, 1)

    def test_yeardays2calendar(self, cal):
        year = cal.yeardays2calendar(5784)
        assert len(year) == 5
        assert len(year[4]) == 1
        assert year[1][2][5][6] == (0, 7)
        assert year[2][0][2][0] == (14, 1)

    def test_yeardayscalendar(self, cal):
        year = cal.yeardayscalendar(5784)
        assert year[2][0][2][0] == 14

    def test_errors(self):
        with raises(hebrewcal.IllegalWeekdayError):
            hebrewcal.HebrewCalendar(0)
        with raises(hebrewcal.IllegalWeekdayError):
            hebrewcal.HebrewCalendar(8)

    def test_error_message(self):
        try:
            hebrewcal.HebrewCalendar(0)
        except hebrewcal.IllegalWeekdayError as e:
            assert str(e).startswith('bad weekday number 0;')
        try:
            Month(5781, 13)
        except hebrewcal.IllegalMonthError as e:
            assert str(e).startswith('bad month number 13;')


PARSER = 'html.parser'


def _soupbuilder(input, tag, class_):
    return BeautifulSoup(input, PARSER).find_all(tag, class_=class_)


@fixture
def htmlcal():
    return HebrewHTMLCalendar()


class TestHebrewHTMLCalendar:

    def test_formatday(self, htmlcal):
        assert htmlcal.formatday(0, 1) == '<td class="noday">&nbsp;</td>'
        assert htmlcal.formatday(1, 3) == '<td class="tue">א</td>'
        assert htmlcal.formatday(15, 7) == '<td class="sat">טו</td>'
        htmlcal.hebrewnumerals = False
        assert htmlcal.formatday(2, 2) == '<td class="mon">2</td>'
        assert htmlcal.formatday(21, 5) == '<td class="thu">21</td>'

    def test_length_in_months(self, htmlcal):
        months = _soupbuilder(htmlcal.formatyear(5784), 'table', 'month')
        assert len(months) == 13
        months = _soupbuilder(htmlcal.formatyear(5783), 'table', 'month')
        assert len(months) == 12

    def test_months(self, htmlcal):
        months = _soupbuilder(htmlcal.formatyear(5784), 'th', 'month')
        for i, month in enumerate(hebrewcal.Year(5784).itermonths()):
            assert months[i].string == month.month_name()
        htmlcal.hebrewmonths = True
        months = _soupbuilder(htmlcal.formatyear(5784), 'th', 'month')
        for i, month in enumerate(hebrewcal.Year(5784).itermonths()):
            assert months[i].string == month.month_name(True)

    def test_weekdays(self, htmlcal):
        year = htmlcal.formatyear(5783)
        sundays = _soupbuilder(year, 'th', 'sun')
        for sun in sundays:
            assert sun.string == calendar.day_abbr[6]
        htmlcal.hebrewweekdays = True
        mondays = _soupbuilder(htmlcal.formatyear(5782), 'th', 'mon')
        for mon in mondays:
            assert mon.string == 'שני'

    def test_days(self, htmlcal):
        year = htmlcal.formatyear(5782)
        soup = BeautifulSoup(year, PARSER)
        assert soup.find('td', class_='tue').string == 'א'
        assert soup.find_all('td', class_='tue')[2].string == 'טו'

    def test_year(self, htmlcal):
        month = htmlcal.formatmonth(5782, 2)
        header = BeautifulSoup(month, PARSER).find('th', class_='month')
        assert header.string == 'Iyar 5782'
        htmlcal.hebrewyear = True
        month = htmlcal.formatmonth(5782, 2)
        header = BeautifulSoup(month, PARSER).find('th', class_='month')
        assert header.string == 'Iyar תשפ״ב'

    def test_rtl(self, htmlcal):
        year = htmlcal.formatyear(5781)
        soup = BeautifulSoup(year, PARSER)
        assert soup.find('table', class_='year').get('dir', None) is None
        for month in soup.find_all('table', class_='month'):
            assert month.get('dir', None) is None
        htmlcal.rtl = True
        year = htmlcal.formatyear(5781)
        soup = BeautifulSoup(year, PARSER)
        assert soup.find('table', class_='year').get('dir', None) == 'rtl'
        for month in soup.find_all('table', class_='month'):
            assert month.get('dir', None) == 'rtl'


@fixture
def tcal():
    return HebrewTextCalendar()


class TestHebrewTextCalendar:

    def test_formatday(self, tcal):
        assert tcal.formatday(0, 1, 3) == '   '
        assert tcal.formatday(2, 4, 4) == '  ב '
        assert tcal.formatday(30, 5, 3) == '  ל'
        assert tcal.formatday(16, 7, 3) == ' טז'
        tcal.hebrewnumerals = False
        assert tcal.formatday(3, 2, 3) == '  3'
        assert tcal.formatday(30, 7, 3) == ' 30'

    def test_formatweekday(self, tcal):
        py_tcal = calendar.TextCalendar(6)
        for w in [3, 10]:
            assert tcal.formatweekday(7, w) == py_tcal.formatweekday(5, w)
        tcal.hebrewweekdays = True
        assert tcal.formatweekday(2, 4) == ' ב׳ '
        assert tcal.formatweekday(3, 5) == 'שלישי'

    def test_formatmonthname(self, tcal):
        assert tcal.formatmonthname(5782, 1) == 'Nissan 5782'
        assert tcal.formatmonthname(5784, 12) == 'Adar 1 5784'
        assert tcal.formatmonthname(5784, 12, withyear=False) == 'Adar 1'
        tcal.hebrewmonths = True
        tcal.hebrewyear = True
        assert tcal.formatmonthname(5784, 12) == 'אדר א׳ תשפ״ד'

    def test_formatyear(self, tcal):
        year = tcal.formatyear(5782)
        assert 'Adar 1' in year
        year = tcal.formatyear(5783)
        assert 'Adar 1' not in year
