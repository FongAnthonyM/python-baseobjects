"""__init__.py
testsuite provides test suite classes.

This module contains the testsuite provides test suite classes.
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
from .dynamicwrappertestsuite import DynamicWrapperTestSuite
from .staticwrappertestsuite import StaticWrapperTestSuite
from .wrapperperformancetestsuite import WrapperPerformanceTestSuite
from .wrappertestsuite import WrapperTestSuite

__all__ = [
    "DynamicWrapperTestSuite",
    "StaticWrapperTestSuite",
    "WrapperPerformanceTestSuite",
    "WrapperTestSuite",
]
