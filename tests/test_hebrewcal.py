import unittest

from pyluach import dates, hebrewcal

class TestMonth(unittest.TestCase):
    def test_subtract_month(self):
        month1 = hebrewcal.Month(5775, 10)
        month2 = hebrewcal.Month(5776, 10)
        month3 = hebrewcal.Month(5777, 10)
        self.assertEqual(month1 - month2, 12)
        self.assertEqual(month3 - month1, 25)

if __name__ == '__main__':
    unittest.main()
