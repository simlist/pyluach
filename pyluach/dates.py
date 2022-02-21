"""The dates module implements classes for representing and
manipulating several date types.

Contents
--------
* :class:`~pyluach.dates.BaseDate`
* :class:`~pyluach.dates.CalendarDateMixin`
* :class:`~pyluach.dates.JulianDay`
* :class:`~pyluach.dates.GregorianDate`
* :class:`~pyluach.dates.HebrewDate`

Note
----
All instances of the classes in this module should be treated as read
only. No attributes should be changed once they're created.
"""

import abc
from datetime import date
from numbers import Number

from pyluach import utils
from pyluach import gematria


class BaseDate(abc.ABC):
    """BaseDate is a base class for all date types.

    It provides the following arithmetic and comparison operators
    common to all child date types.

    ===================  =============================================
    Operation            Result
    ===================  =============================================
    d2 = date1 + int     New date ``int`` days after date1
    d2 = date1 - int     New date ``int`` days before date1
    int = date1 - date2  Integer equal to the absolute value of the
                         difference between date1 and date2
    date1 > date2        True if date1 occurs later than date2
    date1 < date2        True if date1 occurs earlier than date2
    date1 == date2       True if date1 occurs on the same day as date2
    date1 != date2       True if ``date1 == date2`` is False
    date1 >=, <= date2   True if both are True
    ===================  =============================================

    Any child of BaseDate that implements a `jd` attribute
    representing the Julian Day of that date can be compared to and
    diffed with any other valid date type.
    """

    _error_string = 'An error has occured.'

    @property
    @abc.abstractmethod
    def jd(self):
        """Return julian day number."""

    def __hash__(self):
        return hash(self.jd)

    def __add__(self, other):
        try:
            return JulianDay(self.jd + other)._to_x(self)
        except TypeError as e:
            raise TypeError('You can only add a number to a date.') from e

    def __sub__(self, other):
        try:
            if isinstance(other, Number):
                return JulianDay(self.jd - other)._to_x(self)
            return abs(self.jd - other.jd)
        except (AttributeError, TypeError) as e:
            raise TypeError(
                'You can only subtract a number or another date'
                'that has a "jd" attribute from a date'
            ) from e

    def __eq__(self, other):
        try:
            if self.jd == other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

    def __ne__(self, other):
        try:
            if self.jd != other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

    def __lt__(self, other):
        try:
            if self.jd < other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

    def __gt__(self, other):
        try:
            if self.jd > other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

    def __le__(self, other):
        try:
            if self.jd <= other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

    def __ge__(self, other):
        try:
            if self.jd >= other.jd:
                return True
            return False
        except AttributeError as e:
            raise TypeError(self._error_string) from e

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
        ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
            `self` if the date is Shabbos or else the following Shabbos as
            the same date type as operated on.

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

    def fast_day(self, hebrew=False):
        """Return name of fast day of date.

        Parameters
        ----------
        hebrew : bool, optional
            ``True`` if you want the fast day name in Hebrew letters. Default
            is ``False``, which returns the name transliterated into English.

        Returns
        -------
        str or ``None``
            The name of the fast day or ``None`` if the date is not
            a fast day.
        """
        return utils._fast_day_string(self, hebrew)

    def festival(self, israel=False, hebrew=False, include_working_days=True):
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

        Returns
        -------
        str or ``None``
            The name of the festival or ``None`` if the given date is not
            a Jewish festival.
        """
        return utils._festival_string(
            self, israel, hebrew, include_working_days
        )

    def holiday(self, israel=False, hebrew=False):
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

        Returns
        -------
        str or ``None``
            The name of the holiday or ``None`` if the given date is not
            a Jewish holiday.
        """
        return utils._holiday(self, israel, hebrew)


