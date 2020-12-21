pyluach
========
.. image:: https://readthedocs.org/projects/pyluach/badge/?version=latest
  :target: http://pyluach.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://travis-ci.org/simlist/pyluach.svg?branch=master
    :target: https://travis-ci.org/simlist/pyluach
.. image:: https://coveralls.io/repos/github/simlist/pyluach/badge.svg?branch=master
    :target: https://coveralls.io/github/simlist/pyluach?branch=master

Pyluach is a Python package for manipulating Hebrew (Jewish) calendar dates and 
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

    >>> from pyluach import dates, hebrewcal, parshios
    
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
    >>> greg > heb - 1
    True

    >>> rosh_hashana = dates.HebrewDate(5782, 7, 1)
    >>> rosh_hashana.holiday()
    'Rosh Hashana'
    >>> rosh_hashana.holiday(hebrew=True)
    'ראש השנה'
    >>> (rosh_hashana + 3).holiday()
    None
    
    >>> for month in hebrewcal.Year(5774).itermonths():
    ...     print(month.name)
    Tishrei Cheshvan ...

    >>> date = dates.GregorianDate(2010, 10, 6)
    >>> print(parshios.getparsha(date))
    [0]
    >>> parshios.getparsha_string(date, israel=True)
    'Beraishis'
    >>> parshios.getparsha_string(date, hebrew=True)
    'בראשית'
    >>> new_date = dates.GregorianDate(2021, 3, 10)
    >>> parshios.getparsha_string(new_date)
    'Vayakhel, Pekudei'
    >>> parshios.getparsha_string(new_date, hebrew=True)
    'ויקהל, פקודי'

Documentation
-------------
Documentation for pyluach can be found at https://readthedocs.org/projects/pyluach/.

Contact
--------
For questions and comments feel free to contact me at simlist@gmail.com.

License
--------
Pyluach is licensed under the MIT license.

