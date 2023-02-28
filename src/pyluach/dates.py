"""The dates module implements classes for representing and
manipulating several date types.

Contents
--------
* :class:`Rounding`
* :class:`BaseDate`
* :class:`CalendarDateMixin`
* :class:`JulianDay`
* :class:`GregorianDate`
* :class:`HebrewDate`

Note
----
All instances of the classes in this module should be treated as read
only. No attributes should be changed once they're created.
"""

import abc
from datetime import date
from numbers import Number
from enum import Enum, auto

from pyluach import utils
from pyluach import gematria


class Rounding(Enum):
    """Enumerator to provide options for rounding Hebrew dates.

    This provides constants to use as arguments for functions. It
    should not be instantiated.

    Attributes
    ----------
    PREVIOUS_DAY
        If the day is the 30th and the month only has 29 days, round to
        the 29th of the month.
    NEXT_DAY
        If the day is the 30th and the month only has 29 days, round to
        the 1st of the next month.
    EXCEPTION
        If the day is the 30th and the month only has 29 days, raise a
        ValueError.
    """
    PREVIOUS_DAY = auto()
    NEXT_DAY = auto()
    EXCEPTION = auto()


class BaseDate(abc.ABC):
    """BaseDate is a base class for all date types.

    It provides the following arithmetic and comparison operators
    common to all child date types.

    ===================  =================================================
    Operation            Result
    ===================  =================================================
    d2 = date1 + int     New date ``int`` days after date1
    d2 = date1 - int     New date ``int`` days before date1
    int = date1 - date2  Positive integer equal to the duration from date1
                         to date2
    date1 > date2        True if date1 occurs later than date2
    date1 < date2        True if date1 occurs earlier than date2
    date1 == date2       True if date1 occurs on the same day as date2
    date1 != date2       True if ``date1 == date2`` is False
    ===================  =================================================

    Any subclass of ``BaseDate`` can be compared to and diffed with any other
    subclass date.
    """

    @property
    @abc.abstractmethod
    def jd(self):
        """Return julian day number.

        Returns
        -------
        float
            The Julian day number at midnight (as ``n.5``).
        """

    @abc.abstractmethod
    def to_heb(self):
        """Return Hebrew Date.

        Returns
        -------
        HebrewDate
        """

    def __hash__(self):
        return hash(repr(self))

    def __add__(self, other):
        try:
            return JulianDay(self.jd + other)._to_x(self)
        except TypeError:
            return NotImplemented

    def __sub__(self, other):
        try:
            if isinstance(other, Number):
                return JulianDay(self.jd - other)._to_x(self)
            return int(abs(self.jd - other.jd))
        except (AttributeError, TypeError):
            return NotImplemented

    def __eq__(self, other):
        try:
            return self.jd == other.jd
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self.jd != other.jd
        except AttributeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.jd < other.jd
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.jd > other.jd
        except AttributeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.jd <= other.jd
        except AttributeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.jd >= other.jd
        except AttributeError:
            return NotImplemented

    def weekday(self):
        """Return day of week as an integer.

        Returns
        -------
        int
            An integer representing the day of the week with Sunday as 1
            through Saturday as 7.
        """
        return int(self.jd+.5+1) % 7 + 1

    def isoweekday(self):
        """Return the day of the week corresponding to the iso standard.

        Returns
        -------
        int
            An integer representing the day of the week where Monday
            is 1 and and Sunday is 7.
        """
        weekday = self.weekday()
        if weekday == 1:
            return 7
        return weekday - 1

    def shabbos(self):
        """Return the Shabbos on or following the date.

        Returns
        -------
        JulianDay, GregorianDate, or HebrewDate
            `self` if the date is Shabbos or else the following Shabbos as
            the same date type as called from.

        Examples
        --------
        >>> heb_date = HebrewDate(5781, 3, 29)
        >>> greg_date = heb_date.to_greg()
        >>> heb_date.shabbos()
        HebrewDate(5781, 4, 2)
        >>> greg_date.shabbos()
        GregorianDate(2021, 6, 12)
        """
        return self + (7 - self.weekday())

    def _day_of_holiday(self, israel, hebrew=False):
        """Return the day of the holiday.

        Parameters
        ----------
        israel : bool, optional
        hebrew : bool, optional

        Returns
        -------
        str
        """
        name = utils._festival_string(self, israel)
        if name is not None:
            holiday = utils.Days(name)
            if holiday is utils.Days.SHAVUOS and israel:
                return ''
            first_day = utils._first_day_of_holiday(holiday)
            if first_day:
                day = HebrewDate(self.year, *first_day) - self + 1
                if hebrew:
                    day = gematria._num_to_str(day)
                return str(day)
        return ''

    def fast_day(self, hebrew=False):
        """Return name of fast day of date.

        Parameters
        ----------
        hebrew : bool, optional
            ``True`` if you want the fast day name in Hebrew letters. Default
            is ``False``, which returns the name transliterated into English.

        Returns
        -------
        str or None
            The name of the fast day or ``None`` if the date is not
            a fast day.
        """
        return utils._fast_day_string(self, hebrew)

    def festival(
        self,
        israel=False,
        hebrew=False,
        include_working_days=True,
        prefix_day=False
    ):
        """Return name of Jewish festival of date.

        This method will return all major and minor religous
        Jewish holidays not including fast days.

        Parameters
        ----------
        israel : bool, optional
            ``True`` if you want the holidays according to the Israel
            schedule. Defaults to ``False``.
        hebrew : bool, optional
            ``True`` if you want the festival name in Hebrew letters. Default
            is ``False``, which returns the name transliterated into English.
        include_working_days : bool, optional
            ``True`` to include festival days on which melacha (work) is
            allowed; ie. Pesach Sheni, Chol Hamoed, etc.
            Default is ``True``.
        prefix_day : bool, optional
            ``True`` to prefix multi day festivals with the day of the
            festival. Default is ``False``.

        Examples
        --------
        >>> pesach = HebrewDate(2023, 1, 15)
        >>> pesach.festival(prefix_day=True)
        '1 Pesach'
        >>> pesach.festival(hebrew=True, prefix_day=True)
        'א׳ פסח'
        >>> shavuos = HebrewDate(5783, 3, 6)
        >>> shavuos.festival(israel=True, prefix_day=True)
        'Shavuos'

        Returns
        -------
        str or None
            The name of the festival or ``None`` if the given date is not
            a Jewish festival.
        """
        name = utils._festival_string(
            self, israel, hebrew, include_working_days
        )
        if prefix_day and name is not None:
            day = self._day_of_holiday(israel=israel, hebrew=hebrew)
            if day:
                return f'{day} {name}'
        return name

    def holiday(self, israel=False, hebrew=False, prefix_day=False):
        """Return name of Jewish holiday of the date.

        The holidays include the major and minor religious Jewish
        holidays including fast days.

        Parameters
        ----------
        israel : bool, optional
            ``True`` if you want the holidays according to the Israel
            schedule. Defaults to ``False``.
        hebrew : bool, optional
            ``True`` if you want the holiday name in Hebrew letters. Default is
            ``False``, which returns the name transliterated into English.
        prefix_day : bool, optional
            ``True`` to prefix multi day holidays with the day of the
            holiday. Default is ``False``.

        Examples
        --------
        >>> pesach = HebrewDate(2023, 1, 15)
        >>> pesach.holiday(prefix_day=True)
        '1 Pesach'
        >>> pesach.holiday(hebrew=True, prefix_day=True)
        'א׳ פסח'
        >>> taanis_esther = HebrewDate(5783, 12, 13)
        >>> taanis_esther.holiday(prefix_day=True)
        'Taanis Esther'

        Returns
        -------
        str or None
            The name of the holiday or ``None`` if the given date is not
            a Jewish holiday.
        """
        return (
            self.fast_day(hebrew=hebrew)
            or self.festival(israel, hebrew, prefix_day=prefix_day)
        )


