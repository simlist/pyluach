from functools import lru_cache


MONTH_NAMES_HEBREW = [
    'ניסן', 'אייר', 'סיון', 'תמוז', 'אב', 'אלול', 'תשרי', 'חשון', 'כסלו',
    'טבת', 'שבט', 'אדר', 'אדר א׳', 'אדר ב׳'
]


FAST_DAYS = [
    'Tzom Gedalia', '10 of Teves', 'Taanis Esther', '17 of Tammuz', '9 of Av'
]

FAST_DAYS_HEBREW = [
    'צום גדליה', 'י׳ בטבת', 'תענית אסתר', 'י״ז בתמוז', 'ט׳ באב'
]

HOLIDAYS = [
    'Rosh Hashana', 'Yom Kippur', 'Succos', 'Shmini Atzeres', 'Simchas Torah',
    'Chanuka', "Tu B'shvat", 'Purim Katan', 'Purim', 'Shushan Purim',
    'Pesach', 'Pesach Sheni', "Lag Ba'omer", 'Shavuos', "Tu B'av"
]

def _is_leap(year):
    if (((7*year) + 1) % 19) < 7:
        return True
    return False


def _elapsed_months(year):
    return (235 * year - 234) // 19


@lru_cache(maxsize=100)
def _elapsed_days(year):
    months_elapsed = _elapsed_months(year)
    parts_elapsed = 204 + 793*(months_elapsed%1080)
    hours_elapsed = (5 + 12*months_elapsed + 793*(months_elapsed//1080) +
                        parts_elapsed//1080)
    conjunction_day = 1 + 29*months_elapsed + hours_elapsed//24
    conjunction_parts = 1080 * (hours_elapsed%24) + parts_elapsed%1080

    if (
            (conjunction_parts >= 19440) or
            (
            (conjunction_day % 7 == 2) and
            (conjunction_parts >= 9924) and
            (not _is_leap(year))
            ) or
            (
            (conjunction_day % 7 == 1) and
            conjunction_parts >= 16789 and _is_leap(year - 1))):
        # if all that
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
    """Months start with Nissan (Nissan is 1 and Tishrei is 7)"""

    if month in [1, 3, 5, 7, 11]:
        return 30
    elif month in [2, 4, 6, 10, 13]:
        return 29
    elif month == 12:
        return 30 if _is_leap(year) else 29
    elif month == 8:   # if long Cheshvan return 30, else return 29
        return 30 if _long_cheshvan(year) else 29
    elif month == 9:   # if short Kislev return 29, else return 30
        return 29 if _short_kislev(year) else 30


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
    adar = 13 if Year(year).leap else 12

    if month == 7:
        if (weekday == 1 and day == 4) or (weekday != 7 and day == 3):
            return 'Tzom Gedalia'
    elif month == 10 and day == 10:
        return '10 of Teves'
    elif month == adar:
        if (weekday == 5 and day == 11) or weekday != 7 and day == 13:
            return 'Taanis Esther'
    elif month == 4:
        if (weekday == 1 and day == 18) or (weekday != 7 and day == 17):
            return '17 of Tamuz'
    elif month == 5:
        if (weekday == 1 and day == 10) or (weekday != 7 and day == 9):
            return '9 of Av'


def _festival(date, israel=False):
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

    Returns
    -------
    str or ``None``
      The name of the festival or ``None`` if the given date is not
      a Jewish festival.
    """
    date = date.to_heb()
    year = date.year
    month = date.month
    day = date.day
    if month == 7:
        if day in [1, 2]:
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
    elif month == 2 and day == 14:
        return 'Pesach Sheni'
    elif month == 2 and day == 18:
        return "Lag Ba'omer"
    elif month == 3 and (day == 6 if israel else day in (6, 7)):
        return 'Shavuos'
    elif month == 5 and day == 15:
        return "Tu B'av"


def _holiday(date, israel=False):
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

    Returns
    -------
    str or ``None``
      The name of the holiday or ``None`` if the given date is not
      a Jewish holiday.
    """
    fest = _festival(date, israel)
    if fest:
        return fest
    fast = _fast_day(date)
    if fast:
        return fast