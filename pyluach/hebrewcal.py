"""The hebrewcal module contains Hebrew calendar related classes and functions.

It contains classes for representing a Hebrew year and month, functions
for getting the holiday or fast day for a given date, and classes adapting
:py:mod:`calendar` classes to render Hebrew calendars.
"""
from numbers import Number
from itertools import repeat
import calendar

from pyluach.dates import HebrewDate
from pyluach import utils
from pyluach.gematria import _num_to_str
from pyluach.utils import _holiday, _fast_day_string, _festival_string


class IllegalMonthError(ValueError):
    """An exception for an illegal month.

    Subclasses ``ValueError`` to show a message for an invalid month number
    for the Hebrew calendar. Mimics :py:class:`calendar.IllegalMonthError`.

    Parameters
    ----------
    month : int
        The invalid month number
    """
    def __init__(self, month):
        self.month = month

    def __str__(self):
        return (
            f'bad month number {self.month}; must be 1-12 or 13 in a leap year'
        )


class IllegalWeekdayError(ValueError):
    """An exception for an illegal weekday.

    Subclasses ``ValueError`` to show a message for an invalid weekday
    number. Mimics :py:class:`calendar.IllegalWeekdayError`.

    Parameters
    ----------
    month : int
        The invalid month number
    """
    def __init__(self, weekday):
        self.weekday = weekday

    def __str__(self):
        return (
            f'bad weekday number {self.weekday}; '
            f'must be 1 (Sunday) to 7 (Saturday)'
        )


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
        if isinstance(other, Year):
            return self.year == other.year
        return NotImplemented

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
        if isinstance(other, Year):
            return self.year > other.year
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Year):
            return self > other or self == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Year):
            return self.year < other.year
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Year):
            return self < other or self == other
        return NotImplemented

    def __iter__(self):
        """Yield integer for each month in year."""
        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not self.leap:
            months.remove(13)
        for month in months:
            yield month

    def monthscount(self):
        """Return number of months in the year.

        Returns
        -------
        int
        """
        if self.leap:
            return 13
        return 12

    def itermonths(self):
        """Yield Month instance for each month of the year.

        Yields
        ------
        Month
            The next month in the Hebrew calendar year as a
            ``Month`` instance beginning with Tishrei through Elul.
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
        pyluach.dates.HebrewDate
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
        date : ~pyluach.dates.BaseDate
            Any subclass of ``BaseDate``.

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
        pydate : datetime.date
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
            Default is ``False``.

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
    """

    def __init__(self, year, month):
        if year < 1:
            raise ValueError('Year is before creation.')
        self.year = year
        if month < 1 or month > 12 + utils._is_leap(self.year):
            raise IllegalMonthError(month)
        self.month = month

    def __repr__(self):
        return f'Month({self.year}, {self.month})'

    def __len__(self):
        return utils._month_length(self.year, self.month)

    def __iter__(self):
        for day in range(1, len(self) + 1):
            yield day

    def __eq__(self, other):
        if isinstance(other, Month):
            return (self.year == other.year and self.month == other.month)
        return NotImplemented

    def __add__(self, other):
        yearmonths = list(Year(self.year))
        index = yearmonths.index(self.month)
        leftover_months = len(yearmonths[index + 1:])
        try:
            if other <= leftover_months:
                return Month(self.year, yearmonths[index + other])
            return Month(self.year + 1, 7).__add__(other - (leftover_months+1))
        except (AttributeError, TypeError):
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Number):
            yearmonths = list(Year(self.year))
            index = yearmonths.index(self.month)
            if other <= index:
                return Month(self.year, yearmonths[index - other])
            return Month(self.year - 1, 6).__sub__(other - (index+1))
            # Recursive call on the last month of the previous year.
        try:
            return abs(self._elapsed_months() - other._elapsed_months())
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Month):
            return (
                self.year > other.year
                or (
                    self.year == other.year
                    and self._month_number() > other._month_number()
                )
            )
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Month):
            return self > other or self == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Month):
            return (
                self.year < other.year
                or (
                    self.year == other.year
                    and self._month_number() < other._month_number()
                )
            )
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Month):
            return self < other or self == other
        return NotImplemented

    @classmethod
    def from_date(cls, date):
        """Return Month object that given date occurs in.

        Parameters
        ----------
        date : ~pyluach.dates.BaseDate
            Any subclass of ``BaseDate``.
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
        pydate : datetime.date
            A python standard library date object

        Returns
        -------
        Month
            The Hebrew month the given date occurs in
        """
        return cls.from_date(HebrewDate.from_pydate(pydate))

    def _month_number(self):
        """Return month number 1-12 or 13, Tishrei - Elul."""
        return list(Year(self.year)).index(self.month) + 1

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
        pyluach.dates.HebrewDate
            The next Hebrew date of the month.
        """
        for day in self:
            yield HebrewDate(self.year, self.month, day)

    def molad(self):
        """Return the month's molad.

        Returns
        -------
        dict
            A dictionary in the form
            ``{weekday: int, hours: int, parts: int}``

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


