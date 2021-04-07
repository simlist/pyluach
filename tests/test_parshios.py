import pytest

from pyluach import parshios, dates


KNOWN_VALUES = {
    (2016, 1, 7): [13,],
    (2017, 3, 21): [21, 22],
    (2017, 9, 26): None,
    (2020, 9, 19): None,
    }

KNOWN_VALUES_STRINGS = {
    (2016, 1, 7): "Va'eira",
    (2017, 3, 21): "Vayakhel, Pekudei",
    (2017, 9, 26): None
    }


class TestGetParsha:

    def test_getparsha(self):
        for key in KNOWN_VALUES:
            assert (parshios.getparsha(dates.GregorianDate(*key)) ==
                    KNOWN_VALUES[key])

    def test_getparsha_string(self):
        for key in KNOWN_VALUES_STRINGS:
            assert (parshios.getparsha_string(dates.GregorianDate(*key)) ==
                    KNOWN_VALUES_STRINGS[key])

    def test_chukas_balak(self):
        chukas_balak = dates.HebrewDate(5780, 4, 12)
        assert parshios.getparsha(chukas_balak) == [38, 39]
        assert parshios.getparsha(chukas_balak, True) == [39, ]
        assert parshios.getparsha(chukas_balak - 8) == [37, ]
        assert parshios.getparsha(chukas_balak - 13, True) == [38, ]
        shavuos = dates.HebrewDate(5780, 3, 6)
        assert parshios.getparsha_string(shavuos, True) == 'Nasso'
        assert parshios.getparsha_string(shavuos) is None
        assert parshios. getparsha_string(shavuos + 7, True) == "Beha'aloscha"
        assert parshios.getparsha_string(shavuos + 7) == 'Nasso'

    def test_eighth_day_pesach(self):
        eighth_day_pesach = dates.HebrewDate(5779, 1, 22)
        reunion_shabbos = dates.HebrewDate(5779, 5, 2)
        assert parshios.getparsha_string(eighth_day_pesach) is None
        assert parshios.getparsha_string(eighth_day_pesach, True) == 'Acharei Mos'
        assert parshios.getparsha(eighth_day_pesach + 7) == [28,]
        assert parshios.getparsha(eighth_day_pesach + 7, True) == [29,]
        assert parshios.getparsha_string(reunion_shabbos) == "Mattos, Masei"
        assert parshios.getparsha_string(reunion_shabbos, True) == 'Masei'


def test_parshatable():
    assert parshios.parshatable(5777) == parshios._gentable(5777)
    assert parshios.parshatable(5778, True) == parshios._gentable(5778, True)

def test_iterparshios():
    year = 5776
    parshalist = list(parshios.parshatable(year).values())
    index = 0
    for p in parshios.iterparshios(year):
        assert p == parshalist[index]
        index += 1
