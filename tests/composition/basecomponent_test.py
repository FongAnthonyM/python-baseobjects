"""basecomponent_test.py
Tests for the BaseComponent class in the baseobjects package.
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
import pickle
from typing import Any
from unittest.mock import patch

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.composition import BaseComponent, BaseComposite
from baseobjects.testsuite.composition import BaseComponentTestSuite


# Definitions #
# Classes #
class ConcreteCompositeClass(BaseComposite):
    """A test composite class for testing BaseComponent."""


class ConcreteComponentClass(BaseComponent):
    """A test component class for testing BaseComponent."""


class SlotComponentClass(BaseComponent):
    """A test component class with slots."""

    __slots__ = ("extra_slot",)

    def __init__(self, **kwargs: Any) -> None:
        """Initializes SlotComponentClass."""
        super().__init__(**kwargs)
        self.extra_slot = "test"


class SlotComponentPopulatedClass(BaseComponent):
    """A test component class with slots and dict."""

    __slots__ = ("extra_slot",)

    def __init__(self, **kwargs: Any) -> None:
        """Initializes SlotComponentPopulatedClass."""
        super().__init__(**kwargs)
        self.extra_slot = "test"
        self.some_attr = "populated"


# Tests #
class TestBaseComponent(BaseComponentTestSuite):
    """Tests the BaseComponent class.

    This class tests the functionality of the BaseComponent class, which is a basic component object. It creates test
    subclasses of BaseComponent and BaseComposite to test with.
    """

    # Attributes #
    UnitTestClass: type[BaseComponent] = ConcreteComponentClass
    UnitTestComposite: type[BaseComposite] = ConcreteCompositeClass

    # Tests #
    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False)
        assert obj._composite is None

    @pytest.mark.parametrize(
        ("component_class", "init_args", "expected_attrs"),
        [
            (SlotComponentClass, {}, {"extra_slot": "test"}),
            (SlotComponentClass, {"init": False}, {"extra_slot": "test"}),
            (SlotComponentPopulatedClass, {}, {"some_attr": "populated"}),
            (ConcreteComponentClass, {"init": False}, {}),
        ],
    )
    def test_pickling_variations(
        self,
        component_class: type[BaseComponent],
        init_args: dict[str, Any],
        expected_attrs: dict[str, Any],
    ) -> None:
        """Tests pickling with various component classes."""
        obj = component_class(**init_args)

        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        for attr, value in expected_attrs.items():
            assert getattr(loaded, attr) == value
        assert loaded.composite is None

    def test_setstate_tuple_none_dict(self) -> None:
        """Tests setstate with a tuple of (None, dict)."""
        obj = SlotComponentClass(init=False)
        # Manually call setstate with (None, slots)
        state = (None, {"extra_slot": "manual"})
        obj.__setstate__(state)
        assert obj.extra_slot == "manual"
        assert obj.composite is None

    def test_getstate_unknown(self) -> None:
        """Tests getstate when BaseReducible returns an unknown type."""
        obj = self.UnitTestClass()
        with patch("baseobjects.bases.BaseReducible.__getstate__", return_value="unknown"):
            state = obj.__getstate__()
            assert state is None


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
