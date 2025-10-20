"""basedispatchingcomposite_test.py
Tests for the BaseDispatchingComposite class in the baseobjects package.
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
from typing import Any, ClassVar, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.composition import BaseComponent, BaseDispatchingComposite
from src.baseobjects.testsuite.composition import BaseDispatchingCompositeTestSuite


# Definitions #
# Classes #
class ExampleComponentClass(BaseComponent):
    """A test component class for testing BaseDispatchingComposite."""


class ExampleTypeAComponent(BaseComponent):
    """A test component class for type A."""


class ExampleTypeBComponent(BaseComponent):
    """A test component class for type B."""


class ExampleDispatchingCompositeClass(BaseDispatchingComposite):
    """A test dispatching composite class for testing BaseDispatchingComposite."""

    # Class Attributes #
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "default_component": (ExampleComponentClass, {}),
    }

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        type_: str | None = None,
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
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            type_: A string to dispatch components based on.
            component_kwargs: Keyword arguments for components.
            component_types: Types and arguments for components.
            components: The components of the BIDS directory.
            **kwargs: Additional keyword arguments.
        """
        component_types = self.dispatch_component_types(type_) | (component_types or {})

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


# Tests #
class TestBaseDispatchingComposite(BaseDispatchingCompositeTestSuite):
    """Test the BaseDispatchingComposite class.

    This class tests the functionality of the BaseDispatchingComposite class, which is a composite object
    that includes methods for dispatching component objects during instantiation.
    It creates test subclasses of BaseComponent and BaseDispatchingComposite to test with.
    """

    # Attributes #
    TestComponent: type[BaseComponent] = ExampleComponentClass
    TestClass: type[BaseDispatchingComposite] = ExampleDispatchingCompositeClass

    # Instance Methods #
    # Tests
    def test_copy(self, test_object: BaseDispatchingComposite) -> None:
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

    def test_copy_method(self, test_object: BaseDispatchingComposite) -> None:
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

    def test_deepcopy(self, test_object: BaseDispatchingComposite, memo: dict | None = None) -> None:
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

    def test_deepcopy_method(self, test_object: BaseDispatchingComposite, memo: dict | None = None) -> None:
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

    def test_pickling(self, test_object: BaseDispatchingComposite) -> None:
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
        composite = self.TestClass("type_a")
        assert "type_a_component" in composite.components
        assert isinstance(composite.components["type_a_component"], ExampleTypeAComponent)
        assert composite.components["type_a_component"].composite is composite

        # Test with keyword argument
        composite = self.TestClass(type_="type_b")
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

    def test_dispatch_component_types_direct(self) -> None:
        """Test calling the dispatch_component_types method directly.

        This test verifies that the dispatch_component_types method returns the correct component types
        when called directly.
        """
        composite = self.TestClass()

        # Test with positional argument
        dispatched = composite.dispatch_component_types("type_a")
        assert "type_a_component" in dispatched
        assert dispatched["type_a_component"][0] is ExampleTypeAComponent
        assert isinstance(dispatched["type_a_component"][1], dict)

        # Test with keyword argument
        dispatched = composite.dispatch_component_types(type_="type_b")
        assert "type_b_component" in dispatched
        assert dispatched["type_b_component"][0] is ExampleTypeBComponent
        assert isinstance(dispatched["type_b_component"][1], dict)

        # Test with no relevant arguments
        dispatched = composite.dispatch_component_types(irrelevant="value")
        assert len(dispatched) == 0

    def test_dispatch_with_component_types(self) -> None:
        """Test dispatching with additional component_types.

        This test verifies that dispatched component types are combined with explicitly provided component_types.
        """

        # Create a component class
        class CustomComponent(BaseComponent):
            pass

        # Create a composite with both dispatched and explicit component_types
        component_types = {"custom_component": (CustomComponent, {})}
        composite = self.TestClass("type_a", component_types=component_types)

        # Validate
        assert "type_a_component" in composite.components
        assert isinstance(composite.components["type_a_component"], ExampleTypeAComponent)
        assert composite.components["type_a_component"].composite is composite

        assert "custom_component" in composite.components
        assert isinstance(composite.components["custom_component"], CustomComponent)
        assert composite.components["custom_component"].composite is composite

    def test_dispatch_with_components(self) -> None:
        """Test dispatching with additional components.

        This test verifies that dispatched component types are combined with explicitly provided components.
        """
        # Create a component
        component = self.TestComponent()

        # Create a composite with both dispatched component types and explicit components
        components = {"added_component": component}
        composite = self.TestClass("type_a", components=components)

        # Validate
        assert "type_a_component" in composite.components
        assert isinstance(composite.components["type_a_component"], ExampleTypeAComponent)
        assert composite.components["type_a_component"].composite is composite

        assert "added_component" in composite.components
        assert composite.components["added_component"] is component
        assert component.composite is composite


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
