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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects.automaticproperties import AutomaticProperties
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class ConcreteAutomaticProperties(AutomaticProperties):
    """A concrete implementation of AutomaticProperties for testing purposes."""

    # Class Attributes #
    _properties_map_cls = []
    _properties = {"test_prop": "_test_value", "another_prop": "_another_value"}

    def __init__(self) -> None:
        self._test_value = "test value"
        self._another_value = "another value"
        super().__init__()

    @classmethod
    def _construct_properties_map(cls) -> None:
        """Implements the abstract method to define how properties should be constructed."""
        cls._properties_map.append(["_properties", cls._dictionary_to_properties, cls._default_functions_factory])


class CustomCallbackAutomaticProperties(AutomaticProperties):
    """A concrete implementation of AutomaticProperties with custom callbacks."""

    # Class Attributes #
    _properties_map_cls = []
    _properties = {"custom_prop": "_custom_prop"}

    def __init__(self) -> None:
        self._custom_prop = "custom value"
        super().__init__()

    @classmethod
    def property_get(cls, obj: Any, name: str) -> Any:
        """Custom get implementation that adds a prefix."""
        return f"GET: {getattr(obj, name)}"

    @classmethod
    def property_set(cls, obj: Any, name: str, value: Any) -> None:
        """Custom set implementation that adds a suffix."""
        setattr(obj, name, f"{value} (SET)")

    @classmethod
    def property_del(cls, obj: Any, name: str) -> None:
        """Custom delete implementation that sets to a default value instead of deleting."""
        setattr(obj, name, "DELETED")

    @classmethod
    def _construct_properties_map(cls) -> None:
        """Implements the abstract method to define how properties should be constructed."""
        cls._properties_map.append(["_properties", cls._dictionary_to_properties, cls._default_functions_factory])


class TestAutomaticProperties(ClassTest):
    """Test the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which creates properties for a class
    automatically.
    """

    # Class Attributes #
    class_: Type[AutomaticProperties] = AutomaticProperties

    # Instance Methods #
    # Tests
    def test_property_creation(self) -> None:
        """Test that properties are created correctly.

        This test verifies that properties are created based on the _properties attribute and can be accessed and
        modified.
        """
        # Create an instance of the concrete class
        obj = ConcreteAutomaticProperties()

        # Verify properties exist
        assert hasattr(obj, "test_prop")
        assert hasattr(obj, "another_prop")

        # Verify property values
        assert obj.test_prop == "test value"
        assert obj.another_prop == "another value"

        # Modify property values
        obj.test_prop = "new test value"
        obj.another_prop = "new another value"

        # Verify modified values
        assert obj._test_value == "new test value"
        assert obj._another_value == "new another value"
        assert obj.test_prop == "new test value"
        assert obj.another_prop == "new another value"

    def test_custom_callbacks(self) -> None:
        """Test custom property callbacks.

        This test verifies that custom _get, _set, and _del methods work correctly.
        """
        # Create an instance of the class with custom callbacks
        obj = CustomCallbackAutomaticProperties()

        # Verify property exists
        assert hasattr(obj, "custom_prop")

        # Verify get callback
        assert obj.custom_prop == "GET: custom value"

        # Verify set callback
        obj.custom_prop = "new value"
        assert obj._custom_prop == "new value (SET)"
        assert obj.custom_prop == "GET: new value (SET)"

        # Verify del callback
        del obj.custom_prop
        assert obj._custom_prop == "DELETED"
        assert obj.custom_prop == "GET: DELETED"

    def test_iterable_to_properties(self) -> None:
        """Test the _iterable_to_properties method.

        This test verifies that properties can be created from an iterable.
        """
        # Create a class that uses _iterable_to_properties
        class IterablePropertiesTest(AutomaticProperties):
            _properties_map_cls = []
            _properties = ["prop1", "prop2"]

            def __init__(self) -> None:
                self._prop1 = "value1"
                self._prop2 = "value2"
                super().__init__()

            @classmethod
            def property_get(cls, obj: Any, name: str) -> Any:
                """Get the attribute value."""
                return getattr(obj, f"_{name}")

            @classmethod
            def property_set(cls, obj: Any, name: str, value: Any) -> None:
                """Set the attribute value."""
                setattr(obj, f"_{name}", value)

            @classmethod
            def property_del(cls, obj: Any, name: str) -> None:
                """Delete the attribute."""
                delattr(obj, f"_{name}")

            @classmethod
            def _construct_properties_map(cls) -> None:
                cls._properties_map.append(["_properties", cls._iterable_to_properties, cls._default_functions_factory])

        # Create an instance
        obj = IterablePropertiesTest()

        # Verify properties exist
        assert hasattr(obj, "prop1")
        assert hasattr(obj, "prop2")

        # Verify property values
        assert obj.prop1 == "value1"
        assert obj.prop2 == "value2"

        # Modify property values
        obj.prop1 = "new value1"
        obj.prop2 = "new value2"

        # Verify modified values
        assert obj._prop1 == "new value1"
        assert obj._prop2 == "new value2"
        assert obj.prop1 == "new value1"
        assert obj.prop2 == "new value2"

    def test_dictionary_to_properties(self) -> None:
        """Test the _dictionary_to_properties method.

        This test verifies that properties can be created from a dictionary.
        """
        # Create a class that uses _dictionary_to_properties
        class DictPropertiesTest(AutomaticProperties):
            _properties_map_cls = []
            _properties = {"dict_prop1": "_dict_value1", "dict_prop2": "_dict_value2"}

            def __init__(self) -> None:
                self._dict_value1 = "dict value1"
                self._dict_value2 = "dict value2"
                super().__init__()

            @classmethod
            def _construct_properties_map(cls) -> None:
                cls._properties_map.append(["_properties", cls._dictionary_to_properties, cls._default_functions_factory])

        # Create an instance
        obj = DictPropertiesTest()

        # Verify properties exist
        assert hasattr(obj, "dict_prop1")
        assert hasattr(obj, "dict_prop2")

        # Verify property values
        assert obj.dict_prop1 == "dict value1"
        assert obj.dict_prop2 == "dict value2"

        # Modify property values
        obj.dict_prop1 = "new dict value1"
        obj.dict_prop2 = "new dict value2"

        # Verify modified values
        assert obj._dict_value1 == "new dict value1"
        assert obj._dict_value2 == "new dict value2"
        assert obj.dict_prop1 == "new dict value1"
        assert obj.dict_prop2 == "new dict value2"

    def test_missing_attribute(self) -> None:
        """Test that an AttributeError is raised when a required attribute is missing.

        This test verifies that an AttributeError is raised when trying to construct properties with a missing
        attribute.
        """
        # The AttributeError is raised during class creation, not instance creation
        with pytest.raises(AttributeError):
            # Create a class with a missing attribute
            class MissingAttributeTest(AutomaticProperties):
                _properties_map_cls = []
                # _properties is missing

                @classmethod
                def _construct_properties_map(cls) -> None:
                    # Use a non-existent attribute name to trigger AttributeError
                    cls._properties_map.append(["_non_existent_attribute", cls._dictionary_to_properties, cls._default_functions_factory])


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
