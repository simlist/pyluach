import pytest

from pyluach import parshios, dates


KNOWN_VALUES = {
    (2016, 1, 7): [13,],
    (2017, 3, 21): [21, 22],
    (2017, 9, 26): None
    }

KNOWN_VALUES_STRINGS = {
    (2016, 1, 7): "Va'era",
    (2017, 3, 21): "Vayakhel, Pekudei",
    (2017, 9, 26): None
    }


class TestGetParsha(object):

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
        assert parshios.getparsha_string(shavuos, True) == 'Naso'
        assert parshios.getparsha_string(shavuos) is None
        assert parshios. getparsha_string(shavuos + 7, True) == "Beha'aloscha"
        assert parshios.getparsha_string(shavuos + 7) == 'Naso'


def test_parshatable():
    assert parshios.parshatable(5777) == parshios._gentable(5777)
    assert parshios.parshatable(5778, True) == parshios._gentable(5778, True)
