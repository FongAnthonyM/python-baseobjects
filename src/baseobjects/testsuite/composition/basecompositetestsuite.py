"""basecompositetestsuite.py
Base test suite for BaseComposite and its subclasses.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...composition import BaseComposite
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseCompositeTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseComposite.

    This class provides common test functionality for child classes of BaseComposite, including tests for component
    management. Subclasses should set the UnitTestClass attribute and may override or extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
        UnitTestComponent: The component class to use for testing.
    """

    # Attributes #
    UnitTestClass: type[BaseComposite]
    UnitTestComponent: type[Any]

    # Helper Methods #
    def create_components(
        self,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
    ) -> dict[str, Any]:
        """Creates components for the test composite.

        Args:
            component_types: A dictionary mapping component names to a tuple containing the component type and a
                dictionary of keyword arguments to pass to the component constructor.

        Returns:
            Components to add to the test composite.
        """
        if component_types is None:
            component_types = {"test_component": (self.UnitTestComponent, {})}

        return {name: component_type(**kwargs) for name, (component_type, kwargs) in component_types.items()}

    # Tests #
    # Magic Methods #
    def test_add_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Tests the add_component method.

        This test verifies that the add_component method correctly adds a component and sets its composite.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.UnitTestComponent

        component = component_type(*args, **kwargs)
        composite = self.UnitTestClass()
        composite.add_component("test_name", component)

        # Validate
        assert component.composite is composite

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: Any, method: str) -> None:  # type: ignore[override, unused-ignore]
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        assert obj_copy.components is test_object.components
        assert len(obj_copy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_copy.components
            assert obj_copy.components[name] is component

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: Any,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:  # type: ignore[override, unused-ignore]
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)
        assert obj_deepcopy.components is not test_object.components
        assert len(obj_deepcopy.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in obj_deepcopy.components
            assert obj_deepcopy.components[name] is not component
            assert isinstance(obj_deepcopy.components[name], type(component))

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:  # type: ignore[override, unused-ignore]
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)
        assert unpickled.components is not test_object.components
        assert len(unpickled.components) == len(test_object.components)
        for name, component in test_object.components.items():
            assert name in unpickled.components
            assert unpickled.components[name] is not component
            assert isinstance(unpickled.components[name], type(component))

    # Functionality #
    def test_construct_components_defaults(self, component_kwargs: dict[str, dict[str, Any]] | None = None) -> None:
        """Tests the construct_components successfully builds components with default values.

        This test verifies that the default components were built correctly.

        Args:
            component_kwargs: A dictionary mapping component names to a dictionary of keyword arguments to pass to
                component constructor.
        """
        # Creates Composite
        composite = self.UnitTestClass(component_kwargs=component_kwargs)

        # Validate
        for name, (component_type, _) in self.UnitTestClass.default_component_types.items():
            assert name in composite.components
            assert isinstance(composite.components[name], component_type)

    def test_empty_composite(self) -> None:
        """Tests creating an empty composite.

        This test verifies that an empty composite can be created and has no components.
        """

        # Defines an empty composite class
        class EmptyComposite(self.UnitTestClass):  # type: ignore[name-defined, misc]
            default_component_types: dict[str, Any] = {}

        # Creates composite
        composite = EmptyComposite()

        # Validate
        assert len(composite.components) == 0

    def test_component_kwargs(self) -> None:
        """Tests constructing components with keyword arguments.

        This test verifies that components are constructed with the provided keyword arguments.
        """

        # Defines component and composite classes
        class ValueComponent(self.UnitTestComponent):  # type: ignore[name-defined, misc]
            def __init__(self, value: int = 0, **kwargs: Any) -> None:
                self.value = value
                super().__init__(**kwargs)

        class ValueComposite(self.UnitTestClass):  # type: ignore[name-defined, misc]
            default_component_types: dict[str, Any] = {"value_component": (ValueComponent, {"value": 1})}

        # Creates composite with default kwargs
        composite = ValueComposite()
        assert composite.components["value_component"].value == 1

        # Creates composite with overridden kwargs
        composite = ValueComposite(component_kwargs={"value_component": {"value": 2}})
        assert composite.components["value_component"].value == 2

    def test_component_types(self) -> None:
        """Tests constructing components with custom types.

        This test verifies that components can be constructed using custom types provided at initialization.
        """

        # Defines a custom component
        class CustomComponent(self.UnitTestComponent):  # type: ignore[name-defined, misc]
            pass

        # Creates composite with component_types
        composite = self.UnitTestClass(
            component_types={"custom_component": (CustomComponent, {})},
        )

        # Validate
        assert "custom_component" in composite.components
        assert isinstance(composite.components["custom_component"], CustomComponent)

    def test_components(self) -> None:
        """Tests constructing with existing components.

        This test verifies that existing components can be added during initialization.
        """
        # Creates components
        component1 = self.UnitTestComponent()
        component2 = self.UnitTestComponent()

        # Creates composite with components
        composite = self.UnitTestClass(
            components={"comp1": component1, "comp2": component2},
        )

        # Validate
        assert composite.components["comp1"] is component1
        assert composite.components["comp2"] is component2
        assert component1.composite is composite
        assert component2.composite is composite

    def test_component_override(self) -> None:
        """Tests overriding default components.

        This test verifies that default components can be overridden by providing component_types or components.
        """

        # Defines a composite with a default component
        class DefaultComposite(self.UnitTestClass):  # type: ignore[name-defined, misc]
            default_component_types: dict[str, Any] = {"comp": (self.UnitTestComponent, {})}

        # Override with component_types
        class CustomComponent(self.UnitTestComponent):  # type: ignore[name-defined, misc]
            pass

        composite = DefaultComposite(
            component_types={"comp": (CustomComponent, {})},
        )
        assert isinstance(composite.components["comp"], CustomComponent)

        # Override with components
        custom_instance = CustomComponent()
        composite = DefaultComposite(
            components={"comp": custom_instance},
        )
        assert composite.components["comp"] is custom_instance

    @pytest.mark.parametrize(
        ("use_types", "use_instances"),
        [
            (True, False),
            (False, True),
            (True, True),
        ],
    )
    def test_construct_components_variations(
        self,
        use_types: bool,
        use_instances: bool,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Tests the construct_components method using types and/or instances.

        This test verifies that the construct_components method correctly constructs components from component_types and
        component_kwargs.

        Args:
            use_types: Whether to use component_types.
            use_instances: Whether to use components (instances).
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        component_types: dict[str, tuple[type, dict[str, Any]]] = {}
        components: dict[str, Any] = {}

        if use_types:
            component_types["test_component"] = (self.UnitTestComponent, {})

        if use_instances:
            components["test_component_inst"] = self.UnitTestComponent()

        composite = self.UnitTestClass(*args, component_types=component_types, components=components, **kwargs)  # type: ignore[misc]

        # Validate
        if use_types:
            assert isinstance(composite.components["test_component"], self.UnitTestComponent)

        if use_instances:
            assert composite.components["test_component_inst"] is components["test_component_inst"]

    def test_create_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Tests the create_component method.

        This test verifies that the create_component method correctly creates and adds a component.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.UnitTestComponent

        composite = self.UnitTestClass()
        component = composite.create_component("test_name", component_type, *args, **kwargs)

        # Validate
        assert component is not None
        assert component.composite is composite

    def test_remove_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Tests the remove_component method.

        This test verifies that the remove_component method correctly removes a component and clears its composite.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.UnitTestComponent

        composite = self.UnitTestClass()
        component = composite.create_component("test_name", component_type, *args, **kwargs)

        # Validate
        assert component is not None
        assert component.composite is composite

        # Removes
        composite.remove_component("test_name")

        # Validate
        assert component.composite is None
        assert "test_name" not in composite.components
