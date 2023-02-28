==========
Changelog
==========

This document records all notable changes to `pyluach <https://github.com/simlist/pyluach>`_.
This project adheres to `Semantic Versioning <https://semver.org/>`_.

`2.2.0`_(2023-02-??)
====================
* Added `prefix_day` param to ``festival`` and ``holiday`` methods and
  functions.

`2.1.0`_ (2023-02-12)
================================
* Added ``add`` and ``subtract`` methods to ``dates.HebrewDate``.
* Added ``replace`` method to ``CalendarDateMixin``.
* Added missing documentation for `%y` and `%Y` in formatting
  ``HebrewDate``.

`2.0.2`_ (2022-10-24)
=====================
* Fix subtracting one date from another returning ``float`` instead of ``int``.

`2.0.1`_ (2022-08-24)
=====================
* Fix issue (`#24`_) where Shavuos is returned in most months on day 7.

`2.0.0`_ (2022-05-29)
=====================
* Changed equality comparers to compare object identity on unmatched types.
* Equal dates of different types will no longer be considered identical
  keys for dicts.
* Added ``strftime`` and ``__format__`` methods to
  ``dates.GregorianDate``.
* Added ``__format__`` method to ``dates.HebrewDate``.
* Added `withgershayim` parameter to ``dates.HebrewDate.hebrew_day`` and
  ``dates.HebrewDate.hebrew_year`` methods
* Added ``monthcount`` method to ``hebrewcal.Year``.
* Removed deprecated ``hebrewcal.Month.name`` attribute.
* Implemented HebrewCalendar classes for generating calendars similar to
  Calendar classes in the standard library calendar module.

`1.4.2`_ (2022-05-20)
=====================
* Fixed bug in ``hebrewcal.Month`` comparisons when one month is before
  Nissan and one is not.

`1.4.1`_ (2022-03-25)
=====================
* Fixed mistakes in docstring and error message.

`1.4.0`_ (2022-02-21)
=====================
* Added parameter `include_working_days` to ``festival`` method and function.
* Removed support for python < 3.6

`1.3.0`_ (2021-06-09)
=====================
* Added option to get parsha in Hebrew.
* Added ``dates.HebrewDate`` methods to get hebrew day, month, year, and
  date string in Hebrew.
* Added method to get ``hebrewcal.Month`` names in Hebrew.
* Added methods to get year and month strings in Hebrew.
* Added classmethods to ``hebrewcal.Year`` and ``hebrewcal.Month`` to get
  objects from dates and pydates.
* Added methods to dates classes to get holidays, fast days and festivals.
* Implemented more consistent Hebrew to English transliterations for parshios.

`1.2.1`_ (2020-11-08)
=====================
* Fixed molad having weekday of ``0`` when it should be ``7``.

`1.2.0`_ (2020-10-28)
=====================
* Created ``isoweekday`` method for all date types in the ``dates`` module.
* Created fast_day and festival functions (`#11`_)
* Added Pesach Sheni to festival.

`1.1.1`_ (2020-08-14)
=====================
* Fixed error getting parsha of Shabbos on Rosh Hashana.


`1.1.0`_ (2020-06-03)
=====================
* Redesigned documentation.
* Added ``molad`` and ``molad_announcement`` methods to ``hebrewcal.Month``.
* Stopped supporting python < 3.4 and modernized code.


`1.0.1`_ (2019-03-02)
=====================
* Initial public release


.. _`2.2.0`: https://github.com/simlist/pyluach/compare/v2.0.2...v2.2.0
.. _`2.1.0`: https://github.com/simlist/pyluach/compare/v2.0.2...v2.1.0
.. _`2.0.2`: https://github.com/simlist/pyluach/compare/v2.0.1...v2.0.2
.. _`2.0.1`: https://github.com/simlist/pyluach/compare/v2.0.0...v2.0.1
.. _`2.0.0`: https://github.com/simlist/pyluach/compare/v1.4.2...v2.0.0
.. _`1.4.2`: https://github.com/simlist/pyluach/compare/v1.4.1...v1.4.2
.. _`1.4.1`: https://github.com/simlist/pyluach/compare/v1.4.0...v1.4.1
.. _`1.4.0`: https://github.com/simlist/pyluach/compare/v1.3.0...v1.4.0
.. _`1.3.0`: https://github.com/simlist/pyluach/compare/v1.2.1...v1.3.0
.. _`1.2.1`: https://github.com/simlist/pyluach/compare/v1.2.0...v1.2.1
.. _`1.2.0`: https://github.com/simlist/pyluach/compare/v1.1.1...v1.2.0
.. _`1.1.1`: https://github.com/simlist/pyluach/compare/v1.1.0...v1.1.1
.. _`1.1.0`: https://github.com/simlist/pyluach/compare/v1.0.1...v1.1.0
.. _`1.0.1`: https://github.com/simlist/pyluach/releases/tag/v1.0.1

.. _`#11`: https://github.com/simlist/pyluach/issues/11
.. _`#24`: https://github.com/simlist/pyluach/issues/24
