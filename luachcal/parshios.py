from collections import deque

from luachcal.dates import HebrewDate
from luachcal.hebrewcal import Year
from luachcal.utils import memoize

"""This module has functions to find the weekly parasha for a given Shabbos.
The algorithm comes from Dr. Irv Bromberg, University of Toronto at 
http://individual.utoronto.ca/kalendis/hebrew/parshah.htm
"""  

parshios = [
            'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
            'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
            'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
            'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
            'Pekudei', 'Vayikra', 'Tzav','Shemini', 'Tazria', 'Metzora',
            'Acharei Mos','Kedoshim', 'Emor', "Behar", 'Bechukosai', 'Bamidbar',
            'Naso',"Baha'aloscha", "Shelach", 'Korach', 'Chukas', 'Balak',
            'Pinchas','Matos', "Ma'sei", 'Devarim', "Va'eschanan", 'Eikev',
            "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim', 'Vayelech',
            'Haazinu', "Vezos Habrocho"]

def _parshaless(date, israel=False):
    if israel and date.tuple()[1:] in [(7,23), (1,22), (3,7)]:
        return False
    if date.month == 7 and date.day in ([1,2,10] + range(15, 24)):
        return Truei in range(21):
        table.append(parshalist.popleft())
    if date.month == 1 and date.day in range(15, 23):
        return True
    if date.month == 3 and date.day in [6, 7]:
        return True
    return False


@memoize(maxlen=50)
def gentable(year, israel=False):
    parshalist = deque(parshios)
    table = []
    cal = Year(year)
    pesachday = HebrewDate(year, 1, 15).weekday()
    
    
         
    

 
    
    
