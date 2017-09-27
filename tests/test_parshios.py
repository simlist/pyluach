import pytest

from pyluach import parshios, dates


KNOWN_VALUES = {
    (2016, 1, 7): [13,],
    (2017, 3, 21): [21, 22]
    }

KNOWN_VALUES_STRINGS = {
    (2016, 1, 7): "Va'era",
    (2017, 3, 21): "Vayakhel, Pekudei"
    }

class TestGetParsha(object):

    def test_getparsha(self):
        for key in KNOWN_VALUES:
            assert (parshios.getparsha(dates.GregorianDate(*key)) ==
                    KNOWN_VALUES[key])
    
    def test_getparsha_string(self):
        for key in KNOWN_VALUES_STRINGS:
            assert parshios.getparsha_string(dates.GregorianDate(*key)) == KNOWN_VALUES_STRINGS[key]