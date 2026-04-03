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
from typing import Any

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

    _wrapped_map_: list[tuple[str, type[Any] | None]] = [
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


class TestStaticWrapper(StaticWrapperTestSuite, WrapperTestSuite):
    """Test the StaticWrapper class.

    This class tests the functionality of the StaticWrapper class, which is a wrapper that calls wrapped
    attributes/functions by creating property descriptors.
    """

    # Class Attributes #
    UnitTestClass = ConcreteStaticWrapper

    def test_exclude_attributes_logic(self) -> None:
        """Tests that attributes in _exclude_attributes are not wrapped."""

        class TestExclude(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_first", self.ConcreteOne)]
            _exclude_attributes: set[str] = {"one"}

            def __init__(self, first: Any) -> None:
                self._first = first

        example = self.ConcreteOne()
        wrapper = TestExclude(example)

        # 'one' is excluded, so it should NOT be found on wrapper.
        with pytest.raises(AttributeError):
            _ = wrapper.one  # type: ignore[attr-defined]

        # 'common' is NOT excluded, so it should be found.
        assert wrapper.common == "example_one"  # type: ignore[attr-defined]

    def test_setter_delegation(self) -> None:
        """Tests that setting attributes delegates to the wrapped object."""

        class TestSetter(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_first", self.ConcreteOne)]

            def __init__(self, first: Any) -> None:
                self._first = first

        example = self.ConcreteOne()
        wrapper = TestSetter(example)

        assert wrapper.one == "one"  # type: ignore[attr-defined]
        wrapper.one = "new"  # type: ignore[attr-defined]
        assert example.one == "new"
        assert wrapper.one == "new"  # type: ignore[attr-defined]

    def test_nesting(self) -> None:
        """Tests nesting wrappers."""

        class Inner(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_obj", self.ConcreteOne)]

            def __init__(self, obj: Any) -> None:
                self._obj = obj

        class Outer(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_inner", Inner)]

            def __init__(self, inner: Any) -> None:
                self._inner = inner

        inner = self.ConcreteOne()
        wrapper1 = Inner(inner)
        wrapper2 = Outer(wrapper1)

        assert wrapper2.one == "one"  # type: ignore[attr-defined]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
