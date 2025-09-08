"""The parshios module has functions to find the weekly parasha.

Examples
--------
>>> from pyluach import dates, parshios
>>> date = dates.HebrewDate(5781, 10, 5)
>>> parshios.getparsha(date)
'Vayigash'
>>> parshios.getparsha_string(date, hebrew=True)
'ויגש'
>>> parshios.getparsha_string(dates.GregorianDate(2021, 3, 7), hebrew=True)
'ויקהל, פקודי'

Note
----
The algorithm is based on Dr. Irv Bromberg's, University of Toronto at
http://individual.utoronto.ca/kalendis/hebrew/parshah.htm

All English parsha names are transliterated into the American Ashkenazik
pronunciation.


Attributes
----------
PARSHIOS : list of str
    A list of the parshios transliterated into English.
PARSHIOS_HEBREW : list of str
    A list of the parshios in Hebrew.
"""

from collections import deque, OrderedDict
from functools import lru_cache
from enum import Enum, IntEnum, auto

from pyluach.dates import HebrewDate
from pyluach.utils import _is_leap


PARSHIOS = [
    'Bereishis', 'Noach', 'Lech Lecha', 'Vayeira', 'Chayei Sarah', 'Toldos',
    'Vayeitzei', 'Vayishlach', 'Vayeishev', 'Mikeitz', 'Vayigash', 'Vayechi',
    'Shemos', "Va'eira", 'Bo', 'Beshalach', 'Yisro', 'Mishpatim', 'Terumah',
    'Tetzaveh', 'Ki Sisa', 'Vayakhel', 'Pekudei', 'Vayikra', 'Tzav', 'Shemini',
    'Tazria', 'Metzora', 'Acharei Mos', 'Kedoshim', 'Emor', 'Behar',
    'Bechukosai', 'Bamidbar', 'Nasso', "Beha'aloscha", 'Shelach', 'Korach',
    'Chukas', 'Balak', 'Pinchas', 'Mattos', 'Masei', 'Devarim', "Va'eschanan",
    'Eikev', "Re'eh", 'Shoftim', 'Ki Seitzei', 'Ki Savo', 'Nitzavim',
    'Vayeilech', 'Haazinu', 'Vezos Haberachah'
]


PARSHIOS_HEBREW = [
    'בראשית', 'נח', 'לך לך', 'וירא', 'חיי שרה', 'תולדות', 'ויצא', 'וישלח',
    'וישב', 'מקץ', 'ויגש', 'ויחי', 'שמות', 'וארא', 'בא', 'בשלח', 'יתרו',
    'משפטים', 'תרומה', 'תצוה', 'כי תשא', 'ויקהל', 'פקודי', 'ויקרא', 'צו',
    'שמיני', 'תזריע', 'מצורע', 'אחרי מות', 'קדושים', 'אמור', 'בהר', 'בחוקותי',
    'במדבר', 'נשא', 'בהעלותך', 'שלח', 'קרח', 'חקת', 'בלק', 'פינחס', 'מטות',
    'מסעי', 'דברים', 'ואתחנן', 'עקב', 'ראה', 'שופטים', 'כי תצא', 'כי תבא',
    'נצבים', 'וילך', 'האזינו', 'וזאת הברכה'
]


