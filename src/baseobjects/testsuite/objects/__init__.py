"""__init__.py
Test suites for objects in the baseobjects package.

This module contains the test suites for objects in the baseobjects package.
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
from .automaticpropertiestestsuite import AutomaticPropertiesTestSuite
from .callbackmanagertestsuite import CallbackManagerTestSuite
from .callbackschedulertestsuite import CallbackSchedulerTestSuite

__all__ = [
    "AutomaticPropertiesTestSuite",
    "CallbackManagerTestSuite",
    "CallbackSchedulerTestSuite",
]
