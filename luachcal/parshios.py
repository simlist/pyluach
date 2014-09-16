from collections import deque, OrderedDict

from luachcal.dates import HebrewDate
from luachcal.utils import memoize

PARSHIOS = dict(zip(range(54), [
            'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
            'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
            'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
            'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
            'Pekudei', 'Vayikra', 'Tzav','Shemini', 'Tazria', 'Metzora',
            'Acharei Mos','Kedoshim', 'Emor', "Behar", 'Bechukosai', 'Bamidbar',
            'Naso',"Baha'aloscha", "Shelach", 'Korach', 'Chukas', 'Balak',
            'Pinchas','Matos', "Ma'sei", 'Devarim', "Va'eschanan", 'Eikev',
            "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim', 'Vayelech',
            'Haazinu', "Vezos Habrocho"]))

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
    parshalist = deque([51, 52, 53] + range(52))
    table = OrderedDict()
    leap = HebrewDate._is_leap(year)
    pesachday = HebrewDate(year, 1, 15).weekday()
    rosh_hashana = HebrewDate(year, 7, 1)
    shabbos = (rosh_hashana + 2).shabbos()
    if rosh_hashana.weekday > 4:
                parshalist.popleft()
                
    while shabbos.year == year:
        if _parshaless(shabbos, israel):
            table[shabbos.tuple()] = None
        else:
            parsha = parshalist.popleft()
            if parsha == 53:  # Vezos Habrocha
                table[(year, 7, 22 if israel else 23)] = PARSHIOS[parsha]
                parsha = parshalist.popleft()
            table[shabbos.tuple()] = PARSHIOS[parsha]
            if(
               (parsha == 21 and (HebrewDate(year, 1, 14)-shabbos) / 7 < 3) or
               (parsha in [26, 28] and not leap) or
               (parsha == 31 and not leap and (
                                               not israel or pesachday != 7
                                               )) or
               (parsha == 38 and not israel and pesachday == 5) or
               (parsha == 41 and (HebrewDate(year, 5, 9)-shabbos) // 7 < 2)  or
               (parsha == 50 and HebrewDate(year+1, 7, 1).weekday() > 4)
               ):  #  If any of that then it's a double parsha.
                key = shabbos.tuple()
                table[key] = ' '.join(
                                      table[key],
                                      PARSHIOS[parshalist.popleft()]
                                      )
        shabbos += 7
    return table    
        

def getparsha(shabbos, israel=False):
    """Return the parsha for a given date."""
    shabbos = shabbos.shabbos()
    table = _gentable(shabbos.year, israel)
    return table[shabbos.tuple()]


def iterparshios(year, israel=False):
    """Generate all the parshios in the year."""
    table = _gentable(year, israel)
    for shabbos in table:
        yield table[shabbos]
        
            