class CalendarDateMixin(abc.ABC):
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
        The equivelant Julian day at midnight.
    """

    def __init__(self, year, month, day, jd=None):
        """Initialize a calendar date."""
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
        Dict
            A dictionary in the form
            ``{'year': int, 'month': int, 'day': int}``.
        """
        return {'year': self.year, 'month': self.month, 'day': self.day}


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
    jd : float
        Alias for day.
    """

    def __init__(self, day):
        """Initialize a JulianDay instance."""
        if day-int(day) < .5:
            self.day = int(day) - .5
        else:
            self.day = int(day) + .5
        self._error_string = """Only a date with a "jd" attribute can
            be compared to a Julian Day instance."""

    def __repr__(self):
        return f'JulianDay({self.day})'

    def __str__(self):
        return str(self.day)

    def weekday(self):
        """Return weekday of date.

        Returns
        -------
        int
            The weekday with Sunday as 1 through Saturday as 7.
        """
        return (int(self.day+.5) + 1) % 7 + 1

    @property
    def jd(self):
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

        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not utils._is_leap(year):
            months.remove(13)

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
        raise NotImplementedError(
            'This method has not been implemented with that date type.'
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
    jd : float(property)
      The corresponding Julian Day Number at midnight (as *n*.5).

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

    @property
    def jd(self):
        """Return the corresponding Julian day number.

        This property retrieves the corresponding Julian Day as a float
        if it was passed into the init method or already calculated, and
        if it wasn't, it calculates it and saves it for later retrievals
        and returns it.

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

    Parameters
    ----------
    year : int
        The Hebrew year. If the year is less than 1 it will raise a
        ValueError.

    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7).
        If there is a second Adar in the year it is represented as 13.
        A month below 1 or above the last month will raise a ValueError.

    day : int
        The Hebrew day of the month. An invalid day will raise a
        ValueError.

    jd : float, optional
        This parameter should not be assigned manually.

    Attributes
    ----------
    year : int
    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7).
        If there is a second Adar it is represented as 13.
    day : int
        The day of the month.
    """

    def __init__(self, year, month, day, jd=None):

        """Initialize a HebrewDate instance.

        This initializer extends the CalendarDateMixin adding validation
        specific to hebrew dates.
        """
        if year < 1:
            raise ValueError('Date supplied is before creation.')
        if month < 1 or month > 13:
            raise ValueError(f'{month} is an invalid month.')
        if (not utils._is_leap(year)) and month == 13:
            raise ValueError(f'{year} is not a leap year')
        monthlength = utils._month_length(year, month)
        if day < 1 or day > monthlength:
            raise ValueError(f'Given month has {monthlength} days.')
        super().__init__(year, month, day, jd)

    @property
    def jd(self):
        """Return the corresponding Julian day number.

        This property retrieves the corresponding Julian Day as a float
        if it was passed into the init method or already calculated, and
        if it wasn't, it calculates it, saves it for later retrievals,
        and returns it.

        Returns
        -------
        float
            The Julian day number at midnight.

        """
        if self._jd is None:
            months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
            if not utils._is_leap(self.year):
                months.remove(13)

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

        Notes
        -----
        This method coverts the Gregorian date from the time stamp to
        a Hebrew date, so if it is after nightfall but before
        midnight you will have to add one day, ie.
        ``today = HebrewDate.today() + 1``.
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
        """
        Return the name of the month.

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

    def hebrew_day(self):
        """Return the day of the month in Hebrew letters.

        Returns
        -------
        str
            The day of the month in Hebrew letters. For
            example 'א׳' for 1, 'ט״ו' for 15.
        """
        return gematria._num_to_str(self.day)

    def hebrew_year(self, thousands=False):
        """Return the year in Hebrew letters.

        Parameters
        ----------
        thousands : bool
            ``True`` to prefix the year with a letter for the
            thousands place, ie. 'ה׳תשפ״א'. Default is ``False``.

        Returns
        -------
        str
        """
        return gematria._num_to_str(self.year, thousands)

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
