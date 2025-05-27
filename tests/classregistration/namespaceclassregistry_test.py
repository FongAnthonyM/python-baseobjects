#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" namespaceclassregistry_test.py
Tests for the NamespaceClassRegistry class in the baseobjects package.
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
from typing import Any, Type, Dict, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.classregistration import NamespaceClassRegistry
from src.baseobjects.bases import SEARCHSENTINEL
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
class TestNamespaceClassRegistry(BaseBaseObjectTest):
    """Test the NamespaceClassRegistry class.

    This class tests the functionality of the NamespaceClassRegistry class, which is a registry for classes
    in namespaces.
    """

    # Class Definitions #
    class TestClass1:
        """A test class for testing the registry."""
        pass

    class TestClass2:
        """Another test class for testing the registry."""
        pass

    # Attributes #
    class_: Type[NamespaceClassRegistry] = NamespaceClassRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_registry(self) -> NamespaceClassRegistry:
        """Create a test registry instance for use in tests.

        Returns:
            NamespaceClassRegistry: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def populated_registry(self) -> NamespaceClassRegistry:
        """Create a populated test registry for use in tests.

        Returns:
            NamespaceClassRegistry: A populated instance of the test class.
        """
        registry = self.class_()
        registry.register_class(self.TestClass1, namespace="test_namespace", name="TestClass1")
        registry.register_class(self.TestClass2, namespace="test_namespace", name="TestClass2", 
                               class_kwargs={"arg1": "value1"})
        return registry

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of NamespaceClassRegistry can be created."""
        registry = self.class_()
        assert registry is not None
        assert isinstance(registry, NamespaceClassRegistry)

    def test_init_with_classes_dict(self) -> None:
        """Test initializing with a classes dictionary."""
        classes = {
            "test_namespace": {
                "TestClass1": (self.TestClass1, {}),
                "TestClass2": (self.TestClass2, {"arg1": "value1"}),
            }
        }
        registry = self.class_(classes=classes)
        
        # Verify classes were added
        assert "test_namespace" in registry
        assert "TestClass1" in registry["test_namespace"]
        assert "TestClass2" in registry["test_namespace"]
        assert registry["test_namespace"]["TestClass1"][0] == self.TestClass1
        assert registry["test_namespace"]["TestClass2"][0] == self.TestClass2
        assert registry["test_namespace"]["TestClass2"][1] == {"arg1": "value1"}

    def test_init_with_classes_iterable(self) -> None:
        """Test initializing with a classes iterable."""
        classes = [
            (self.TestClass1, "test_namespace", "TestClass1", {}),
            (self.TestClass2, "test_namespace", "TestClass2", {"arg1": "value1"}),
        ]
        registry = self.class_(classes=classes)
        
        # Verify classes were added
        assert "test_namespace" in registry
        assert "TestClass1" in registry["test_namespace"]
        assert "TestClass2" in registry["test_namespace"]
        assert registry["test_namespace"]["TestClass1"][0] == self.TestClass1
        assert registry["test_namespace"]["TestClass2"][0] == self.TestClass2
        assert registry["test_namespace"]["TestClass2"][1] == {"arg1": "value1"}

    def test_register_class(self, test_registry: NamespaceClassRegistry) -> None:
        """Test registering a class.

        Args:
            test_registry: A test registry instance.
        """
        # Register a class
        test_registry.register_class(self.TestClass1, namespace="test_namespace", name="TestClass1")
        
        # Verify class was registered
        assert "test_namespace" in test_registry
        assert "TestClass1" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["TestClass1"][0] == self.TestClass1
        assert test_registry["test_namespace"]["TestClass1"][1] == {}

    def test_register_class_with_kwargs(self, test_registry: NamespaceClassRegistry) -> None:
        """Test registering a class with keyword arguments.

        Args:
            test_registry: A test registry instance.
        """
        # Register a class with keyword arguments
        test_registry.register_class(
            self.TestClass2, namespace="test_namespace", name="TestClass2", class_kwargs={"arg1": "value1"}
        )
        
        # Verify class was registered with keyword arguments
        assert "test_namespace" in test_registry
        assert "TestClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["TestClass2"][0] == self.TestClass2
        assert test_registry["test_namespace"]["TestClass2"][1] == {"arg1": "value1"}

    def test_register_class_default_namespace_and_name(self, test_registry: NamespaceClassRegistry) -> None:
        """Test registering a class with default namespace and name.

        Args:
            test_registry: A test registry instance.
        """
        # Register a class without specifying namespace and name
        test_registry.register_class(self.TestClass1)
        
        # Verify class was registered with default namespace and name
        assert self.TestClass1.__module__ in test_registry
        assert self.TestClass1.__name__ in test_registry[self.TestClass1.__module__]
        assert test_registry[self.TestClass1.__module__][self.TestClass1.__name__][0] == self.TestClass1

    def test_register_classes(self, test_registry: NamespaceClassRegistry) -> None:
        """Test registering multiple classes.

        Args:
            test_registry: A test registry instance.
        """
        # Register multiple classes
        classes = [
            (self.TestClass1, "test_namespace", "TestClass1", {}),
            (self.TestClass2, "test_namespace", "TestClass2", {"arg1": "value1"}),
        ]
        test_registry.register_classes(classes)
        
        # Verify classes were registered
        assert "test_namespace" in test_registry
        assert "TestClass1" in test_registry["test_namespace"]
        assert "TestClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["TestClass1"][0] == self.TestClass1
        assert test_registry["test_namespace"]["TestClass2"][0] == self.TestClass2
        assert test_registry["test_namespace"]["TestClass2"][1] == {"arg1": "value1"}

    def test_update_classes(self, test_registry: NamespaceClassRegistry) -> None:
        """Test updating classes.

        Args:
            test_registry: A test registry instance.
        """
        # Update classes
        classes = {
            "test_namespace": {
                "TestClass1": (self.TestClass1, {}),
                "TestClass2": (self.TestClass2, {"arg1": "value1"}),
            }
        }
        test_registry.update_classes(classes)
        
        # Verify classes were updated
        assert "test_namespace" in test_registry
        assert "TestClass1" in test_registry["test_namespace"]
        assert "TestClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["TestClass1"][0] == self.TestClass1
        assert test_registry["test_namespace"]["TestClass2"][0] == self.TestClass2
        assert test_registry["test_namespace"]["TestClass2"][1] == {"arg1": "value1"}

    def test_get_class(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a class.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a class
        cls = populated_registry.get_class("test_namespace", "TestClass1")
        
        # Verify class was retrieved
        assert cls == self.TestClass1

    def test_get_class_with_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a class with keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a class with keyword arguments
        cls_and_kwargs = populated_registry.get_class("test_namespace", "TestClass2", with_kwargs=True)
        
        # Verify class and keyword arguments were retrieved
        assert cls_and_kwargs[0] == self.TestClass2
        assert cls_and_kwargs[1] == {"arg1": "value1"}

    def test_get_class_with_default(self, test_registry: NamespaceClassRegistry) -> None:
        """Test getting a non-existent class with a default value.

        Args:
            test_registry: A test registry instance.
        """
        # Get a non-existent class with a default value
        default = object()
        cls = test_registry.get_class("non_existent_namespace", "NonExistentClass", default=default)
        
        # Verify default was returned
        assert cls is default

    def test_get_class_raises_key_error(self, test_registry: NamespaceClassRegistry) -> None:
        """Test that getting a non-existent class raises a KeyError.

        Args:
            test_registry: A test registry instance.
        """
        # Verify getting a non-existent class raises a KeyError
        with pytest.raises(KeyError):
            test_registry.get_class("non_existent_namespace", "NonExistentClass")

    def test_get_new(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a new instance of a class.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a new instance of a class
        instance = populated_registry.get_new("test_namespace", "TestClass1")
        
        # Verify instance was created
        assert isinstance(instance, self.TestClass1)

    def test_get_new_with_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a new instance of a class with keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """
        # Create a class that accepts keyword arguments
        class TestClassWithKwargs:
            def __init__(self, arg1=None, arg2=None):
                self.arg1 = arg1
                self.arg2 = arg2
        
        # Register the class
        populated_registry.register_class(
            TestClassWithKwargs, namespace="test_namespace", name="TestClassWithKwargs",
            class_kwargs={"arg1": "default_value"}
        )
        
        # Get a new instance with additional keyword arguments
        instance = populated_registry.get_new(
            "test_namespace", "TestClassWithKwargs", class_kwargs={"arg2": "custom_value"}
        )
        
        # Verify instance was created with merged keyword arguments
        assert isinstance(instance, TestClassWithKwargs)
        assert instance.arg1 == "default_value"
        assert instance.arg2 == "custom_value"

    def test_get_new_without_default_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a new instance of a class without using default keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """
        # Create a class that accepts keyword arguments
        class TestClassWithKwargs:
            def __init__(self, arg1=None, arg2=None):
                self.arg1 = arg1
                self.arg2 = arg2
        
        # Register the class
        populated_registry.register_class(
            TestClassWithKwargs, namespace="test_namespace", name="TestClassWithKwargs",
            class_kwargs={"arg1": "default_value"}
        )
        
        # Get a new instance without using default keyword arguments
        instance = populated_registry.get_new(
            "test_namespace", "TestClassWithKwargs", with_kwargs=False,
            class_kwargs={"arg2": "custom_value"}
        )
        
        # Verify instance was created with only the provided keyword arguments
        assert isinstance(instance, TestClassWithKwargs)
        assert instance.arg1 is None
        assert instance.arg2 == "custom_value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])