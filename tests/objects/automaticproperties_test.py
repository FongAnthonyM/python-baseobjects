#!/usr/bin/env python
"""automaticproperties_test.py
Test for the AutomaticProperties class.

This module provides tests for the AutomaticProperties class, which is an abstract class that creates properties
automatically based on a properties dictionary.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.objects import AutomaticProperties
from src.baseobjects.testsuite.objects import AutomaticPropertiesTestSuite


# Definitions #
# Classes #
class TestAutomaticPropertiesClass(AutomaticProperties):
    """A concrete implementation of AutomaticProperties for testing."""

    # Class Attributes #
    properties = {
        "test_prop": "_test_prop",
        "another_prop": "_another_prop",
        "complex_prop": ("property_method_factory", "_complex_prop", {}),
    }


class TestAutomaticProperties(AutomaticPropertiesTestSuite):
    """Test the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which is an abstract class that creates
    properties automatically based on a properties dictionary.
    """

    # Attributes #
    TestClass = TestAutomaticPropertiesClass

    # Instance Methods #
    # Tests
    def test_complex_property_definition(self) -> None:
        """Test that complex property definitions work correctly.

        This test verifies that properties defined with a tuple of (factory, attribute, kwargs) work correctly.
        """
        # Create Object
        obj = self.TestClass()
        obj._complex_prop = "complex value"

        # Validate
        assert hasattr(self.TestClass, "complex_prop")
        assert isinstance(self.TestClass.complex_prop, property)
        assert obj.complex_prop == "complex value"

    def test_default_property_function_factory(self) -> None:
        """Test the default_property_function_factory attribute.

        This test verifies that the default_property_function_factory attribute is used when a property is defined
        with just a string.
        """

        # Create Test Class
        class TestClass(AutomaticProperties):
            """Test class for default_property_function_factory."""

            default_property_function_factory = "property_class_method_factory"
            properties = {"default_factory_prop": "_default_factory_prop"}

        # Create Object
        obj = TestClass()
        obj._default_factory_prop = "default factory value"

        # Validate
        assert hasattr(TestClass, "default_factory_prop")
        assert isinstance(TestClass.default_factory_prop, property)
        assert obj.default_factory_prop == "default factory value"

    def test_property_inheritance(self) -> None:
        """Test that properties are inherited correctly.

        This test verifies that properties defined in a parent class are available in child classes.
        """

        # Create Child Class
        class ChildClass(self.TestClass):
            """Child class for testing property inheritance."""

            properties = {"child_prop": "_child_prop"}

        # Create Object
        obj = ChildClass()
        obj._test_prop = "test value"
        obj._another_prop = "another value"
        obj._child_prop = "child value"

        # Validate
        assert hasattr(ChildClass, "test_prop")
        assert hasattr(ChildClass, "another_prop")
        assert hasattr(ChildClass, "child_prop")
        assert isinstance(ChildClass.test_prop, property)
        assert isinstance(ChildClass.another_prop, property)
        assert isinstance(ChildClass.child_prop, property)
        assert obj.test_prop == "test value"
        assert obj.another_prop == "another value"
        assert obj.child_prop == "child value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