def _to_pyweekday(weekday):
    if weekday == 1:
        return 6
    return weekday - 2


def _year_and_month(month):
    return month.year, month.month


def to_hebrew_numeral(num, thousands=False, withgershayim=True):
    """Convert int to Hebrew numeral.

    Function useful in formatting Hebrew calendars.

    Parameters
    ----------
    num : int
        The number to convert
    thousands : bool, optional
        True if the hebrew returned should include a letter for the
        thousands place ie. 'ה׳' for five thousand. Default is  ``False``.
    withgershayim : bool, optional
        ``True`` to include a geresh after a single letter and double
        geresh before the last letter if there is more than one letter.
        Default is ``True``.

    Returns
    -------
    str
        The Hebrew numeral representation of the number.
    """
    return _num_to_str(num, thousands, withgershayim)


class HebrewCalendar(calendar.Calendar):
    """Calendar base class.

    This class extends the python library
    :py:class:`Calendar <calendar.Calendar>` class for the Hebrew calendar. The
    weekdays are 1 for Sunday through 7 for Shabbos.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the day of the month with Hebrew
        numerals. ``False`` shows the day of the month as a number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a number.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool

    Note
    ----
    All of the parameters other than `firstweekday` are not used in the
    ``HebrewCalendar`` base class. They're there for use in child
    classes.
    """

    def __init__(
        self, firstweekday=1, hebrewnumerals=True, hebrewweekdays=False,
        hebrewmonths=False, hebrewyear=False
    ):
        if not (1 <= firstweekday <= 7):
            raise IllegalWeekdayError(firstweekday)
        self._firstweekday = firstweekday
        self._firstpyweekday = _to_pyweekday(firstweekday)
        self.hebrewnumerals = hebrewnumerals
        self.hebrewweekdays = hebrewweekdays
        self.hebrewmonths = hebrewmonths
        self.hebrewyear = hebrewyear

    @property
    def firstweekday(self):
        """Get and set the weekday the weeks should start with.

        Returns
        -------
        int
        """
        return self._firstweekday

    @firstweekday.setter
    def firstweekday(self, thefirstweekday):
        self._firstweekday = thefirstweekday
        self._firstpyweekday = _to_pyweekday(thefirstweekday)

    def iterweekdays(self):
        """Return one week of weekday numbers.

        The numbers start with the configured first one.

        Yields
        ------
        int
            The next weekday with 1-7 for Sunday - Shabbos.
            The iterator starts with the ``HebrewCalendar`` object's
            configured first weekday ie. if configured to start with
            Monday it will first yield `2` and end with `1`.
        """
        for i in range(self.firstweekday, self.firstweekday + 7):
            yield i % 7 or 7

    def itermonthdates(self, year, month):
        """Yield dates for one month.

        The iterator will always iterate through complete weeks, so it
        will yield dates outside the specified month.

        Parameters
        ----------
        year : int
        month : int
          The Hebrew month starting with 1 for Nissan through 13 for
          Adar Sheni if necessary.

        Yields
        ------
        pyluach.dates.HebrewDate
            The next Hebrew Date of the month starting with the first
            date of the week the first of the month falls in, and ending
            with the last date of the week that the last day of the month
            falls in.
        """
        for y, m, d in self.itermonthdays3(year, month):
            yield HebrewDate(y, m, d)

    def itermonthdays(self, year, month):
        """Like ``itermonthdates()`` but will yield day numbers.
        For days outside the specified month the day number is 0.

        Parameters
        ----------
        year : int
        month : int

        Yields
        ------
        int
            The day of the month or 0 if the date is before or after the
            month.
        """
        currmonth = Month(year, month)
        day1 = _to_pyweekday(currmonth.starting_weekday())
        ndays = len(currmonth)
        days_before = (day1 - self._firstpyweekday) % 7
        yield from repeat(0, days_before)
        yield from range(1, ndays + 1)
        days_after = (self._firstpyweekday - day1 - ndays) % 7
        yield from repeat(0, days_after)

    def itermonthdays2(self, year, month):
        """Return iterator for the days and weekdays of the month.

        Parameters
        ----------
        year : int
        month : int

        Yields
        ------
        tuple of ints
            A tuple of ints in the form ``(day of month, weekday)``.
        """
        for i, d in enumerate(
            self.itermonthdays(year, month), self.firstweekday
        ):
            yield d, i % 7 or 7

    def itermonthdays3(self, year, month):
        """Return iterator for the year, month, and day of the month.

        Parameters
        ----------
        year : int
        month : int

        Yields
        ------
        tuple of ints
            A tuple of ints in the form ``(year, month, day)``.
        """
        currmonth = Month(year, month)
        day1 = _to_pyweekday(currmonth.starting_weekday())
        ndays = len(currmonth)
        days_before = (day1 - self._firstpyweekday) % 7
        days_after = (self._firstpyweekday - day1 - ndays) % 7
        try:
            prevmonth = currmonth - 1
        except ValueError:
            prevmonth = currmonth
        y, m = _year_and_month(prevmonth)
        end = len(prevmonth) + 1
        for d in range(end - days_before, end):
            yield y, m, d
        for d in range(1, ndays + 1):
            yield year, month, d
        y, m = _year_and_month(currmonth + 1)
        for d in range(1, days_after + 1):
            yield y, m, d

    def itermonthdays4(self, year, month):
        """Return iterator for the year, month, day, and weekday

        Parameters
        ----------
        year : int
        month : int

        Yields
        ------
        tuple of ints
            A tuple of ints in the form ``(year, month, day, weekday)``.
        """
        for i, (y, m, d) in enumerate(self.itermonthdays3(year, month)):
            yield y, m, d, (self.firstweekday + i) % 7 or 7

    def yeardatescalendar(self, year, width=3):
        """Return data of specified year ready for formatting.

        Parameters
        ----------
        year : int
        width : int, optional
            The number of months per row. Default is 3.

        Returns
        ------
        list of lists of lists of lists of ``HebrewDates``
            Returns a list of month rows. Each month row contains a list
            of up to `width` months. Each month contains either 5 or 6
            weeks, and each week contains 7 days. Days are ``HebrewDate``
            objects.
        """
        months = [
            self.monthdatescalendar(year, m)
            for m in Year(year)
        ]
        return [months[i:i+width] for i in range(0, len(months), width)]

    def yeardays2calendar(self, year, width=3):
        """Return the data of the specified year ready for formatting.

        This method is similar to the ``yeardatescalendar`` except the
        entries in the week lists are ``(day number, weekday number)``
        tuples.

        Parameters
        ----------
        year : int
        width : int, optional
            The number of months per row. Default is 3.

        Returns
        -------
        list of lists of lists of lists of tuples
            Returns a list of month rows. Each month row contains a list
            of up to `width` months. Each month contains between 4 and 6
            weeks, and each week contains 1-7 days. Days are tuples with
            the form ``(day number, weekday number)``.
        """
        months = [
            self.monthdays2calendar(year, m)
            for m in Year(year)
        ]
        return [months[i:i+width] for i in range(0, len(months), width)]

    def yeardayscalendar(self, year, width=3):
        """Return the data of the specified year ready for formatting.

        This method is similar to the ``yeardatescalendar`` except the
        entries in the week lists are day numbers.

        Parameters
        ----------
        year : int
        width : int, optional
            The number of months per row. Default is 3.

        Returns
        -------
        list of lists of lists of lists of ints
            Returns a list of month rows. Each month row contains a list
            of up to `width` months. Each month contains either 5 or 6
            weeks, and each week contains 1-7 days. Each day is the day of
            the month as an int.
        """
        months = [
            self.monthdayscalendar(year, m)
            for m in Year(year)
        ]
        return [months[i:i+width] for i in range(0, len(months), width)]

    def monthdatescalendar(self, year, month):
        """Return matrix (list of lists) of dates for month's calendar.

        Each row represents a week; week entries are HebrewDate instances.

        Parameters
        ----------
        year : int
        month : int

        Returns
        -------
        list of lists of HebrewDate
            List of weeks in the month containing 7 ``HebrewDate``
            instances each.
        """
        return super().monthdatescalendar(year, month)


