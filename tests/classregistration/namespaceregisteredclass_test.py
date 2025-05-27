#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the NamespaceRegisteredClass class in the baseobjects package.

This module contains unit tests for the NamespaceRegisteredClass class, which is an abstract class that registers
subclasses with namespaces, allowing subclass dispatching.
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
from src.baseobjects.classregistration import NamespaceRegisteredClass, NamespaceClassRegistry
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
# Class Definitions #
class TestNamespaceClassRegistry(NamespaceClassRegistry):
    """A custom NamespaceClassRegistry for testing purposes."""

    def register_classes(self, cls: type, namespace: str, name: str, class_kwargs: dict[str, Any] = None) -> None:
        """Registers a class with the given namespace and name.

        This method is overridden to handle the way it's called in NamespaceRegisteredClass.

        Args:
            cls: The class to register.
            namespace: The namespace of the class.
            name: The name of the class.
            class_kwargs: The keyword arguments for creating the class.
        """
        if class_kwargs is None:
            class_kwargs = {}
        self.register_class(cls, namespace, name, class_kwargs)

class TestNamespaceRegisteredClass(BaseBaseObjectTest):
    """Test the NamespaceRegisteredClass class.

    This class tests the functionality of the NamespaceRegisteredClass class, which is an abstract class that registers
    subclasses with namespaces, allowing subclass dispatching. It creates test subclasses of NamespaceRegisteredClass to
    test with.

    Attributes:
        class_: The test class to use for testing, an instance of BaseTestNamespaceRegisteredClass.
    """

    # Class Definitions #
    class BaseTestNamespaceRegisteredClass(NamespaceRegisteredClass):
        """A base test subclass of NamespaceRegisteredClass for testing purposes."""

        # Class Attributes #
        class_registry_type: ClassVar[Type[NamespaceClassRegistry]] = TestNamespaceClassRegistry
        class_registration: ClassVar[bool] = True

    # Attributes #
    class_: Type[BaseTestNamespaceRegisteredClass] = BaseTestNamespaceRegisteredClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_instance(self) -> "TestNamespaceRegisteredClass.BaseTestNamespaceRegisteredClass":
        """Create a test instance for use in tests.

        Returns:
            An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTestNamespaceRegisteredClass can be created."""
        instance = self.class_()
        assert instance is not None
        assert isinstance(instance, NamespaceRegisteredClass)

    def test_class_registry_type(self) -> None:
        """Test that the class_registry_type is TestNamespaceClassRegistry."""
        assert self.class_.class_registry_type == TestNamespaceClassRegistry

    def test_init_subclass_with_registration(self) -> None:
        """Test that subclasses are registered when class_registration is True."""
        # Create a subclass with registration enabled
        class RegisteredSubclass(self.class_):
            class_registration = True

        # Verify subclass was registered
        namespace = RegisteredSubclass.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert RegisteredSubclass.class_registry is not None
        assert namespace in RegisteredSubclass.class_registry
        assert "RegisteredSubclass" in RegisteredSubclass.class_registry[namespace]
        assert RegisteredSubclass.class_registry[namespace]["RegisteredSubclass"][0] == RegisteredSubclass

    def test_init_subclass_with_custom_namespace_and_name(self) -> None:
        """Test that subclasses are registered with custom namespace and name."""
        # Create a subclass with custom namespace and name
        class CustomNamespaceAndNameClass(self.class_, namespace="custom_namespace", name="CustomName"):
            class_registration = True

        # Verify subclass was registered with custom namespace and name
        assert CustomNamespaceAndNameClass.class_registry is not None
        assert "custom_namespace" in CustomNamespaceAndNameClass.class_registry
        assert "CustomName" in CustomNamespaceAndNameClass.class_registry["custom_namespace"]
        assert CustomNamespaceAndNameClass.class_registry["custom_namespace"]["CustomName"][0] == CustomNamespaceAndNameClass

    def test_init_subclass_with_class_registry_namespace_and_name(self) -> None:
        """Test that subclasses are registered with class_registry_namespace and class_registry_name."""
        # Create a subclass with class_registry_namespace and class_registry_name
        class ClassRegistryNamespaceAndNameClass(self.class_):
            class_registration = True
            class_registry_namespace = "registry_namespace"
            class_registry_name = "RegistryName"

        # Verify subclass was registered with class_registry_namespace and class_registry_name
        assert ClassRegistryNamespaceAndNameClass.class_registry is not None
        assert "registry_namespace" in ClassRegistryNamespaceAndNameClass.class_registry
        assert "RegistryName" in ClassRegistryNamespaceAndNameClass.class_registry["registry_namespace"]
        assert ClassRegistryNamespaceAndNameClass.class_registry["registry_namespace"]["RegistryName"][0] == ClassRegistryNamespaceAndNameClass

    def test_init_subclass_without_registration(self) -> None:
        """Test that subclasses are not registered when class_registration is False."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Create a subclass with registration disabled
        class UnregisteredSubclass(self.class_):
            class_registration = False

        # Verify subclass was not registered
        namespace = UnregisteredSubclass.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert UnregisteredSubclass.class_registry is not None
        if namespace in UnregisteredSubclass.class_registry:
            assert "UnregisteredSubclass" not in UnregisteredSubclass.class_registry[namespace]

    def test_register_class(self) -> None:
        """Test registering a class."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Register class
        self.class_.register_class(namespace="test_namespace", name="TestClass")

        # Verify class was registered
        assert "test_namespace" in self.class_.class_registry
        assert "TestClass" in self.class_.class_registry["test_namespace"]
        assert self.class_.class_registry["test_namespace"]["TestClass"][0] == self.class_

    def test_register_class_with_default_namespace_and_name(self) -> None:
        """Test registering a class with default namespace and name."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Register class without specifying namespace and name
        self.class_.register_class()

        # Verify class was registered with default namespace and name
        namespace = self.class_.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert namespace in self.class_.class_registry
        assert self.class_.__name__ in self.class_.class_registry[namespace]
        assert self.class_.class_registry[namespace][self.class_.__name__][0] == self.class_

    def test_get_registered_class(self) -> None:
        """Test getting a registered class."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Register class
        self.class_.register_class(namespace="test_namespace", name="TestClass")

        # Get registered class
        retrieved_class = self.class_.get_registered_class("test_namespace", "TestClass")

        # Verify class was retrieved
        assert retrieved_class == self.class_

    def test_get_registered_class_with_nonexistent_class(self) -> None:
        """Test getting a non-existent registered class."""
        # Reset class registry for testing
        self.class_.class_registry = None
        self.class_.create_class_registry()

        # Get non-existent registered class
        with pytest.raises(KeyError):
            retrieved_class = self.class_.get_registered_class("non_existent_namespace", "NonExistentClass")

    def test_module_attribute(self) -> None:
        """Test the _module_ attribute."""
        # Create a subclass with _module_ attribute
        class ModuleAttributeClass(self.class_):
            class_registration = True
            _module_ = "custom_module"

        # Reset class registry for testing
        ModuleAttributeClass.class_registry = None
        ModuleAttributeClass.create_class_registry()

        # Register class without specifying namespace
        ModuleAttributeClass.register_class()

        # Verify class was registered with _module_ as namespace
        assert "custom_module" in ModuleAttributeClass.class_registry
        assert ModuleAttributeClass.__name__ in ModuleAttributeClass.class_registry["custom_module"]
        assert ModuleAttributeClass.class_registry["custom_module"][ModuleAttributeClass.__name__][0] == ModuleAttributeClass


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
