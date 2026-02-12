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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.composition import BaseComponent, BaseComposite
from baseobjects.testsuite.composition import BaseCompositeTestSuite


# Definitions #
# Classes #
class ConcreteComponentClass(BaseComponent):
    """A test component class for testing BaseComposite."""


class ConcreteCompositeClass(BaseComposite):
    """A test composite class for testing BaseComposite."""

    # Class Attributes #
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "default_component": (ConcreteComponentClass, {}),
    }


# Tests #
class TestBaseComposite(BaseCompositeTestSuite):
    """Tests the BaseComposite class.

    This class tests the functionality of the BaseComposite class, which is a basic composite object composed of
    component objects. It creates test subclasses of BaseComponent and BaseComposite to test with.
    """

    # Attributes #
    UnitTestComponent: ClassVar[type[BaseComponent]] = ConcreteComponentClass
    UnitTestClass: type[BaseComposite] = ConcreteCompositeClass

    # Tests #
    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False)
        assert not obj.components

    def test_remove_component_detached(self) -> None:
        """Tests removing a component that is already detached."""
        composite = self.UnitTestClass()
        component = self.UnitTestComponent()
        composite.add_component("test", component)

        # Detach manually
        component.composite = None

        # Remove
        removed = composite.remove_component("test")
        assert removed is component
        assert component.composite is None


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
