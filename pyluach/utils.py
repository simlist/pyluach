"""The utils module contains functions to be shared between modules.

They are to be used internally.
"""
from functools import lru_cache


MONTH_NAMES = [
    'Nissan', 'Iyar', 'Sivan', 'Tammuz', 'Av', 'Elul', 'Tishrei', 'Cheshvan',
    'Kislev', 'Teves', 'Shevat', 'Adar', 'Adar 1', 'Adar 2']

MONTH_NAMES_HEBREW = [
    'ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול', 'תשרי', 'חשון', 'כסלו',
    'טבת', 'שבט', 'אדר', 'אדר א׳', 'אדר ב׳']

FAST_DAYS = [
    'Tzom Gedalia', '10 of Teves', 'Taanis Esther', '17 of Tamuz', '9 of Av']

FAST_DAYS_HEBREW = [
    'צום גדליה', 'י׳ בטבת', 'תענית אסתר', 'י״ז בתמוז', 'ט׳ באב']

FESTIVALS = [
    'Rosh Hashana', 'Yom Kippur', 'Succos', 'Shmini Atzeres', 'Simchas Torah',
    'Chanuka', "Tu B'shvat", 'Purim Katan', 'Purim', 'Shushan Purim',
    'Pesach', 'Pesach Sheni', "Lag Ba'omer", 'Shavuos', "Tu B'av"]

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


def _month_name(year, month, hebrew):
    index = month
    if month < 12 or not _is_leap(year):
        index -= 1
    if hebrew:
        return MONTH_NAMES_HEBREW[index]
    return MONTH_NAMES[index]


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
            return 0
    elif month == 10 and day == 10:
        return 1
    elif month == adar:
        if (weekday == 5 and day == 11) or weekday != 7 and day == 13:
            return 2
    elif month == 4:
        if (weekday == 1 and day == 18) or (weekday != 7 and day == 17):
            return 3
    elif month == 5:
        if (weekday == 1 and day == 10) or (weekday != 7 and day == 9):
            return 4
    return None


def _fast_day_string(date, hebrew=False):
    fast = _fast_day(date)
    if fast is None:
        return None
    if hebrew:
        return FAST_DAYS_HEBREW[fast]
    return FAST_DAYS[fast]


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
            return 0
        if day == 10:
            return 1
        if (
            not include_working_days
            and (day in range(17, 22) or (israel and day == 16))
        ):
            return None
        if day in range(15, 22):
            return 2
        if day == 22:
            return 3
        if day == 23 and not israel:
            return 4
    elif month in [9, 10] and include_working_days:
        kislev_length = _month_length(year, 9)
        if (
            month == 9 and day in range(25, kislev_length + 1)
            or month == 10 and day in range(1, 8 - (kislev_length - 25))
        ):
            return 5
    elif month == 11 and day == 15 and include_working_days:
        return 6
    elif month == 12 and include_working_days:
        leap = _is_leap(year)
        if day == 14:
            return 7 if leap else 8
        if day == 15 and not leap:
            return 9
    elif month == 13 and include_working_days:
        if day == 14:
            return 8
        if day == 15:
            return 9
    elif month == 1:
        if (
            not include_working_days
            and (day in range(17, 21) or (israel and day == 16))
        ):
            return None
        if day in range(15, 22 if israel else 23):
            return 10
    elif month == 2 and day == 14 and include_working_days:
        return 11
    elif month == 2 and day == 18 and include_working_days:
        return 12
    elif month == 3 and (day == 6 or (not israel and day == 7)):
        return 13
    elif month == 5 and day == 15 and include_working_days:
        return 14
    return None


def _festival_string(
        date, israel=False, hebrew=False, include_working_days=True):
    festival = _festival(date, israel, include_working_days)
    if festival is None:
        return None
    if hebrew:
        return FESTIVALS_HEBREW[festival]
    return FESTIVALS[festival]


def _holiday(date, israel=False, hebrew=False):
    """Return Jewish holiday of given date.

    The holidays include the major and minor religious Jewish
    holidays including fast days.

    Parameters
    ----------
    date : ``HebrewDate``, ``GregorianDate``, or ``JulianDay``
      Any date that implements a ``to_heb()`` method which returns a
      ``HebrewDate`` can be used.

    israel : bool, optional
      ``True`` if you want the holidays according to the israel
      schedule. Defaults to ``False``.

    hebrew : bool, optional
    ``True`` if you want the holiday name in Hebrew letters. Default is
    ``False``.

    Returns
    -------
    str or ``None``
      The name of the holiday or ``None`` if the given date is not
      a Jewish holiday.
    """
    festival = _festival_string(date, israel, hebrew)
    if festival is not None:
        return festival
    fast = _fast_day_string(date, hebrew)
    return fast
