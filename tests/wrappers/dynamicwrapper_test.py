#!/usr/bin/env python
"""dynamicwrapper_test.py
Tests for the DynamicWrapper class in the baseobjects package.
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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.testsuite.wrappers.dynamicwrappertestsuite import DynamicWrapperTestSuite
from baseobjects.testsuite.wrappers.wrappertestsuite import WrapperTestSuite
from baseobjects.wrappers import DynamicWrapper


# Definitions #
# Classes #
class ConcreteDynamicWrapper(DynamicWrapper, WrapperTestSuite):
    """A test class that inherits from DynamicWrapper.

    This class uses DynamicWrapper to wrap ConcreteOne and ConcreteTwo objects.
    """

    _wrapped_map_: list[str] = ["_first", "_second"]

    def __init__(self, first: Any = None, second: Any = None, init: bool = True, **kwargs: Any) -> None:
        """Initialize with wrapped objects.

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
            init: Whether to initialize the object.
            **kwargs: Keyword arguments to pass to the super class.
        """
        super().__init__(init=init, **kwargs)
        if init:
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


# Tests #
class TestDynamicWrapper(DynamicWrapperTestSuite):
    """Test the DynamicWrapper class.

    This class tests the functionality of the DynamicWrapper class, which is a wrapper that
    calls wrapped attributes/functions by changing the __getattr__ method.
    """

    # Class Attributes #
    UnitTestClass = ConcreteDynamicWrapper


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
