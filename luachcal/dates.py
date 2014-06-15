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
#                               that has a "jd" attribute from a date""")
        
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
    

class BaseFullDate(object):
    """Mixin for Hebrew and Gregorian but not jd"""
    
    def to_tuple(self):
        return (self.year, self.month, self.day)
    
    def to_dict(self):
        return {'year': self.year, 'month': self.month,'day': self.day}
    
class JulianDay(BaseDate):
    
    def __init__(self, day):
        self.day = day
        self.jd = day
        
    def __repr__(self):
        return 'JulianDay({0})'.format(self.day)
        
    def __str__(self):
        return str(self.day)
    
    
    @staticmethod
    def today():
        """Return instance of current Julian day"""
        return GregorianDate.today().to_jd()
    
    def to_greg(self):
        """Return instance of GregorianDate calculated from Julian day"""
        jd = int(self.day + .5)
        L = jd + 68569
        n = 4*L / 146097
        L = L - (146097*n + 3) / 4
        i = (4000 * (L+1)) / 1461001
        L = L - ((1461*i) / 4) + 31
        j = (80*L) / 2447
        day = L - 2447*j / 80
        L = j / 11
        month = j + 2 - 12*L
        year = 100 * (n-49) + i + L
    
        return GregorianDate(year, month, day, self.day)
    
    def to_heb(self):
        """ Return an instance of HebrewDate calculated from Julian day."""
    
        if self.day <= 347997:
            raise ValueError('Date is before creation')
    
        jd = int(self.day + .5)  # Try to account for half day
        jd -= 347997
        year = int(jd/365) + 2  ## try that to debug early years
        first_day = hebrewcal.elapsed_days(year)
    
        while first_day > jd:
            year -= 1
            first_day = hebrewcal.elapsed_days(year)
        
        months = [7, 8, 9, 10 , 11 , 12 , 13, 1, 2, 3, 4, 5, 6]
        if not hebrewcal.is_leap(year):
            months.remove(13)
        
        days_remaining = jd - first_day
        for month in months:
            if days_remaining >= hebrewcal.month_length(year, month):
                days_remaining -= hebrewcal.month_length(year, month)
            else:
                return HebrewDate(year, month, days_remaining + 1, self.day)

    def to_x(self, cls):
        if isinstance(cls, GregorianDate):
            return self.to_greg()
        elif isinstance(cls, HebrewDate):
            return self.to_heb()
        elif isinstance(cls, JulianDay):
            return self
    
    def to_tuple(self):
        raise NotImplementedError
#  Work in progress past here
        
        
class GregorianDate(BaseDate, BaseFullDate):

    def __iter__(self):
        yield self.year
        yield self.month
        yield self.day
        
    
    @property
    def jd(self):
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
        return GregorianDate(*date.today().timetuple()[:3])
    
    def is_leap(self):
        if(
            (self.year % 4 == 0) and not
            (self.year % 100 == 0 and self.year % 400 != 0)
          ):
                return True
        return False
            
        
    def to_jd(self):
        return JulianDay(self.jd)
    
    def to_heb(self):
        return self.to_jd().to_heb()
            
    
class HebrewDate(BaseDate, BaseFullDate):
    """
    A class for working with Hebrew dates.
    
    The month is an integer starting with 1 for Nissan and ending
    with 13 for the second Adar of a leap year.
    """

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.year, self.month, self.day)
    
    def __iter__(self):
        yield self.year
        yield self.month
        yield self.day
    
    @property
    def jd(self):
        if self._jd is None:
            months = [7, 8, 9, 10 , 11 , 12 , 13, 1, 2, 3, 4, 5, 6]
            if not hebrewcal.is_leap(self.year):
                months.remove(13)
    
            jd = hebrewcal.elapsed_days(self.year)
            for m in months:
                if m != self.month:
                    jd += hebrewcal.month_length(self.year, m)
                else:
                    self._jd = jd + (self.day-1) + 347997
                    
        return self._jd
            
    
    @staticmethod
    def today():
        return GregorianDate.today().to_heb()
     
    
    def to_jd(self):
        """Return an instance of JulianDay"""
        return JulianDay(self.jd)
            
    def to_greg(self):
        """Return instance of GregorianDate"""
        return self.to_jd().to_greg()
 
 