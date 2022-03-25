"""The hebrewcal module implements classes for representing a Hebrew
year and month.

It also has functions for getting the holiday or fast day for a given
date.
"""
from collections import deque
from numbers import Number
import calendar

from pyluach.dates import HebrewDate
from pyluach import utils
from pyluach.gematria import _num_to_str
from pyluach.utils import _holiday, _fast_day_string, _festival_string


def fast_day(date, hebrew=False):
    """Return name of fast day or None.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    hebrew : bool, optional
      ``True`` if you want the fast_day name in Hebrew letters. Default
      is ``False``, which returns the name transliterated into English.

    Returns
    -------
    str or ``None``
      The name of the fast day or ``None`` if the given date is not
      a fast day.
    """
    return _fast_day_string(date, hebrew)


def festival(date, israel=False, hebrew=False, include_working_days=True):
    """Return Jewish festival of given day.

    This method will return all major and minor religous
    Jewish holidays not including fast days.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    israel : bool, optional
      ``True`` if you want the festivals according to the Israel
      schedule. Defaults to ``False``.

    hebrew : bool, optional
      ``True`` if you want the festival name in Hebrew letters. Default
      is ``False``, which returns the name transliterated into English.

    include_working_days : bool, optional
      ``True`` to include festival days on which melacha (work) is
      allowed; ie. Pesach Sheni, Chol Hamoed, etc.
      Default is ``True``.

    Returns
    -------
    str or ``None``
      The name of the festival or ``None`` if the given date is not
      a Jewish festival.
    """
    return _festival_string(date, israel, hebrew, include_working_days)


def holiday(date, israel=False, hebrew=False):
    """Return Jewish holiday of given date.

    The holidays include the major and minor religious Jewish
    holidays including fast days.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
        Any date that implements a ``to_heb()`` method which returns a
        ``HebrewDate`` can be used.
    israel : bool, optional
        ``True`` if you want the holidays according to the israel
        schedule. Defaults to ``False``.
    hebrew : bool, optional
        ``True`` if you want the holiday name in Hebrew letters. Default
        is ``False``, which returns the name transliterated into English.

    Returns
    -------
    str or ``None``
      The name of the holiday or ``None`` if the given date is not
      a Jewish holiday.
    """
    return _holiday(date, israel, hebrew)


class Year:
    """A Year object represents a Hebrew calendar year.

    It provided the following operators:

    =====================  ================================================
    Operation              Result
    =====================  ================================================
    year2 = year1 + int    New ``Year`` ``int``  days after year1.
    year2 = year1 - int    New ``Year`` ``int`` days before year1.
    int = year1 - year2    ``int`` equal to the absolute value of
                           the difference between year2 and year1.
    bool = year1 == year2  True if year1 represents the same year as year2.
    bool = year1 > year2   True if year1 is later than year2.
    bool = year1 >= year2  True if year1 is later or equal to year2.
    bool = year1 < year2   True if year 1 earlier than year2.
    bool = year1 <= year2  True if year 1 earlier or equal to year 2.
    =====================  ================================================

    Parameters
    ----------
    year : int
        A Hebrew year.

    Attributes
    ----------
    year : int
        The hebrew year.
    leap : bool
        True if the year is a leap year else false.
    """

    def __init__(self, year):
        if year < 1:
            raise ValueError(f'Year {year} is before creation.')
        self.year = year
        self.leap = utils._is_leap(year)

    def __repr__(self):
        return f'Year({self.year})'

    def __len__(self):
        return utils._days_in_year(self.year)

    def __eq__(self, other):
        if isinstance(other, Year) and self.year == other.year:
            return True
        return False

    def __add__(self, other):
        """Add int to year."""
        try:
            return Year(self.year + other)
        except TypeError:
            return NotImplemented

    def __sub__(self, other):
        """Subtract int or Year from Year.

        If other is an int return a new Year other before original year. If
        other is a Year object, return delta of the two years as an int.
        """
        if isinstance(other, Year):
            return abs(self.year - other.year)
        try:
            return Year(self.year - other)
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        if self.year > other.year:
            return True
        return False

    def __ge__(self, other):
        if self == other or self > other:
            return True
        return False

    def __lt__(self, other):
        if self.year < other.year:
            return True
        return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        return False

    def __iter__(self):
        """Yield integer for each month in year."""
        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not self.leap:
            months.remove(13)
        for month in months:
            yield month

    def itermonths(self):
        """Yield Month instance for each month of the year.

        Yields
        ------
        ``Month``
            The next month in the Hebrew calendar year as a
            ``luachcal.hebrewcal.Month`` instance beginning with
            Tishrei and ending with Elul.
        """
        for month in self:
            yield Month(self.year, month)

    def iterdays(self):
        """Yield integer for each day of the year.

        Yields
        ------
        int
            An integer beginning with 1 representing the next day of
            the year.
        """
        for day in range(1, len(self) + 1):
            yield day

    def iterdates(self):
        """Yield HebrewDate instance for each day of the year.

        Yields
        ------
        HebrewDate
            The next date of the Hebrew calendar year starting with
            the first of Tishrei.
        """
        for month in self.itermonths():
            for day in month:
                yield HebrewDate(self.year, month.month, day)

    @classmethod
    def from_date(cls, date):
        """Return Year object that given date occurs in.

        Parameters
        ----------
        date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
            Any one of the ``pyluach`` date types.

        Returns
        -------
        Year
        """
        return cls(date.to_heb().year)

    @classmethod
    def from_pydate(cls, pydate):
        """Return Year object from python date object.

        Parameters
        ----------
        pydate : ``datetime.date``
            A python standard library date object

        Returns
        -------
        Year
            The Hebrew year the given date occurs in
        """
        return cls.from_date(HebrewDate.from_pydate(pydate))

    def year_string(self, thousands=False):
        """Return year as a Hebrew string.

        Parameters
        ----------
        thousands: bool, optional
            ``True`` to prefix the year with the thousands place.
            default is ``False``.

        Examples
        --------
        >>> year = Year(5781)
        >>> year.year_string()
        תשפ״א
        >>> year.year_string(True)
        ה׳תשפ״א
        """
        return _num_to_str(self.year, thousands)