class _Parshios_Enum(IntEnum):
    BEREISHIS = 0
    NOACH = 1
    LECH_LECHA = auto()
    VAYEIRA = auto()
    CHAYEI_SARAH = auto()
    TOLDOS = auto()
    VAYEITZEI = auto()
    VAYISHLACH = auto()
    VAYEISHEV = auto()
    MIKEITZ = auto()
    VAYIGASH = auto()
    VAYECHI = auto()
    SHEMOS = auto()
    VAEIRA = auto()
    BO = auto()
    BESHALACH = auto()
    YISRO = auto()
    MISHPATIM = auto()
    TERUMAH = auto()
    TETZAVEH = auto()
    KI_SISA = auto()
    VAYAKHEL = auto()
    PEKUDEI = auto()
    VAYIKRA = auto()
    TZAV = auto()
    SHEMINI = auto()
    TAZRIA = auto()
    METZORA = auto()
    ACHAREI_MOS = auto()
    KEDOSHIM = auto()
    EMOR = auto()
    BEHAR = auto()
    BECHUKOSAI = auto()
    BAMIDBAR = auto()
    NASSO = auto()
    BEHAALOSCHA = auto()
    SHELACH = auto()
    KORACH = auto()
    CHUKAS = auto()
    BALAK = auto()
    PINCHAS = auto()
    MATTOS = auto()
    MASEI = auto()
    DEVARIM = auto()
    VAESCHANAN = auto()
    EIKEV = auto()
    REEH = auto()
    SHOFTIM = auto()
    KI_SEITZEI = auto()
    KI_SAVO = auto()
    NITZAVIM = auto()
    VAYEILECH = auto()
    HAAZINU = auto()
    VEZOS_HABERACHAH = auto()


class _FourParshiosEnum(Enum):
    SHEKALIM = auto()
    ZACHOR = auto()
    PARAH = auto()
    HACHODESH = auto()


_FOUR_PARSHIOS = {
    _FourParshiosEnum.ZACHOR: 'Zachor',
    _FourParshiosEnum.SHEKALIM: 'Shekalim',
    _FourParshiosEnum.HACHODESH: 'Hachodesh',
    _FourParshiosEnum.PARAH: 'Parah',
}


_FOUR_PARSHIOS_HEBREW = {
    _FourParshiosEnum.ZACHOR: 'זכור',
    _FourParshiosEnum.SHEKALIM: 'שקלים',
    _FourParshiosEnum.PARAH: 'פרה',
    _FourParshiosEnum.HACHODESH: 'החודש'
}


def _parshaless(date, israel=False):
    if israel and date.tuple()[1:] in [(7, 23), (1, 22), (3, 7)]:
        return False
    if date.month == 7 and date.day in ([1, 2, 10] + list(range(15, 24))):
        return True
    if date.month == 1 and date.day in range(15, 23):
        return True
    if date.month == 3 and date.day in [6, 7]:
        return True
    return False


@lru_cache(maxsize=10)
def _gentable(year, israel=False):
    """Return OrderedDict mapping date of Shabbos to list of parsha numbers.

    The numbers start with Beraishis as 0. Double parshios are represented
    as a list of the two numbers. If there is no Parsha the value is None.
    """
    parshalist = deque([51, 52] + list(range(52)))
    table = OrderedDict()
    leap = _is_leap(year)
    pesachday = HebrewDate(year, 1, 15).weekday()
    rosh_hashana = HebrewDate(year, 7, 1)
    shabbos = rosh_hashana.shabbos()
    if rosh_hashana.weekday() > 4:
        parshalist.popleft()

    while shabbos.year == year:
        if _parshaless(shabbos, israel):
            table[shabbos] = None
        else:
            parsha = parshalist.popleft()
            table[shabbos] = [parsha]
            if (
                (
                    parsha == _Parshios_Enum.VAYAKHEL
                    and (HebrewDate(year, 1, 14) - shabbos) // 7 < 3
                )
                or (
                    parsha in [
                        _Parshios_Enum.TAZRIA, _Parshios_Enum.ACHAREI_MOS
                    ] and not leap
                )
                or (
                    parsha == _Parshios_Enum.BEHAR and not leap
                    and (not israel or pesachday != 7)
                )
                or (
                    parsha == _Parshios_Enum.CHUKAS
                    and not israel and pesachday == 5
                )
                or (
                    parsha == _Parshios_Enum.MATTOS
                    and (HebrewDate(year, 5, 9)-shabbos) // 7 < 2
                )
                or (
                    parsha == _Parshios_Enum.NITZAVIM
                    and HebrewDate(year+1, 7, 1).weekday() > 4
                )
            ):
                #  If any of that then it's a double parsha.
                table[shabbos].append(parshalist.popleft())
        shabbos += 7
    return table


