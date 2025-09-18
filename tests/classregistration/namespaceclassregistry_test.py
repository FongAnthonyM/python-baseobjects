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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.testsuite.classregistration.baseclassregistrytestsuite import BaseClassRegistryTestSuite


# Definitions #
# Classes #
class TestNamespaceClassRegistry(BaseClassRegistryTestSuite):
    """Tests the NamespaceClassRegistry, which is a registry for classes in namespaces.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[NamespaceClassRegistry] = NamespaceClassRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def populated_registry(self, *args: Any, **kwargs: Any) -> NamespaceClassRegistry:
        """Create a populated test registry for use in tests_old_.

        Returns:
            NamespaceClassRegistry: A populated instance of the test class.
        """
        registry = self.create_test_registry(*args, **kwargs)
        registry.register_class(
            self.ExampleClass1,  
            namespace="test_namespace", 
            name="ExampleClass1",
        )
        registry.register_class(
            self.ExampleClass2,   
            namespace="test_namespace", 
            name="ExampleClass2",
            class_kwargs={"arg1": "value1"},
        )
        return registry
    
    # Tests
    def test_init_with_classes_dict(self) -> None:
        """Test initializing with a classes dictionary."""
        classes = {
            "test_namespace": {
                "ExampleClass1": (self.ExampleClass1, {}),
                "ExampleClass2": (self.ExampleClass2, {"arg1": "value1"}),
            }
        }
        registry = self.TestClass(classes=classes)

        # Verify classes were added
        assert "test_namespace" in registry
        assert "ExampleClass1" in registry["test_namespace"]
        assert "ExampleClass2" in registry["test_namespace"]
        assert registry["test_namespace"]["ExampleClass1"][0] == self.ExampleClass1
        assert registry["test_namespace"]["ExampleClass2"][0] == self.ExampleClass2
        assert registry["test_namespace"]["ExampleClass2"][1] == {"arg1": "value1"}

    def test_init_with_classes_iterable(self) -> None:
        """Test initializing with a classes iterable."""
        classes = [
            (self.ExampleClass1, "test_namespace", "ExampleClass1", {}),
            (self.ExampleClass2, "test_namespace", "ExampleClass2", {"arg1": "value1"}),
        ]
        registry = self.TestClass(classes=classes)

        # Verify classes were added
        assert "test_namespace" in registry
        assert "ExampleClass1" in registry["test_namespace"]
        assert "ExampleClass2" in registry["test_namespace"]
        assert registry["test_namespace"]["ExampleClass1"][0] == self.ExampleClass1
        assert registry["test_namespace"]["ExampleClass2"][0] == self.ExampleClass2
        assert registry["test_namespace"]["ExampleClass2"][1] == {"arg1": "value1"}
    
    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Test the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to use in testing the register_class method.
            **kwargs: Keyword arguments to pass to use in testing the register_class method.
        """
        # Register a class
        test_registry = self.create_test_registry(*args, **kwargs)
        test_registry.register_class(self.ExampleClass1, namespace="test_namespace", name="ExampleClass1")

        # Verify
        assert "test_namespace" in test_registry
        assert "ExampleClass1" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["ExampleClass1"][0] == self.ExampleClass1
        assert test_registry["test_namespace"]["ExampleClass1"][1] == {}

    def test_register_classes(self, *args: Any, **kwargs: Any) -> None:
        """Test registering multiple classes.
        
         Args:
            *args: Positional arguments to pass to use in testing the register_classes method.
            **kwargs: Keyword arguments to pass to use in testing the register_classes method.
        """
        # Register multiple classes
        test_registry = self.create_test_registry(*args, **kwargs)
        classes = [
            (self.ExampleClass1, "test_namespace", "ExampleClass1", {}),
            (self.ExampleClass2, "test_namespace", "ExampleClass2", {"arg1": "value1"}),
        ]
        test_registry.register_classes(classes)

        # Verify classes were registered
        assert "test_namespace" in test_registry
        assert "ExampleClass1" in test_registry["test_namespace"]
        assert "ExampleClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["ExampleClass1"][0] == self.ExampleClass1
        assert test_registry["test_namespace"]["ExampleClass2"][0] == self.ExampleClass2
        assert test_registry["test_namespace"]["ExampleClass2"][1] == {"arg1": "value1"}

    def test_get_class(self, populated_registry: NamespaceClassRegistry, *args: Any, **kwargs: Any) -> None:
        """Test the get_class method.

        This test verifies that the get_class method correctly retrieves a registered class.

        Args:
            *args: Positional arguments to pass to use in testing the get_class method.
            **kwargs: Keyword arguments to pass to use in testing the get_class method.
        """
        cls = populated_registry.get_class("test_namespace", "ExampleClass1")

        # Verify class was retrieved
        assert cls == self.ExampleClass1

    def test_get_class_with_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a class with keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a class with keyword arguments
        cls_and_kwargs = populated_registry.get_class("test_namespace", "ExampleClass2", with_kwargs=True)

        # Verify class and keyword arguments were retrieved
        assert cls_and_kwargs[0] == self.ExampleClass2
        assert cls_and_kwargs[1] == {"arg1": "value1"}

    def test_get_class_with_default(self, *args: Any, **kwargs: Any) -> None:
        """Test getting a non-existent class with a default value.

        Args:
            *args: Positional arguments to pass to use in testing the get_classes method.
            **kwargs: Keyword arguments to pass to use in testing the get_classes method.
        """
        # Get a non-existent class with a default value
        test_registry = self.create_test_registry(*args, **kwargs)
        default = object()
        cls = test_registry.get_class("non_existent_namespace", "NonExistentClass", default=default)

        # Verify default was returned
        assert cls is default

    def test_get_class_raises_key_error(self, *args: Any, **kwargs: Any) -> None:
        """Test that getting a non-existent class raises a KeyError.

        Args:
            *args: Positional arguments to pass to use in testing the get_classes method.
            **kwargs: Keyword arguments to pass to use in testing the get_classes method.
        """
        # Verify getting a non-existent class raises a KeyError
        test_registry = self.create_test_registry(*args, **kwargs)
        with pytest.raises(KeyError):
            test_registry.get_class("non_existent_namespace", "NonExistentClass")

    def test_get_new(self, populated_registry: NamespaceClassRegistry) -> None:
        """Test getting a new instance of a class.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a new instance of a class
        instance = populated_registry.get_new("test_namespace", "ExampleClass1")

        # Verify instance was created
        assert isinstance(instance, self.ExampleClass1)

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

    def test_update_classes(self, *args: Any, **kwargs: Any) -> None:
        """Test updating classes.

        Args:
            *args: Positional arguments to pass to use in testing the update_classes method.
            **kwargs: Keyword arguments to pass to use in testing the update_classes method.
        """
        # Update classes
        test_registry = self.create_test_registry(*args, **kwargs)
        classes = {
            "test_namespace": {
                "ExampleClass1": (self.ExampleClass1, {}),
                "ExampleClass2": (self.ExampleClass2, {"arg1": "value1"}),
            }
        }
        test_registry.update_classes(classes)

        # Verify classes were updated
        assert "test_namespace" in test_registry
        assert "ExampleClass1" in test_registry["test_namespace"]
        assert "ExampleClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["ExampleClass1"][0] == self.ExampleClass1
        assert test_registry["test_namespace"]["ExampleClass2"][0] == self.ExampleClass2
        assert test_registry["test_namespace"]["ExampleClass2"][1] == {"arg1": "value1"}


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
