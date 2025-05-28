#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" automaticproperties_test.py
Tests for the automaticproperties.py module in the baseobjects package.
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
from functools import partial
from typing import Any, ClassVar, Dict, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects.automaticproperties import AutomaticProperties
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class BaseTestAutomaticProperties(ClassTest):
    """Base Tests for the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which creates properties for classes
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties]

    # Instance Methods #
    # Tests
    def test_construct_properties(self) -> None:
        """Test the _construct_properties_ method.

        This test verifies that the _construct_properties_ method correctly creates properties from a property map.
        """
        # Create a test class with properties
        class PropertyTest(self.class_):
            properties = {}

        # Define a property map
        property_map = {
            "dynamic_prop": "_dynamic_prop"
        }

        # Construct properties
        PropertyTest._construct_properties_(property_map)

        # Verify the property was created
        assert hasattr(PropertyTest, "dynamic_prop")

    def test_automatic_property_creation(self) -> None:
        """Test the automatic creation of properties.

        This test verifies that properties are automatically created based on the properties dictionary.
        """
        # Verify the properties were created
        for prop in self.class_.properties.keys():
            assert hasattr(self.class_, prop)


class AutomaticPropertiesDefaultTestObject(AutomaticProperties):
    """A subclass of AutomaticProperties for testing purposes."""

    # Class Attributes #
    properties = {
        "test_property": "_test_property",
        "complex_property": (AutomaticProperties.property_method_factory, "_complex_property", {})
    }

    # Attributes #
    _test_property = "test value"
    _complex_property = "complex value"


class TestAutomaticProperties(BaseTestAutomaticProperties):
    """Test the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which creates properties for classes
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties] = AutomaticPropertiesDefaultTestObject

    # Instance Methods #
    # Tests
    def test_property_get(self) -> None:
        """Test the property_get method.

        This test verifies that the property_get method correctly retrieves attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_get method directly
        assert obj.property_get("_test_property") == "test value"

        # Test with a non-existent attribute (should raise AttributeError)
        with pytest.raises(AttributeError):
            obj.property_get("_nonexistent")

    def test_property_set(self) -> None:
        """Test the property_set method.

        This test verifies that the property_set method correctly sets attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_set method directly
        obj.property_set("new value", "_test_property")
        assert obj._test_property == "new value"

        # Test setting a new attribute
        obj.property_set("created value", "_new_property")
        assert obj._new_property == "created value"

    def test_property_del(self) -> None:
        """Test the property_del method.

        This test verifies that the property_del method correctly deletes attributes.
        """
        # Create a test instance
        obj = self.class_()

        # Create a new attribute
        obj._new_property = "new value"

        # Test the property_del method directly
        obj.property_del("_new_property")

        # Verify the attribute was deleted
        with pytest.raises(AttributeError):
            getattr(obj, "_new_property")

    def test_property(self) -> None:
        # Create a test instance
        obj = self.class_()

        # Test getting the property
        assert obj.test_property == "test value"

        # Test setting the property
        obj.test_property = "new value"
        assert obj._test_property == "new value"

        # Test deleting the property
        del obj.test_property
        assert obj._test_property == "test value"


class AutomaticPropertiesComplexTestObject(AutomaticProperties):
    """A subclass of AutomaticProperties for testing purposes."""

    # Class Attributes #
    properties = {
        "test_property": "_test_property",
        "complex_property": ("custom_factory", "_complex_property", {})
    }

    # Class Methods #
    @classmethod
    def custom_factory(cls, info: str) -> tuple:
        """A factory method for creating property modification methods."""
        name = info

        _property_get = partial(cls.property_get, name=name)
        _property_set = partial(cls.custom_set, name=name)
        _property_del = partial(cls.property_del, name=name)

        return _property_get, _property_set, _property_del

    # Attributes #
    _test_property = "test value"
    _complex_property = "complex value"

    # Instance Methods #
    def property_get(self, name: str) -> Any:
        """Custom getter that adds a prefix."""
        return f"PREFIX_{getattr(self, name)}"

    def custom_set(self, value: Any, name: str) -> None:
        """Custom setter that adds a suffix."""
        setattr(self, name, f"{value}_SUFFIX")


