"""test_basecomposite.py
Tests for the BaseComposite class in the baseobjects.composition package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.composition import BaseComponent, BaseComposite
from tests.composition.base_test import BaseCompositeTest


# Definitions #
# Classes #
class TestBaseComposite(BaseCompositeTest):
    """Test the BaseComposite class.

    This class tests the functionality of the BaseComposite class, which is the base class for all composites in the 
    composition pattern.
    """

    # Class Attributes #
    class_: Type[BaseComposite] = BaseComposite
    component_class: Type[BaseComponent] = BaseComponent

    # Instance Methods #
    # Tests
    def test_initialization(self, test_composite: BaseComposite) -> None:
        """Test that the BaseComposite initializes correctly.

        Args:
            test_composite: A fixture providing a BaseComposite instance.
        """
        assert isinstance(test_composite, BaseComposite)
        assert hasattr(test_composite, "components")
        assert isinstance(test_composite.components, dict)
        assert len(test_composite.components) == 0

    def test_add_component(self, test_composite: BaseComposite) -> None:
        """Test adding a component to the composite.

        Args:
            test_composite: A fixture providing a BaseComposite instance.
        """
        # Create a component
        component = self.component_class()

        # Add the component
        test_composite.add_component("test_component", component)

        # Verify the component was added
        assert component is test_composite.components["test_component"]
        assert component.composite is test_composite

    def test_remove_component(self, test_composite: BaseComposite) -> None:
        """Test removing a component from the composite.

        Args:
            test_composite: A fixture providing a BaseComposite instance.
        """
        # Create a component
        component = self.component_class()

        # Add the component
        test_composite.add_component("test_component", component)

        # Verify the component was added
        assert component in test_composite.components.values()

        # Remove the component
        removed_component = test_composite.remove_component("test_component")

        # Verify the component was removed
        assert removed_component is component
        assert test_composite.components == {}
        assert component.composite is None

    def test_multiple_component_instances(self, test_composite: BaseComposite) -> None:
        """Test that multiple instances of the same component type can be added.

        Args:
            test_composite: A fixture providing a BaseComposite instance.
        """
        # Create two components of the same type
        component1 = self.component_class()
        component2 = self.component_class()

        # Add both components
        test_composite.add_component("component1", component1)
        test_composite.add_component("component2", component2)

        # Verify both components were added
        assert component1 is test_composite.components["component1"]
        assert component2 is test_composite.components["component2"]
        assert component1.composite is test_composite
        assert component2.composite is test_composite
        assert len(test_composite.components) == 2

    def test_construct_components_default(self, test_composite: BaseComposite) -> None:
        """Test the construct_components method with default parameters.

        Args:
            test_composite: A fixture providing a BaseComposite instance.
        """
        # Call construct_components with default parameters
        test_composite.construct_components()

        # Verify no components were added (since default_component_types is empty)
        assert len(test_composite.components) == 0

    def test_construct_components_with_component_types(self) -> None:
        """Test the construct_components method with custom component_types."""
        # Create a composite with custom component_types
        component_types = {
            "test_component": (self.component_class, {})
        }
        composite = self.class_(component_types=component_types)

        # Verify the component was created and added
        assert "test_component" in composite.components
        assert isinstance(composite.components["test_component"], self.component_class)
        assert composite.components["test_component"].composite is composite

    def test_construct_components_with_component_kwargs(self) -> None:
        """Test the construct_components method with custom component_kwargs."""
        # Create a composite class with default_component_types
        class TestComposite(BaseComposite):
            default_component_types = {
                "test_component": (BaseComponent, {})
            }

        # Create a composite with custom component_kwargs
        component_kwargs = {
            "test_component": {"custom_kwarg": "test_value"}
        }

        # Create a mock component class that captures kwargs
        class MockComponent(BaseComponent):
            def __init__(self, composite=None, init=True, **kwargs):
                self.captured_kwargs = kwargs
                super().__init__(composite=composite, init=init, **kwargs)

        # Override the component class in default_component_types
        TestComposite.default_component_types = {
            "test_component": (MockComponent, {})
        }

        composite = TestComposite(component_kwargs=component_kwargs)

        # Verify the component was created with the custom kwargs
        assert "test_component" in composite.components
        assert isinstance(composite.components["test_component"], MockComponent)
        assert composite.components["test_component"].composite is composite
        assert composite.components["test_component"].captured_kwargs.get("custom_kwarg") == "test_value"

    def test_construct_components_with_components(self) -> None:
        """Test the construct_components method with pre-created components."""
        # Create a component
        component = self.component_class()

        # Create a composite with the pre-created component
        components = {
            "test_component": component
        }
        composite = self.class_(components=components)

        # Verify the component was added
        assert "test_component" in composite.components
        assert composite.components["test_component"] is component
        assert component.composite is composite

    def test_construct_components_with_combination(self) -> None:
        """Test the construct_components method with a combination of parameters."""
        # Create a component
        component1 = self.component_class()

        # Create component types
        component_types = {
            "component2": (self.component_class, {})
        }

        # Create component kwargs
        component_kwargs = {
            "component2": {"custom_kwarg": "test_value"}
        }

        # Create a mock component class that captures kwargs
        class MockComponent(BaseComponent):
            def __init__(self, composite=None, init=True, **kwargs):
                self.captured_kwargs = kwargs
                super().__init__(composite=composite, init=init, **kwargs)

        # Update component_types to use MockComponent
        component_types = {
            "component2": (MockComponent, {})
        }

        # Create components dict
        components = {
            "component1": component1
        }

        # Create a composite with all parameters
        composite = self.class_(
            component_types=component_types,
            component_kwargs=component_kwargs,
            components=components
        )

        # Verify both components were added
        assert "component1" in composite.components
        assert "component2" in composite.components
        assert composite.components["component1"] is component1
        assert isinstance(composite.components["component2"], MockComponent)
        assert component1.composite is composite
        assert composite.components["component2"].composite is composite
        assert composite.components["component2"].captured_kwargs.get("custom_kwarg") == "test_value"

    def test_construct_components_override_default(self) -> None:
        """Test that components override default component types."""
        # Create a composite class with default_component_types
        class TestComposite(BaseComposite):
            default_component_types = {
                "test_component": (BaseComponent, {})
            }

        # Create a component
        component = self.component_class()

        # Create a composite with the pre-created component
        components = {
            "test_component": component
        }
        composite = TestComposite(components=components)

        # Verify the pre-created component was used instead of creating a new one
        assert "test_component" in composite.components
        assert composite.components["test_component"] is component
        assert component.composite is composite

    def test_construct_components_existing_components(self) -> None:
        """Test that existing components in self.components prevent creation from component_types."""
        # Create a composite class with default_component_types
        class TestComposite(BaseComposite):
            default_component_types = {
                "test_component": (BaseComponent, {}),
                "another_component": (BaseComponent, {})
            }

        # Create a component and add it to a composite
        composite = TestComposite()
        component = self.component_class()
        composite.add_component("test_component", component)

        # Clear the components dictionary to verify only our component remains
        initial_components_count = len(composite.components)

        # Call construct_components again with new component_types
        new_component_types = {
            "test_component": (BaseComponent, {}),  # Should be ignored as it already exists
            "new_component": (BaseComponent, {})    # Should be created
        }

        composite.construct_components(component_types=new_component_types)

        # Verify the existing component was not replaced and the new one was added
        assert "test_component" in composite.components
        assert "new_component" in composite.components
        assert "another_component" in composite.components
        assert composite.components["test_component"] is component
        assert isinstance(composite.components["new_component"], BaseComponent)
        assert isinstance(composite.components["another_component"], BaseComponent)
        assert len(composite.components) == initial_components_count + 1

    def test_construct_components_kwargs_for_default_types(self) -> None:
        """Test that component_kwargs works for components in default_component_types."""
        # Create a mock component class that captures kwargs
        class MockComponent(BaseComponent):
            def __init__(self, composite=None, init=True, **kwargs):
                self.captured_kwargs = kwargs
                super().__init__(composite=composite, init=init, **kwargs)

        # Create a composite class with default_component_types
        class TestComposite(BaseComposite):
            default_component_types = {
                "default_component": (MockComponent, {"default_kwarg": "default_value"})
            }

        # Create component_kwargs for the default component
        component_kwargs = {
            "default_component": {"custom_kwarg": "custom_value"}
        }

        # Create a composite with the component_kwargs
        composite = TestComposite(component_kwargs=component_kwargs)

        # Verify the component was created with merged kwargs
        assert "default_component" in composite.components
        assert isinstance(composite.components["default_component"], MockComponent)
        assert composite.components["default_component"].composite is composite
        assert composite.components["default_component"].captured_kwargs.get("default_kwarg") == "default_value"
        assert composite.components["default_component"].captured_kwargs.get("custom_kwarg") == "custom_value"

    def test_construct_components_with_none_values(self) -> None:
        """Test that construct_components handles None values correctly."""
        # Create a composite class with default_component_types
        class TestComposite(BaseComposite):
            default_component_types = {
                "default_component": (BaseComponent, {})
            }

        # Create a composite
        composite = TestComposite()

        # Clear components to start fresh
        composite.components = {}

        # Call construct_components with None values
        composite.construct_components(
            component_kwargs=None,
            component_types=None,
            components=None
        )

        # Verify the default component was created
        assert "default_component" in composite.components
        assert isinstance(composite.components["default_component"], BaseComponent)
        assert composite.components["default_component"].composite is composite

        # Test with explicit None for components but other values provided
        composite.components = {}

        # Create component types
        component_types = {
            "explicit_component": (BaseComponent, {})
        }

        # Call construct_components with None for components
        composite.construct_components(
            component_kwargs=None,
            component_types=component_types,
            components=None
        )

        # Verify both components were created
        assert "default_component" in composite.components
        assert "explicit_component" in composite.components
        assert isinstance(composite.components["default_component"], BaseComponent)
        assert isinstance(composite.components["explicit_component"], BaseComponent)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
