"""dispatchablecomposite_test.py
Tests for the DispatchableComposite class in the baseobjects package.
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
import copy
import pickle
from typing import Any, ClassVar, Optional, Type, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.classregistration import BaseClassRegistry
from src.baseobjects.composition import BaseComponent, DispatchableComposite
from src.baseobjects.testsuite.composition import DispatchableCompositeTestSuite


# Definitions #
# Classes #
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


class ExampleComponentClass(BaseComponent):
    """A test component class for testing DispatchableComposite."""


class ExampleTypeAComponent(BaseComponent):
    """A test component class for type A."""


class ExampleTypeBComponent(BaseComponent):
    """A test component class for type B."""


class ExampleDispatchableComposite(DispatchableComposite):
    """A base test subclass of DispatchableComposite for testing purposes."""

    # Class Attributes #
    class_registry_type: ClassVar[Type[BaseClassRegistry]] = ConcreteClassRegistry
    class_registration: ClassVar[bool] = True
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "default_component": (ExampleComponentClass, {})
    }

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
        if "type_" in kwargs and isinstance(kwargs["type_"], str):
            return (kwargs["type_"],)
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
    def get_registered_class(cls, name: str, default: Any = None) -> Optional["DispatchableComposite"]:
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

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        type_: str | None = None,
        component_type: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Attributes #
        self.components: dict[str, Any] = self.components.copy()

        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                type_=type_,
                component_type=component_type,
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors #
    def construct(
        self,
        type_: str | None = None,
        component_type: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            type_: A string to dispatch classes based on.
            component_type: A string to dispatch components based on.
            component_kwargs: Keyword arguments for components.
            component_types: Types and arguments for components.
            components: The components of the BIDS directory.
            **kwargs: Additional keyword arguments.
        """
        component_types = self.dispatch_component_types(component_type) | (component_types or {})

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def dispatch_component_types(self, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """Dispatches component types using the given arguments.

        Args:
            *args: Positional arguments to use in dispatching.
            **kwargs: Keyword arguments to use in dispatching.

        Returns:
            A dictionary mapping component names to tuples containing the component type and a dictionary
            of keyword arguments.
        """
        if args and isinstance(args[0], str):
            if args[0] == "type_a":
                return {"type_a_component": (ExampleTypeAComponent, {})}
            elif args[0] == "type_b":
                return {"type_b_component": (ExampleTypeBComponent, {})}

        if "type_" in kwargs and isinstance(kwargs["type_"], str):
            if kwargs["type_"] == "type_a":
                return {"type_a_component": (ExampleTypeAComponent, {})}
            elif kwargs["type_"] == "type_b":
                return {"type_b_component": (ExampleTypeBComponent, {})}

        return {}


class TypeADispatchable(ExampleDispatchableComposite):
    """A subclass of ExampleDispatchableComposite for testing dispatching to type A."""

    class_registration = True


class TypeBDispatchable(ExampleDispatchableComposite):
    """A subclass of ExampleDispatchableComposite for testing dispatching to type B."""

    class_registration = True


# Tests #
class TestDispatchableComposite(DispatchableCompositeTestSuite):
    """Test the DispatchableComposite class.

    This class tests the functionality of the DispatchableComposite class, which is a composite object
    that combines component dispatching and class dispatching capabilities.
    It creates test subclasses of BaseComponent and DispatchableComposite to test with.
    """

    # Attributes #
    TestClass: Type[DispatchableComposite] = ExampleDispatchableComposite
    TestComponent: Type[BaseComponent] = ExampleComponentClass

    # Instance Methods #
    # Tests
    def test_copy(self, test_object: DispatchableComposite) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.components is test_object.components
        assert len(obj_copy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_copy.components
            assert obj_copy.components[name] is component

    def test_copy_method(self, test_object: DispatchableComposite) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.components is test_object.components
        assert len(obj_copy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_copy.components
            assert obj_copy.components[name] is component

    def test_deepcopy(self, test_object: DispatchableComposite, memo: dict | None = None) -> None:
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
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.components is not test_object.components
        assert len(obj_deepcopy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_deepcopy.components
            assert obj_deepcopy.components[name] is not component
            assert isinstance(obj_deepcopy.components[name], type(component))
            assert obj_deepcopy.components[name].composite is obj_deepcopy

    def test_deepcopy_method(self, test_object: DispatchableComposite, memo: dict | None = None) -> None:
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
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.components is not test_object.components
        assert len(obj_deepcopy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_deepcopy.components
            assert obj_deepcopy.components[name] is not component
            assert isinstance(obj_deepcopy.components[name], type(component))
            assert obj_deepcopy.components[name].composite is obj_deepcopy

    def test_pickling(self, test_object: DispatchableComposite) -> None:
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
        assert isinstance(unpickled, self.TestClass)
        assert unpickled.components is not test_object.components
        assert len(unpickled.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in unpickled.components
            assert unpickled.components[name] is not component
            assert isinstance(unpickled.components[name], type(component))
            assert unpickled.components[name].composite is unpickled

    def test_construct_components_defaults(self, component_kwargs: dict[str, dict[str, Any]] | None = None) -> None:
        """Test the construct_components successfully builds components with default values.

        This test verifies that the default components were built correctly.

        Args:
            component_kwargs: A dictionary mapping component names to a dictionary of keyword arguments to pass to
                component constructor.
        """
        composite = self.TestClass(component_kwargs=component_kwargs)

        # Validate
        assert "default_component" in composite.components
        assert isinstance(composite.components["default_component"], self.TestComponent)
        assert composite.components["default_component"].composite is composite

    def test_dispatch_component_types(self, *args: Any, **kwargs: Any) -> None:
        """Test the dispatch_component_types method.

        This test verifies that the dispatch_component_types method correctly dispatches component types based on the
        given arguments.

        Args:
            *args: Positional arguments to pass to the dispatch_component_types method.
            **kwargs: Keyword arguments to pass to the dispatch_component_types method.
        """
        # Test with positional argument
        composite = self.TestClass(None, "type_a")
        assert "type_a_component" in composite.components
        assert isinstance(composite.components["type_a_component"], ExampleTypeAComponent)
        assert composite.components["type_a_component"].composite is composite

        # Test with keyword argument
        composite = self.TestClass(component_type="type_b")
        assert "type_b_component" in composite.components
        assert isinstance(composite.components["type_b_component"], ExampleTypeBComponent)
        assert composite.components["type_b_component"].composite is composite

        # Test with no relevant arguments
        composite = self.TestClass(irrelevant="value")
        assert "default_component" in composite.components
        assert isinstance(composite.components["default_component"], self.TestComponent)
        assert composite.components["default_component"].composite is composite
        assert "type_a_component" not in composite.components
        assert "type_b_component" not in composite.components

    def test_get_class_information(self, *args: Any, **kwargs: Any) -> None:
        """Test the get_class_information method.

        This test verifies that the get_class_information method correctly extracts class information from arguments.

        Args:
            *args: Positional arguments to test the get_class_information method.
            **kwargs: Keyword arguments to test the get_class_information method.
        """
        # Test with positional argument
        info = self.TestClass.get_class_information("TypeADispatchable")
        assert info == ("TypeADispatchable",)

        # Test with keyword argument
        info = self.TestClass.get_class_information(type_="TypeBDispatchable")
        assert info == ("TypeBDispatchable",)

        # Test with no relevant arguments
        info = self.TestClass.get_class_information(123, irrelevant="value")
        assert info == (self.TestClass.__name__,)

    def test_class_dispatch(self, *args: Any, **kwargs: Any) -> None:
        """Test class dispatching.

        Args:
            *args: Positional arguments to test the class dispatching.
            **kwargs: Keyword arguments to test the class dispatching.
        """
        # Test dispatching with positional argument
        instance = self.TestClass("TypeADispatchable")
        assert isinstance(instance, TypeADispatchable)

        # Test dispatching with keyword argument
        instance = self.TestClass(type_="TypeBDispatchable")
        assert isinstance(instance, TypeBDispatchable)

        # Test dispatching with unknown type
        instance = self.TestClass("UnknownType")
        assert isinstance(instance, self.TestClass)
        assert type(instance) is self.TestClass

        # Test that dispatching doesn't happen when called from a subclass
        instance = TypeADispatchable("TypeBDispatchable")
        assert isinstance(instance, TypeADispatchable)
        assert not isinstance(instance, TypeBDispatchable)

        # Test that dispatching doesn't happen when no arguments are provided
        instance = self.TestClass()
        assert isinstance(instance, self.TestClass)
        assert type(instance) is self.TestClass

    def test_combined_dispatch(self) -> None:
        """Test combined class and component dispatching.

        This test verifies that both class dispatching and component dispatching work together.
        """
        # Test class dispatching with component dispatching
        instance = self.TestClass("TypeADispatchable", component_type="type_b")
        assert isinstance(instance, TypeADispatchable)
        assert "type_b_component" in instance.components
        assert isinstance(instance.components["type_b_component"], ExampleTypeBComponent)
        assert instance.components["type_b_component"].composite is instance

        # Test component dispatching with class dispatching
        instance = self.TestClass(component_type="type_a", type_="TypeBDispatchable")
        assert isinstance(instance, TypeBDispatchable)
        assert "type_a_component" in instance.components
        assert isinstance(instance.components["type_a_component"], ExampleTypeAComponent)
        assert instance.components["type_a_component"].composite is instance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