class CalendarDateMixin:
    """CalendarDateMixin is a mixin for Hebrew and Gregorian dates.

    Parameters
    ----------
    year : int
    month : int
    day : int

    Attributes
    ----------
    year : int
    month : int
    day : int
    jd : float
        The equivalent Julian day at midnight.
    """

    def __init__(self, year, month, day, jd=None):
        self.year = year
        self.month = month
        self.day = day
        self._jd = jd

    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name}({self.year}, {self.month}, {self.day})'

    def __str__(self):
        return f'{self.year:04d}-{self.month:02d}-{self.day:02d}'

    def __iter__(self):
        yield self.year
        yield self.month
        yield self.day

    def tuple(self):
        """Return date as tuple.

        Returns
        -------
        tuple of ints
            A tuple of ints in the form ``(year, month, day)``.
        """
        return (self.year, self.month, self.day)

    def dict(self):
        """Return the date as a dictionary.

        Returns
        -------
        dict
            A dictionary in the form
            ``{'year': int, 'month': int, 'day': int}``.
        """
        return {'year': self.year, 'month': self.month, 'day': self.day}

    def replace(self, year=None, month=None, day=None):
        """Return new date with new values for the specified field.

        Parameters
        ----------
        year : int, optional
        month: int, optional
        day : int, optional

        Returns
        -------
        CalendarDateMixin
            Any date that inherits from CalendarDateMixin
            (``GregorianDate``, ````HebrewDate``).

        Raises
        ValueError
            Raises a ``ValueError`` if the new date does not exist.
        """
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        return type(self)(year, month, day)


