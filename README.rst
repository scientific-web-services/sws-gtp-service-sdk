========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | TODO
        |
    * - package
      - | |commits-since|
        .. | |version| |wheel| |supported-versions| |supported-implementations|

.. |version| image:: https://img.shields.io/pypi/v/sws-gtp-service-sdk.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/sws-gtp-service-sdk

.. |wheel| image:: https://img.shields.io/pypi/wheel/sws-gtp-service-sdk.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/sws-gtp-service-sdk

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sws-gtp-service-sdk.svg
    :alt: Supported versions
    :target: https://pypi.org/project/sws-gtp-service-sdk

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sws-gtp-service-sdk.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/sws-gtp-service-sdk

.. |commits-since| image:: https://img.shields.io/github/commits-since/softwareengineerprogrammer/sws-gtp-service-sdk/v0.7.2.svg
    :alt: Commits since latest release
    :target: https://github.com/softwareengineerprogrammer/sws-gtp-service-sdk/compare/v0.7.2...main



.. end-badges

SWS GTP Service SDK


Installation
============

::

Install the in-development version with::

    pip install https://github.com/scientific-web-services/sws-gtp-service-sdk/archive/main.zip

(Package may eventually be published to PyPi, enabling `pip install sws-gtp-service-sdk`)

Documentation
=============


See example usage in https://github.com/softwareengineerprogrammer/sws-gtp-service-sdk/blob/main/tests/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
