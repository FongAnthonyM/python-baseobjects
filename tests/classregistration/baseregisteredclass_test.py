#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baseregisteredclass_test.py
Tests for the BaseRegisteredClass class in the baseobjects package.
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
from typing import Any, ClassVar, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.classregistration import BaseRegisteredClass, BaseClassRegistry
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
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

class TestBaseRegisteredClass(BaseBaseObjectTest):
    """Test the BaseRegisteredClass class.

    This class tests the functionality of the BaseRegisteredClass class, which is an abstract class
    that registers subclasses, allowing subclass dispatching. It creates test subclasses of
    BaseRegisteredClass to test with since BaseRegisteredClass is abstract.
    """

    # Class Definitions #
    class BaseTestRegisteredClass(BaseRegisteredClass):
        """A base test subclass of BaseRegisteredClass for testing purposes."""

        # Class Attributes #
        class_registry_type: ClassVar[Type[BaseClassRegistry]] = ConcreteClassRegistry

        @classmethod
        def register_class(cls, *args: Any, **kwargs: Any) -> None:
            """Registers this class with the registry.

            Args:
                *args: Positional arguments.
                **kwargs: Keyword arguments.
            """
            if cls.class_registry is not None:
                cls.class_registry.register_class(cls)

        @classmethod
        def get_registered_class(cls, name: str, default: Any = None) -> Optional["BaseRegisteredClass"]:
            """Gets a subclass from the registry.

            Args:
                name: The name of the class to get.
                default: The default value to return if the class is not found.

            Returns:
                The requested subclass or the default value.
            """
            if cls.class_registry is None:
                return default
            return cls.class_registry.get_class(name, default)

    # Attributes #
    class_: Type[BaseTestRegisteredClass] = BaseTestRegisteredClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_instance(self) -> "TestBaseRegisteredClass.BaseTestRegisteredClass":
        """Create a test instance for use in tests.

        Returns:
            BaseTestRegisteredClass: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTestRegisteredClass can be created."""
        instance = self.class_()
        assert instance is not None
        assert isinstance(instance, BaseRegisteredClass)

    def test_create_class_registry(self) -> None:
        """Test creating a class registry."""
        # Reset class registry for testing
        self.class_.class_registry = None

        # Create class registry
        self.class_.create_class_registry()

        # Verify class registry was created
        assert self.class_.class_registry is not None
        assert isinstance(self.class_.class_registry, BaseClassRegistry)
        assert self.class_.class_registry.head_class == self.class_

    def test_register_class(self) -> None:
        """Test registering a class."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Register class
        self.class_.register_class()

        # Verify class was registered
        assert self.class_.__name__ in self.class_.class_registry
        assert self.class_.class_registry[self.class_.__name__] == self.class_

    def test_get_registered_class(self) -> None:
        """Test getting a registered class."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()
        self.class_.register_class()

        # Get registered class
        retrieved_class = self.class_.get_registered_class(self.class_.__name__)

        # Verify class was retrieved
        assert retrieved_class == self.class_

    def test_get_registered_class_with_default(self) -> None:
        """Test getting a non-existent registered class with a default value."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Get non-existent registered class with default
        default = object()
        retrieved = self.class_.get_registered_class("NonExistentClass", default=default)

        # Verify default was returned
        assert retrieved is default

    def test_init_subclass_with_registration(self) -> None:
        """Test that subclasses are registered when class_registration is True."""
        # Create a subclass with registration enabled
        class RegisteredSubclass(self.class_):
            class_registration = True

        # Verify subclass was registered
        assert RegisteredSubclass.__name__ in self.class_.class_registry
        assert self.class_.class_registry[RegisteredSubclass.__name__] == RegisteredSubclass

    def test_init_subclass_without_registration(self) -> None:
        """Test that subclasses are not registered when class_registration is False."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Create a subclass with registration disabled
        class UnregisteredSubclass(self.class_):
            class_registration = False

        # Verify subclass was not registered
        assert UnregisteredSubclass.__name__ not in self.class_.class_registry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
