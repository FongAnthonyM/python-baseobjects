"""dispatchableclasstestsuite.py
Base test suite for DispatchableClass and its subclasses.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #

# Local Packages #
from ...classregistration import DispatchableClass
from .baseregisteredclasstestsuite import BaseRegisteredClassTestSuite


# Definitions #
# Classes #
class DispatchableClassTestSuite(BaseRegisteredClassTestSuite):
    """Base test suite for children of DispatchableClass.

    This class provides common test functionality for child classes of DispatchableClass, including tests for class
    dispatching. Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[DispatchableClass]
