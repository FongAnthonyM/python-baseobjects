"""__init__.py
Package initialization for the baseobjects.testsuite.cachingtools package.

This module serves as an initialization file for the testsuite.cachingtools package, which provides test suite
classes for testing the cachingtools functionality. It imports and exposes classes like
BaseTimedCacheCallableTestSuite, making them available for direct import from the testsuite.cachingtools package.
These test suites ensure the proper functioning of caching mechanisms in the baseobjects package.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .basetimedcachecallabletestsuite import BaseTimedCacheCallableTestSuite
