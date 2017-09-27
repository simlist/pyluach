pyluach
========
.. image:: https://readthedocs.org/projects/pyluach/badge/?version=latest
:target: http://pyluach.readthedocs.io/en/latest/?badge=latest
:alt: Documentation Status

Pyluach is a Python package for manipulating Hebrew calendar dates and 
Hebrew-Gregorian conversions.

Features
---------
* Conversion between Hebrew and Gregorian dates
* Finding the difference between two dates
* Finding a date at a given duration from the given date
* Rich comparisons between dates
* Finding the weekday of a given date
* Finding the weekly Parsha reading of a given date

Installation
-------------
Use ``pip install pyluach``.

Typical use
------------
::

    from pyluach import dates, hebrewcal
    
    >>> today = dates.HebrewDate.today()
    >>> lastweek_gregorian = (today - 7).to_greg()
    >>> lastweek_gregorian < today
	True
    >>> today - lastweek_gregorian
	7
    >>> greg = GregorianDate(1986, 3, 21)
    >>> heb = HebrewDate(5746, 13, 10)
    >>> greg == heb
	True
    
    >>> for month in hebrewcal.Year(5774).itermonths():
    ...     print month.name
	Tishrei Cheshvan ...

Documentation
-------------
Documentation for pyluach can be found at https://readthedocs.org/projects/pyluach/.

Contact
--------
For questions and comments feel free to contact me at simlist@gmail.com.

License
--------
Pyluach is licensed under the MIT license.

