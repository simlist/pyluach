GEMATRIOS = {
    1: 'א',
    2: 'ב',
    3: 'ג',
    4: 'ד',
    5: 'ה',
    6: 'ו',
    7: 'ז',
    8: 'ח',
    9: 'ט',
    10: 'י',
    20: 'כ',
    30: 'ל',
    40: 'מ',
    50: 'נ',
    60: 'ס',
    70: 'ע',
    80: 'פ',
    90: 'צ',
    100: 'ק',
    200: 'ר',
    300: 'ש',
    400: 'ת'
}

def stringify_gematria(letters):
    length = len(letters)
    if length > 1:
        return '{}״{}'.format(letters[:-1], letters[-1])
    if length == 1:
        return '{}׳'.format(letters, '׳')
    return ''

def num_to_str(num, thousands=False):
    """Return gematria string for number up to 10,000.
    
    Parameters
    ----------
    num : int
        The number to get the Hebrew letter representation
    thousands : bool, optional
        True if the hebrew returned should include a letter for the
        thousands place ie. 'ה׳' for five thousand.
    
    Returns
    -------
    str
        The Hebrew representation of the number.
    """
    ones = num % 10
    tens = num % 100 - ones
    hundreds = num % 1000 - tens - ones
    four_hundreds = ''.join(['ת' for i in range(hundreds // 400)])
    ones = GEMATRIOS.get(ones, '')
    tens = GEMATRIOS.get(tens, '')
    hundreds = GEMATRIOS.get(hundreds % 400, '')
    letters = '{}{}{}{}'.format(four_hundreds, hundreds, tens, ones)
    letters = letters.replace('יה', 'טו').replace('יו', 'טז')
    letters = stringify_gematria(letters)
    if thousands:
        thousand = stringify_gematria(GEMATRIOS.get(num // 1000, ''))
        letters = thousand + letters
    return letters