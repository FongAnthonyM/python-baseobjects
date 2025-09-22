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
from abc import abstractmethod
import copy
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import NamespaceRegisteredClass
from .baseregisteredclasstestsuite import BaseRegisteredClassTestSuite


# Definitions #
# Classes #
class NamespaceRegisteredClassTestSuite(BaseRegisteredClassTestSuite):
    """Base test suite for children of NamespaceRegisteredClass.

    This class provides common test functionality for child classes of NamespaceRegisteredClass, including tests_old_ for
    namespace-based class registration and retrieval. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[NamespaceRegisteredClass]

    # Instance Methods #
    # Tests
    @abstractmethod
    def test_copy(self, test_object: Any) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_copy_method(self, test_object: Any) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object

    @abstractmethod
    def test_deepcopy(self, test_object: Any, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object

    @abstractmethod
    def test_deepcopy_method(self, test_object: Any, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object

    @abstractmethod
    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object

    def test_init_subclass_with_registration(self) -> None:
        """Test that subclasses are registered when class_registration is True."""

        # Create a subclass with registration enabled
        class RegisteredSubclass(self.TestClass):
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
        class CustomNamespaceAndNameClass(self.TestClass, namespace="custom_namespace", name="CustomName"):
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
        """Test that subclasses are registered with class_registry_namespace and class_registry_name."""

        # Create a subclass with class_registry_namespace and class_registry_name
        class ClassRegistryNamespaceAndNameClass(self.TestClass):
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
        """Test that subclasses are not registered when class_registration is False."""
        # Reset class registry for testing
        self.TestClass.class_registry = None
        self.TestClass.create_class_registry()

        # Create a subclass with registration disabled
        class UnregisteredSubclass(self.TestClass):
            class_registration = False

        # Verify subclass was not registered
        namespace = UnregisteredSubclass.__module__
        namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        assert UnregisteredSubclass.class_registry is not None
        if namespace in UnregisteredSubclass.class_registry:
            assert "UnregisteredSubclass" not in UnregisteredSubclass.class_registry[namespace]

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Test the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to the register_class method.
            **kwargs: Keyword arguments to pass to the register_class method.
        """

        class NewTestSubclass(self.TestClass):
            class_registration = False

        # Register class
        NewTestSubclass.register_class(namespace="test_namespace", name="NewClass")

        # Verify class was registered
        assert "test_namespace" in self.TestClass.class_registry
        assert "NewClass" in self.TestClass.class_registry["test_namespace"]
        assert self.TestClass.class_registry["test_namespace"]["NewClass"][0] is NewTestSubclass

    def test_get_registered_class(self) -> None:
        """Test getting a registered class."""
        # Reset class registry for testing
        self.TestClass.class_registry = None
        self.TestClass.create_class_registry()

        # Register class
        self.TestClass.register_class(namespace="test_namespace", name="TestClass")

        # Get registered class
        retrieved_class = self.TestClass.get_registered_class("test_namespace", "TestClass")

        # Verify class was retrieved
        assert retrieved_class is self.TestClass

    def test_get_registered_class_with_nonexistent_class(self) -> None:
        """Test getting a non-existent registered class."""
        # Reset class registry for testing
        self.TestClass.class_registry = None
        self.TestClass.create_class_registry()

        # Get non-existent registered class
        with pytest.raises(KeyError):
            retrieved_class = self.TestClass.get_registered_class("non_existent_namespace", "NonExistentClass")

    def test_module_attribute(self) -> None:
        """Test the _module_ attribute."""

        # Create a subclass with _module_ attribute
        class ModuleAttributeClass(self.TestClass):
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
