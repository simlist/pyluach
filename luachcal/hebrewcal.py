from __future__ import unicode_literals
from __future__ import division

from collections import deque
from numbers import Number

from luachcal.dates import HebrewDate





class Year(object):
    
    def __init__(self, year):
        self. year = year
        self.leap = HebrewDate._is_leap(year)
        
    def __repr__(self):
        return 'Year({0})'.format(self.year)

    def __len__(self):
        return HebrewDate._days_in_year(self.year)
    
    def __iter__(self):
        """Yield integer for each month in year."""
        months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
        if not self.leap:
            months.remove(13)
        for month in months:
            yield month
            
    def itermonths(self):
        """Yield Month instance for each month of the year."""
        for month in self:
            yield Month(self.year, month)
    def iterdays(self):
        """Yield integer for each day of the year."""
        for day in range(1, len(self) + 1):
            yield day
            
    def iterdates(self):
        """Yield HebrewDate instance for each day of the year."""
        for month in self.itermonths():
            for day in month:
                yield HebrewDate(self.year, month.month, day)
        

class Month(object):
    
    monthnames = {7: 'Tishrei', 8: 'Cheshvan', 9: 'Kislev', 10: 'Teves', 
                  11: 'Shvat', 13:'Adar Sheni', 1: 'Nissan', 2: 'Iyar',
                  3: 'Sivan', 4: 'Tamuz', 5: 'Av', 6: 'Elul'}
    
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.monthnames[12] = ('Adar Rishon' if 
                               HebrewDate._is_leap(self.year) else 
                               ' Adar'
                               ) 
        self.name = self.monthnames[self.month]
        
    def __repr__(self):
        return 'Month({0}, {1})'.format(self.year, self.month)
            
    def __len__(self):
        return HebrewDate._month_length(self.year, self.month) 
    
    def __iter__(self):
        for day in range(1, len(self) + 1):
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
        return HebrewDate(self.year, self.month, 1).weekday()
    
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
    
    def iterdates(self):
        """Return iterator that yields an instance of HebrewDate."""
        for day in self:
            yield HebrewDate(self.year, self.month, day)
