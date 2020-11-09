from collections import deque
from numbers import Number
from functools import lru_cache

from pyluach.dates import HebrewDate
from pyluach.utils import _holiday, _fast_day_string, _festival_string


MONTH_NAMES = [
    'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul', 'Tishrei', 'Cheshvan',
    'Kislev', 'Teves', 'Shevat', 'Adar', 'Adar 1', 'Adar 2'
]

MONTH_NAMES_HEBREW = [
    'ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול', 'תשרי', 'חשון', 'כסלו',
    'טבת', 'שבט', 'אדר', 'אדר א׳', 'אדר ב׳'
]


def fast_day(date, hebrew=False):
    """Return name of fast day or None.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    Returns
    -------
    str or ``None``
      The name of the fast day or ``None`` if the given date is not
      a fast day.
    """
    return _fast_day_string(date, hebrew)


def festival(date, israel=False, hebrew=False):
    """Return Jewish festival of given day.

    This method will return all major and minor religous
    Jewish holidays not including fast days.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    israel : bool, optional
      ``True`` if you want the holidays according to the Israel
      schedule. Defaults to ``False``.

    Returns
    -------
    str or ``None``
      The name of the festival or ``None`` if the given date is not
      a Jewish festival.
    """
    return _festival_string(date, israel, hebrew)


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
            raise ValueError('Year {0} is before creation.'.format(year))
        self.year = year
        self.leap = HebrewDate._is_leap(year)

    def __repr__(self):
        return 'Year({0})'.format(self.year)

    def __len__(self):
        return HebrewDate._days_in_year(self.year)

    def __eq__(self, other):
        if isinstance(other, Year) and self.year == other.year:
            return True
        return False

    def __add__(self, other):
        """Add int to year."""
        try:
            return Year(self.year + other)
        except TypeError:
            raise TypeError('You can only add a number to a year.')

    def __sub__(self, other):
        """Subtract int or Year from Year.

        If other is an int return a new Year other before original year. If
        other is a Year object, return delta of the two years as an int.
        """
        if isinstance(other, Year):
            return abs(self.year - other.year)
        else:
            try:
                return Year(self.year - other)
            except TypeError:
                raise TypeError('Only an int or another Year object can'
                                ' be subtracted from a year.')

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
        Month
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
    

class Month:
    """A Month object represents a month of the Hebrew calendar.

    It provides the same operators as a `Year` object.

    .. deprecated:: 1.3.0
      `name` attribute will be replaced by `month_name` method, because
      the latter allows a `hebrew` parameter. The month_name also uses
      slightly different transliteration.

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
    """

    _monthnames = {7: 'Tishrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Teves',
                  11: 'Shvat', 13:'Adar Sheni', 1: 'Nissan', 2: 'Iyar',
                  3: 'Sivan', 4: 'Tamuz', 5: 'Av', 6: 'Elul'}

    def __init__(self, year, month):
        if year < 1:
            raise ValueError('Year is before creation.')
        self.year = year
        leap = HebrewDate._is_leap(self.year)
        yearlength = 13 if leap else 12
        if month < 1 or month > yearlength:
            raise ValueError('''Month must be between 1 and 12 for a normal
            year and 13 for a leap year.''')
        self.month = month
        self._monthnames[12] = 'Adar Rishon' if leap else 'Adar'
        self.name = self._monthnames[self.month]

    def __repr__(self):
        return 'Month({0}, {1})'.format(self.year, self.month)

    def __len__(self):
        return HebrewDate._month_length(self.year, self.month)

    def __iter__(self):
        for day in range(1, len(self) + 1):
            yield day

    def __eq__(self, other):
        if(
           isinstance(other, Month) and
           self.year == other.year and
           self.month == other.month):
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
            raise TypeError('You can only add a number to a year.')


    def __sub__(self, other):
        if isinstance(other, Number):
            yearmonths = list(Year(self.year))
            index = yearmonths.index(self.month)
            leftover_months = index
            if other <= leftover_months:
                return Month(self.year, yearmonths[index - other])
            return Month(self.year - 1,
                         deque(Year(self.year - 1), maxlen=1).pop()).__sub__(
                                                    other - 1 - leftover_months
                                                    )
                    # Recursive call on the last month of the previous year. 
        try:
            return abs(self._elapsed_months() - other._elapsed_months())
        except AttributeError:
            raise TypeError('''You can only subtract a number or a month
                            object from a month.''')

    def __gt__(self, other):
        if (
            self.year > other.year
            or (self.year == other.year and self.month > other.month)
        ):
            return True
        return False

    def __ge__(self, other):
        if self > other or self == other:
            return True
        return False

    def __lt__(self, other):
        if (
            self.year < other.year
            or (self.year == other.year and self.month < other.month)
        ):
            return True
        return False

    def __le__(self, other):
        if self < other or self == other:
            return True
        return False

    def month_name(self, hebrew=False):
        """Return the name of the month.

        Replaces `name` attribute.

        Parameters
        ----------
        hebrew : bool, optional
          `True` if the month name should be written with Hebrew letters
          and False to be transliterated into English using the Ashkenazic
          pronunciation. Default is `False`.
        """
        index = self.month
        if self.month < 12 or not HebrewDate._is_leap(self.year):
            index -=1
        if hebrew:
            return MONTH_NAMES_HEBREW[index]
        return MONTH_NAMES[index]

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
        '''Return number of months elapsed from beginning of calendar'''
        yearmonths = tuple(Year(self.year))
        months_elapsed = (
            HebrewDate._elapsed_months(self.year)
            + yearmonths.index(self.month)
        )
        return months_elapsed

    def iterdates(self):
        """Return iterator that yields an instance of HebrewDate.

        Yields
        ------
        ``HebrewDate``
          The next Hebrew Date of the year starting the first day of
          Tishrei through the last day of Ellul.
        """
        for day in self:
            yield HebrewDate(self.year, self.month, day)

    def molad(self):
        """Return the month's molad.

        Returns
        -------
        dict
          A dictionary in the form {weekday: int, hours: int, parts: int}

        Notes
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
          A dictionary in the form
          ::
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