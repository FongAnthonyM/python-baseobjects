"""baseclasstestsuite.py
Base class for test suites which test a class.
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
from abc import abstractmethod
from typing import Any, Type

# Local Packages #
from .basetestsuite import BaseTestSuite


# Definitions #
# Classes #
class BaseClassTestSuite(BaseTestSuite):
    """Base class for test suites which test a class.

    This class provides common functionality for test suites, including fixtures and utility methods. Subclasses should
    implement the test_instance_creation method and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: type[Any]

    # Instance Methods #
    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
