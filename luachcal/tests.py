#!usr/bin/env python

import unittest

import dates

KNOWN_VALUES = {(2009, 8, 21): (5769, 6, 1),
                (2009, 9, 30): (5770, 7, 12),
                (2009, 11, 13): (5770, 8, 26),
                (2010, 1, 21): (5770, 11, 6),
                (2010, 5, 26): (5770, 3, 13),
                (2013, 11, 17): (5774, 9, 14),
                (2014, 3, 12): (5774, 13, 10),
                (2014, 6, 10): (5774, 3, 12)
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
            

caltype = (dates.GregorianDate, dates.HebrewDate, dates.JulianDay)

class OperatorsTest(unittest.TestCase):
    
    def test_add(self):
        for cal in caltype:
            for delta in [0, 1, 29, 73, 1004]:
                date = cal.today()
                date2 = date + delta
                self.assertEqual(date.jd + delta, date2.jd)
        
    def test_min_int(self):
        '''Test subtracting a number from a date'''
        for cal in caltype:
            for delta in [0, 1, 29, 73, 1004]:
                date = cal.today()
                date2 = date - delta
                self.assertEqual(date.jd - delta, date2.jd)
            
    def test_min_delta(self):
        '''Test subtracting one date from another'''
        for cal in caltype:
            for i in [0, 1, 17, 219, 366, 1508]:
                today = cal.today()
                delta = (today-i) - today
                self.assertEqual(delta, i)
            

class OperatorTests(unittest.TestCase):
    
    def test_gt(self):
        for cal in caltype:
            today = cal.today()
            result = today > today-1
            self.assertTrue(result,
                            '{0} is not greater than{1}'.format(
                                                            today,today - 1))
            self. assertTrue(today >= today-1)
            self.assertFalse(today == today-1)
            self.assertFalse(today < today-1)
            self.assertFalse(today <= today-1)
            
    def test_lt(self):
        for cal in caltype:
            today = cal.today()
            self.assertLess(today, today+1)
            self.assertLessEqual(today, today + 1)
            for operator in [today.__gt__, today.__ge__, today.__eq__]:
                self.assertFalse(operator(today + 1))            
    
    def test_eq(self):
        for cal in caltype:
            today = cal.today()
            for operator in [today.__eq__, today.__ge__, today.__le__]:
                self.assertTrue(operator(today))
            for operator in [today.__gt__, today.__lt__]:
                self.assertFalse(operator(today) or operator(today))
                

   
if __name__ == '__main__':
    unittest.main()