#  from __future__ import division

from datetime import date
from numbers import Number

from luachcal import hebrewcal


class BaseDate(object):
    
    def __init__(self, year, month, day, jd=None):
        self.year = year
        self.month = month
        self.day = day
        self._jd = jd
        
        
    def __repr__(self):
        return '{0}({1}, {2}, {3})'.format(self.__class__.__name__,
                                           self.year,
                                           self.month,
                                           self.day)
        
    def __add__(self, other):
        try:
            return JulianDay(self.jd + other).to_x(self)
        except AttributeError:
            raise TypeError('You can only add a number to a date.') 
    
    def __sub__(self, other):
        try:
            if isinstance(other, Number): 
                return JulianDay(self.jd - other).to_x(self)
            else:
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
            return NotImplemented
    
    def __ne__(self, other):
        try:
            if not self == other:
                return True
            return False
        except AttributeError:
            return NotImplemented
    
    def __lt__(self, other):
        try:
            if self.jd < other.jd:
                return True
            return False
        except AttributeError:
            return NotImplemented
    
    def __gt__(self, other):
        try:
            if self.jd > other.jd:
                return True
            return False
        except AttributeError:
            return NotImplemented

    
    def __le__(self, other):
        try:
            if self < other or self == other:
                return True
            return False
        except AttributeError:
            return NotImplemented
    
    def __ge__(self, other):
        try:
            if self > other or self == other:
                return True
            return False
        except AttributeError:
            return NotImplemented
    

class CalendarDateMixin(object):
    """Mixin for Hebrew and Gregorian but not jd"""
    
    @property
    def weekday(self):
        """Return integer with Sunday as 1 and Saturday as 7."""
        return int(self.jd+.5+1) % 7 + 1
    
    def tuple(self):
        """Return tuple of date in the form (year, month, day)."""
        return (self.year, self.month, self.day)
    
    def dict(self):
        """Return dictionary of date with keys year, date, and month."""
        return {'year': self.year, 'month': self.month,'day': self.day}
    

class JulianDay(BaseDate):
    
    def __init__(self, day):
        self.day = day
        self.jd = day
        
    def __repr__(self):
        return 'JulianDay({0})'.format(self.day)
        
    def __str__(self):
        return str(self.day)
    
    def weekday(self):
        """Return weekday as integer with Sunday as 1 and Saturday as 7."""
        return (int(self.day+.5) + 1) % 7 + 1
    
    @staticmethod
    def today():
        """Return instance of current Julian day"""
        return GregorianDate.today().to_jd()
    
    def to_greg(self):
        """Return instance of GregorianDate calculated from Julian day"""
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
        """ Return an instance of HebrewDate calculated from Julian day."""
    
        if self.day <= 347997:
            raise ValueError('Date is before creation')
    
        jd = int(self.day + .5)  # Try to account for half day
        jd -= 347997
        year = int(jd//365) + 2  ## try that to debug early years
        first_day = hebrewcal._elapsed_days(year)
    
        while first_day > jd:
            year -= 1
            first_day = hebrewcal._elapsed_days(year)
        
        months = [7, 8, 9, 10 , 11 , 12 , 13, 1, 2, 3, 4, 5, 6]
        if not hebrewcal._is_leap(year):
            months.remove(13)
        
        days_remaining = jd - first_day
        for month in months:
            if days_remaining >= hebrewcal._month_length(year, month):
                days_remaining -= hebrewcal._month_length(year, month)
            else:
                return HebrewDate(year, month, days_remaining + 1, self.day)

    def to_x(self, type_):
        """Return a date object of the given type."""
        
        if isinstance(type_, GregorianDate):
            return self.to_greg()
        elif isinstance(type_, HebrewDate):
            return self.to_heb()
        elif isinstance(type_, JulianDay):
            return self
        
    def to_pydate(self):
        """Return instance of datetime.date"""
        return self.to_greg().to_pydate()
           
class GregorianDate(BaseDate, CalendarDateMixin):

    def __iter__(self):
        yield self.year
        yield self.month
        yield self.day
        
    
    @property
    def jd(self):
        """Return the corresponding Julian Day.
        
        This property retrieves the corresponding Julian Day as an int
        if it was passed into the init method or already calculated, and
        if it wasn't, it calculates it and saves it for later retrievals
        and returns it. 
        """
        if self._jd is None:
            a = (
             1721424.5 +     # Gregorian epoch - 1
             (365 * (self.year-1)) +
             ((self.year-1) / 4 ) -
             ((self.year-1) / 100) +
             ((self.year-1) / 400) 
            )
            b = (((367*self.month) - 362) / 12)
      
            if self.month > 2:
                if self.is_leap():
                    b -= 1
                else:
                    b -= 2
              
            b += self.day
        
            self._jd = a + int(b)  

        return self._jd            
            
    @staticmethod
    def today():
        """Return a GregorianDate object for the current day.
        
        This static method wraps the Python library's date.today() method
        to get the date from the timestamp.
        """
        return GregorianDate(*date.today().timetuple()[:3])
    
    def is_leap(self):
        """Return True if year of date is a leap year, otherwise False."""
        if(
            (self.year % 4 == 0) and not
            (self.year % 100 == 0 and self.year % 400 != 0)
          ):
                return True
        return False
            
    def to_jd(self):
        """Return instance of JulianDay."""
        return JulianDay(self.jd)
    
    def to_heb(self):
        """Return instance of HebrewDate."""
        return self.to_jd().to_heb()
    
    def to_pydate(self):
        """Return instance of datetime.date."""
        return date(*self.tuple())
            
    
class HebrewDate(BaseDate, CalendarDateMixin):
    """
    A class for manipulating Hebrew dates.
    
    The month is an integer starting with 1 for Nissan and ending
    with 13 for the second Adar of a leap year.
    """
    
    def __init__(self, year, month, day, jd=None):
        if year < 1:
            raise ValueError('Date supplied is before creation.')
        BaseDate.__init__(self, year, month, day, jd)
        
    def __str__(self):
        return '{0}-{1}-{2}'.format(self.year, self.month, self.day)
    
    @property
    def jd(self):
        if self._jd is None:
            months = [7, 8, 9, 10 , 11 , 12 , 13, 1, 2, 3, 4, 5, 6]
            if not hebrewcal._is_leap(self.year):
                months.remove(13)
    
            jd = hebrewcal._elapsed_days(self.year)
            for m in months:
                if m != self.month:
                    jd += hebrewcal._month_length(self.year, m)
                else:
                    self._jd = jd + (self.day-1) + 347997
                    
        return self._jd
            
    @staticmethod
    def today():
        """Return HebrewDate object from timestamp.
        
        This is a static factory method that wraps the built in 
        datetime.date.today method converting it to a Hebrew date.
        """
        return GregorianDate.today().to_heb()
     
    def to_jd(self):
        """Return an instance of JulianDay"""
        return JulianDay(self.jd)
            
    def to_greg(self):
        """Return instance of GregorianDate"""
        return self.to_jd().to_greg()

    def to_pydate(self):
        return self.to_greg().to_pydate()
    