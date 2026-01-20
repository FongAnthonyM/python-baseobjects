#!/usr/bin/env python
"""staticwrapper_test.py
Tests for the StaticWrapper class in the baseobjects package.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.testsuite.wrappers.staticwrappertestsuite import StaticWrapperTestSuite
from baseobjects.testsuite.wrappers.wrappertestsuite import WrapperTestSuite
from baseobjects.wrappers import StaticWrapper


# Definitions #
# Classes #
class ConcreteStaticWrapper(StaticWrapper):
    """A test class that inherits from StaticWrapper.

    This class uses StaticWrapper to wrap ConcreteOne and ConcreteTwo objects.
    """

    _wrapped_map_: ClassVar[list[tuple[str, type[Any] | None]]] = [
        ("first", WrapperTestSuite.ConcreteOne),
        ("second", WrapperTestSuite.ConcreteTwo),
    ]

    def __init__(self, first: Any = None, second: Any = None) -> None:
        """Initialize with wrapped objects.

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
        """
        self._first = first
        self._second = second

        if first is not None:
            self.two = "wrapper"

        self.four = "wrapper"

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class TestStaticWrapper(StaticWrapperTestSuite):
    """Test the StaticWrapper class.

    This class tests the functionality of the StaticWrapper class, which is a wrapper that calls wrapped
    attributes/functions by creating property descriptors.
    """

    # Class Attributes #
    UnitTestClass = ConcreteStaticWrapper


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
