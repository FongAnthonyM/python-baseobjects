"""staticwrappertestsuite.py
Test suite for the StaticWrapper class.
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
from ...wrappers import StaticWrapper
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class StaticWrapperTestSuite(BaseObjectTestSuite):
    """Tests suite for the StaticWrapper class.

    This class provides common test functionality for StaticWrapper classes.
    """

    UnitTestClass: type[StaticWrapper]

    # Tests #
    def test_exclude_attributes(self) -> None:
        """Tests the _exclude_attributes property."""
        wrapper = self.UnitTestClass()
        assert isinstance(wrapper._exclude_attributes, set)
        assert "__slotnames__" in wrapper._exclude_attributes

    def test_get_previous_wrapped(self) -> None:
        """Tests getting the previously wrapped object."""

        class SimpleGetPreviousWrapper(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_wrapped_obj", Any)]

            def __init__(self, wrapped: Any = None) -> None:
                self._wrapped_obj = wrapped

        obj1 = "obj1"
        wrapper = SimpleGetPreviousWrapper(obj1)

        assert wrapper._wrapped_obj == obj1

    def test_class_rewrap(self) -> None:
        """Tests re-wrapping the class."""

        class UnitTestClassRewrap(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_first", Any), ("_second", Any)]

            def __init__(self, first: Any = None, second: Any = None) -> None:
                self._first = first
                self._second = second

        wrapper = UnitTestClassRewrap(1, 2)
        assert wrapper._first == 1
        assert wrapper._second == 2

    def test_method_descriptor_wrapping(self) -> None:
        """Tests wrapping objects with method descriptors (e.g. built-ins like list)."""

        class ListWrapper(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("_list", list)]

            def __init__(self, inner: list) -> None:  # type: ignore[type-arg]
                self._list = inner

        lst = [1, 2, 3]
        wrapper = ListWrapper(lst)

        wrapper.append(4)  # type: ignore[attr-defined]
        assert lst == [1, 2, 3, 4]
        assert wrapper.pop() == 4  # type: ignore[attr-defined]
        assert lst == [1, 2, 3]

    def test_wrapped_attribute_persistence(self) -> None:
        """Tests that attributes persist when wrapped object is missing."""

        class Simple:
            attr = "default"

        class PersistenceWrapper(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self) -> None:
                pass

        wrapper = PersistenceWrapper()

        # Sets when missing
        wrapper.attr = "persistent"  # type: ignore[attr-defined]
        assert wrapper.attr == "persistent"  # type: ignore[attr-defined]
        # store_name is '_obj'. Temp name is f"__{'_obj'}_{'attr'}_" -> "___obj_attr_"
        assert getattr(wrapper, "___obj_attr_") == "persistent"

        # Deletes
        del wrapper.attr  # type: ignore[attr-defined]
        with pytest.raises(AttributeError):
            _ = wrapper.attr  # type: ignore[attr-defined]
        assert not hasattr(wrapper, "___obj_attr_")

    def test_previous_wrapped_transfer(self) -> None:
        """Tests transferring attributes from previous wrapped object."""

        class Simple:
            attr = "default"

        class TransferWrapper(StaticWrapper):
            _get_previous_wrapped = True
            _set_next_wrapped = True
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        obj1 = Simple()
        obj1.attr = "value1"
        wrapper = TransferWrapper(obj1)

        obj2 = Simple()
        # Transfer happens when setting new wrapped object
        wrapper.obj = obj2

        assert obj2.attr == "value1"

    def test_del_wrapped_saving(self) -> None:
        """Tests saving attributes when deleting wrapped object."""

        class Simple:
            attr = "default"

        class SaveWrapper(StaticWrapper):
            _get_previous_wrapped = True
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        obj1 = Simple()
        obj1.attr = "saved"
        wrapper = SaveWrapper(obj1)

        del wrapper.obj

        assert wrapper.attr == "saved"  # type: ignore[attr-defined]
        assert getattr(wrapper, "___obj_attr_") == "saved"

    def test_explicit_rewrap(self) -> None:
        """Tests explicitly re-wrapping the class."""

        class RewrapTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = []

        # Initially empty
        wrapper = RewrapTest()

        # Rewrap with list
        RewrapTest._class_rewrap([("_list", list)])

        wrapper._list = [1]  # type: ignore[attr-defined]
        wrapper.append(2)  # type: ignore[attr-defined]
        assert wrapper._list == [1, 2]  # type: ignore[attr-defined]

    def test_set_wrapped_none_saving(self) -> None:
        """Tests saving attributes when setting wrapped object to None."""

        class Simple:
            attr = "default"

        class SaveWrapper(StaticWrapper):
            _get_previous_wrapped = True
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        obj1 = Simple()
        obj1.attr = "saved_on_none"
        wrapper = SaveWrapper(obj1)

        wrapper.obj = None

        assert wrapper.attr == "saved_on_none"  # type: ignore[attr-defined]
        assert getattr(wrapper, "___obj_attr_") == "saved_on_none"

    def test_instance_wrap_update(self) -> None:
        """Tests the _wrap instance method updates the class with new attributes."""

        class DynamicSimple:
            pass

        class InstanceWrapTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", DynamicSimple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        inner = DynamicSimple()
        wrapper = InstanceWrapTest(inner)

        # Adds attribute to inner object AFTER wrapping
        inner.new_attr = "new"  # type: ignore[attr-defined]

        assert not hasattr(wrapper, "new_attr")

        # Calls _wrap on instance
        wrapper._wrap()

        assert wrapper.new_attr == "new"  # type: ignore[attr-defined]

    def test_del_wrapped_attribute_delegation(self) -> None:
        """Tests that deleting an attribute delegates to the wrapped object."""

        class Simple:
            pass

        class DelTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        inner = Simple()
        wrapper = DelTest(inner)

        inner.attr = "value"  # type: ignore[attr-defined]
        wrapper._wrap()

        assert wrapper.attr == "value"  # type: ignore[attr-defined]

        del wrapper.attr  # type: ignore[attr-defined]

        assert not hasattr(inner, "attr")
        with pytest.raises(AttributeError):
            _ = wrapper.attr  # type: ignore[attr-defined]

    def test_get_wrapped_attribute_failure(self) -> None:
        """Tests proper AttributeError when wrapped attribute is missing."""

        class Simple:
            attr = "value"

        class FailTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        inner = Simple()
        wrapper = FailTest(inner)

        assert wrapper.attr == "value"  # type: ignore[attr-defined]

        # Force delete on inner to cause failure in wrapper property access
        inner.inst_attr = "inst"  # type: ignore[attr-defined]
        wrapper._wrap()  # Catch the new attr

        assert wrapper.inst_attr == "inst"  # type: ignore[attr-defined]
        del inner.inst_attr  # type: ignore[attr-defined]

        with pytest.raises(AttributeError) as excinfo:
            _ = wrapper.inst_attr  # type: ignore[attr-defined]

        assert "object has no attribute 'inst_attr'" in str(excinfo.value)

    def test_class_rewrap_removal(self) -> None:
        """Tests that _class_rewrap removes attributes from previous wrapping."""

        class TypeA:
            attr_a = "a"

        class TypeB:
            attr_b = "b"

        class RewrapRemovalTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", TypeA)]

            def __init__(self, obj: Any) -> None:
                self.obj = obj

        wrapper = RewrapRemovalTest(TypeA())
        assert hasattr(wrapper, "attr_a")
        assert not hasattr(wrapper, "attr_b")

        # Rewrap with TypeB
        RewrapRemovalTest._class_rewrap([("obj", TypeB)])
        wrapper.obj = TypeB()

        assert not hasattr(wrapper, "attr_a")
        assert hasattr(wrapper, "attr_b")

    @pytest.mark.parametrize(
        ("setup_temp_value", "operation", "expect_raise"),
        [
            (None, "set", False),  # Set new
            ("saved", "del", False),  # Del existing
            (None, "del", True),  # Del missing
        ],
    )
    def test_attribute_operations_when_none(
        self,
        setup_temp_value: str | None,
        operation: str,
        expect_raise: bool,
    ) -> None:
        """Tests setting/deleting attributes when the wrapped object is None.

        Args:
            setup_temp_value: Value to pre-set in the wrapper (simulating saved temp attribute).
            operation: The operation to perform ('set' or 'del').
            expect_raise: Whether an AttributeError is expected.
        """

        class Simple:
            attr = "default"

        class NoneTest(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any = None) -> None:
                self.obj = obj

        wrapper = NoneTest(None)

        if setup_temp_value:
            wrapper.attr = setup_temp_value  # type: ignore[attr-defined]

        if expect_raise:
            if operation == "set":
                with pytest.raises(AttributeError, match="object has no attribute 'attr'"):
                    wrapper.attr = "new"  # type: ignore[attr-defined]
            elif operation == "del":
                with pytest.raises(AttributeError, match="object has no attribute 'attr'"):
                    del wrapper.attr  # type: ignore[attr-defined]
        else:
            if operation == "set":
                wrapper.attr = "new_value"  # type: ignore[attr-defined]
                assert wrapper.attr == "new_value"  # type: ignore[attr-defined]
                assert getattr(wrapper, "___obj_attr_") == "new_value"
            elif operation == "del":
                del wrapper.attr  # type: ignore[attr-defined]
                assert not hasattr(wrapper, "___obj_attr_")
                with pytest.raises(AttributeError):
                    _ = wrapper.attr  # type: ignore[attr-defined]

    def test_restore_temp_attributes(self) -> None:
        """Tests restoring temp attributes to a new wrapped object."""

        class Simple:
            attr = "default"

        class RestoreTest(StaticWrapper):
            _set_next_wrapped = True
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any = None) -> None:
                self.obj = obj

        wrapper = RestoreTest(None)

        # Saves to temp
        wrapper.attr = "restored"  # type: ignore[attr-defined]
        assert getattr(wrapper, "___obj_attr_") == "restored"

        # Sets new object
        new_obj = Simple()
        wrapper.obj = new_obj

        # Checks transfer
        assert new_obj.attr == "restored"
        assert wrapper.attr == "restored"  # type: ignore[attr-defined]
        assert not hasattr(wrapper, "___obj_attr_")

    def test_class_wrap_with_none(self) -> None:
        """Tests _class_wrap with None in wrapped list."""

        class NoneWrap(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", None)]

        assert not hasattr(NoneWrap, "_obj")

    def test_class_unwrap_non_property(self) -> None:
        """Tests _class_unwrap does not remove non-properties."""

        class UnwrapTest(StaticWrapper):
            pass

        UnwrapTest.new_attr = "keep me"  # type: ignore[attr-defined]
        UnwrapTest._class_unwrap()
        assert UnwrapTest.new_attr == "keep me"  # type: ignore[attr-defined]

    def test_instance_wrap_none_attribute(self) -> None:
        """Tests _wrap when attribute is None."""

        class WrapNone(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", list)]

        wrapper = WrapNone()
        wrapper._wrap()

    def test_instance_wrap_method_descriptor(self) -> None:
        """Tests _wrap instance method with MethodDescriptorType."""

        class SetWrap(StaticWrapper):
            _wrapped_map_: list[tuple[str, type[Any] | None]] = []

        wrapper = SetWrap()
        SetWrap._wrapped_map_ = [("obj", set)]
        wrapper._obj = set  # type: ignore[attr-defined]
        wrapper._wrap()

        assert hasattr(SetWrap, "add")
        # wrapper.add is a bound method that delegates to set.add
        # Since we wrapped the 'set' class, we must pass an instance to add
        s = set()  # type: ignore[var-annotated]
        wrapper.add(s, 1)  # type: ignore[attr-defined]
        assert 1 in s

    @pytest.mark.parametrize(
        ("get_previous_wrapped", "initial_obj_state", "setup_missing", "action"),
        [
            (False, "simple", False, "del"),  # test_del_wrapped_no_previous_wrapped
            (True, "none", False, "del"),  # test_del_wrapped_previous_is_none
            (True, "simple", True, "del"),  # test_del_wrapped_missing_attribute_on_previous
            (True, "simple", True, "set_none"),  # test_set_wrapped_missing_attribute_on_previous
        ],
    )
    def test_previous_wrapped_handling_edge_cases(
        self,
        get_previous_wrapped: bool,
        initial_obj_state: str,
        setup_missing: bool,
        action: str,
    ) -> None:
        """Tests handling of previous wrapped object in edge cases (delete/set).

        Verifies that operations succeed without error even when previous wrapped is None, disabled, or missing
        attributes.

        Args:
            get_previous_wrapped: Value for _get_previous_wrapped attribute.
            initial_obj_state: Initial state of wrapped object ('simple' or 'none').
            setup_missing: Whether to setup a missing attribute scenario.
            action: The action to perform ('del' or 'set_none').
        """

        class Simple:
            pass

        class EdgeCaseWrapper(StaticWrapper):
            _get_previous_wrapped = get_previous_wrapped
            _wrapped_map_: list[tuple[str, type[Any] | None]] = [("obj", Simple)]

            def __init__(self, obj: Any = None) -> None:
                self.obj = obj

        # Setup initial object
        if initial_obj_state == "simple":
            obj = Simple()
            if setup_missing:
                # Adds initially so we can register it
                obj.attr = "val"  # type: ignore[attr-defined]
        else:
            obj = None

        wrapper = EdgeCaseWrapper(obj)

        if setup_missing and obj is not None:
            wrapper._wrap()  # Register 'attr'
            # Deletes from wrapped so it's missing on transfer
            del obj.attr  # type: ignore[attr-defined]

        # Performs action
        if action == "del":
            del wrapper.obj
            # Verifies clean deletion
            assert not hasattr(wrapper, "_obj")
            if setup_missing:
                assert not hasattr(wrapper, "___obj_attr_")
        elif action == "set_none":
            wrapper.obj = None
            if setup_missing:
                assert not hasattr(wrapper, "___obj_attr_")
