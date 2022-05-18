import calendar

from pytest import fixture
from bs4 import BeautifulSoup

from pyluach import hebrewcal
from pyluach.hebrewcal import HebrewHTMLCalendar, HebrewTextCalendar


PARSER = 'html.parser'


def _soupbuilder(input, tag, class_):
    return BeautifulSoup(input, PARSER).find_all(tag, class_=class_)


@fixture
def cal():
    return HebrewHTMLCalendar()


class TestHebrewHTMLCalendar:

    def test_formatday(self, cal):
        assert cal.formatday(0, 1) == '<td class="noday">&nbsp;</td>'
        assert cal.formatday(1, 3) == '<td class="tue">א</td>'
        assert cal.formatday(15, 7) == '<td class="sat">טו</td>'
        cal.hebrewnumerals = False
        assert cal.formatday(2, 2) == '<td class="mon">2</td>'
        assert cal.formatday(21, 5) == '<td class="thu">21</td>'

    def test_length_in_months(self, cal):
        months = _soupbuilder(cal.formatyear(5784), 'table', 'month')
        assert len(months) == 13
        months = _soupbuilder(cal.formatyear(5783), 'table', 'month')
        assert len(months) == 12

    def test_months(self, cal):
        months = _soupbuilder(cal.formatyear(5784), 'th', 'month')
        for i, month in enumerate(hebrewcal.Year(5784).itermonths()):
            assert months[i].string == month.month_name()
        cal.hebrewmonths = True
        months = _soupbuilder(cal.formatyear(5784), 'th', 'month')
        for i, month in enumerate(hebrewcal.Year(5784).itermonths()):
            assert months[i].string == month.month_name(True)

    def test_weekdays(self, cal):
        year = cal.formatyear(5783)
        sundays = _soupbuilder(year, 'th', 'sun')
        for sun in sundays:
            assert sun.string == calendar.day_abbr[6]
        cal.hebrewweekdays = True
        mondays = _soupbuilder(cal.formatyear(5782), 'th', 'mon')
        for mon in mondays:
            assert mon.string == 'שני'

    def test_days(self, cal):
        year = cal.formatyear(5782)
        soup = BeautifulSoup(year, PARSER)
        assert soup.find('td', class_='tue').string == 'א'
        assert soup.find_all('td', class_='tue')[2].string == 'טו'

    def test_year(self, cal):
        month = cal.formatmonth(5782, 2)
        header = BeautifulSoup(month, PARSER).find('th', class_='month')
        assert header.string == 'Iyar 5782'
        cal.hebrewyear = True
        month = cal.formatmonth(5782, 2)
        header = BeautifulSoup(month, PARSER).find('th', class_='month')
        assert header.string == 'Iyar תשפ״ב'

    def test_rtl(self, cal):
        year = cal.formatyear(5781)
        soup = BeautifulSoup(year, PARSER)
        assert soup.find('table', class_='year').get('dir', None) is None
        for month in soup.find_all('table', class_='month'):
            assert month.get('dir', None) is None
        cal.rtl = True
        year = cal.formatyear(5781)
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
