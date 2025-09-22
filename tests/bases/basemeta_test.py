"""basemeta_test.py
Tests for the BaseMeta class in the baseobjects package.

This module provides tests for the BaseMeta class, which is an abstract metaclass that inherits from ABCMeta and adds
functionality for copying and deep copying metaclass objects.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseMeta
from src.baseobjects.testsuite.bases import BaseClassTestSuite


# Classes #
class BaseTestMeta(BaseMeta):
    """A subclass of BaseMeta for testing purposes."""

    pass


class BaseTestClass(metaclass=BaseTestMeta):
    """A class that uses BaseTestMeta as its metaclass."""

    def __init__(self) -> None:
        """Initialize with some attributes."""
        self.value = 42


# Tests#
class TestBaseMeta(BaseClassTestSuite):
    """Test the BaseMeta class.

    This class tests the functionality of the BaseMeta metaclass, which is the base metaclass for all classes in the
    baseobjects package.
    """

    # Attributes #
    TestClass: Type[BaseMeta] = BaseTestMeta
    TestBaseClass: Type[BaseTestClass] = BaseTestClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class(self) -> Type:
        """Create a test class with the test metaclass.

        Returns:
            Type: A class that uses the test metaclass.
        """
        return self.TestBaseClass

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the metaclass can be created.

        This test verifies that classes can be created with the metaclass.
        """

        # Create a class with the metaclass
        class TestClass(metaclass=self.TestClass):
            pass

        # Validate
        assert TestClass.__class__ is self.TestClass

    def test_class_instance_creation(self, test_class: Type) -> None:
        """Test that instances of classes with the metaclass can be created.

        Args:
            test_class: A fixture providing a class that uses the test metaclass.
        """
        # Create an instance of the class
        instance = test_class()

        # Validate
        assert isinstance(instance, test_class)
        assert instance.value == 42


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
