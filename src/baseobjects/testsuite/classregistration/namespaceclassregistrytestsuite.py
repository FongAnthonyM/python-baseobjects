"""namespaceclassregistrytestsuite.py
Base test suite for NamespaceClassRegistry and its subclasses.
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
import unittest.mock
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import NamespaceClassRegistry
from .baseclassregistrytestsuite import BaseClassRegistryTestSuite


# Definitions #
# Classes #
class NamespaceClassRegistryTestSuite(BaseClassRegistryTestSuite):
    """Base test suite for children of NamespaceClassRegistry.

    This class provides common test functionality for child classes of NamespaceClassRegistry.
    Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: ClassVar[type[NamespaceClassRegistry]]

    # Fixtures #
    @pytest.fixture
    def populated_registry(self, *args: Any, **kwargs: Any) -> NamespaceClassRegistry:
        """Creates a populated test registry for use in tests.

        Returns:
            NamespaceClassRegistry: A populated instance of the test class.
        """
        registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        registry.register_class(
            self.ConcreteClass1,
            namespace="test_namespace",
            name="ConcreteClass1",
        )
        registry.register_class(
            self.ConcreteClass2,
            namespace="test_namespace",
            name="ConcreteClass2",
            class_kwargs={"arg1": "value1"},
        )
        return registry

    # Tests #
    @pytest.mark.parametrize("input_type", ["dict", "iterable"])
    def test_init_with_classes(self, input_type: str) -> None:
        """Tests initializing with classes.

        Args:
            input_type: The type of input to use for initialization ("dict" or "iterable").

        Raises:
            ValueError: If the input type is invalid.
        """
        if input_type == "dict":
            classes = {
                "test_namespace": {
                    "ConcreteClass1": (self.ConcreteClass1, {}),
                    "ConcreteClass2": (self.ConcreteClass2, {"arg1": "value1"}),
                },
            }
        elif input_type == "iterable":
            classes = [  # type: ignore[assignment]
                (self.ConcreteClass1, "test_namespace", "ConcreteClass1", {}),
                (self.ConcreteClass2, "test_namespace", "ConcreteClass2", {"arg1": "value1"}),
            ]
        else:
            msg = f"Invalid input_type: {input_type}"
            raise ValueError(msg)

        registry = self.UnitTestClass(classes=classes)

        # Verify classes were added
        assert "test_namespace" in registry
        assert "ConcreteClass1" in registry["test_namespace"]
        assert "ConcreteClass2" in registry["test_namespace"]
        assert registry["test_namespace"]["ConcreteClass1"][0] == self.ConcreteClass1
        assert registry["test_namespace"]["ConcreteClass2"][0] == self.ConcreteClass2
        assert registry["test_namespace"]["ConcreteClass2"][1] == {"arg1": "value1"}

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:  # type: ignore[override, unused-ignore]
        """Tests the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to use in testing the register_class method.
            **kwargs: Keyword arguments to pass to use in testing the register_class method.
        """
        # Register a class
        test_registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        test_registry.register_class(self.ConcreteClass1, namespace="test_namespace", name="ConcreteClass1")

        # Verify
        assert "test_namespace" in test_registry
        assert "ConcreteClass1" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["ConcreteClass1"][0] == self.ConcreteClass1
        assert test_registry["test_namespace"]["ConcreteClass1"][1] == {}

    def test_register_classes(self, *args: Any, **kwargs: Any) -> None:
        """Tests registering multiple classes.

        Args:
           *args: Positional arguments to pass to use in testing the register_classes method.
           **kwargs: Keyword arguments to pass to use in testing the register_classes method.
        """
        # Register multiple classes
        test_registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        classes = [
            (self.ConcreteClass1, "test_namespace", "ConcreteClass1", {}),
            (self.ConcreteClass2, "test_namespace", "ConcreteClass2", {"arg1": "value1"}),
        ]
        test_registry.register_classes(classes)

        # Verify classes were registered
        assert "test_namespace" in test_registry
        assert "ConcreteClass1" in test_registry["test_namespace"]
        assert "ConcreteClass2" in test_registry["test_namespace"]
        assert test_registry["test_namespace"]["ConcreteClass1"][0] == self.ConcreteClass1
        assert test_registry["test_namespace"]["ConcreteClass2"][0] == self.ConcreteClass2
        assert test_registry["test_namespace"]["ConcreteClass2"][1] == {"arg1": "value1"}

    def test_get_class(self, populated_registry: NamespaceClassRegistry, *args: Any, **kwargs: Any) -> None:  # type: ignore[override]
        """Tests the get_class method.

        This test verifies that the get_class method correctly retrieves a registered class.

        Args:
            populated_registry: A populated test registry.
            *args: Positional arguments to pass to use in testing the get_class method.
            **kwargs: Keyword arguments to pass to use in testing the get_class method.
        """
        cls = populated_registry.get_class("test_namespace", "ConcreteClass1")

        # Verify class was retrieved
        assert cls == self.ConcreteClass1

    def test_get_class_with_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Tests getting a class with keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a class with keyword arguments
        cls_and_kwargs = populated_registry.get_class("test_namespace", "ConcreteClass2", with_kwargs=True)

        # Verify class and keyword arguments were retrieved
        assert cls_and_kwargs[0] == self.ConcreteClass2
        assert cls_and_kwargs[1] == {"arg1": "value1"}

    def test_get_class_with_default(self, *args: Any, **kwargs: Any) -> None:
        """Tests getting a non-existent class with a default value.

        Args:
            *args: Positional arguments to pass to use in testing the get_classes method.
            **kwargs: Keyword arguments to pass to use in testing the get_classes method.
        """
        # Get a non-existent class with a default value
        test_registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        default = object()
        cls = test_registry.get_class("non_existent_namespace", "NonExistentClass", default=default)

        # Verify default was returned
        assert cls is default

    def test_get_class_raises_key_error(self, *args: Any, **kwargs: Any) -> None:
        """Tests that getting a non-existent class raises a KeyError.

        Args:
            *args: Positional arguments to pass to use in testing the get_classes method.
            **kwargs: Keyword arguments to pass to use in testing the get_classes method.
        """
        # Verify getting a non-existent class raises a KeyError
        test_registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        with pytest.raises(KeyError):
            test_registry.get_class("non_existent_namespace", "NonExistentClass")

    def test_get_new(self, populated_registry: NamespaceClassRegistry) -> None:
        """Tests getting a new instance of a class.

        Args:
            populated_registry: A populated test registry.
        """
        # Get a new instance of a class
        instance = populated_registry.get_new("test_namespace", "ConcreteClass1")

        # Verify instance was created
        assert isinstance(instance, self.ConcreteClass1)

    def test_get_new_with_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Tests getting a new instance of a class with keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """

        class UnitTestClassWithKwargs:  # noqa: B903
            def __init__(self, arg1: Any = None, arg2: Any = None) -> None:
                self.arg1 = arg1
                self.arg2 = arg2

        # Register a class that accepts kwargs
        populated_registry.register_class(
            UnitTestClassWithKwargs,
            namespace="test_namespace",
            name="UnitTestClassWithKwargs",
            class_kwargs={"arg1": "default"},
        )

        # Get a new instance with overridden kwargs
        instance = populated_registry.get_new(
            "test_namespace",
            "UnitTestClassWithKwargs",
            class_kwargs={"arg2": "overridden"},
        )

        # Verify instance was created with correct args
        assert isinstance(instance, UnitTestClassWithKwargs)
        assert instance.arg1 == "default"
        assert instance.arg2 == "overridden"

    def test_get_new_without_default_kwargs(self, populated_registry: NamespaceClassRegistry) -> None:
        """Tests getting a new instance of a class without default keyword arguments.

        Args:
            populated_registry: A populated test registry.
        """

        class UnitTestClassWithKwargs:  # noqa: B903
            def __init__(self, arg1: Any = None, arg2: Any = None) -> None:
                self.arg1 = arg1
                self.arg2 = arg2

        # Register a class
        populated_registry.register_class(
            UnitTestClassWithKwargs,
            namespace="test_namespace",
            name="UnitTestClassWithKwargs",
            class_kwargs={"arg1": "default_value"},
        )

        # Get a new instance without using default keyword arguments
        instance = populated_registry.get_new(
            "test_namespace",
            "UnitTestClassWithKwargs",
            with_kwargs=False,
            class_kwargs={"arg2": "custom_value"},
        )

        # Verify instance was created with only the provided keyword arguments
        assert isinstance(instance, UnitTestClassWithKwargs)
        assert instance.arg1 is None
        assert instance.arg2 == "custom_value"

    def test_update_classes(self, *args: Any, **kwargs: Any) -> None:
        """Tests updating the classes in the registry.

        Args:
            *args: Positional arguments to pass to use in testing the update_classes method.
            **kwargs: Keyword arguments to pass to use in testing the update_classes method.
        """
        # Create registries
        registry1 = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
        registry2 = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))

        # Register classes in registry1
        registry1.register_class(self.ConcreteClass1, namespace="ns1", name="Class1")

        # Register classes in registry2
        registry2.register_class(self.ConcreteClass2, namespace="ns2", name="Class2")

        # Update registry1 with registry2
        registry1.update_classes(registry2)

        # Verify classes were updated
        assert "ns1" in registry1
        assert "Class1" in registry1["ns1"]
        assert "ns2" in registry1
        assert "Class2" in registry1["ns2"]
        assert registry1["ns2"]["Class2"][0] == self.ConcreteClass2

    @pytest.mark.parametrize("scenario", ["namespace", "class"])
    def test_get_class_dynamic_import(
        self,
        scenario: str,
        populated_registry: NamespaceClassRegistry,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests dynamic import.

        Args:
            scenario: The scenario to test ("namespace" or "class").
            populated_registry: A populated test registry.
            *args: Positional arguments to pass to use in testing.
            **kwargs: Keyword arguments to pass to use in testing.

        Raises:
            ValueError: If the scenario is invalid.
        """
        if scenario == "namespace":
            # Registry without namespace
            registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
            namespace = "new_ns"
            class_name = "ConcreteClass1"
        elif scenario == "class":
            # Registry with namespace but missing class
            registry = populated_registry
            namespace = "test_namespace"
            class_name = "NewClass"
        else:
            msg = f"Invalid scenario: {scenario}"
            raise ValueError(msg)

        with unittest.mock.patch("baseobjects.classregistration.namespaceclassregistry.import_module") as mock_import:
            # Setup side effect to register class when imported
            def side_effect(name: str) -> None:
                registry.register_class(self.ConcreteClass1, namespace=namespace, name=class_name)

            mock_import.side_effect = side_effect

            cls = registry.get_class(namespace, class_name, module="test.module")

            mock_import.assert_called_with("test.module")
            assert cls == self.ConcreteClass1

    @pytest.mark.parametrize("scenario", ["namespace", "class"])
    def test_get_class_dynamic_import_fail(
        self,
        scenario: str,
        populated_registry: NamespaceClassRegistry,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests dynamic import failure.

        Args:
            scenario: The scenario to test ("namespace" or "class").
            populated_registry: A populated test registry.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            ValueError: If the scenario is invalid.
        """
        if scenario == "namespace":
            registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))
            namespace = "new_ns"
            class_name = "ConcreteClass1"
        elif scenario == "class":
            registry = populated_registry
            namespace = "test_namespace"
            class_name = "NewClass"
        else:
            msg = f"Invalid scenario: {scenario}"
            raise ValueError(msg)

        with unittest.mock.patch("baseobjects.classregistration.namespaceclassregistry.import_module") as mock_import:
            mock_import.side_effect = ImportError("Test Error")

            with pytest.warns(UserWarning, match="Failed to import module"):
                with pytest.raises(KeyError):
                    registry.get_class(namespace, class_name, module="test.module")

    def test_init_no_init(self) -> None:
        """Tests initializing with init=False."""
        registry = self.UnitTestClass(init=False)
        assert len(registry) == 0

    def test_register_class_defaults(self, *args: Any, **kwargs: Any) -> None:
        """Tests register_class with default arguments (inferred name/namespace)."""
        registry = cast(NamespaceClassRegistry, self.create_test_registry(*args, **kwargs))

        registry.register_class(self.ConcreteClass1)  # namespace=None, name=None

        expected_namespace = self.ConcreteClass1.__dict__.get("_module_", self.ConcreteClass1.__module__)
        expected_name = self.ConcreteClass1.__name__

        assert expected_namespace in registry
        assert expected_name in registry[expected_namespace]
        assert registry[expected_namespace][expected_name][0] == self.ConcreteClass1

    def test_get_class_missing_class_with_default(self, populated_registry: NamespaceClassRegistry) -> None:
        """Tests getting a non-existent class in an existing namespace with default."""
        default = object()
        # "test_namespace" exists in populated_registry
        cls = populated_registry.get_class("test_namespace", "MissingClass", default=default)
        assert cls is default
