"""dispatchablecompositetestsuite.py
Base test suite for DispatchableComposite and its subclasses.
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
from ...composition import DispatchableComposite
from ..classregistration import DispatchableClassTestSuite
from .basedispatchingcompositetestsuite import BaseDispatchingCompositeTestSuite


# Definitions #
# Classes #
class DispatchableCompositeTestSuite(BaseDispatchingCompositeTestSuite, DispatchableClassTestSuite):
    """Base test suite for children of DispatchableComposite.

    This class provides common test functionality for child classes of DispatchableComposite, including tests for
    dispatchable class functionality. Subclasses should set the UnitTestClass attribute and may override or extend the
    test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[DispatchableComposite]
