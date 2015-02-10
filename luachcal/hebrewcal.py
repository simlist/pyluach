from __future__ import unicode_literals
from __future__ import division

from collections import deque
from numbers import Number

from luachcal.dates import HebrewDate
from luachcal.utils import memoize

def _adjust_postponed(date):
    """Return actual date of fast day.
    
    For usual date of a fast day returns fast day adjusted for any
    postponements. 
    """
    if date.weekday() == 7:
        if date.month in [12, 13]:
            date -= 2
        else:
            date += 1
    return date
        

@memoize(maxlen=50)
def _fast_day_table(year):
    table = dict()
    workingdate = _adjust_postponed(HebrewDate(year, 7, 3))
    table[workingdate] = 'Tzom Gedalia'
    
    workingdate = _adjust_postponed(HebrewDate(year, 10, 10))
    table[workingdate] = '10 of Teves'
    
    month = 13 if Year(year).leap else 12
    workingdate = _adjust_postponed(HebrewDate(year, month, 13))
    table[workingdate] = 'Taanis Esther'
    
    workingdate = _adjust_postponed(HebrewDate(year, 4, 17))
    table[workingdate] = '17 of Tamuz'
    
    workingdate = _adjust_postponed(HebrewDate(year, 5, 9))
    table[workingdate] = '9 of Av'
    
    return table

def holiday(date, israel=False):
    """Return Jewish holiday of given date.
    
    The holidays include the major and minor religious Jewish
    holidays including fast days.
    
    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.
      
    israel : boolian, optional
      True if you want the holidays according to the israel schedule.
      Defaults to ``False``.
    
    Returns
    -------
    str or ``None``
      The name of the holiday or ``None`` if the given date is not
      a Jewish holiday.
    """
    date = date.to_heb()
    year = date.year
    month = date.month
    day = date.day
    table = _fast_day_table(year)
    if date in table:
        return table[date]
    if month == 7:
        if day in range(1, 3):
            return 'Rosh Hashana'
        elif day == 10:
            return 'Yom Kippur'
        elif day in range(15, 22):
            return 'Succos'
        elif day == 22:
            return 'Shmini Atzeres'
        elif day == 23 and israel == False:
            return 'Simchas Torah'
    elif(
         (month == 9 and day in range(25, 30)) or 
         date in [(HebrewDate(year, 9, 29) + n) for n in range(1, 4)]
         ):
        return 'Chanuka'
    elif month == 11 and day == 15:
        return "Tu B'shvat"
    elif month == 12:
        leap = HebrewDate._is_leap(year)
        if day == 14:
            return 'Purim Katan' if leap else 'Purim'
        if day == 15 and not leap:
            return 'Shushan Purim'
    elif month == 13:
        if day == 14:
                return 'Purim'
        elif day == 15:
            return 'Shushan Purim'
    elif month == 1 and day in range(15, 22 if israel else 23):
        return 'Pesach'
    elif month == 2 and day == 18:
        return "Lag Ba'omer"
    elif month == 3 and (day == 6 if israel else day in (6, 7)):
        return 'Shavuos'
    elif month == 5 and day == 15:
        return "Tu B'av" 


class Year(object):
    
    """
    A Year object represents a Hebrew calendar year.
    
    Parameter
    ---------
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
        
        """
        The initializer for a Year object.
        """
        if year < 1:
            raise ValueError('Year {0} is before creation.'.format(year))
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
        ``HebrewDate``
            The next date of the Hebrew calendar year starting with
            the first of Tishrei. 
        """
        for month in self.itermonths():
            for day in month:
                yield HebrewDate(self.year, month.month, day)
        

class Month(object):
    
    """
    A Month object represents a month of the Hebrew calendar.
    
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
        """Return iterator that yields an instance of HebrewDate.
        
        Yields
        ------
        ``HebrewDate``
          The next Hebrew Date of the year starting the first day of
          Tishrei through the last day of Ellul.
        """
        for day in self:
            yield HebrewDate(self.year, self.month, day)