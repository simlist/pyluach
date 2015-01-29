"""The dates module implements classes for representing and
manipulating several date types.

Classes
-------
* BaseDate
* CalendarDateMixin
* JulianDay
* GregorianDate
* HebrewDate

Note
----
All instances of the classes in this module should be treated as read
only. No attributes should be changed once they're created.
"""

from __future__ import division

from datetime import date
from numbers import Number

from utils import memoize



class BaseDate(object):
    
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
    
    Any child of BaseDate that implements a ``jd`` attribute
    representing the Julian Day of that date can be compared to and
    diffed with any other valid date type.
    """ 
    
    def __hash__(self):
        return hash(self.jd)
        
    def __add__(self, other):
        try:
            return JulianDay(self.jd + other)._to_x(self)
        except AttributeError:
            raise TypeError('You can only add a number to a date.')
    
    def __sub__(self, other):
        if isinstance(other, Number):
            return JulianDay(self.jd - other)._to_x(self)
        try:
            return abs(self.jd - other.jd)
        except AttributeError:
            raise TypeError("""You can only subtract a number or another date
                              that has a "jd" attribute from a date""")
        
    def __eq__(self, other):
        try:
            if self.jd == other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)
    
    def __ne__(self, other):
        try:
            if self.jd != other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)
    
    def __lt__(self, other):
        try:
            if self.jd < other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)
    
    def __gt__(self, other):
        try:
            if self.jd > other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)

    
    def __le__(self, other):
        try:
            if self.jd <= other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)
    
    def __ge__(self, other):
        try:
            if self.jd >= other.jd:
                return True
            return False
        except AttributeError:
            raise TypeError(self.error_string)
        
    def shabbos(self):
        """Return the Shabbos on or following the date.
        
        Returns
        -------
        Date
          Self if it's Shabbos or else the following Shabbos as
          the same date type as operated on.
        """
        return self + (7 - self.weekday()) 
    

class CalendarDateMixin(object):
    """CalendarDateMixin is a mixin for Hebrew and Gregorian dates.

    Parameters
    ----------
    Year : int
    Month : int
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
        self. error_string = ('''Only a date with a "jd" attribute can
                              be compared to a {0}'''.format(
                                                self.__class__.__name__)
                              )
        
    def __repr__(self):
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__,
                                           self.year,
                                           self.month,
                                           self.day)
    
    def __str__(self):
        return '{0}-{1}-{2}'.format(self.year, self.month, self.day)
    
    def weekday(self):
        """Return day of week as an integer.
        
        Returns
        -------
        int
          An integer representing the day of the week with Sunday as 1
          through Saturday as 7.
        """
        return int(self.jd+.5+1) % 7 + 1
    
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
        self.jd = self.day
        
    def __repr__(self):
        return 'JulianDay({0})'.format(self.day)
        
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

        Note
        ----
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
        year = int(jd//365) + 2  ## try that to debug early years
        first_day = HebrewDate._elapsed_days(year)
    
        while first_day > jd:
            year -= 1
            first_day = HebrewDate._elapsed_days(year)
        
        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not HebrewDate._is_leap(year):
            months.remove(13)
        
        days_remaining = jd - first_day
        for month in months:
            if days_remaining >= HebrewDate._month_length(year, month):
                days_remaining -= HebrewDate._month_length(year, month)
            else:
                return HebrewDate(year, month, days_remaining + 1, self.day)

    def _to_x(self, type_):
        """Return a date object of the given type."""
        
        if isinstance(type_, GregorianDate):
            return self.to_greg()
        elif isinstance(type_, HebrewDate):
            return self.to_heb()
        elif isinstance(type_, JulianDay):
            return self
        
    def to_pydate(self):
        """Convert to a datetime.date object.
        
        Returns
        -------
        datetime.date
          A standard library datetime.date instance.
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
    """
 
    def __init__(self, year, month, day, jd=None):
        """Initialize a GregorianDate.
        
        This initializer extends the CalendarDateMixin initializer
        adding in date validation specific to Gregorian dates.
        """
        if month < 1 or month > 12:
            raise ValueError('{0} is an invalid month.'.format(str(month)))
        monthlength = self._monthlength(year, month)
        if day < 1 or day > monthlength:
            raise ValueError('Given month has {0} days.'.format(monthlength))
        super(GregorianDate, self).__init__(year, month, day, jd)
           
    def __iter__(self):
        yield self.year
        yield self.month
        yield self.day
        
    
    @property
    def jd(self):
        """Return the corresponding Julian Day.
        
        This property retrieves the corresponding Julian Day as a float
        if it was passed into the init method or already calculated, and
        if it wasn't, it calculates it and saves it for later retrievals
        and returns it.
        """
        if self._jd is None:
            year = self.year
            month = self.month + 1
            day = self.day
            if month in [1, 2]:
                year -= 1
                month += 12
            a = year // 100
            b = 2 - a + a//4
            self._jd = (int(365.25*year) + 
                        int(30.6001*month) + b + day + 1720994.5)
        return self._jd
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
        return GregorianDate(*date.today().timetuple()[:3])
    
    @staticmethod
    def _is_leap(year):
        """Return True if year of date is a leap year, otherwise False."""
        if(
            (year % 4 == 0) and not
            (year % 100 == 0 and year % 400 != 0)
          ):
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
        elif month != 2:
            return 30
        else:
            return 29 if cls._is_leap(year) else 28
            
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
          The equivalent Hebrew date instance.
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
            raise ValueError('{0} is an invalid month.'.format(str(month)))
        if (not self._is_leap(year)) and month == 13:
            raise ValueError('{0} is not a leap year'.format(year))
        monthlength = self._month_length(year, month)
        if day < 1 or day > monthlength:
            raise ValueError('Given month has {0} days.'.format(monthlength))
        super(HebrewDate, self).__init__(year, month, day, jd)
    
    @property
    def jd(self):
        if self._jd is None:
            months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
            if not HebrewDate._is_leap(self.year):
                months.remove(13)
    
            jd = HebrewDate._elapsed_days(self.year)
            for m in months:
                if m != self.month:
                    jd += HebrewDate._month_length(self.year, m)
                else:
                    self._jd = jd + (self.day-1) + 347996.5
                    
        return self._jd
            
    @staticmethod
    def today():
        """Return HebrewDate instance for the current day.
        
        This static method wraps the Python standard library's
        date.today() method to get the date from the timestamp.
        
        Returns
        -------
        HebrewDate
          The current Hebrew date from the computer's timestamp.
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
    
    
    @staticmethod
    def _is_leap(year):
        if (((7*year) + 1) % 19) < 7:
            return True
        return False
    
    @classmethod
    @memoize(maxlen=100)
    def _elapsed_days(cls, year):
        months_elapsed = (
                      (235 * ((year-1) // 19)) + (12 * ((year-1) % 19)) + 
                      (7 * ((year-1) % 19) + 1) // 19
                      )
        parts_elapsed = 204 + 793*(months_elapsed%1080)
        hours_elapsed = (5 + 12*months_elapsed + 793*(months_elapsed//1080) +
                         parts_elapsed//1080)
        conjunction_day = 1 + 29*months_elapsed + hours_elapsed//24
        conjunction_parts = 1080 * (hours_elapsed%24) + parts_elapsed%1080
    
        if (
              (conjunction_parts >= 19440) or
              (
               (conjunction_day % 7 == 2) and
               (conjunction_parts >= 9924) and
               (not cls._is_leap(year))
              ) or
              (
               (conjunction_day % 7 == 1) and
               conjunction_parts >= 16789 and cls._is_leap(year - 1))):
            # if all that
            alt_day = conjunction_day + 1
    
        else:
            alt_day = conjunction_day
        
        if (alt_day % 7) in (0, 3, 5):
            alt_day += 1
    
        return alt_day

    @classmethod
    def _days_in_year(cls, year):
        return cls._elapsed_days(year + 1) - cls._elapsed_days(year)

    @classmethod
    def _long_cheshvan(cls, year):
        """Returns True if Cheshvan has 30 days"""
        return cls._days_in_year(year) % 10 == 5

    @classmethod
    def _short_kislev(cls, year):
        """Returns True if Kislev has 29 days"""
        return cls._days_in_year(year) % 10 == 3

    @classmethod
    def _month_length(cls, year, month):
        """Months start with Nissan (Nissan is 1 and Tishrei is 7"""
        
        if month in [1, 3, 5, 7, 11]:
            return 30
        elif month in [2, 4, 6, 10, 13]:
            return 29
        elif month == 12:
            return 30 if cls._is_leap(year) else 29
        elif month == 8:   # if long Cheshvan return 30, else return 29
            return 30 if cls._long_cheshvan(year) else 29
        elif month == 9:   # if short Kislev return 29, else return 30
            return 29 if cls._short_kislev(year) else 30