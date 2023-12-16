"""The utils module contains shared functions and constants.

They are to be used internally.
"""
from functools import lru_cache
from enum import Enum


class Transliteration(Enum):
    ASHKENAZ = "Ashkenaz"
    MIXED_ISRAELI = "Mixed Israeli"
    MODERN_ISRAELI = "Modern Israeli"

class _Days(Enum):
    ROSH_HASHANA = 'Rosh Hashana'
    YOM_KIPPUR = 'Yom Kippur'
    SUCCOS = 'Succos'
    SHMINI_ATZERES = 'Shmini Atzeres'
    SIMCHAS_TORAH = 'Simchas Torah'
    CHANUKA = 'Chanuka'
    TU_BSHVAT = "Tu B'shvat"
    PURIM_KATAN = 'Purim Katan'
    PURIM = 'Purim'
    SHUSHAN_PURIM = 'Shushan Purim'
    PESACH = 'Pesach'
    PESACH_SHENI = 'Pesach Sheni'
    LAG_BAOMER = "Lag Ba'omer"
    SHAVUOS = 'Shavuos'
    TU_BAV = "Tu B'av"
    TZOM_GEDALIA = 'Tzom Gedalia'
    TENTH_OF_TEVES = '10 of Teves'
    TAANIS_ESTHER = 'Taanis Esther'
    SEVENTEENTH_OF_TAMUZ = '17 of Tamuz'
    NINTH_OF_AV = '9 of Av'


_days_hebrew = {
    _Days.ROSH_HASHANA: 'ראש השנה',
    _Days.YOM_KIPPUR: 'יום כיפור',
    _Days.SUCCOS: 'סוכות',
    _Days.SHMINI_ATZERES: 'שמיני עצרת',
    _Days.SIMCHAS_TORAH: 'שמחת תורה',
    _Days.CHANUKA: 'חנוכה',
    _Days.TU_BSHVAT: 'ט״ו בשבט',
    _Days.PURIM_KATAN: 'פורים קטן',
    _Days.PURIM: 'פורים',
    _Days.SHUSHAN_PURIM: 'שושן פורים',
    _Days.PESACH: 'פסח',
    _Days.PESACH_SHENI: 'פסח שני',
    _Days.LAG_BAOMER: 'ל״ג בעומר',
    _Days.SHAVUOS: 'שבועות',
    _Days.TU_BAV: 'ט״ו באב',
    _Days.TZOM_GEDALIA: 'צום גדליה',
    _Days.TENTH_OF_TEVES: 'י׳ בטבת',
    _Days.TAANIS_ESTHER: 'תענית אסתר',
    _Days.SEVENTEENTH_OF_TAMUZ: 'י״ז בתמוז',
    _Days.NINTH_OF_AV: 'ט׳ באב'
}

_days_israeli_en = {k:k.value for k in _Days}
_days_israeli_en.update({
    _Days.SUCCOS: 'Sukkot',
    _Days.SHMINI_ATZERES: 'Shmini Atzeret',
    _Days.SIMCHAS_TORAH: 'Simchat Torah',
    _Days.SHAVUOS: 'Shavuot',
    _Days.TENTH_OF_TEVES: '10th of Tevet',
    _Days.TAANIS_ESTHER: "Ta'anit Esther",
})

MONTH_NAMES = [
    'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul', 'Tishrei', 'Cheshvan',
    'Kislev', 'Teves', 'Shevat', 'Adar', 'Adar 1', 'Adar 2']

MONTH_NAMES_ISRAELI_EN = [
    'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul', 'Tishrei', 'Cheshvan',
    'Kislev', 'Tevet', 'Shvat', 'Adar', 'Adar 1', 'Adar 2']

MONTH_NAMES_HEBREW = [
    'ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול', 'תשרי', 'חשון', 'כסלו',
    'טבת', 'שבט', 'אדר', 'אדר א׳', 'אדר ב׳']

FAST_DAYS = [
    'Tzom Gedalia', '10 of Teves', 'Taanis Esther', '17 of Tamuz', '9 of Av']

FAST_DAYS_ISRAELI_EN = [
    'Tzom Gedalia', '10th of Tevet', 'Taanit Esther', '17 of Tamuz', '9 of Av']

FAST_DAYS_HEBREW = [
    'צום גדליה', 'י׳ בטבת', 'תענית אסתר', 'י״ז בתמוז', 'ט׳ באב']

