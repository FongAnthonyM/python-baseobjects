"""__init__.py
testsuite provides test suite classes.
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
from .wrappertestsuite import WrapperTestSuite
from .wrapperperformancetestsuite import WrapperPerformanceTestSuite
