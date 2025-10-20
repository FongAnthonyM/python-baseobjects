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
from abc import abstractmethod
from typing import Any

# Local Packages #
from ...composition import BaseComposite
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseCompositeTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseComposite.

    This class provides common test functionality for child classes of BaseComposite, including tests for component
    management. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestComponent: type[Any]
    TestClass: type[BaseComposite]

    # Instance Methods #
    def create_components(
        self, component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
    ) -> dict[str, Any]:
        """Create components for the test composite.

        Args:
            component_types: A dictionary mapping component names to a tuple containing the component type and a
                dictionary of keyword arguments to pass to the component constructor.

        Returns:
            Components to add to the test composite.
        """
        if component_types is None:
            component_types = {"test_component", (self.TestComponent, {})}

        return {name: component_type(**kwargs) for name, (component_type, kwargs) in component_types.items()}

    # Fixtures

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

    @abstractmethod
    def test_construct_components_defaults(self, component_kwargs: dict[str, dict[str, Any]] | None = None) -> None:
        """Test the construct_components successfully builds components with default values.

        This test verifies that the defualt components were built correctly.

        Args:
            component_kwargs: A dictionary mapping component names to a dictionary of keyword arguments to pass to
                component constructor.
        """
        # Create Composite
        # composite = self.TestClass(component_kwargs=component_kwargs)

        # Validate
        # assert isinstance(test_object.components["component_name"], ComponentType)
        # assert isinstance(test_object.components["other_component_name", ComponentType2]

    def test_construct_components_types(self, *args: Any, **kwargs: Any) -> None:
        """Test the construct_components method using component types.

        This test verifies that the construct_components method correctly constructs components from component_types and
        component_kwargs.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        component_types = {"test_component": (self.TestComponent, {})}

        composite = self.TestClass(*args, component_types=component_types, **kwargs)

        # Validate
        assert isinstance(composite.components["test_component"], self.TestComponent)

    def test_construct_components_instances(self, *args: Any, **kwargs: Any) -> None:
        """Test the construct_components method using types.

        This test verifies that the construct_components method correctly constructs components from component_types and
        component_kwargs.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        components = {"test_component": self.TestComponent()}

        composite = self.TestClass(*args, components=components, **kwargs)

        # Validate
        assert composite.components["test_component"] is components["test_component"]

    def test_construct_components(self, *args: Any, **kwargs: Any) -> None:
        """Test the construct_components method using types and instances.

        This test verifies that the construct_components method correctly constructs components from component_types and
        component_kwargs.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        component_types = {"test_component": (self.TestComponent, {})}
        components = {"test_component_added": self.TestComponent()}

        composite = self.TestClass(*args, component_types=component_types, components=components, **kwargs)

        # Validate
        assert isinstance(composite.components["test_component"], self.TestComponent)
        assert composite.components["test_component_added"] is components["test_component_added"]

    def test_create_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Test the create_component method.

        This test verifies that the create_component method correctly creates and adds a component.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.TestComponent

        composite = self.TestClass()
        component = composite.create_component("test_name", component_type, *args, **kwargs)

        # Validate
        assert component is not None
        assert component.composite is composite

    def test_add_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Test the add_component method.

        This test verifies that the add_component method correctly adds a component and sets its composite.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.TestComponent

        component = component_type(*args, **kwargs)
        composite = self.TestClass()
        composite.add_component("test_name", component)

        # Validate
        assert component.composite is composite

    def test_remove_component(self, component_type: type[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Test the remove_component method.

        This test verifies that the remove_component method correctly removes a component and clears its composite.

        Args:
            component_type: The type of component to create. If None, the default component type is used.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        if component_type is None:
            component_type = self.TestComponent

        composite = self.TestClass()
        component = composite.create_component("test_name", component_type, *args, **kwargs)

        # Validate
        assert component is not None
        assert component.composite is composite

        # Remove
        composite.remove_component("test_name")

        # Validate
        assert component.composite is None
        assert "test_name" not in composite.components
