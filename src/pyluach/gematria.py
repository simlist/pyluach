"""Gematria conversion — Hebrew numerals from integers.

This module provides functions to convert integers into their Hebrew
letter (gematria) representation, with optional geresh/gershayim
punctuation and thousands-place notation.
"""

# Mapping of integer values to their single Hebrew letter equivalents.
# Covers the 22 standard gematria values from 1 to 400.
_GEMATRIOS = {
    1: 'א', 2: 'ב', 3: 'ג', 4: 'ד', 5: 'ה',
    6: 'ו', 7: 'ז', 8: 'ח', 9: 'ט', 10: 'י',
    20: 'כ', 30: 'ל', 40: 'מ', 50: 'נ', 60: 'ס',
    70: 'ע', 80: 'פ', 90: 'צ', 100: 'ק', 200: 'ר',
    300: 'ש', 400: 'ת',
}

# Special substitutions: 15 and 16 are written as טו and טז
# (not יה and יו) to avoid writing the names of God.
_SPECIAL_REPLACEMENTS = {'יה': 'טו', 'יו': 'טז'}

_GERESH = '׳'
_GERSHAYIM = '״'
_TAV = 'ת'


def _apply_special_replacements(letters):
    """Apply traditional gematria substitutions to avoid divine names."""
    for original, replacement in _SPECIAL_REPLACEMENTS.items():
        letters = letters.replace(original, replacement)
    return letters


def _stringify_gematria(letters):
    """Insert geresh or gershayim symbols into gematria.

    Parameters
    ----------
    letters : str
        A string of Hebrew letters representing a gematria value.

    Returns
    -------
    str
        The input with gershayim (״) inserted before the last character
        for multi-character strings, or geresh (׳) appended for single
        characters. Returns an empty string for empty input.
    """
    if not letters:
        return ''
    if len(letters) == 1:
        return f'{letters}{_GERESH}'
    return f'{letters[:-1]}{_GERSHAYIM}{letters[-1]}'


def _get_letters(num):
    """Convert numbers under 1,000 into raw Hebrew letters.

    Breaks the number into hundreds, tens, and ones place values,
    then maps each to its corresponding Hebrew letter. Values
    of 400 or more in the hundreds place are represented using
    repeated ת characters (e.g., 500 = תק, 900 = תתק).

    Parameters
    ----------
    num : int
        A non-negative integer less than 1000.

    Returns
    -------
    str
        The Hebrew letter representation with special substitutions
        applied (טו for 15, טז for 16).
    """
    ones_digit = num % 10
    tens_digit = (num % 100) - ones_digit
    hundreds_raw = (num % 1000) - tens_digit - ones_digit

    # Hundreds >= 400 are represented as repeated ת (400) + remainder
    tav_count = hundreds_raw // 400
    hundreds_remainder = hundreds_raw % 400

    ones_letter = _GEMATRIOS.get(ones_digit, '')
    tens_letter = _GEMATRIOS.get(tens_digit, '')
    hundreds_letter = _GEMATRIOS.get(hundreds_remainder, '')
    tav_prefix = _TAV * tav_count

    raw_letters = f'{tav_prefix}{hundreds_letter}{tens_letter}{ones_letter}'
    return _apply_special_replacements(raw_letters)


def _num_to_str(num, thousands=False, withgershayim=True):
    """Return gematria string for number.

    Parameters
    ----------
    num : int
        The number to get the Hebrew letter representation
    thousands : bool, optional
        True if the hebrew returned should include a letter for the
        thousands place ie. 'ה׳' for five thousand.
    withgershayim : bool, optional
        True to include geresh/gershayim punctuation marks.
        Default is True.

    Returns
    -------
    str
        The Hebrew representation of the number.
    """
    letters = _get_letters(num)
    if withgershayim:
        letters = _stringify_gematria(letters)
    if thousands:
        thousand_letters = _get_letters(num // 1000)
        if withgershayim:
            thousand_letters = f'{thousand_letters}{_GERESH}'
        letters = f'{thousand_letters}{letters}'
    return letters
