from __future__ import unicode_literals
from __future__ import division

from collections import deque
from numbers import Number

import luachcal
from luachcal.utils import memoize


def _is_leap(year):
    if (( (7*year) + 1) % 19) < 7:
        return True
    return False
    
@memoize(maxlength=100)    
def _elapsed_days(year):
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
            (conjunction_day % 7 == 2) and (conjunction_parts >= 9924) and 
           (not _is_leap(year))
         ) or
        (
            (conjunction_day % 7 == 1) and
         conjunction_parts >= 16789 and _is_leap(year - 1)
         )
        ):
        alt_day = conjunction_day + 1
    
    else:
        alt_day = conjunction_day
        
    if (alt_day % 7) in (0, 3, 5):
        alt_day += 1
    
    return alt_day


def _days_in_year(year):
    return _elapsed_days(year + 1) - _elapsed_days(year)


def _long_cheshvan(year):
    """Returns True if Cheshvan has 30 days"""
    return _days_in_year(year) % 10 == 5


def _short_kislev(year):
    """Returns True if Kislev has 29 days"""
    return _days_in_year(year) % 10 == 3


def _month_length(year, month):
    """Months start with Nissan (Nissan is 1 and Tishrei is 7"""
        
    if month in (1, 3, 5, 7, 11):
        return 30
    elif month in (2, 4, 6, 10, 13):
        return 29
    elif month == 12:
        return 30 if _is_leap(year) else 29
    elif month == 8:   # if long Cheshvan return 30, else return 29
        return 30 if _long_cheshvan(year) else 29
    elif month == 9:   # if short Kislev return 29, else return 30
        return 29 if _short_kislev(year) else 30


class Year(object):
    
    def __init__(self, year):
        self. year = year
        self.leap = _is_leap(year)
        
    def __len__(self):
        return _days_in_year(self.year)
    
    def __iter__(self):
        """Return generator of integers of months of year."""
        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not self.leap:
            months.remove(13)
        for month in months:
            yield month
            
    def iter_days(self):
        """Return generator of integers of days in year"""
        for day in xrange(1, len(self) + 1):
            yield day


class Month(object):
    
    monthnames = {7: 'Tishrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Teves', 
                  11: 'Shvat', 13:'Adar Sheni', 1: 'Nissan', 2: 'Iyar',
                  3: 'Sivan', 4: 'Tamuz', 5: 'Av', 6: 'Elul'}
    
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.monthnames[12] = 'Adar Rishon' if _is_leap(self.year) else ' Adar' 
        self.name = self.monthnames[self.month]
        
    def __repr__(self):
        return 'Month({0}, {1})'.format(self.year, self.month)
            
    def __len__(self):
        return _month_length(self.year, self.month) 
    
    def __iter__(self):
        for day in xrange(1, len(self) + 1):
            yield day
            
    def __add__(self, other):
        yearmonths = list(Year(self.year))
        index = yearmonths.index(self.month)
        leftover_months = len(yearmonths[index:]) - 1
        if other < leftover_months:
            return Month(self.year, yearmonths[index + other])
        return Month(self.year + 1, 1).__add__(other - leftover_months)
                                               
    
    def __sub__(self, other):
        if isinstance(other, Number):
            yearmonths = list(Year(self.year))
            index = yearmonths.index(self.month)
            leftover_months = index
            if other < leftover_months:
                return Month(self.year, yearmonths[index - other])
            return Month(self.year - 1,
                         deque(Year(self.year - 1), maxlen=1).pop()).__sub__(
                                                    other - leftover_months
                                                    )
                    # Recursive call on the last month of the previous year. 
        try:
            return abs(self._elapsed_months() - other._elapsed_months())
        except AttributeError:
            raise TypeError('''You can only subtract a number or a month
                            object from a month''')
            
            
    @property
    def starting_weekday(self):
        return luachcal.dates.HebrewDate(self.year, self.month, 1).weekday
    
    def _elapsed_months(self):
        '''Return number of months elapsed from beginning of calendar'''
        yearmonths = tuple(Year(self.year))
        months_elapsed = (
                      (235 * ((self.year-1) // 19)) +
                      (12 * ((self.year-1) % 19)) + 
                      (7 * ((self.year-1) % 19) + 1) // 19 +
                      yearmonths.index(self.month)
                      )
        return months_elapsed
