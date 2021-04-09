==========
Change Log
==========

This document records all notable changes to `pyluach <https://github.com/simlist/pyluach>`_.
This project adheres to `Semantic Versioning <https://semver.org/>`_.


`1.3.0`_ (2021-04-__)
---------------------
* Added option to get parsha in Hebrew.
* Added option to get Month names in Hebrew.
* Added HebrewDate methods to get hebrew day, month, year, and
  date string in Hebrew.
* Implemented more consistent Hebrew to English transliterations for parshios.

`1.2.1`_ (2020-11-08)
---------------------
* Fixed molad having weekday of `0` when it should be `7`.

`1.2.0`_ (2020-10-28)
---------------------
* Created isoweekday method for all date types.
* Created fast_day and festival functions (`#11`_)
* Added Pesach Sheni to festival.

`1.1.1`_ (2020-08-14)
---------------------
* Fixed error getting parsha of Shabbos on Rosh Hashana.


`1.1.0`_ (2020-06-03)
---------------------
* Redesigned documentation.
* Added molad and molad_announcement methods to hebrewcal.Month.
* Stopped supporting python < 3.4 and modernized code.


`1.0.1`_ (2019-03-02)
---------------------

* Initial public release


.. _`1.2.1`: https://github.com/simlist/pyluach/compare/v1.2.0...v1.2.1
.. _`1.2.0`: https://github.com/simlist/pyluach/compare/v1.1.1...v1.2.0
.. _`1.1.1`: https://github.com/simlist/pyluach/compare/v1.1.0...v1.1.1
.. _`1.1.0`: https://github.com/simlist/pyluach/compare/v1.0.1...v1.1.0
.. _`1.0.1`: https://github.com/simlist/pyluach/releases/tag/v1.0.1

.. _`#11`: https://github.com/simlist/pyluach/issues/11