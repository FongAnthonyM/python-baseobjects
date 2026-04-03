"""dynamicwrappertestsuite.py
Test suite for the DynamicWrapper class.
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
import pytest

# Local Packages #
from ...wrappers import DynamicWrapper
from .wrappertestsuite import WrapperTestSuite


# Definitions #
# Classes #
class ConcreteDynamicWrapperWithGetAttr(DynamicWrapper):
    """A test class that inherits from DynamicWrapper and wraps an object with __getattr__.

    This class is used to test how DynamicWrapper handles objects with __getattr__.
    """

    _wrapped_map_: list[str] = ["_wrapped_obj"]

    def __init__(self, wrapped: Any = None) -> None:
        """Initializes with a wrapped object.

        Args:
            wrapped: The object to wrap.
        """
        self.existing = "wrapper_existing"
        self._wrapped_obj = wrapped


class DynamicWrapperTestSuite(WrapperTestSuite):
    """Tests suite for the DynamicWrapper class.

    This class provides common test functionality for DynamicWrapper classes.
    """

    UnitTestClass: type[DynamicWrapper]

    # Tests #
    def test_setattr_method(self) -> None:
        """Tests the _setattr method."""
        wrapper = self.UnitTestClass()
        wrapper._setattr("new_attr", "value")
        assert wrapper.new_attr == "value"
        assert "new_attr" in wrapper.__dict__

    def test_dynamic_attribute_creation(self) -> None:
        """Tests the dynamic attribute creation."""

        class ConcreteWithGetAttr:
            def __init__(self) -> None:
                self.normal = "normal"

            def __getattr__(self, name: str) -> str:
                if name.startswith("dynamic_"):
                    return f"got_{name}"
                msg = f"'{type(self).__name__}' object has no attribute '{name}'"
                raise AttributeError(msg)

        example = ConcreteWithGetAttr()
        wrapper = ConcreteDynamicWrapperWithGetAttr(wrapped=example)

        assert wrapper.normal == "normal"
        assert wrapper.dynamic_attr == "got_dynamic_attr"
        assert wrapper.existing == "wrapper_existing"

        with pytest.raises(AttributeError):
            _ = wrapper.missing_attr

    def test_nested_wrappers(self) -> None:
        """Tests how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper, and that attribute
        access works correctly through multiple levels of wrapping.
        """
        # Creates a wrapper
        wrapper1 = self.UnitTestClass(self.ConcreteOne())

        # Creates a wrapper that wraps the first wrapper
        wrapper2 = self.UnitTestClass(wrapper1)

        # Verifies that attribute access works through multiple levels of wrapping
        assert wrapper2.one == "one"  # type: ignore[attr-defined, unused-ignore]
        assert wrapper2.method() == "one"  # type: ignore[attr-defined, unused-ignore]

        # Verifies that setting attributes works through multiple levels of wrapping
        wrapper2.one = "nested"  # type: ignore[attr-defined, unused-ignore]

        # DynamicWrapper sets on self, does not delegate set
        assert wrapper2.one == "nested"
        assert wrapper1.one == "one"  # Original remains unchanged

    def test_setattr_on_wrapped(self) -> None:
        """Tests setting an attribute on a wrapped object."""
        wrapped = self.ConcreteOne()
        wrapper = self.UnitTestClass(wrapped)

        assert wrapped.one == "one"
        wrapper.one = "new_value"
        assert wrapped.one == "new_value"
        assert wrapper.one == "new_value"

    @pytest.mark.parametrize(
        ("init_wrapped", "set_on_self", "attr_to_del", "should_raise"),
        [
            (True, None, "one", False),  # test_delattr_on_wrapped
            (False, "on_self", "on_self", False),  # test_delattr_on_self
            (True, None, "non_existent_attr", True),  # test_delattr_not_in_wrapped
            (False, None, "non_existent_attr", True),  # test_delattr_missing_completely
        ],
    )
    def test_delattr_scenarios(
        self,
        init_wrapped: bool,
        set_on_self: str | None,
        attr_to_del: str,
        should_raise: bool,
    ) -> None:
        """Tests deleting attributes in various scenarios (on wrapped, on self, missing).

        Args:
            init_wrapped: Whether to initialize with a wrapped object.
            set_on_self: Name of attribute to set on the wrapper instance itself (value "value").
            attr_to_del: Name of attribute to delete.
            should_raise: Whether AttributeError is expected.
        """
        if init_wrapped:
            wrapped = self.ConcreteOne()
            obj = self.UnitTestClass(wrapped)
        else:
            # No wrapped object or empty wrapper
            wrapped = None
            obj = self.UnitTestClass()

        if set_on_self:
            setattr(obj, set_on_self, "value")

        if should_raise:
            with pytest.raises(AttributeError):
                delattr(obj, attr_to_del)
        else:
            # Should succeed
            assert hasattr(obj, attr_to_del) or (wrapped and hasattr(wrapped, attr_to_del))
            delattr(obj, attr_to_del)
            assert not hasattr(obj, attr_to_del)
            if wrapped and attr_to_del == "one":
                assert not hasattr(wrapped, attr_to_del)

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        dw = self.UnitTestClass(init=False)
        assert not dw.__dict__

    def test_getstate_none_return(self) -> None:
        """Tests __getstate__ when object is empty."""
        dw = self.UnitTestClass(init=False)
        state = dw.__getstate__()
        assert state is None or state == {}

    def test_delattr_missing_in_wrapped_but_in_map(self) -> None:
        """Tests deleting an attribute when a wrapped object container is missing."""

        class TestMissingMap(self.UnitTestClass):  # type: ignore[misc, name-defined]
            _wrapped_map_: list[str] = ["_missing"]

        obj = TestMissingMap()

        with pytest.raises(AttributeError):
            del obj.any_attr
