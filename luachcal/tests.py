#!usr/bin/env python

import unittest
import time_conversion
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

class SanityCheck(unittest.TestCase):
    
    def test_sanity_heb(self):
        for i in xrange(347998, 2460000, 117):
            heb = time_conversion.jd_to_heb(i)
            jd = time_conversion.heb_to_jd(*heb)
            self.assertEqual(i, jd,'i = {0}, jd = {1}'.format(i, jd))
            
    def test_jdtogreg(self):
        jd = time_conversion.jd_to_greg(2451964.5)
        self.assertEqual(jd, (2001, 2, 24), 'jd = {0}'.format(jd))
        
    def test_gregtojd(self):
        greg = (2014, 6, 3)
        jd = time_conversion.greg_to_jd(*greg)
        self.assertEqual(2456811.5, jd, 'jd = {0}'.format(jd))
    
    def test_sanity_greg(self):
        for i in xrange(347998, 2460000, 117):
            greg = time_conversion.jd_to_greg(i + .5)
            jd = time_conversion.greg_to_jd(*greg)
            self.assertEqual(i + .5, jd, 'i = {0}, jd = {1}'.format(i, jd))
            
            
class ClassesSanityTest(unittest.TestCase):
    def test_greg_sanity(self):
        for i in xrange(347998,2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_greg().to_jd()
            self.assertEqual(jd.day, conf.day, 'jd={0},conv={1}'.format(jd.day,conf.day))
            
    def test_heb_sanity(self):
        for i in xrange(347998, 2460000, 117):
            jd = dates.JulianDay(i)
            conf = jd.to_heb().to_jd()
            self.assertEqual(jd.day, conf.day, 'jd={0}, conf={1}'.format(jd,conf))
            
            
class ClassesConversionTest(unittest.TestCase):
    def test_from_greg(self):
        for date in KNOWN_VALUES:
            heb = dates.GregorianDate(*date).to_heb().to_tuple()
            self.assertEqual(KNOWN_VALUES[date], heb)
            
    def test_from_heb(self):
        for date in KNOWN_VALUES:
            greg = dates.HebrewDate(*KNOWN_VALUES[date]).to_greg().to_tuple()
            self.assertEqual(date, greg)
                              
   
if __name__ == '__main__':
    unittest.main()