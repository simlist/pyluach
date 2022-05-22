pyluach
=======
.. image:: https://readthedocs.org/projects/pyluach/badge/?version=stable
  :target: http://pyluach.readthedocs.io/en/latest/?badge=stable
  :alt: Documentation Status
.. image:: https://github.com/simlist/pyluach/actions/workflows/testing-and-coverage.yml/badge.svg?branch=master
    :target: https://github.com/simlist/pyluach/actions/workflows/testing-and-coverage.yml
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
* Generating and rendering Hebrew calendars in text and HTML

Installation
-------------
Use ``pip install pyluach``.

Documentation
-------------
Documentation for pyluach can be found at https://readthedocs.org/projects/pyluach/.

Examples
------------
::

    >>> from pyluach import dates, hebrewcal, parshios
    
    >>> today = dates.HebrewDate.today()
    >>> lastweek_gregorian = (today - 7).to_greg()
    >>> lastweek_gregorian < today
	True
    >>> today - lastweek_gregorian
    7
    >>> greg = dates.GregorianDate(1986, 3, 21)
    >>> heb = dates.HebrewDate(5746, 13, 10)
    >>> greg == heb
    True

    >>> purim = dates.HebrewDate(5781, 12, 14)
    >>> purim.hebrew_day()
    'י״ד'
    >>> purim.hebrew_date_string()
    'י״ד אדר תשפ״א'
    >>> purim.hebrew_date_string(True)
    'י״ד אדר ה׳תשפ״א'

    >>> rosh_hashana = dates.HebrewDate(5782, 7, 1)
    >>> rosh_hashana.holiday()
    'Rosh Hashana'
    >>> rosh_hashana.holiday(hebrew=True)
    'ראש השנה'
    >>> (rosh_hashana + 3).holiday()
    None
    
    >>> month = hebrewcal.Month(5781, 10)
    >>> month.month_name()
    'Teves'
    >>> month.month_name(True)
    'טבת'
    >>> month + 3
    Month(5781, 1)
    >>> for month in hebrewcal.Year(5774).itermonths():
    ...     print(month.month_name())
    Tishrei Cheshvan ...

    >>> date = dates.GregorianDate(2010, 10, 6)
    >>> parshios.getparsha(date)
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

Contact
--------
For questions and comments please `raise an issue in github
<https://github.com/simlist/pyluach/issues>`_ or contact me at
simlist@gmail.com.

License
--------
Pyluach is licensed under the MIT license.