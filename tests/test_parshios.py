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


def test_parshatable():
    assert parshios.parshatable(5777) == parshios._gentable(5777)
    assert parshios.parshatable(5778, True) == parshios._gentable(5778, True)
