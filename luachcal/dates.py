from datetime import date
from numbers import Number


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
            if self > other or self == jd:
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
        first_day = HebrewDate.elapsed_days(year)
    
        while first_day > jd:
            year -= 1
            first_day = HebrewDate.elapsed_days(year)
        
        months = [7, 8, 9, 10 , 11 , 12 , 13, 1, 2, 3, 4, 5, 6]
        if not HebrewDate.is_leap(year):
            months.remove(13)
        
        days_remaining = jd - first_day
        for month in months:
            if days_remaining >= HebrewDate.month_length(year, month):
                days_remaining -= HebrewDate.month_length(year, month)
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
            if not self.is_leap(self.year):
                months.remove(13)
    
            jd = self.elapsed_days(self.year)
            for m in months:
                if m != self.month:
                    jd += self.month_length(self.year, m)
                else:
                    self._jd = jd + (self.day-1) + 347997
                    
        return self._jd
            
    
    @staticmethod
    def today():
        return GregorianDate.today().to_heb()
     
    @staticmethod
    def is_leap(year):
        if (( (7*year) + 1) % 19) < 7:
            return True
        return False
    
    @classmethod
    def elapsed_days(cls, year):
        months_elapsed = (
                      (235 * ((year-1) / 19)) + (12 * ((year-1) % 19)) + 
                      (7 * ((year-1) % 19) + 1) / 19
                      )
        parts_elapsed = 204 + 793*(months_elapsed%1080)
        hours_elapsed = 5 + 12*months_elapsed + 793*(months_elapsed/1080) + parts_elapsed/1080
        conjunction_day = 1 + 29*months_elapsed + hours_elapsed/24
        conjunction_parts = 1080 * (hours_elapsed%24) + parts_elapsed%1080
    
        if (
            (conjunction_parts >= 19440) or
            (
               (conjunction_day % 7 == 2) and (conjunction_parts >= 9924) and 
               (not cls.is_leap(year))
             ) or
            (
             (conjunction_day % 7 == 1) and
             conjunction_parts >= 16789 and cls.is_leap(year - 1)
             )
            ):
            alt_day = conjunction_day + 1
    
        else:
            alt_day = conjunction_day
        
        if (alt_day % 7) in (0, 3, 5):
            alt_day += 1
    
        return alt_day

    @classmethod
    def days_in_year(cls, year):
        return cls.elapsed_days(year + 1) - cls.elapsed_days(year)

    @classmethod
    def long_cheshvan(cls, year):
        """Returns True if Cheshvan has 30 days"""
        return cls.days_in_year(year) % 10 == 5

    @classmethod
    def short_kislev(cls, year):
        """Returns True if Kislev has 29 days"""
        return cls.days_in_year(year) % 10 == 3

    @classmethod
    def month_length(cls, year, month):
        """Months start with Nissan (Nissan is 1 and Tishrei is 7"""
        
        if month in (1, 3, 5, 7, 11):
            return 30
        elif month in (2, 4, 6, 10, 13):
            return 29
        elif month == 12:
            return 30 if cls.is_leap(year) else 29
        elif month == 8:   # if long Cheshvan return 30, else return 29
            return 30 if cls.long_cheshvan(year) else 29
        elif month == 9:   # if short Kislev return 29, else return 30
            return 29 if cls.short_kislev(year) else 30
    ###todo add exception for out of range (maybe decorator to validate date range   
    
    def to_jd(self):
        """Return an instance of JulianDay"""
        return JulianDay(self.jd)
            
    def to_greg(self):
        """Return instance of GregorianDate"""
        return self.to_jd().to_greg()
 
 