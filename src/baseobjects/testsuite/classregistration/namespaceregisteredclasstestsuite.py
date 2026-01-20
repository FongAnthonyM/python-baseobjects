"""namespaceregisteredclasstestsuite.py
Base test suite for NamespaceRegisteredClass and its subclasses.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import NamespaceRegisteredClass
from .baseregisteredclasstestsuite import BaseRegisteredClassTestSuite


# Definitions #
# Classes #
class NamespaceRegisteredClassTestSuite(BaseRegisteredClassTestSuite):
    """Base test suite for children of NamespaceRegisteredClass.

    This class provides common test functionality for child classes of NamespaceRegisteredClass, including tests for
    namespace-based class registration and retrieval. Subclasses should set the UnitTestClass attribute and may override
    or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: ClassVar[type[NamespaceRegisteredClass]]

    # Tests #
    def test_init_subclass_with_registration(self) -> None:
        """Tests that subclasses are registered when class_registration is True."""

        # Create a subclass with registration enabled
        class RegisteredSubclass(self.UnitTestClass):  # type: ignore[misc, name-defined]
            class_registration = True

        # Verify subclass was registered
        namespace = RegisteredSubclass.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert RegisteredSubclass.class_registry is not None
        assert namespace in RegisteredSubclass.class_registry
        assert "RegisteredSubclass" in RegisteredSubclass.class_registry[namespace]
        assert RegisteredSubclass.class_registry[namespace]["RegisteredSubclass"][0] == RegisteredSubclass

    def test_init_subclass_with_custom_namespace_and_name(self) -> None:
        """Tests that subclasses are registered with custom namespace and name."""

        # Create a subclass with custom namespace and name
        class CustomNamespaceAndNameClass(self.UnitTestClass, namespace="custom_namespace", name="CustomName"):  # type: ignore[misc, call-arg, name-defined]
            class_registration = True

        # Verify subclass was registered with custom namespace and name
        assert CustomNamespaceAndNameClass.class_registry is not None
        assert "custom_namespace" in CustomNamespaceAndNameClass.class_registry
        assert "CustomName" in CustomNamespaceAndNameClass.class_registry["custom_namespace"]
        assert (
            CustomNamespaceAndNameClass.class_registry["custom_namespace"]["CustomName"][0]
            == CustomNamespaceAndNameClass
        )

    def test_init_subclass_with_class_registry_namespace_and_name(self) -> None:
        """Tests that subclasses are registered with class_registry_namespace and class_registry_name."""

        # Create a subclass with class_registry_namespace and class_registry_name
        class ClassRegistryNamespaceAndNameClass(self.UnitTestClass):  # type: ignore[misc, name-defined]
            class_registration = True
            class_registry_namespace = "registry_namespace"
            class_registry_name = "RegistryName"

        # Verify subclass was registered with class_registry_namespace and class_registry_name
        assert ClassRegistryNamespaceAndNameClass.class_registry is not None
        assert "registry_namespace" in ClassRegistryNamespaceAndNameClass.class_registry
        assert "RegistryName" in ClassRegistryNamespaceAndNameClass.class_registry["registry_namespace"]
        assert (
            ClassRegistryNamespaceAndNameClass.class_registry["registry_namespace"]["RegistryName"][0]
            is ClassRegistryNamespaceAndNameClass
        )

    def test_init_subclass_without_registration(self) -> None:
        """Tests that subclasses are not registered when class_registration is False."""
        # Reset class registry for testing
        self.UnitTestClass.class_registry = None
        self.UnitTestClass.create_class_registry()

        # Create a subclass with registration disabled
        class UnregisteredSubclass(self.UnitTestClass):  # type: ignore[misc, name-defined]
            class_registration = False

        # Verify subclass was not registered
        namespace = UnregisteredSubclass.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert UnregisteredSubclass.class_registry is not None
        if namespace in UnregisteredSubclass.class_registry:
            assert "UnregisteredSubclass" not in UnregisteredSubclass.class_registry[namespace]

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Tests the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to the register_class method.
            **kwargs: Keyword arguments to pass to the register_class method.
        """

        class NewTestSubclass(self.UnitTestClass):  # type: ignore[misc, name-defined]
            class_registration = False

        # Register class
        NewTestSubclass.register_class(namespace="test_namespace", name="NewClass")

        # Verify class was registered
        assert self.UnitTestClass.class_registry is not None
        assert "test_namespace" in self.UnitTestClass.class_registry
        assert "NewClass" in self.UnitTestClass.class_registry["test_namespace"]
        assert self.UnitTestClass.class_registry["test_namespace"]["NewClass"][0] is NewTestSubclass

    def test_get_registered_class(self) -> None:  # type: ignore[override]
        """Tests getting a registered class."""
        # Reset class registry for testing
        self.UnitTestClass.class_registry = None
        self.UnitTestClass.create_class_registry()

        # Register class
        self.UnitTestClass.register_class(namespace="test_namespace", name="UnitTestClass")

        # Get registered class
        retrieved_class = self.UnitTestClass.get_registered_class("test_namespace", "UnitTestClass")

        # Verify class was retrieved
        assert retrieved_class is self.UnitTestClass

    def test_get_registered_class_with_nonexistent_class(self) -> None:
        """Tests getting a non-existent registered class."""
        # Reset class registry for testing
        self.UnitTestClass.class_registry = None
        self.UnitTestClass.create_class_registry()

        # Get non-existent registered class
        with pytest.raises(KeyError):
            self.UnitTestClass.get_registered_class("non_existent_namespace", "NonExistentClass")

    def test_module_attribute(self) -> None:
        """Tests the _module_ attribute."""

        # Create a subclass with _module_ attribute
        class ModuleAttributeClass(self.UnitTestClass):  # type: ignore[misc, name-defined]
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
        assert (
            ModuleAttributeClass.class_registry["custom_module"][ModuleAttributeClass.__name__][0]
            is ModuleAttributeClass
        )

    @pytest.mark.parametrize("use_registry_namespace", [True, False])
    def test_register_class_namespace_handling(self, use_registry_namespace: bool) -> None:
        """Tests registration with and without class_registry_namespace.

        Args:
            use_registry_namespace: Whether to define class_registry_namespace in the class.
        """
        if use_registry_namespace:

            class TestClass(self.UnitTestClass):  # type: ignore[name-defined, misc]
                class_registry_namespace = "custom_registry_ns"
                class_registration = False  # Don't auto-register yet

        else:

            class TestClass(self.UnitTestClass):  # type: ignore[misc, name-defined, no-redef]
                # No class_registry_namespace
                class_registration = False

        # Manually create registry to isolate test
        TestClass.create_class_registry()

        # Register the class
        TestClass.register_class()

        # Verify it was registered
        registry = TestClass.class_registry
        assert registry is not None

        if use_registry_namespace:
            assert "custom_registry_ns" in registry
            assert "TestClass" in registry["custom_registry_ns"]
        else:
            # It should use the module name (minus src/ if applicable) or _module_
            expected_namespace = TestClass.__module__
            expected_namespace = (
                expected_namespace[4:] if expected_namespace.split(".")[0] == "src" else expected_namespace
            )
            assert expected_namespace in registry
            assert "TestClass" in registry[expected_namespace]