FESTIVALS = [
    'Rosh Hashana', 'Yom Kippur', 'Succos', 'Shmini Atzeres', 'Simchas Torah',
    'Chanuka', "Tu B'shvat", 'Purim Katan', 'Purim', 'Shushan Purim',
    'Pesach', 'Pesach Sheni', "Lag Ba'omer", 'Shavuos', "Tu B'av"]

FESTIVALS_ISRAELI_EN = [
    'Rosh Hashana', 'Yom Kippur', 'Sukkot', 'Shmini Atzeret', 'Simchat Torah',
    'Chanuka', "Tu B'shvat", 'Purim Katan', 'Purim', 'Shushan Purim',
    'Pesach', 'Pesach Sheni', "Lag Ba'omer", 'Shavuot', "Tu B'av"]

FESTIVALS_HEBREW = [
    'ראש השנה', 'יום כיפור', 'סוכות', 'שמיני עצרת', 'שמחת תורה', 'חנוכה',
    'ט״ו בשבט', 'פורים קטן', 'פורים', 'שושן פורים', 'פסח', 'פסח שני',
    'ל״ג בעומר', 'שבועות', 'ט״ו באב'
]


WEEKDAYS = {
    1: 'ראשון',
    2: 'שני',
    3: 'שלישי',
    4: 'רביעי',
    5: 'חמישי',
    6: 'שישי',
    7: 'שבת'
}


def _is_leap(year):
    if (((7*year) + 1) % 19) < 7:
        return True
    return False


def _elapsed_months(year):
    return (235 * year - 234) // 19