class HebrewTextCalendar(HebrewCalendar, calendar.TextCalendar):
    """Subclass of HebrewCalendar that outputs a plaintext calendar.

    ``HebrewTextCalendar`` adapts :py:class:`calendar.TextCalendar` for the
    Hebrew calendar.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the day of the month with Hebrew
        numerals. ``False`` shows the day of the month as a number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a number.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool

    Note
    ----
    This class generates plain text calendars. Any program that adds
    any formatting may distort the calendars when using any Hebrew
    characters.
    """

    def formatday(self, day, weekday, width):
        """Return a formatted day.

        Extends calendar.TextCalendar formatday method.

        Parameters
        ----------
        day : int
            The day of the month.
        weekday : int
            The weekday 1-7 Sunday-Shabbos.
        width : int
            The width of the day column.

        Returns
        -------
        str
        """
        if self.hebrewnumerals:
            if day == 0:
                s = ''
            else:
                s = f'{to_hebrew_numeral(day, withgershayim=False):>2}'
            return s.center(width)
        return super().formatday(day, weekday, width)

    def formatweekday(self, day, width):
        """Return formatted weekday.

        Extends calendar.TextCalendar formatweekday method.

        Parameters
        ----------
        day : int
            The weekday 1-7 Sunday-Shabbos.
        width : int
            The width of the day column.

        Returns
        -------
        str
        """
        if self.hebrewweekdays:
            if width < 5:
                name = to_hebrew_numeral(day)
            else:
                name = utils.WEEKDAYS[day]
            return name[:width].center(width)
        return super().formatweekday(_to_pyweekday(day), width)

    def formatmonthname(
        self, theyear, themonth, width=0, withyear=True
    ):
        """Return formatted month name.

        Parameters
        ----------
        theyear : int
        themonth : int
            1-12 or 13 for Nissan-Adar Sheni
        width : int, optional
            The number of columns per day. Default is 0
        withyear : bool, optional
            Default is ``True`` to include the year with the month name.

        Returns
        -------
        str
        """
        s = Month(theyear, themonth).month_name(self.hebrewmonths)
        if withyear:
            if self.hebrewyear:
                year = to_hebrew_numeral(theyear)
            else:
                year = theyear
            s = f'{s} {year}'
        return s.center(width)

    def formatyear(self, theyear, w=2, l=1, c=6, m=3):
        """Return a year's calendar as a multi-line string.

        Parameters
        ----------
        theyear : int
        w : int, optional
            The date column width. Default is 2
        l : int, optional
            The number of lines per week. Default is 1.
        c : int, optional
            The number of columns in between each month. Default is 6
        m : int, optional
            The number of months per row. Default is 3.

        Returns
        -------
        str
        """
        w = max(2, w)
        l = max(1, l)
        c = max(2, c)
        colwidth = (w + 1) * 7 - 1
        v = []
        a = v.append
        a(repr(theyear).center(colwidth*m+c*(m-1)).rstrip())
        a('\n'*l)
        header = self.formatweekheader(w)
        yearmonths = list(Year(theyear))
        for (i, row) in enumerate(self.yeardays2calendar(theyear, m)):
            # months in this row
            months = range(m*i+1, min(m*(i+1)+1, len(yearmonths)+1))
            a('\n'*l)
            names = (
                self.formatmonthname(theyear, yearmonths[k-1], colwidth, False)
                for k in months
            )
            a(calendar.formatstring(names, colwidth, c).rstrip())
            a('\n'*l)
            headers = (header for k in months)
            a(calendar.formatstring(headers, colwidth, c).rstrip())
            a('\n'*l)
            # max number of weeks for this row
            height = max(len(cal) for cal in row)
            for j in range(height):
                weeks = []
                for cal in row:
                    if j >= len(cal):
                        weeks.append('')
                    else:
                        weeks.append(self.formatweek(cal[j], w))
                a(calendar.formatstring(weeks, colwidth, c).rstrip())
                a('\n' * l)
        return ''.join(v)


