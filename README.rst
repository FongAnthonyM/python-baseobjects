baseobjects
===========

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit|

.. |PyPI| image:: https://img.shields.io/pypi/v/baseobjects.svg
   :target: https://pypi.org/project/baseobjects/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/baseobjects.svg
   :target: https://pypi.org/project/baseobjects/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/baseobjects
   :target: https://pypi.org/project/baseobjects
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/baseobjects
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/python-baseobjects/latest.svg?label=Read%20the%20Docs
   :target: https://python-baseobjects.readthedocs.io/
   :alt: Read the documentation at https://python-baseobjects.readthedocs.io/
.. |Tests| image:: https://github.com/AnthonyTechnologies/python-baseobjects/workflows/Tests/badge.svg
   :target: https://github.com/AnthonyTechnologies/baseobjects/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/AnthonyTechnologies/python-baseobjects/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/AnthonyTechnologies/python-baseobjects
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit


Features
--------

Baseobjects is a collection of carefully designed, reusable building blocks for Python applications. It provides a
consistent set of base classes, utilities, and patterns intended for inheritance and composition for building
reliable, testable, and maintainable software faster. The package focuses on practical foundations: common object
patterns, light-weight data containers, function helpers, and robust operational utilities.

* bases: Low level base classes.
* cachingtools: Objects and decorators for local caching.
* collections: Objects for storing other objects.
* composition: Objects for creating compositions style objects.
* dataclasses: Objects for storing information efficiently.
* functions: Objects for creating function and method objects.
* metaclasses: Base metaclasses.
* objects: Uncategorized base objects.
* operations: An assortment of functions for common operations.
* typing: Objects to be used when adding typing to python code.
* versioning: Objects for tracking versions.
* wrappers: Objects for wrapping other objects.

Requirements
------------

* Python 3.14 or later
* bidict

Installation
------------

Install *baseobjects* via pip_ from PyPI_:

.. code:: console

   $ pip install baseobjects


Documentation
-------------

For comprehensive guides, see the full documentation on Read the Docs:
https://python-baseobjects.readthedocs.io/

The documentation includes a user guide, API reference, tutorials, and examples to help with getting productive quickly.

For project-wide conventions and contribution standards, refer to `Anthony's Python Style Guide`_.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_, *baseobjects* is free and open source software.


Issues
------

If problems are encountered,
please `file an issue`_ along with a detailed description.


Credits
-------

Project Organization: `Anthony's Python Style Guide`_ based on `The Google Style Guide`_ and `Hypermodern Python`_ by `Claudio Jolowicz`_.

.. _pip: https://pip.pypa.io/
.. _PyPI: https://pypi.org/
.. _MIT license: https://opensource.org/licenses/MIT
.. _file an issue: https://github.com/AnthonyTechnologies/python-baseobjects/issues
.. _Anthony's Python Style Guide: https://github.com/AnthonyTechnologies/python-styleguide
.. _The Google Style Guide: https://google.github.io/styleguide/pyguide.html
.. _Hypermodern Python: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/
.. _Claudio Jolowicz: https://github.com/cjolowicz
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
