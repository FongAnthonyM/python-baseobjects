"""basecomposite_test.py
Tests for the BaseComposite class in the baseobjects package.
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

# Local Packages #
from src.baseobjects.composition import BaseComponent, BaseComposite
from src.baseobjects.testsuite.composition import BaseCompositeTestSuite


# Definitions #
# Classes #
class ExampleComponentClass(BaseComponent):
    """A test component class for testing BaseComposite."""


class ExampleCompositeClass(BaseComposite):
    """A test composite class for testing BaseComposite."""
    # Class Attributes #
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "default_component": (ExampleComponentClass, {})
    }

class TestBaseComposite(BaseCompositeTestSuite):
    """Test the BaseComposite class.

    This class tests the functionality of the BaseComposite class, which is a basic composite object
    composed of component objects. It creates test subclasses of BaseComponent and BaseComposite to test with.
    """

    # Attributes #
    TestClass: Type[BaseComposite] = ExampleCompositeClass
    TestComponent: Type[BaseComponent] = ExampleComponentClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> BaseComposite:
        """Create a test object.

        Returns:
            A test composite object instance.
        """
        return self.TestClass()

    # Tests
    def test_copy(self, test_object: BaseComposite) -> None:
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

    def test_copy_method(self, test_object: BaseComposite) -> None:
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

    def test_deepcopy(self, test_object: BaseComposite, memo: dict | None = None) -> None:
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

    def test_deepcopy_method(self, test_object: BaseComposite, memo: dict | None = None) -> None:
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

    def test_pickling(self, test_object: BaseComposite) -> None:
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

    def test_empty_composite(self) -> None:
        """Test creating an empty composite.

        This test verifies that a composite can be created with no components.
        """
        # Create a composite class with no default components
        class EmptyComposite(BaseComposite):
            default_component_types = {}

        # Create an empty composite
        composite = EmptyComposite()

        # Validate
        assert len(composite.components) == 0

    def test_component_kwargs(self) -> None:
        """Test passing component_kwargs to the constructor.

        This test verifies that component_kwargs are correctly passed to the component constructors.
        """
        # Create a component class that takes a value parameter
        class ValueComponent(BaseComponent):
            def __init__(self, value: int = 0, **kwargs: Any) -> None:
                self.value = value
                super().__init__(**kwargs)

        # Create a composite class that uses ValueComponent
        class ValueComposite(BaseComposite):
            default_component_types = {
                "value_component": (ValueComponent, {})
            }

        # Create a composite with component_kwargs
        component_kwargs = {"value_component": {"value": 42}}
        composite = ValueComposite(component_kwargs=component_kwargs)

        # Validate
        assert "value_component" in composite.components
        assert isinstance(composite.components["value_component"], ValueComponent)
        assert composite.components["value_component"].value == 42

    def test_component_types(self) -> None:
        """Test passing component_types to the constructor.

        This test verifies that component_types are correctly used to create components.
        """
        # Create a component class
        class CustomComponent(BaseComponent):
            pass

        # Create a composite with component_types
        component_types = {"custom_component": (CustomComponent, {})}
        composite = self.TestClass(component_types=component_types)

        # Validate
        assert "custom_component" in composite.components
        assert isinstance(composite.components["custom_component"], CustomComponent)
        assert composite.components["custom_component"].composite is composite

    def test_components(self) -> None:
        """Test passing components to the constructor.

        This test verifies that components are correctly added to the composite.
        """
        # Create a component
        component = self.TestComponent()

        # Create a composite with components
        components = {"added_component": component}
        composite = self.TestClass(components=components)

        # Validate
        assert "added_component" in composite.components
        assert composite.components["added_component"] is component
        assert component.composite is composite

    def test_component_override(self) -> None:
        """Test that components override component_types.

        This test verifies that if a component and a component_type have the same name,
        the component takes precedence.
        """
        # Create a component
        component = self.TestComponent()

        # Create a component type
        class CustomComponent(BaseComponent):
            pass

        # Create a composite with both
        components = {"test_component": component}
        component_types = {"test_component": (CustomComponent, {})}
        composite = self.TestClass(components=components, component_types=component_types)

        # Validate
        assert "test_component" in composite.components
        assert composite.components["test_component"] is component
        assert not isinstance(composite.components["test_component"], CustomComponent)
        assert component.composite is composite

    def test_create_component(self) -> None:
        """Test the create_component method.

        This test verifies that the create_component method correctly creates and adds a component.
        """
        # Create a composite
        composite = self.TestClass()

        # Create a component
        component = composite.create_component("created_component", self.TestComponent)

        # Validate
        assert "created_component" in composite.components
        assert composite.components["created_component"] is component
        assert component.composite is composite

    def test_add_component(self) -> None:
        """Test the add_component method.

        This test verifies that the add_component method correctly adds a component and sets its composite.
        """
        # Create a composite
        composite = self.TestClass()

        # Create a component
        component = self.TestComponent()

        # Add the component
        added_component = composite.add_component("added_component", component)

        # Validate
        assert "added_component" in composite.components
        assert composite.components["added_component"] is component
        assert added_component is component
        assert component.composite is composite

    def test_remove_component(self) -> None:
        """Test the remove_component method.

        This test verifies that the remove_component method correctly removes a component and clears its composite.
        """
        # Create a composite
        composite = self.TestClass()

        # Create a component
        component = composite.create_component("test_component", self.TestComponent)

        # Validate
        assert "test_component" in composite.components
        assert composite.components["test_component"] is component
        assert component.composite is composite

        # Remove the component
        removed_component = composite.remove_component("test_component")

        # Validate
        assert "test_component" not in composite.components
        assert removed_component is component
        assert component.composite is None

    def test_remove_component_error(self) -> None:
        """Test the remove_component method with a non-existent component.

        This test verifies that the remove_component method raises a KeyError when trying to remove
        a component that doesn't exist.
        """
        # Create a composite
        composite = self.TestClass()

        # Try to remove a non-existent component
        with pytest.raises(KeyError):
            composite.remove_component("non_existent")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])