class HebrewHTMLCalendar(HebrewCalendar, calendar.HTMLCalendar):
    """Class to generate html calendars .

    Adapts :py:class:`calendar.HTMLCalendar` for the Hebrew calendar.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the day of the month with Hebrew
        numerals. ``False`` shows the day of the month as a number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a number.
    rtl : bool, optional
        ``True``  to arrange the months and the days of the month from
        right to left. Default is ``False``.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool
    rtl : bool
    """

    def __init__(
        self, firstweekday=1, hebrewnumerals=True, hebrewweekdays=False,
        hebrewmonths=False, hebrewyear=False, rtl=False
    ):
        self.rtl = rtl
        super().__init__(
            firstweekday,
            hebrewnumerals,
            hebrewweekdays,
            hebrewmonths,
            hebrewyear
        )

    def _rtl_str(self):
        if self.rtl:
            return ' dir="rtl"'
        return ''

    def formatday(self, day, weekday):
        """Return a day as an html table cell.

        Parameters
        ----------
        day : int
            The day of the month or zero for a day outside the month.
        weekday : int
            The weekday with 1 as Sunday through 7 as Shabbos.

        Returns
        -------
        str
        """
        pyweekday = _to_pyweekday(weekday)
        if day == 0:
            return f'<td class="{self.cssclass_noday}">&nbsp;</td>'
        if self.hebrewnumerals:
            day = to_hebrew_numeral(day, withgershayim=False)
        return f'<td class="{self.cssclasses[pyweekday]}">{day}</td>'

    def formatweekday(self, day):
        """Return a weekday name as an html table header.

        Parameters
        ----------
        day : int
            The day of the week 1-7 with Sunday as 1 and Shabbos as 7.

        Returns
        -------
        str
        """
        pyday = _to_pyweekday(day)
        if self.hebrewweekdays:
            dayname = utils.WEEKDAYS[day][:3]
        else:
            dayname = calendar.day_abbr[pyday]
        return (
            f'<th class="{self.cssclasses_weekday_head[pyday]}">{dayname}</th>'
        )

    def formatyearnumber(self, theyear):
        """Return a formatted year.

        Parameters
        ----------
        theyear : int

        Returns
        -------
        int or str
            If ``self.hebrewyear`` is ``True`` return the year as a Hebrew
            numeral str, else return `theyear` as is.
        """
        if self.hebrewyear:
            return to_hebrew_numeral(theyear)
        return theyear

    def formatmonthname(self, theyear, themonth, withyear=True):
        """Return month name as an html table row.

        Parameters
        ----------
        theyear : int
        themonth : int
            The month as an int 1-12 Nissan - Adar and 13 if leap year.
        withyear : bool, optional
            ``True`` to append the year to the month name. Default is
            ``True``.

        Return
        ------
        str
        """
        s = Month(theyear, themonth).month_name(self.hebrewmonths)
        if withyear:
            s = f'{s} {self.formatyearnumber(theyear)}'
        return (
            f'<tr><th colspan="7" class="{self.cssclass_month_head}">'
            f'{s}</th></tr>'
        )

    def formatmonth(self, theyear, themonth, withyear=True):
        """Return a formatted month as an html table.

        Parameters
        ----------
        theyear : int
        themonth : int
        withyear : bool, optional
            ``True`` to have the year appended to the month name. Default
            is ``True``.

        Returns
        -------
        str
        """
        v = []
        a = v.append
        a(
            '<table border="0" cellpadding="0" cellspacing="0"'
            f'class="{self.cssclass_month}"{self._rtl_str()}>'
        )
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, theyear, width=3):
        """Return a formatted year as an html table.

        Parameters
        ----------
        theyear : int
        width : int, optional
            The number of months to display per row. Default is 3.

        Returns
        -------
        str
        """
        year = Year(theyear)
        monthscount = year.monthscount()
        yearmonths = list(year)
        v = []
        a = v.append
        width = max(width, 1)
        a(
            '<table border="0" cellpadding="0" cellspacing="0"'
            f'class="{self.cssclass_year}"{self._rtl_str()}>'
        )
        a('\n')
        a(
            f'<tr><th colspan="{width}" class="{self.cssclass_year_head}">'
            f'{self.formatyearnumber(theyear)}</th></tr>'
        )
        for i in range(1, monthscount + 1, width):
            # months in this row
            months = range(i, min(i+width, monthscount + 1))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(
                    theyear, yearmonths[m-1], withyear=False
                ))
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)


def fast_day(date, hebrew=False):
    """Return name of fast day or None.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
      Any date instance from a subclass of ``BaseDate`` can be used.

    hebrew : bool, optional
      ``True`` if you want the fast_day name in Hebrew letters. Default
      is ``False``, which returns the name transliterated into English.

    Returns
    -------
    str or None
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
    date : ~pyluach.dates.BaseDate
      Any subclass of ``BaseDate`` can be used.

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
    str or None
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
    date : ~pyluach.dates.BaseDate
        Any subclass of ``BaseDate`` can be used.
    israel : bool, optional
        ``True`` if you want the holidays according to the israel
        schedule. Default is ``False``.
    hebrew : bool, optional
        ``True`` if you want the holiday name in Hebrew letters. Default
        is ``False``, which returns the name transliterated into English.

    Returns
    -------
    str or None
      The name of the holiday or ``None`` if the given date is not
      a Jewish holiday.
    """
    return _holiday(date, israel, hebrew)
