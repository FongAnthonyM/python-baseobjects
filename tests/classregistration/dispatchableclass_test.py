#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dispatchableclass_test.py
Tests for the DispatchableClass class in the baseobjects package.
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
from typing import Any, ClassVar, Optional, Type, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.classregistration import DispatchableClass, BaseClassRegistry
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

class TestDispatchableClass(BaseBaseObjectTest):
    """Test the DispatchableClass class.

    This class tests the functionality of the DispatchableClass class, which is an abstract class
    that dispatches to subclasses based on arguments. It creates test subclasses of
    DispatchableClass to test with since DispatchableClass is abstract.
    """

    # Class Definitions #
    class BaseTestDispatchableClass(DispatchableClass):
        """A base test subclass of DispatchableClass for testing purposes."""

        # Class Attributes #
        class_registry_type: ClassVar[Type[BaseClassRegistry]] = ConcreteClassRegistry
        class_registration: ClassVar[bool] = True

        @classmethod
        def get_class_information(cls, *args: Any, **kwargs: Any) -> Tuple[str]:
            """Gets a class's lookup information from a given set of arguments.

            Args:
                *args: Positional arguments to get the name from.
                **kwargs: Keyword arguments to get the name from.

            Returns:
                A tuple containing the class name to look up.
            """
            if args and isinstance(args[0], str):
                return (args[0],)
            if "type" in kwargs and isinstance(kwargs["type"], str):
                return (kwargs["type"],)
            return (cls.__name__,)

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
        def get_registered_class(cls, name: str, default: Any = None) -> Optional["DispatchableClass"]:
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

    class TypeADispatchable(BaseTestDispatchableClass):
        """A subclass of BaseTestDispatchableClass for testing dispatching to type A."""
        class_registration = True

    class TypeBDispatchable(BaseTestDispatchableClass):
        """A subclass of BaseTestDispatchableClass for testing dispatching to type B."""
        class_registration = True

    # Attributes #
    class_: Type[BaseTestDispatchableClass] = BaseTestDispatchableClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_instance(self) -> "TestDispatchableClass.BaseTestDispatchableClass":
        """Create a test instance for use in tests.

        Returns:
            BaseTestDispatchableClass: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTestDispatchableClass can be created."""
        instance = self.class_()
        assert instance is not None
        assert isinstance(instance, DispatchableClass)

    def test_get_class_information(self) -> None:
        """Test the get_class_information method."""
        # Test with positional argument
        info = self.class_.get_class_information("TypeADispatchable")
        assert info == ("TypeADispatchable",)

        # Test with keyword argument
        info = self.class_.get_class_information(type="TypeBDispatchable")
        assert info == ("TypeBDispatchable",)

        # Test with no relevant arguments
        info = self.class_.get_class_information(123, irrelevant="value")
        assert info == (self.class_.__name__,)

    def test_dispatch_with_positional_arg(self) -> None:
        """Test dispatching with a positional argument."""
        # Create instance with type name as positional argument
        instance = self.class_("TypeADispatchable")

        # Verify instance is of the correct type
        assert isinstance(instance, self.TypeADispatchable)

    def test_dispatch_with_keyword_arg(self) -> None:
        """Test dispatching with a keyword argument."""
        # Create instance with type name as keyword argument
        instance = self.class_(type="TypeBDispatchable")

        # Verify instance is of the correct type
        assert isinstance(instance, self.TypeBDispatchable)

    def test_dispatch_with_unknown_type(self) -> None:
        """Test dispatching with an unknown type."""
        # Create instance with unknown type name
        instance = self.class_("UnknownType")

        # Verify instance is of the base type
        assert isinstance(instance, self.class_)
        assert type(instance) is self.class_

    def test_dispatch_from_subclass(self) -> None:
        """Test that dispatching doesn't happen when called from a subclass."""
        # Create instance from subclass with type name that would dispatch to a different subclass
        instance = self.TypeADispatchable("TypeBDispatchable")

        # Verify instance is of the calling type, not the dispatched type
        assert isinstance(instance, self.TypeADispatchable)
        assert not isinstance(instance, self.TypeBDispatchable)

    def test_no_dispatch_without_args(self) -> None:
        """Test that dispatching doesn't happen when no arguments are provided."""
        # Create instance without arguments
        instance = self.class_()

        # Verify instance is of the base type
        assert isinstance(instance, self.class_)
        assert type(instance) is self.class_


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