class Month:
    """A Month object represents a month of the Hebrew calendar.

    It provides the same operators as a `Year` object.

    Parameters
    ----------
    year : int
    month : int
        The month as an integer starting with 7 for Tishrei through 13
        if necessary for Adar Sheni and then 1-6 for Nissan - Elul.

    Attributes
    ----------
    year : int
        The Hebrew year.
    month : int
        The month as an integer starting with 7 for Tishrei through 13
        if necessary for Adar Sheni and then 1-6 for Nissan - Elul.
    name : str
        The name of the month.

        .. deprecated:: 1.3.0
            `name` attribute will be removed in pyluach 2.0.0, it is replaced
            by `month_name` method, because the latter allows a `hebrew`
            parameter. The month_name also uses slightly different
            transliteration.
    """

    _monthnames = {
        7: 'Tishrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Teves',
        11: 'Shvat', 13: 'Adar Sheni', 1: 'Nissan', 2: 'Iyar',
        3: 'Sivan', 4: 'Tamuz', 5: 'Av', 6: 'Elul'}

    def __init__(self, year, month):
        if year < 1:
            raise ValueError('Year is before creation.')
        self.year = year
        leap = utils._is_leap(self.year)
        yearlength = 13 if leap else 12
        if month < 1 or month > yearlength:
            raise ValueError(
                'Month must be between 1 and 12 for a normal '
                'year and 13 for a leap year.'
            )
        self.month = month
        self.name = utils._month_name(self.year, self.month, False)

    def __repr__(self):
        return f'Month({self.year}, {self.month})'

    def __len__(self):
        return utils._month_length(self.year, self.month)

    def __iter__(self):
        for day in range(1, len(self) + 1):
            yield day

    def __eq__(self, other):
        if(
           isinstance(other, Month)
           and self.year == other.year
           and self.month == other.month):
            return True
        return False

    def __add__(self, other):
        yearmonths = list(Year(self.year))
        index = yearmonths.index(self.month)
        leftover_months = len(yearmonths[index + 1:])
        try:
            if other <= leftover_months:
                return Month(self.year, yearmonths[index + other])
            return Month(self.year + 1, 7).__add__(other - 1 - leftover_months)
        except (AttributeError, TypeError):
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Number):
            yearmonths = list(Year(self.year))
            index = yearmonths.index(self.month)
            leftover_months = index
            if other <= leftover_months:
                return Month(self.year, yearmonths[index - other])
            return Month(
                self.year - 1,
                deque(Year(self.year - 1), maxlen=1).pop()
            ).__sub__(other - 1 - leftover_months)
            # Recursive call on the last month of the previous year.
        try:
            return abs(self._elapsed_months() - other._elapsed_months())
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        return (
            self.year > other.year
            or (
                self.year == other.year
                and self._month_number() > other._month_number()
            )
        )

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        return (
            self.year < other.year
            or (
                self.year == other.year
                and self._month_number() < other._month_number()
            )
        )

    def __le__(self, other):
        return self < other or self == other

    @classmethod
    def from_date(cls, date):
        """Return Month object that given date occurs in.

        Parameters
        ----------
        date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
            Any ``pyluach`` date type
        Returns
        -------
        Month
            The Hebrew month the given date occurs in
        """
        heb = date.to_heb()
        return Month(heb.year, heb.month)

    @classmethod
    def from_pydate(cls, pydate):
        """Return Month object from python date object.

        Parameters
        ----------
        pydate : ``datetime.date``
            A python standard library date object

        Returns
        -------
        Month
            The Hebrew month the given date occurs in
        """
        return cls.from_date(HebrewDate.from_pydate(pydate))

    def month_name(self, hebrew=False):
        """Return the name of the month.

        Replaces `name` attribute.

        Parameters
        ----------
        hebrew : bool, optional
            `True` if the month name should be written with Hebrew letters
            and False to be transliterated into English using the Ashkenazic
            pronunciation. Default is `False`.

        Returns
        -------
        str
        """
        return utils._month_name(self.year, self.month, hebrew)

    def month_string(self, thousands=False):
        """Return month and year in Hebrew.

        Parameters
        ----------
        thousands : bool, optional
            ``True`` to prefix year with thousands place.
            Default is ``False``.

        Returns
        -------
        str
            The month and year in Hebrew in the form ``f'{month} {year}'``.
        """
        return f'{self.month_name(True)} {_num_to_str(self.year, thousands)}'

    def starting_weekday(self):
        """Return first weekday of the month.

        Returns
        -------
        int
            The weekday of the first day of the month starting with Sunday as 1
            through Saturday as 7.
        """
        return HebrewDate(self.year, self.month, 1).weekday()

    def _month_number(self):
        """Return month number 1-12 or 13, Tishrei - Elul."""
        return list(Year(self.year)).index(self.month) + 1

    def _elapsed_months(self):
        """Return number of months elapsed from beginning of calendar"""
        yearmonths = tuple(Year(self.year))
        months_elapsed = (
            utils._elapsed_months(self.year)
            + yearmonths.index(self.month)
        )
        return months_elapsed

    def iterdates(self):
        """Return iterator that yields an instance of HebrewDate.

        Yields
        ------
        ``HebrewDate``
            The next Hebrew date of the month.
        """
        for day in self:
            yield HebrewDate(self.year, self.month, day)

    def molad(self):
        """Return the month's molad.

        Returns
        -------
        dict
            A dictionary in the form {weekday: int, hours: int, parts: int}

        Note
        -----
        This method does not return the molad in the form that is
        traditionally announced in the shul. This is the molad in the
        form used to calculate the length of the year.

        See Also
        --------
        molad_announcement: The molad as it is traditionally announced.
        """
        months = self._elapsed_months()
        parts = 204 + months*793
        hours = 5 + months*12 + parts//1080
        days = 2 + months*29 + hours//24
        weekday = days % 7 or 7
        return {'weekday': weekday, 'hours': hours % 24, 'parts': parts % 1080}

    def molad_announcement(self):
        """Return the months molad in the announcement form.

        Returns a dictionary in the form that the molad is traditionally
        announced. The weekday is adjusted to change at midnight and
        the hour of the day and minutes are given as traditionally announced.
        Note that the hour is given as in a twenty four hour clock ie. 0 for
        12:00 AM through 23 for 11:00 PM.

        Returns
        -------
        dict
            A dictionary in the form::

                {
                    weekday: int,
                    hour: int,
                    minutes: int,
                    parts: int
                }
        """
        molad = self.molad()
        weekday = molad['weekday']
        hour = 18 + molad['hours']
        if hour < 24:
            if weekday != 1:
                weekday -= 1
            else:
                weekday = 7
        else:
            hour -= 24
        minutes = molad['parts'] // 18
        parts = molad['parts'] % 18
        return {
            'weekday': weekday, 'hour': hour,
            'minutes': minutes, 'parts': parts
        }


def _weekday(year, month, day):
    return HebrewDate(year, month, day).weekday()


def _month_range(year, month):
    return _weekday(year, month, 1), len(Month(year, month))


class Calendar(calendar.Calendar):
    """Calendar class."""
    def __init__(self, firstweekday=1):
        super().__init__(firstweekday)

    def _first_day(self, year, month):
        starting_date = HebrewDate(year, month, 1)
        starting_weekday = starting_date.weekday()
        if starting_weekday == self.firstweekday:
            return starting_date
        return starting_date - (starting_weekday - self.firstweekday) % 7
