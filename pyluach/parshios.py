"""This module has functions to find the weekly parasha for a given Shabbos.

Attributes
----------
PARSHIOS : list of str
  A list of all of the parsha names starting with Beraishis through V'zos
  Habrocha.

Notes
-----
The algorithm is based on Dr. Irv Bromberg's, University of Toronto at 
http://individual.utoronto.ca/kalendis/hebrew/parshah.htm

All parsha names are transliterated into the American Ashkenazik pronunciation.
"""

from __future__ import division

from collections import deque, OrderedDict

from pyluach.dates import HebrewDate
from pyluach.utils import memoize

  

PARSHIOS = [
            'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
            'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
            'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
            'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
            'Pekudei', 'Vayikra', 'Tzav','Shemini', 'Tazria', 'Metzora',
            'Acharei Mos','Kedoshim', 'Emor', "Behar", 'Bechukosai', 'Bamidbar',
            'Naso',"Baha'aloscha", "Shelach", 'Korach', 'Chukas', 'Balak',
            'Pinchas','Matos', "Ma'sei", 'Devarim', "Va'eschanan", 'Eikev',
            "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim', 'Vayelech',
            'Haazinu', "V'zos Habrocha" 
            ]


def _parshaless(date, israel=False):
    if israel and date.tuple()[1:] in [(7,23), (1,22), (3,7)]:
        return False
    if date.month == 7 and date.day in ([1,2,10] + range(15, 24)):
        return True
    if date.month == 1 and date.day in range(15, 23):
        return True
    if date.month == 3 and date.day in [6, 7]:
        return True
    return False


@memoize(maxlen=50)
def _gentable(year, israel=False):
    """Return OrderedDict mapping date of Shabbos to parsha name."""
    parshalist = deque([51, 52] + range(52))
    table = OrderedDict()
    leap = HebrewDate._is_leap(year)
    pesachday = HebrewDate(year, 1, 15).weekday()
    rosh_hashana = HebrewDate(year, 7, 1)
    shabbos = (rosh_hashana + 2).shabbos()
    if rosh_hashana.weekday() > 4:
        parshalist.popleft()
                
    while shabbos.year == year:
        if _parshaless(shabbos, israel):
            table[shabbos] = None
        else:
            parsha = parshalist.popleft()
            table[shabbos] = PARSHIOS[parsha]
            if(
               (parsha == 21 and (HebrewDate(year, 1, 14)-shabbos) // 7 < 3) or
               (parsha in [26, 28] and not leap) or
               (parsha == 31 and not leap and (
                                               not israel or pesachday != 7
                                               )) or
               (parsha == 38 and not israel and pesachday == 5) or
               (parsha == 41 and (HebrewDate(year, 5, 9)-shabbos) // 7 < 2)  or
               (parsha == 50 and HebrewDate(year+1, 7, 1).weekday() > 4)
               ):  #  If any of that then it's a double parsha.
                table[shabbos] = ', '.join([
                                      table[shabbos],
                                      PARSHIOS[parshalist.popleft()]
                                      ])
        shabbos += 7
    return table    
        

def getparsha(date, israel=False):
    """Return the parsha for a given date.
    
    Returns the parsha for the Shabbos on or following the given 
    date.
    
    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      This date does not have to be a Shabbos.
      
    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``.
      
    Returns
    -------
    str or ``None``
      The name of the parsha, or ``None`` if the Shabbos doesn't have
      a parsha (i.e. it's on Yom Tov).
    """
    shabbos = date.to_heb().shabbos()
    table = _gentable(shabbos.year, israel)
    return table[shabbos]


def iterparshios(year, israel=False):
    """Generate all the parshios in the year.
    
    Parameters
    ----------
    year : int
      The Hebrew year to get the parshios for.
    
    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``
      
    Yields
    ------
    str
      The name of the parsha for the next Shabbos in the given year.
      Yields ``None`` for a Shabbos that doesn't have its own parsha
      (i.e. it occurs on a yom tov). 
    """
    table = _gentable(year, israel)
    for shabbos in table:
        yield table[shabbos]    

def parshatable(year, israel=False):
    """Return a table of all the Shabbosos in the year
    
    Parameters
    ----------
    year : int
      The Hebrew year to get the parshios for.
    
    israel : bool, optional
      ``True`` if you want the parshios according to the Israel
      schedule (with only one day of Yom Tov). Defaults to ``False``.
      
    Returns
    -------
    OrderedDict
      An ordered dictionary with the date of each Shabbos
      as the key mapped to the parsha as a string, or ``None`` for a
      Shabbos with no parsha.
    """
    return _gentable(year, israel)
