"""compositefactoryclasstestsuite.py
Base test suite for CompositeFactoryClass and its subclasses.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...composition import BaseComponent, CompositeFactoryClass
from ..classregistration import NamespaceRegisteredClassTestSuite
from .basedispatchingcompositetestsuite import BaseDispatchingCompositeTestSuite


# Definitions #
# Classes #
class MockComponent(BaseComponent):
    """A mock component for testing."""


class MockFactory(CompositeFactoryClass):
    """A mock factory for testing."""

    class_registration: bool = True


class MockFactoryPreset(MockFactory):
    """A mock factory preset for testing."""

    default_component_types: dict[str, tuple[type, dict[str, Any]]] = {
        "mock_comp": (MockComponent, {}),
    }


class CompositeFactoryClassTestSuite(BaseDispatchingCompositeTestSuite, NamespaceRegisteredClassTestSuite):
    """Base test suite for children of CompositeFactoryClass.

    This class provides common test functionality for child classes of CompositeFactoryClass, including tests for
    component factory behavior. Subclasses should set the UnitTestClass attribute and may override or extend the test
    methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
        MockComponent: A mock component for testing.
        MockFactoryPreset: A mock factory preset for testing.
    """

    # Attributes #
    UnitTestClass: type[CompositeFactoryClass]
    UnitTestComponent: type[BaseComponent] = MockComponent
    MockComponent: type[BaseComponent] = MockComponent
    MockFactoryPreset: type[CompositeFactoryClass]

    # Tests #
    def test_is_head_class(self) -> None:
        """Tests that the class is a head class."""
        assert self.UnitTestClass.class_registration is True
        assert self.UnitTestClass.class_registry is not None
        assert self.UnitTestClass.class_registry.head_class is self.UnitTestClass

    def test_init_subclass_attributes(self) -> None:
        """Tests that the init_subclass method correctly sets the init attributes."""
        assert hasattr(self.UnitTestClass, "init_parameters")
        assert hasattr(self.UnitTestClass, "init_args")
        assert hasattr(self.UnitTestClass, "init_defaults")

        assert isinstance(self.UnitTestClass.init_parameters, dict)
        assert isinstance(self.UnitTestClass.init_args, tuple)
        assert isinstance(self.UnitTestClass.init_defaults, dict)

    def test_reverse_dispatch(self) -> None:
        """Tests that instantiating a subclass returns an instance of the head class with subclass components."""
        # Create an instance of the subclass
        instance = self.MockFactoryPreset()

        # Check that the instance is of the head class, not the subclass
        head_class = self.MockFactoryPreset.class_registry.head_class
        assert type(instance) is head_class
        assert not isinstance(instance, self.MockFactoryPreset)

        # Check that the components from the subclass were used
        assert "mock_comp" in instance.components
        assert isinstance(instance.components["mock_comp"], self.MockComponent)

    def test_head_class_instantiation(self) -> None:
        """Tests that instantiating the head class directly works as expected."""
        # Create an instance of the head class
        instance = self.UnitTestClass()

        # Check that the instance is of the head class
        assert type(instance) is self.UnitTestClass

        # Check that it doesn't have the components defined only in subclasses
        assert "mock_comp" not in instance.components
