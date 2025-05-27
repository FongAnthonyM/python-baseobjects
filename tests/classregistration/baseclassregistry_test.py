#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baseclassregistry_test.py
Tests for the BaseClassRegistry class in the baseobjects package.
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
from src.baseobjects.classregistration import BaseClassRegistry
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
class TestBaseClassRegistry(BaseBaseObjectTest):
    """Test the BaseClassRegistry class.

    This class tests the functionality of the BaseClassRegistry class, which is a registry for classes. It creates a
    test subclass of BaseClassRegistry to test with since BaseClassRegistry is abstract.
    """

    # Class Definitions #
    class ConcreteClassRegistry(BaseClassRegistry):
        """A concrete subclass of BaseClassRegistry for testing purposes."""
        
        def register_class(self, cls: type, *args: Any, **kwargs: Any) -> None:
            """Registers a class with the registry.

            Args:
                cls: The class to register.
                *args: Positional arguments.
                **kwargs: Keyword arguments.
            """
            self[cls.__name__] = cls
        
        def get_class(self, name: str, default: Any = None) -> Any:
            """Gets a class from the registry.

            Args:
                name: The name of the class to get.
                default: The default value to return if the class is not found.

            Returns:
                The requested class or the default value.
            """
            return self.get(name, default)

    # Attributes #
    class_: Type[ConcreteClassRegistry] = ConcreteClassRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_registry(self) -> "TestBaseClassRegistry.ConcreteClassRegistry":
        """Create a test registry instance for use in tests.

        Returns:
            ConcreteClassRegistry: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def test_class(self) -> Type:
        """Create a test class for use in tests.

        Returns:
            Type: A test class.
        """
        class TestClass:
            pass
        return TestClass

    @pytest.fixture
    def populated_registry(self, test_registry: "TestBaseClassRegistry.ConcreteClassRegistry", test_class: Type) -> "TestBaseClassRegistry.ConcreteClassRegistry":
        """Create a populated test registry for use in tests.

        Args:
            test_registry: A test registry instance.
            test_class: A test class.

        Returns:
            ConcreteClassRegistry: A populated test registry.
        """
        test_registry.register_class(test_class)
        return test_registry

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of ConcreteClassRegistry can be created."""
        registry = self.class_()
        assert registry is not None
        assert isinstance(registry, BaseClassRegistry)

    def test_init_with_head_class(self, test_class: Type) -> None:
        """Test initializing with a head class.

        Args:
            test_class: A test class.
        """
        registry = self.class_(head_class=test_class)
        assert registry.head_class == test_class

    def test_construct(self, test_registry: "TestBaseClassRegistry.ConcreteClassRegistry", test_class: Type) -> None:
        """Test the construct method.

        Args:
            test_registry: A test registry instance.
            test_class: A test class.
        """
        test_registry.construct(head_class=test_class)
        assert test_registry.head_class == test_class

    def test_register_class(self, test_registry: "TestBaseClassRegistry.ConcreteClassRegistry", test_class: Type) -> None:
        """Test registering a class.

        Args:
            test_registry: A test registry instance.
            test_class: A test class.
        """
        test_registry.register_class(test_class)
        assert test_class.__name__ in test_registry
        assert test_registry[test_class.__name__] == test_class

    def test_get_class(self, populated_registry: "TestBaseClassRegistry.ConcreteClassRegistry", test_class: Type) -> None:
        """Test getting a class from the registry.

        Args:
            populated_registry: A populated test registry.
            test_class: A test class.
        """
        retrieved_class = populated_registry.get_class(test_class.__name__)
        assert retrieved_class == test_class

    def test_get_class_with_default(self, test_registry: "TestBaseClassRegistry.ConcreteClassRegistry") -> None:
        """Test getting a non-existent class with a default value.

        Args:
            test_registry: A test registry instance.
        """
        default = object()
        retrieved = test_registry.get_class("NonExistentClass", default=default)
        assert retrieved is default


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])