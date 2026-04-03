#!/usr/bin/env python
"""automaticproperties_test.py
Test for the AutomaticProperties class.

This module provides tests for the AutomaticProperties class, which is an abstract class that creates properties
automatically based on a properties dictionary.
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.objects import AutomaticProperties
from baseobjects.testsuite.objects import AutomaticPropertiesTestSuite


# Definitions #
# Classes #
class ConcreteAutomaticPropertiesClass(AutomaticProperties):
    """A concrete implementation of AutomaticProperties for testing."""

    # Class Attributes #
    properties: dict[str, str | tuple[Any, ...]] = {
        "test_prop": "_test_prop",
        "another_prop": "_another_prop",
        "complex_prop": ("property_method_factory", "_complex_prop", {}),
    }


class SlotAutomaticProperties(AutomaticProperties):
    """A AutomaticProperties subclass with slots for testing."""

    __slots__ = ("extra",)

    def __init__(self, **kwargs: Any) -> None:
        """Initializes SlotAutomaticProperties."""
        self.extra = 1
        super().__init__(**kwargs)


class TestAutomaticProperties(AutomaticPropertiesTestSuite):
    """Tests the AutomaticProperties class.

    This class tests the functionality of the AutomaticProperties class, which is an abstract class that creates
    properties automatically based on a properties dictionary.
    """

    # Attributes #
    UnitTestClass = ConcreteAutomaticPropertiesClass

    # Instance Methods #
    # Tests
    def test_pickling_slots(self) -> None:
        """Tests pickling with __slots__.

        This test verifies that objects with __slots__ can be pickled and unpickled correctly.
        """
        obj = SlotAutomaticProperties()
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.extra == 1
        assert isinstance(loaded, SlotAutomaticProperties)

    @pytest.mark.parametrize("prop", ["test_prop", "another_prop"])
    def test_property_creation(self, prop: str) -> None:
        """Tests that properties are created correctly."""
        assert hasattr(self.UnitTestClass, prop)
        assert isinstance(getattr(self.UnitTestClass, prop), property)

    @pytest.mark.parametrize(("prop", "attr"), [("test_prop", "_test_prop"), ("another_prop", "_another_prop")])
    def test_property_access(self, test_object: ConcreteAutomaticPropertiesClass, prop: str, attr: str) -> None:
        """Tests that properties can be accessed correctly."""
        setattr(test_object, attr, "test value")
        assert getattr(test_object, prop) == "test value"

    @pytest.mark.parametrize(("prop", "attr"), [("test_prop", "_test_prop"), ("another_prop", "_another_prop")])
    def test_property_modification(self, test_object: ConcreteAutomaticPropertiesClass, prop: str, attr: str) -> None:
        """Tests that properties can be modified correctly."""
        setattr(test_object, prop, "new test value")
        assert getattr(test_object, attr) == "new test value"
        assert getattr(test_object, prop) == "new test value"

    @pytest.mark.parametrize(("prop", "attr"), [("test_prop", "_test_prop"), ("another_prop", "_another_prop")])
    def test_property_deletion(self, test_object: ConcreteAutomaticPropertiesClass, prop: str, attr: str) -> None:
        """Tests that properties can be deleted correctly."""
        setattr(test_object, attr, "test value")
        delattr(test_object, prop)

        assert not hasattr(test_object, attr)
        with pytest.raises(AttributeError):
            getattr(test_object, prop)

    def test_construct_properties(self) -> None:
        """Tests the _construct_properties_ method."""

        class UnitTestClass(ConcreteAutomaticPropertiesClass):
            """A test class for _construct_properties_."""

        property_map: dict[str, Any] = {
            "dynamic_prop": "_dynamic_prop",
            "another_dynamic_prop": "_another_dynamic_prop",
        }
        UnitTestClass._construct_properties_(property_map)

        obj = UnitTestClass()
        obj._dynamic_prop = "dynamic value"  # type: ignore[attr-defined]
        obj._another_dynamic_prop = "another dynamic value"  # type: ignore[attr-defined]

        assert hasattr(UnitTestClass, "dynamic_prop")
        assert hasattr(UnitTestClass, "another_dynamic_prop")
        assert isinstance(UnitTestClass.dynamic_prop, property)
        assert isinstance(UnitTestClass.another_dynamic_prop, property)
        assert obj.dynamic_prop == "dynamic value"  # type: ignore[attr-defined]
        assert obj.another_dynamic_prop == "another dynamic value"  # type: ignore[attr-defined]

    def test_complex_property_definition(self) -> None:
        """Tests that complex property definitions work correctly."""

        class ComplexPropertyClass(ConcreteAutomaticPropertiesClass):
            properties: dict[str, Any] = {
                "complex_prop_2": ("property_method_factory", "_complex_prop_2", {}),
            }

        obj: Any = ComplexPropertyClass()
        obj._complex_prop_2 = "complex value"

        assert hasattr(ComplexPropertyClass, "complex_prop_2")
        assert isinstance(ComplexPropertyClass.complex_prop_2, property)
        assert obj.complex_prop_2 == "complex value"

    def test_default_property_function_factory(self) -> None:
        """Tests the default_property_function_factory attribute."""

        class DefaultFactoryClass(ConcreteAutomaticPropertiesClass):
            """A test class for default_property_function_factory."""

            default_property_function_factory = "property_class_method_factory"
            properties: dict[str, Any] = {"default_factory_prop": "_default_factory_prop"}

        obj: Any = DefaultFactoryClass()
        obj._default_factory_prop = "default factory value"

        assert hasattr(DefaultFactoryClass, "default_factory_prop")
        assert isinstance(DefaultFactoryClass.default_factory_prop, property)
        assert obj.default_factory_prop == "default factory value"

    def test_property_inheritance(self) -> None:
        """Tests that properties are inherited correctly."""

        class ParentClass(ConcreteAutomaticPropertiesClass):
            properties: dict[str, Any] = {"parent_prop": "_parent_prop"}

        class ChildClass(ParentClass):
            """Child class for testing property inheritance."""

            properties: dict[str, Any] = {"child_prop": "_child_prop"}

        obj: Any = ChildClass()
        obj._parent_prop = "parent value"
        obj._child_prop = "child value"

        assert hasattr(ChildClass, "parent_prop")
        assert hasattr(ChildClass, "child_prop")
        assert isinstance(ChildClass.parent_prop, property)
        assert isinstance(ChildClass.child_prop, property)
        assert obj.parent_prop == "parent value"
        assert obj.child_prop == "child value"

    def test_callable_factory(self) -> None:
        """Tests using a callable as a property factory."""

        def custom_factory(
            info: str,
        ) -> tuple[Callable[[Any], Any], Callable[[Any, Any], None] | None, Callable[[Any], None] | None]:
            return self.UnitTestClass.property_method_factory(info)

        class CallableFactoryClass(ConcreteAutomaticPropertiesClass):
            """A test class for callable factory."""

            properties: dict[str, Any] = {
                "callable_prop": (custom_factory, "_callable_prop", {}),
            }

        obj: Any = CallableFactoryClass()
        obj._callable_prop = "callable value"

        assert hasattr(CallableFactoryClass, "callable_prop")
        assert isinstance(CallableFactoryClass.callable_prop, property)
        assert obj.callable_prop == "callable value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
