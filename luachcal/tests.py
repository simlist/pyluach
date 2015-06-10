#!usr/bin/env python

import unittest
from operator import gt, lt, eq, ne, ge, le

from luachcal import dates


KNOWN_VALUES = {(2009, 8, 21): (5769, 6, 1),
                (2009, 9, 30): (5770, 7, 12),
                (2009, 11, 13): (5770, 8, 26),
                (2010, 1, 21): (5770, 11, 6),
                (2010, 5, 26): (5770, 3, 13),
                (2013, 11, 17): (5774, 9, 14),
                (2014, 3, 12): (5774, 13, 10),
                (2014, 6, 10): (5774, 3, 12),
                (2016, 2, 10): (5776, 12, 1)
                }
        
            
class ClassesSanityTest(unittest.TestCase):
    def test_greg_sanity(self):
        for i in xrange(347998,2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_greg().to_jd()
            self.assertEqual(jd.day,
                             conf.day,
                             'jd={0},conv={1}'.format(jd.day,conf.day)
                             )
            
    def test_heb_sanity(self):
        for i in xrange(347998, 2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_heb().to_jd()
            self.assertEqual(jd.day, conf.day, 'jd={0}, conf={1}'.format(jd,conf))
            
            
class ClassesConversionTest(unittest.TestCase):
    def test_from_greg(self):
        for date in KNOWN_VALUES:
            heb = dates.GregorianDate(*date).to_heb().tuple()
            self.assertEqual(KNOWN_VALUES[date], heb)
            
    def test_from_heb(self):
        for date in KNOWN_VALUES:
            greg = dates.HebrewDate(*KNOWN_VALUES[date]).to_greg().tuple()
            self.assertEqual(date, greg)
            

class OperatorsTest(unittest.TestCase):
    
    def setUp(self):
        self.caltypes = [dates.GregorianDate, dates.HebrewDate, dates.JulianDay]
        self.deltas = [0, 1, 29, 73, 1004]

    def test_add(self):
        for cal in self.caltypes:
            for delta in self.deltas:
                date = cal.today()
                date2 = date + delta
                self.assertEqual(date.jd + delta, date2.jd)
        
    def test_min_int(self):
        '''Test subtracting a number from a date'''
        for cal in self.caltypes:
            for delta in self.deltas:
                date = cal.today()
                date2 = date - delta
                self.assertEqual(date.jd - delta, date2.jd)
             
    def test_min_date(self):
        '''Test subtracting one date from another
        
        This test loops through subtracting the current date of each
        calendar from a date of each calendar at intervals from the
        current date.   
        '''
        for cal in self.caltypes:
            for cal2 in self.caltypes:  
                for delta in self.deltas:
                    today = cal.today()
                    difference = (cal2.today() - delta) - today
                    self.assertEqual(delta, difference)
             
 
class ComparisonTests(unittest.TestCase):
    """In ComparisonTests, comparisons are tested.
    
    Every function tests one test case comparing a date from each
    calendar type to another date from each calendar type.
    """
    
    def setUp(self):
        self.caltypes = [dates.GregorianDate, dates.HebrewDate, dates.JulianDay]
    
    def test_gt(self):
        """Test all comparers when one date is greater."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                yesterday = cal2.today() - 1
                for comp in [gt, ge, ne]:
                    self.assertTrue(comp(today, yesterday))
                for comp in [eq, lt, le]:
                    self.assertFalse(comp(today, yesterday))
             
    def test_lt(self):
        """Test all comparers when one date is less than another."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                tomorrow = cal2.today() + 1
                for comp in [lt, le, ne]:
                    self.assertTrue(comp(today, tomorrow))
                for comp in [gt, ge, eq]:
                    self.assertFalse(comp(today, tomorrow))    
     
    def test_eq(self):
        """Test all comparers when the dates are equal."""
        for cal in self.caltypes:
            today = cal.today()
            for cal2 in self.caltypes:
                today2 = cal2.today()
                for comp in [eq, ge, le]:
                    self.assertTrue(comp(today, today2))
                for comp in [gt, lt, ne]:
                    self.assertFalse(comp(today, today2))
                    
                    
class TestErrors(unittest.TestCase):
    
    def test_too_low_heb(self):
        self.assertRaises(ValueError, dates.HebrewDate, 0, 7, 1)
        self.assertRaises(ValueError, dates.HebrewDate, -1, 7, 1)

 
if __name__ == '__main__':
    unittest.main()
