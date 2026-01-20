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
from typing import ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseMeta
from baseobjects.testsuite.bases import BaseClassTestSuite


# Classes #
class BaseMetaSubclass(BaseMeta):
    """A subclass of BaseMeta for testing purposes."""


class ConcreteClass(metaclass=BaseMetaSubclass):
    """A class that uses BaseMetaSubclass as its metaclass."""

    def __init__(self) -> None:
        """Initialize with some attributes."""
        self.value = 42


# Tests #
class TestBaseMeta(BaseClassTestSuite):
    """Test the BaseMeta class.

    This class tests the functionality of the BaseMeta metaclass, which is the base metaclass for all classes in the
    baseobjects package.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[BaseMeta]] = BaseMetaSubclass
    ConcreteUnitTestClass: type[ConcreteClass] = ConcreteClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class(self) -> type[ConcreteClass]:
        """Create a test class with the test metaclass.

        Returns:
            Type: A class that uses the test metaclass.
        """
        return self.ConcreteUnitTestClass

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the metaclass can be created.

        This test verifies that classes can be created with the metaclass.
        """

        # Create a class with the metaclass
        class UnitTestClass(metaclass=BaseMetaSubclass):
            pass

        # Validate
        cls_type = type(UnitTestClass)
        assert cls_type is BaseMetaSubclass

    def test_class_instance_creation(self, test_class: type[ConcreteClass]) -> None:
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