@lru_cache(maxsize=10)
def _elapsed_days(year):
    months_elapsed = _elapsed_months(year)
    parts_elapsed = 204 + 793*(months_elapsed%1080)
    hours_elapsed = (
        5 + 12*months_elapsed + 793*(months_elapsed//1080)
        + parts_elapsed//1080)
    conjunction_day = 1 + 29*months_elapsed + hours_elapsed//24
    conjunction_parts = 1080 * (hours_elapsed%24) + parts_elapsed%1080

    if (
        (conjunction_parts >= 19440)
        or (
            (conjunction_day % 7 == 2) and (conjunction_parts >= 9924)
            and not _is_leap(year)
        )
        or (
            (conjunction_day % 7 == 1) and conjunction_parts >= 16789
            and _is_leap(year - 1)
        )
    ):
        alt_day = conjunction_day + 1
    else:
        alt_day = conjunction_day
    if alt_day % 7 in [0, 3, 5]:
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
    """Months start with Nissan (Nissan is 1 and Tishrei is 7)"""
    if month in [1, 3, 5, 7, 11]:
        return 30
    if month in [2, 4, 6, 10, 13]:
        return 29
    if month == 12:
        if _is_leap(year):
            return 30
        return 29
    if month == 8:   # if long Cheshvan return 30, else return 29
        if _long_cheshvan(year):
            return 30
        return 29
    if month == 9:   # if short Kislev return 29, else return 30
        if _short_kislev(year):
            return 29
        return 30
    raise ValueError('Invalid month')


def _month_name(year, month, hebrew, transliteration=Transliteration.ASHKENAZ):
    index = month
    if month < 12 or not _is_leap(year):
        index -= 1
    if hebrew:
        return MONTH_NAMES_HEBREW[index]
    return MONTH_NAMES[index] if transliteration==Transliteration.ASHKENAZ else MONTH_NAMES_ISRAELI_EN[index]

def _monthslist(year):
    months = [7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4, 5, 6]
    if not _is_leap(year):
        months.remove(13)
    return months


def _add_months(year, month, num):
    monthslist = _monthslist(year)
    index = monthslist.index(month)
    months_remaining = len(monthslist[index+1:])
    if num <= months_remaining:
        return (year, monthslist[index + num])
    return _add_months(year + 1, 7, num - months_remaining - 1)


def _subtract_months(year, month, num):
    monthslist = _monthslist(year)
    index = monthslist.index(month)
    if num <= index:
        return (year, monthslist[index - num])
    return _subtract_months(year - 1, 6, num - (index+1))


def _fast_day(date):
    """Return name of fast day or None.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    Returns
    -------
    str or ``None``
      The name of the fast day or ``None`` if the given date is not
      a fast day.
    """
    date = date.to_heb()
    year = date.year
    month = date.month
    day = date.day
    weekday = date.weekday()
    adar = 13 if _is_leap(year) else 12

    if month == 7:
        if (weekday == 1 and day == 4) or (weekday != 7 and day == 3):
            return _Days.TZOM_GEDALIA
    elif month == 10 and day == 10:
        return _Days.TENTH_OF_TEVES
    elif month == adar:
        if (weekday == 5 and day == 11) or weekday != 7 and day == 13:
            return _Days.TAANIS_ESTHER
    elif month == 4:
        if (weekday == 1 and day == 18) or (weekday != 7 and day == 17):
            return _Days.SEVENTEENTH_OF_TAMUZ
    elif month == 5:
        if (weekday == 1 and day == 10) or (weekday != 7 and day == 9):
            return _Days.NINTH_OF_AV
    return None


def _fast_day_string(date, hebrew=False, transliteration=Transliteration.ASHKENAZ):
    fast = _fast_day(date)
    if fast is None:
        return None
    if hebrew:
        return _days_hebrew[fast]
    return fast.value if transliteration==Transliteration.ASHKENAZ else _days_israeli_en[fast]


def _first_day_of_holiday(holiday):
    if holiday is _Days.ROSH_HASHANA:
        return (7, 1)
    if holiday is _Days.SUCCOS:
        return (7, 15)
    if holiday is _Days.CHANUKA:
        return (9, 25)
    if holiday is _Days.PESACH:
        return (1, 15)
    if holiday is _Days.SHAVUOS:
        return (3, 6)
    return None


def _festival(date, israel=False, include_working_days=True):
    """Return Jewish festival of given day.

    This method will return all major and minor religous
    Jewish holidays not including fast days.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    israel : bool, optional
      ``True`` if you want the holidays according to the Israel
      schedule. Defaults to ``False``.

    include_working_days : bool, optional
      ``True`` to include festival days in which melacha (work) is
      allowed; ie. Pesach Sheni, Chol Hamoed, etc.
      Default is ``True``.

    Returns
    -------
    str or ``None``
      The festival or ``None`` if the given date is not a Jewish
      festival.
    """
    date = date.to_heb()
    year = date.year
    month = date.month
    day = date.day
    if month == 7:
        if day in [1, 2]:
            return _Days.ROSH_HASHANA
        if day == 10:
            return _Days.YOM_KIPPUR
        if (
            not include_working_days
            and (day in range(17, 22) or (israel and day == 16))
        ):
            return None
        if day in range(15, 22):
            return _Days.SUCCOS
        if day == 22:
            return _Days.SHMINI_ATZERES
        if day == 23 and not israel:
            return _Days.SIMCHAS_TORAH
    elif month in [9, 10] and include_working_days:
        kislev_length = _month_length(year, 9)
        if (
            month == 9 and day in range(25, kislev_length + 1)
            or month == 10 and day in range(1, 8 - (kislev_length - 25))
        ):
            return _Days.CHANUKA
    elif month == 11 and day == 15 and include_working_days:
        return _Days.TU_BSHVAT
    elif month == 12 and include_working_days:
        leap = _is_leap(year)
        if day == 14:
            return _Days.PURIM_KATAN if leap else _Days.PURIM
        if day == 15 and not leap:
            return _Days.SHUSHAN_PURIM
    elif month == 13 and include_working_days:
        if day == 14:
            return _Days.PURIM
        if day == 15:
            return _Days.SHUSHAN_PURIM
    elif month == 1:
        if (
            not include_working_days
            and (day in range(17, 21) or (israel and day == 16))
        ):
            return None
        if day in range(15, 22 if israel else 23):
            return _Days.PESACH
    elif month == 2 and day == 14 and include_working_days:
        return _Days.PESACH_SHENI
    elif month == 2 and day == 18 and include_working_days:
        return _Days.LAG_BAOMER
    elif month == 3 and (day == 6 or (not israel and day == 7)):
        return _Days.SHAVUOS
    elif month == 5 and day == 15 and include_working_days:
        return _Days.TU_BAV
    return None


def _festival_string(
    date,
    israel=False,
    hebrew=False,
    include_working_days=True,
    transliteration=Transliteration.ASHKENAZ
):
    festival = _festival(date, israel, include_working_days)
    if festival is None:
        return None
    if hebrew:
        return _days_hebrew[festival]
    return festival.value if transliteration==Transliteration.ASHKENAZ else _days_israeli_en[festival]
