#!/usr/bin/env python
"""runtime_test.py
Tests for the runtime warnings module.
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
from baseobjects.testsuite import BaseClassTestSuite
from baseobjects.warnings import NotImplementedWarning, TimeoutWarning


# Definitions #
# Classes #
class TestNotImplementedWarning(BaseClassTestSuite):
    """Tests NotImplementedWarning."""

    # Attributes #
    UnitTestClass = NotImplementedWarning

    # Tests #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created."""
        warning = self.UnitTestClass(*args, **kwargs)
        assert isinstance(warning, self.UnitTestClass)
        assert str(warning) == "A method or function has not been implemented yet."

    def test_init_with_name(self) -> None:
        """Tests the initialization with a specific name."""
        warning = NotImplementedWarning("MyFunc")
        assert str(warning) == "MyFunc has not been implemented yet."


class TestTimeoutWarning(BaseClassTestSuite):
    """Tests TimeoutWarning."""

    # Attributes #
    UnitTestClass = TimeoutWarning

    # Tests #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created."""
        warning = self.UnitTestClass(*args, **kwargs)
        assert isinstance(warning, self.UnitTestClass)
        assert str(warning) == "A function timed out"

    def test_init_with_name(self) -> None:
        """Tests the initialization with a specific name."""
        warning = TimeoutWarning("MyFunc")
        assert str(warning) == "MyFunc timed out"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
