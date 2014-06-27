luachcal
============================

Luachcal is a Python package for manipulating Hebrew calendar dates and 
Hebrew-Gregorian conversions.

Features
---------------
* Conversion between Hebrew and Gregorian dates
* Finding the difference between two dates
* Finding a date at a given duration from the given date
* Rich comparisons between dates
* Finding the weekday of a given date

Installation
---------------------
Still under developement. When completed use ``pip install luachcal``

Typical use
--------------------
::

    from luachcal import dates, hebrewcal
    
    today = dates.HebrewDate.today()
    lastweek_gregorian = (today - 7).to_greg()
    lastweek_gregorian < today   # True
    today - lastweek_gregorian  # 7
    greg = GregorianDate(1986, 3, 21)
    heb = HebrewDate(5746, 13, 10)
    greg == heb  # True
    
    for months in hebrewcal.Year(5774):
        print month.name  # 'Tishrei' 'Cheshvan' ...

Contact
----------------
For questions and comments feel free to contact me at simlist@gmail.com.

License
--------------
Luachcal is licensed under the MIT license.