def getparsha(date, israel=False):
    """Return the parsha for a given date.

    Returns the parsha for the Shabbos on or following the given
    date.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
      Any subclass of ``BaseDate``. This date does not have to be a Shabbos.

    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Defaults to ``False``.

    Returns
    -------
    list of int or None
      A list of the numbers of the parshios for the Shabbos of the given date,
      beginning with 0 for Beraishis, or ``None`` if the Shabbos doesn't
      have a parsha (i.e. it's on Yom Tov).
    """
    shabbos = date.to_heb().shabbos()
    table = _gentable(shabbos.year, israel)
    return table[shabbos]


def getparsha_string(date, israel=False, hebrew=False):
    """Return the parsha as a string for the given date.

    This function wraps ``getparsha`` returning the parsha name.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
      Any subclass of ``BaseDate``. The date does not have to be a Shabbos.

    israel : bool, optional
      ``True`` if you want the parsha according to the Israel schedule
      (with only one day of Yom Tov). Default is ``False``.

    hebrew : bool, optional
      ``True`` if you want the name of the parsha in Hebrew.
      Default is ``False``.

    Returns
    -------
    str or None
      The name of the parsha separated by a comma and space if it is a
      double parsha or ``None`` if there is no parsha that Shabbos
      (ie. it's yom tov).
    """
    parsha = getparsha(date, israel)
    if parsha is None:
        return None
    if not hebrew:
        name = [PARSHIOS[n] for n in parsha]
    else:
        name = [PARSHIOS_HEBREW[n] for n in parsha]
    return ', '.join(name)


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
    :obj:`list` of :obj:`int` or :obj:`None`
      A list of the numbers of the parshios for the next Shabbos in the
      given year. Yields ``None`` for a Shabbos that doesn't have its
      own parsha (i.e. it occurs on a yom tov).
    """
    table = _gentable(year, israel)
    for shabbos in table.values():
        yield shabbos


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
    ~collections.OrderedDict
      An ordered dictionary with the ``HebrewDate`` of each Shabbos
      as the key mapped to the parsha as a list of ints, or ``None`` for a
      Shabbos with no parsha.
    """
    return _gentable(year, israel)


def _get_hachodesh(date):
    """Return Hachodesh given Hebrew date."""
    year = date.year
    shabbos = date.shabbos()
    rc_nissan = HebrewDate(year, 1, 1)
    if shabbos <= rc_nissan and shabbos - rc_nissan < 7:
        return _FourParshiosEnum.HACHODESH
    return None


def _get_four_parshios(date):
    """Return the special parsha given Hebrew date."""
    year = date.year
    adar = 12
    if _is_leap(year):
        adar = 13
    shabbos = date.shabbos()
    rc_adar = HebrewDate(year, adar, 1)
    if shabbos <= rc_adar and rc_adar - shabbos < 7:
        return _FourParshiosEnum.SHEKALIM
    if shabbos.month == adar:
        purim = HebrewDate(year, adar, 14)
        if shabbos < purim and (purim - shabbos) < 7:
            return _FourParshiosEnum.ZACHOR
        if _get_hachodesh(date + 7):
            return _FourParshiosEnum.PARAH
    if _get_hachodesh(date):
        return _FourParshiosEnum.HACHODESH
    return None


def four_parshios(date, hebrew=False):
    """Return which of the four parshios is given date's Shabbos.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
      Any subclass of ``BaseDate``. This date does not have to be a Shabbos.

    hebrew : bool
      ``True`` if you want the name of the parsha in Hebrew.
      Default is ``False``.

    Returns
    -------
    str
      The name of the one of the four parshios or an empty string
      if that shabbos is not one of them.
    """
    date = date.to_heb()
    special_parsha = _get_four_parshios(date)
    if special_parsha is None:
        return ''
    if hebrew:
        return _FOUR_PARSHIOS_HEBREW[special_parsha]
    return _FOUR_PARSHIOS[special_parsha]
