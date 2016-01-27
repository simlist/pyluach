import unittest

from pyluach import parshios, dates

KNOWN_VALUES = {
    (2016, 1, 7): 13,
    (2017, 3, 21): [21, 22]
    }

class TestGetParsha(unittest.TestCase):
    
    def test_getparsha(self):
        for key in KNOWN_VALUES:
            self.assertEqual(parshios.getparsha(dates.GregorianDate(*key)),
                             KNOWN_VALUES[key])

if __name__ == '__main__':
    unittest.main()