class TestAutomaticComplexProperties(TestAutomaticProperties):
    """Test the AutomaticProperties class with complex property configuration.

    This class tests the functionality of the AutomaticProperties class, which creates properties for classes
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties] = AutomaticPropertiesComplexTestObject

    # Instance Methods #
    # Tests
    def test_property_get(self) -> None:
        """Test the property_get method.

        This test verifies that the property_get method correctly retrieves attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_get method directly
        assert obj.property_get("_test_property") == "PREFIX_test value"

        # Test with a non-existent attribute (should raise AttributeError)
        with pytest.raises(AttributeError):
            obj.property_get("_nonexistent")

    def test_custom_set(self) -> None:
        """Test the property_set method.

        This test verifies that the property_set method correctly sets attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_set method directly
        obj.custom_set("new value", "_test_property")
        assert obj._test_property == "new value_SUFFIX"

        # Test setting a new attribute
        obj.custom_set("created value", "_new_property")
        assert obj._new_property == "created value_SUFFIX"

    def test_property(self) -> None:
        # Create a test instance
        obj = self.class_()

        # Test getting the property
        assert obj.test_property == "PREFIX_test value"

        # Test setting the property
        obj.test_property = "new value"
        assert obj._test_property == "new value"

        # Test deleting the property
        del obj.test_property
        assert obj._test_property == "test value"

        # Test getting the complex property
        assert obj.complex_property == "PREFIX_complex value"

        # Test setting the complex property
        obj.complex_property = "new value"
        assert obj._complex_property == "new value_SUFFIX"

        # Test deleting the property
        del obj.complex_property
        assert obj._complex_property == "complex value"


class AutomaticPropertiesClassMethodTestObject(AutomaticProperties):
    """A subclass of AutomaticProperties for testing purposes."""

    # Class Attributes #
    default_property_function_factory = AutomaticProperties.property_class_method_factory
    properties = {
        "test_property": "_test_property",
        "complex_property": (AutomaticProperties.property_class_method_factory, "_complex_property", {})
    }

    # Attributes #
    _test_property = "test value"
    _complex_property = "complex value"


class TestAutomaticClassMethodProperties(BaseTestAutomaticProperties):
    """Test the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which creates properties for classes
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties] = AutomaticPropertiesClassMethodTestObject

    # Instance Methods #
    # Tests
    def test_property_class_get(self) -> None:
        """Test the property_class_get method.

        This test verifies that the property_class_get method correctly retrieves attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_class_get method directly
        assert self.class_.property_class_get(obj, "_test_property") == "test value"

        # Test with a non-existent attribute (should raise AttributeError)
        with pytest.raises(AttributeError):
            self.class_.property_class_get(obj, "_nonexistent")

    def test_property_class_set(self) -> None:
        """Test the property_class_set method.

        This test verifies that the property_class_set method correctly sets attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_class_set method directly
        self.class_.property_class_set(obj, "new value", "_test_property")
        assert obj._test_property == "new value"

        # Test setting a new attribute
        self.class_.property_class_set(obj, "created value", "_new_property")
        assert obj._new_property == "created value"

    def test_property_class_del(self) -> None:
        """Test the property_class_del method.

        This test verifies that the property_class_del method correctly deletes attributes.
        """
        # Create a test instance
        obj = self.class_()

        # Create a new attribute
        obj._new_property = "new value"

        # Test the property_class_del method directly
        self.class_.property_class_del(obj, "_new_property")

        # Verify the attribute was deleted
        with pytest.raises(AttributeError):
            getattr(obj, "_new_property")

    def test_property(self) -> None:
        # Create a test instance
        obj = self.class_()

        # Test getting the property
        assert obj.test_property == "test value"

        # Test setting the property
        obj.test_property = "new value"
        assert obj._test_property == "new value"

        # Test deleting the property
        del obj.test_property
        assert obj._test_property == "test value"


class AutomaticPropertiesComplexClassMethodTestObject(AutomaticProperties):
    """A subclass of AutomaticProperties for testing purposes."""

    # Class Attributes #
    default_property_function_factory = "property_class_method_factory"
    properties = {
        "test_property": "_test_property",
        "complex_property": ("custom_factory", "_complex_property", {})
    }

    # Attributes #
    _test_property = "test value"
    _complex_property = "complex value"

    # Class Methods #
    # Property Methods
    @classmethod
    def property_class_get(cls, self, name: str) -> Any:
        """Custom getter that adds a prefix."""
        return f"{cls.__name__}_PREFIX_{getattr(self, name)}"

    @classmethod
    def custom_class_set(cls, self, value: Any, name: str) -> None:
        """Custom setter that adds a suffix."""
        setattr(self, name, f"{value}_SUFFIX_{cls.__name__}")

    # Callback Factories
    @classmethod
    def custom_factory(cls, info: str) -> tuple:
        """A factory method for creating property modification methods."""
        name = info

        _property_get = partial(cls.property_class_get, name=name)
        _property_set = partial(cls.custom_class_set, name=name)
        _property_del = partial(cls.property_class_del, name=name)

        return _property_get, _property_set, _property_del


class TestAutomaticComplexClassMethodProperties(TestAutomaticClassMethodProperties):
    """Test the AutomaticProperties class with complex property configuration.

    This class tests the functionality of the AutomaticProperties class, which creates properties for classes
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties] = AutomaticPropertiesComplexClassMethodTestObject

    # Instance Methods #
    # Tests
    def test_property_class_get(self) -> None:
        """Test the property_class_get method.

        This test verifies that the property_class_get method correctly retrieves attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_class_get method directly
        assert self.class_.property_class_get(obj, "_test_property") == f"{self.class_.__name__}_PREFIX_test value"

        # Test with a non-existent attribute (should raise AttributeError)
        with pytest.raises(AttributeError):
            self.class_.property_class_get(obj, "_nonexistent")

    def test_custom_class_set(self) -> None:
        """Test the property_class_set method.

        This test verifies that the property_class_set method correctly sets attribute values.
        """
        # Create a test instance
        obj = self.class_()

        # Test the property_class_set method directly
        self.class_.custom_class_set(obj, "new value", "_test_property")
        assert obj._test_property == f"new value_SUFFIX_{self.class_.__name__}"

        # Test setting a new attribute
        self.class_.custom_class_set(obj, "created value", "_new_property")
        assert obj._new_property == f"created value_SUFFIX_{self.class_.__name__}"

    def test_property(self) -> None:
        # Create a test instance
        obj = self.class_()

        # Test getting the property
        assert obj.test_property == f"{self.class_.__name__}_PREFIX_test value"

        # Test setting the property
        obj.test_property = "new value"
        assert obj._test_property == f"new value"

        # Test deleting the property
        del obj.test_property
        assert obj._test_property == "test value"

        # Test getting the custom property
        assert obj.complex_property == f"{self.class_.__name__}_PREFIX_complex value"

        # Test setting the custom property
        obj.complex_property = "new value"
        assert obj._complex_property == f"new value_SUFFIX_{self.class_.__name__}"

        # Test deleting the property
        del obj._complex_property
        assert obj._complex_property == "complex value"

# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