class JulianDay(BaseDate):
    """A JulianDay object represents a Julian Day at midnight.

    Parameters
    ----------
    day : float or int
        The julian day. Note that Julian days start at noon so day
        number 10 is represented as 9.5 which is day 10 at midnight.

    Attributes
    ----------
    day : float
        The Julian Day Number at midnight (as *n*.5)
    """

    def __init__(self, day):
        if day-int(day) < .5:
            self.day = int(day) - .5
        else:
            self.day = int(day) + .5

    def __repr__(self):
        return f'JulianDay({self.day})'

    def __str__(self):
        return str(self.day)

    @property
    def jd(self):
        """Return julian day.

        Returns
        -------
        float
        """
        return self.day

    @staticmethod
    def from_pydate(pydate):
        """Return a `JulianDay` from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance

        Returns
        -------
        JulianDay
        """
        return GregorianDate.from_pydate(pydate).to_jd()

    @staticmethod
    def today():
        """Return instance of current Julian day from timestamp.

        Extends the built-in ``datetime.date.today()``.

        Returns
        -------
        JulianDay
            A JulianDay instance representing the current Julian day from
            the timestamp.

        Warning
        -------
        Julian Days change at noon, but pyluach treats them as if they
        change at midnight, so at midnight this method will return
        ``JulianDay(n.5)`` until the following midnight when it will
        return ``JulianDay(n.5 + 1)``.
        """
        return GregorianDate.today().to_jd()

    def to_greg(self):
        """Convert JulianDay to a Gregorian Date.

        Returns
        -------
        GregorianDate
            The equivalent Gregorian date instance.

        Notes
        -----
        This method uses the Fliegel-Van Flandern algorithm.
        """
        jd = int(self.day + .5)
        L = jd + 68569
        n = 4*L // 146097
        L = L - (146097*n + 3) // 4
        i = (4000 * (L+1)) // 1461001
        L = L - ((1461*i) // 4) + 31
        j = (80*L) // 2447
        day = L - 2447*j // 80
        L = j // 11
        month = j + 2 - 12*L
        year = 100 * (n-49) + i + L
        if year < 1:
            year -= 1
        return GregorianDate(year, month, day, self.day)

    def to_heb(self):
        """ Convert to a Hebrew date.

        Returns
        -------
        HebrewDate
            The equivalent Hebrew date instance.
        """

        if self.day <= 347997:
            raise ValueError('Date is before creation')

        jd = int(self.day + .5)  # Try to account for half day
        jd -= 347997
        year = int(jd//365) + 2  # try that to debug early years
        first_day = utils._elapsed_days(year)

        while first_day > jd:
            year -= 1
            first_day = utils._elapsed_days(year)

        months = utils._monthslist(year)
        days_remaining = jd - first_day
        for month in months:
            if days_remaining >= utils._month_length(year, month):
                days_remaining -= utils._month_length(year, month)
            else:
                return HebrewDate(year, month, days_remaining + 1, self.day)

    def _to_x(self, type_):
        """Return a date object of the given type."""

        if isinstance(type_, GregorianDate):
            return self.to_greg()
        if isinstance(type_, HebrewDate):
            return self.to_heb()
        if isinstance(type_, JulianDay):
            return self
        raise TypeError(
            'This method has not been implemented with that type.'
        )

    def to_pydate(self):
        """Convert to a datetime.date object.

        Returns
        -------
        datetime.date
            A standard library ``datetime.date`` instance.
        """
        return self.to_greg().to_pydate()


class GregorianDate(BaseDate, CalendarDateMixin):
    """A GregorianDate object represents a Gregorian date (year, month, day).

    This is an idealized date with the current Gregorian calendar
    infinitely extended in both directions.

    Parameters
    ----------
    year : int
    month : int
    day : int
    jd : float, optional
      This parameter should not be assigned manually.

    Attributes
    ----------
    year : int
    month : int
    day : int

    Warnings
    --------
    Although B.C.E. dates are allowed, they should be treated as
    approximations as they may return inconsistent results when converting
    between date types and using arithmetic and comparison operators!
    """

    def __init__(self, year, month, day, jd=None):
        """Initialize a GregorianDate.

        This initializer extends the CalendarDateMixin initializer
        adding in date validation specific to Gregorian dates.
        """
        if month < 1 or month > 12:
            raise ValueError(f'{str(month)} is an invalid month.')
        monthlength = self._monthlength(year, month)
        if day < 1 or day > monthlength:
            raise ValueError(f'Given month has {monthlength} days.')
        super().__init__(year, month, day, jd)

    def __format__(self, fmt):
        return self.strftime(fmt)

    def strftime(self, fmt):
        """Return formatted date.

        Wraps :py:meth:`datetime.date.strftime` method and uses the same
        format options.

        Parameters
        ----------
        fmt : str
            The format string.

        Returns
        -------
        str
        """
        return self.to_pydate().strftime(fmt)

    @property
    def jd(self):
        """Return the corresponding Julian day number.

        Returns
        -------
        float
            The Julian day number at midnight.
        """
        if self._jd is None:
            year = self.year
            month = self.month
            day = self.day
            if year < 0:
                year += 1
            if month < 3:
                year -= 1
                month += 12
            month += 1
            a = year // 100
            b = 2 - a + a//4
            self._jd = (
                int(365.25*year) + int(30.6001*month) + b + day + 1720994.5
            )
        return self._jd

    @classmethod
    def from_pydate(cls, pydate):
        """Return a `GregorianDate` instance from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance.

        Returns
        -------
        GregorianDate
        """
        return cls(*pydate.timetuple()[:3])

    @staticmethod
    def today():
        """Return a GregorianDate instance for the current day.

        This static method wraps the Python standard library's
        date.today() method to get the date from the timestamp.

        Returns
        -------
        GregorianDate
          The current Gregorian date from the computer's timestamp.
        """
        return GregorianDate.from_pydate(date.today())

    @staticmethod
    def _is_leap(year):
        """Return True if year of date is a leap year, otherwise False."""
        if year < 0:
            year += 1
        if (year % 4 == 0) and not (year % 100 == 0 and year % 400 != 0):
            return True
        return False

    def is_leap(self):
        """Return if the date is in a leap year

        Returns
        -------
        bool
            True if the date is in a leap year, False otherwise.
        """
        return self._is_leap(self.year)

    @classmethod
    def _monthlength(cls, year, month):
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        if month == 2:
            if cls._is_leap(year):
                return 29
            return 28
        return 30

    def to_jd(self):
        """Convert to a Julian day.

        Returns
        -------
        JulianDay
            The equivalent JulianDay instance.
        """
        return JulianDay(self.jd)

    def to_heb(self):
        """Convert to Hebrew date.

        Returns
        -------
        HebrewDate
            The equivalent HebrewDate instance.
        """
        return self.to_jd().to_heb()

    def to_pydate(self):
        """Convert to a standard library date.

        Returns
        -------
        datetime.date
            The equivalent datetime.date instance.
        """
        return date(*self.tuple())


class HebrewDate(BaseDate, CalendarDateMixin):
    """A class for manipulating Hebrew dates.

    The following format options are available similar to strftime:

    ====== ======= ===========================================================
    Format Example Meaning
    ====== ======= ===========================================================
    %a     Sun     Weekday as locale's abbreviated name
    %A     Sunday  Weekday as locale's full name
    %w     1       Weekday as decimal number 1-7 Sunday-Shabbos
    %d     07      Day of the month as a 0-padded 2 digit decimal number
    %-d    7       Day of the month as a decimal number
    %B     Iyar    Month name transliterated into English
    %m     02      Month as a 0-padded 2 digit decimal number
    %-m    2       Month as a decimal number
    %y     82, 01  Year without century as a zero-padded decimal number
    %Y     5782    Year as a decimal number
    %*a    א׳      Weekday as a Hebrew numeral
    %*A    ראשון   Weekday name in Hebrew
    %*d    ז׳, ט״ז Day of month as Hebrew numeral
    %*-d   א, טו   Day of month without gershayim
    %*B    אייר    Name of month in Hebrew
    %*y    תשפ״ב   Year in Hebrew numerals without the thousands place
    %*Y    ה'תשפ״ב Year in Hebrew numerals with the thousands place
    %%     %       A literal '%' character
    ====== ======= ===========================================================

    Example
    -------
    >>> date = HebrewDate(5783, 1, 15)
    >>> f'Today is {date:%a - %*-d %*B, %*y}'
    'Today is Thu - טו אייר, תשפ"ג'

    Parameters
    ----------
    year : int
        The Hebrew year.

    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7). If
        there is a second Adar in the year it is has a value of 13.

    day : int
        The Hebrew day of the month.

    jd : float, optional
        This parameter should not be assigned manually.

    Attributes
    ----------
    year : int
    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7).
        If there is a second Adar it has a value of 13.
    day : int
        The day of the month.

    Raises
    ------
    ValueError
        If the year is less than 1, if the month is less than 1 or greater
        than the last month, or if the day does not exist in the month a
        ``ValueError`` will be raised.
    """

    def __init__(self, year, month, day, jd=None):

        """Initialize a HebrewDate instance.

        This initializer extends the CalendarDateMixin adding validation
        specific to hebrew dates.
        """
        if year < 1:
            raise ValueError('Year must be >= 1.')
        if month < 1 or month > 13:
            raise ValueError(f'{month} is an invalid month.')
        if (not utils._is_leap(year)) and month == 13:
            raise ValueError(f'{year} is not a leap year')
        monthlength = utils._month_length(year, month)
        if day < 1 or day > monthlength:
            raise ValueError(f'Given month has {monthlength} days.')
        super().__init__(year, month, day, jd)

    def __format__(self, fmt):
        new = []
        i = 0
        while i < len(fmt):
            if fmt[i] != '%':
                new.append(fmt[i])
            else:
                i += 1
                try:
                    curr = fmt[i]
                except IndexError as e:
                    raise ValueError(
                        'Format string cannot end with single "%".'
                    ) from e
                if curr == '%':
                    new.append('%')
                elif curr == '*':
                    i += 1
                    try:
                        curr = fmt[i]
                    except IndexError as e:
                        raise ValueError(
                            'Format string cannot end with "%*".'
                        ) from e
                    if curr == '-':
                        i += 1
                        try:
                            curr = fmt[i]
                        except IndexError as e:
                            raise ValueError(
                                'Format string cannot end with "%*-"'
                            ) from e
                        if curr == 'd':
                            new.append(self.hebrew_day(False))
                        else:
                            raise ValueError('Invalid format string.')
                    elif curr == 'a':
                        new.append(gematria._num_to_str(self.weekday()))
                    elif curr == 'A':
                        new.append(utils.WEEKDAYS[self.weekday()])
                    elif curr == 'd':
                        new.append(self.hebrew_day())
                    elif curr == 'B':
                        new.append(self.month_name(True))
                    elif curr.casefold() == 'y':
                        new.append(self.hebrew_year(curr == 'Y'))
                    else:
                        raise ValueError('Invalid format string.')
                elif curr == '-':
                    i += 1
                    try:
                        curr = fmt[i]
                    except IndexError as e:
                        raise ValueError(
                            'Format string cannot end with "%-"'
                        ) from e
                    if curr == 'd':
                        new.append(str(self.day))
                    elif curr == 'm':
                        new.append(str(self.month))
                    else:
                        raise ValueError('Invalid format string.')
                else:
                    if curr.casefold() == 'a':
                        new.append(self.to_pydate().strftime(f'%{curr}'))
                    elif curr == 'w':
                        new.append(str(self.weekday()))
                    elif curr == 'd':
                        new.append(format(self.day, '02d'))
                    elif curr == 'B':
                        new.append(self.month_name(False))
                    elif curr == 'm':
                        new.append(format(self.month, '02d'))
                    elif curr.casefold() == 'y':
                        new.append(date(self.year, 1, 1).strftime(f'%{curr}'))
                    else:
                        raise ValueError('Invalid format string.')
            i += 1
        return ''.join(new)

    @property
    def jd(self):
        """Return the corresponding Julian day number.

        Returns
        -------
        float
            The Julian day number at midnight.

        """
        if self._jd is None:
            months = utils._monthslist(self.year)
            jd = utils._elapsed_days(self.year)
            for m in months:
                if m != self.month:
                    jd += utils._month_length(self.year, m)
                else:
                    self._jd = jd + (self.day-1) + 347996.5

        return self._jd

    @staticmethod
    def from_pydate(pydate):
        """Return a `HebrewDate` from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance

        Returns
        -------
        HebrewDate
        """
        return GregorianDate.from_pydate(pydate).to_heb()

    @staticmethod
    def today():
        """Return HebrewDate instance for the current day.

        This static method wraps the Python standard library's
        ``date.today()`` method to get the date from the timestamp.

        Returns
        -------
        HebrewDate
            The current Hebrew date from the computer's timestamp.

        Warning
        -------
        Pyluach treats Hebrew dates as if they change at midnight. If it's
        after nightfall but before midnight, to get the true Hebrew date do
        ``HebrewDate.today() + 1``.
        """
        return GregorianDate.today().to_heb()

    def to_jd(self):
        """Convert to a Julian day.

        Returns
        -------
        JulianDay
            The equivalent JulianDay instance.
        """
        return JulianDay(self.jd)

    def to_greg(self):
        """Convert to a Gregorian date.

        Returns
        -------
        GregorianDate
            The equivalent GregorianDate instance.
        """
        return self.to_jd().to_greg()

    def to_pydate(self):
        """Convert to a standard library date.

        Returns
        -------
        datetime.date
            The equivalent datetime.date instance.
        """
        return self.to_greg().to_pydate()

    def to_heb(self):
        return self

    def month_name(self, hebrew=False):
        """Return the name of the month.

        Parameters
        ----------
        hebrew : bool, optional
            ``True`` if the month name should be in Hebrew characters.
            Default is ``False`` which returns the month name
            transliterated into English.

        Returns
        -------
        str
        """
        return utils._month_name(self.year, self.month, hebrew)

    def hebrew_day(self, withgershayim=True):
        """Return the day of the month in Hebrew letters.

        Parameters
        ----------
        withgershayim : bool, optional
            Default is ``True`` which includes a geresh with a single
            character and gershayim between two characters.

        Returns
        -------
        str
            The day of the month in Hebrew letters.

        Examples
        --------
        >>> date = HebrewDate(5782, 3, 6)
        >>> date.hebrew_day()
        'ו׳'
        >>> date.hebrew_day(False)
        'ו'
        >>> HebrewDate(5783, 12, 14).hebrew_day()
        'י״ד'
        """
        return gematria._num_to_str(self.day, withgershayim=withgershayim)

    def hebrew_year(self, thousands=False, withgershayim=True):
        """Return the year in Hebrew letters.

        Parameters
        ----------
        thousands : bool
            ``True`` to prefix the year with a letter for the
            thousands place, ie. 'ה׳תשפ״א'. Default is ``False``.
        withgershayim : bool, optional
            Default is ``True`` which includes a geresh after the thousands
            place if applicable and a gershayim before the last character
            of the year.

        Returns
        -------
        str
        """
        return gematria._num_to_str(self.year, thousands, withgershayim)

    def hebrew_date_string(self, thousands=False):
        """Return a Hebrew string representation of the date.

        The date is in the form ``f'{day} {month} {year}'``.

        Parameters
        ----------
        thousands : bool
            ``True`` to have the thousands include in the year.
            Default is ``False``.

        Returns
        -------
        str

        Examples
        --------
        >>> date = HebrewDate(5781, 9, 25)
        >>> date.hebrew_date_string()
        'כ״ה כסלו תשפ״א'
        >>> date.hebrew_date_string(True)
        'כ״ה כסלו ה׳תשפ״א'
        """
        day = self.hebrew_day()
        month = self.month_name(True)
        year = self.hebrew_year(thousands)
        return f'{day} {month} {year}'

    def add(
        self,
        years=0,
        months=0,
        days=0,
        adar1=False,
        rounding=Rounding.NEXT_DAY
    ):
        """Add years, months, and days to date.

        Parameters
        ----------
        years : int, optional
            The number of years to add. Default is 0.
        months : int, optional
            The number of months to add. Default is 0.
        days : int, optional
            The number of days to add. Default is 0.
        adar1 : bool, optional
            True to return a date in Adar Aleph if `self` is in a regular
            Adar and after adding the years it's leap year. Default is
            ``False`` which will return the date in Adar Beis.
        rounding : Rounding, optional
            Choose what to do if self is the 30th day of the month, and
            there are only 29 days in the destination month.
            :obj:`Rounding.NEXT_DAY` to return the first day of the next
            month. :obj:`Rounding.PREVIOUS_DAY` to return the last day of
            the month. :obj:`Rounding.EXCEPTION` to raise a ValueError.
            Default is :obj:`Rounding.NEXT_DAY`.

        Returns
        -------
        HebrewDate

        Note
        ----
        This method first adds the `years`. If the starting month is
        Adar and the destination year has two Adars, it chooses which
        one based on the `adar1` argument, then it adds the `months`. If
        the starting day doesn't exist in that month it adjusts it based
        on the `rounding` argument, then it adds the `days`.

        Examples
        --------
        >>> date = HebrewDate(5783, 11, 30)
        >>> date.add(months=1)
        HebrewDate(5783, 1, 1)
        >>> date.add(months=1, rounding=Rounding.PREVIOUS_DAY)
        HebrewDate(5783, 12, 29)
        """
        year = self.year + years
        month = self.month
        if self.month == 13 and not utils._is_leap(year):
            month = 12
        elif (
            self.month == 12
            and not utils._is_leap(self.year)
            and utils._is_leap(year)
            and not adar1
        ):
            month = 13
        if months > 0:
            year, month = utils._add_months(year, month, months)
        elif months < 0:
            year, month = utils._subtract_months(year, month, -months)
        if utils._month_length(year, month) < self.day:
            date = HebrewDate(year, month, 29)
            if rounding is Rounding.EXCEPTION:
                raise ValueError(f'{date:%B %Y} has only 29 days.')
            if rounding is Rounding.NEXT_DAY:
                date += 1
            elif not isinstance(rounding, Rounding):
                raise TypeError(
                    'The rounding argument can only be a member of the'
                    ' dates.Rounding enum.'
                )
        else:
            date = HebrewDate(year, month, self.day)
        return date + days

    def subtract(
        self,
        years=0,
        months=0,
        days=0,
        adar1=False,
        rounding=Rounding.NEXT_DAY
    ):
        """Subtract years, months, and days from date.

        Parameters
        ----------
        years : int, optional
            The number of years to subtract. Default is 0.
        months : int, optional
            The number of months to subtract. Default is 0.
        days : int, optional
            The number of days to subtract. Default is 0.
        adar1 : bool, optional
            True to return a date in Adar Aleph if `self` is in a regular
            Adar and the destination year is leap year. Default is
            ``False`` which will return the date in Adar Beis.
        rounding : Rounding, optional
            Choose what to do if self is the 30th day of the month, and
            there are only 29 days in the destination month.
            :obj:`Rounding.NEXT_DAY` to return the first day of the next
            month. :obj:`Rounding.PREVIOUS_DAY` to return the last day of
            the month. :obj:`Rounding.EXCEPTION` to raise a ValueError.
            Default is :obj:`Rounding.NEXT_DAY`.

        Returns
        -------
        HebrewDate

        Note
        ----
        This method first subtracts the `years`. If the starting month
        is Adar and the destination year has two Adars, it chooses which
        one based on the `adar1` argument, then it subtracts the
        `months`. If the starting day doesn't exist in that month it
        adjusts it based on the `rounding` argument, then it subtracts
        the `days`.
        """
        return self.add(-years, -months, -days, adar1, rounding)
