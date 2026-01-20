"""basemethod_test.py
Tests for the BaseMethod class in the baseobjects package.

This module provides tests for the BaseMethod class, which extends BaseCallable to create method-like callable objects
that maintain a reference to the instance they're bound to and properly handle method binding semantics. This class is
particularly useful for creating custom method types, method factories, and method decorators.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Standard Libraries #
import gc

# Imports #
import pickle
import weakref
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseCallable, BaseMethod
from baseobjects.testsuite.bases import BaseMethodTestSuite, ConcreteBindTarget, concrete_method


# Classes #
class SlotCallable(BaseCallable):
    """A callable class with slots for testing."""

    __slots__ = ("_extra",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the SlotCallable."""
        super().__init__(*args, **kwargs)
        self._extra = 1


class SlottedMethod(BaseMethod):
    """A method class with slots for testing."""

    __slots__ = ("_extra",)

    def __init__(self, *args: Any, init: bool = True, **kwargs: Any) -> None:
        """Initializes the SlottedMethod."""
        super().__init__(*args, init=init, **kwargs)
        if init:
            self._extra = 1


# Helper Functions #
def setup_slotted_linked() -> tuple[BaseMethod, SlotCallable]:
    """Sets up a slotted method linked to an instance.

    Returns:
        tuple[BaseMethod, SlotCallable]: The method and the instance.
    """
    i = SlotCallable(len)
    return SlottedMethod(len, instance=i), i


def setup_slotted_cleared() -> SlottedMethod:
    """Sets up a slotted method with its dict cleared.

    Returns:
        SlottedMethod: The slotted method.
    """
    i = SlotCallable(len)
    m = SlottedMethod(len, instance=i)
    if hasattr(m, "__dict__"):
        m.__dict__.clear()
    return m


class TestBaseMethod(BaseMethodTestSuite):
    """Tests the BaseMethod class.

    This class tests the functionality of the BaseMethod class, which extends BaseCallable to create method-like
    callable objects that maintain a reference to the instance they're bound to.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[BaseMethod]] = BaseMethod

    # Instance Methods #
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test method
        instance = self.UnitTestClass(concrete_method)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has the correct wrapped function
        assert instance.__func__ is concrete_method

        # Verify it has no bound instance by default
        assert instance.__self__ is None

        # Create an instance with a test method and a bound instance
        bind_target = self.create_bind_target()
        bound_instance = self.UnitTestClass(concrete_method, instance=bind_target, owner=self.BindTargetClass)

        # Verify it has the correct bound instance
        assert bound_instance.__self__ is bind_target
        assert bound_instance.__owner__ is self.BindTargetClass

    def test_is_binding_flag(self) -> None:
        """Tests the is_binding flag."""
        # Create a method with is_binding=False
        method = self.create_method_object(is_binding=False)

        # Verify the flag is set correctly
        assert method.is_binding is False  # type: ignore[attr-defined]

        # Create a class with the method as a descriptor
        class DescriptorTest:
            descriptor_method = method

        # Create an instance of the class
        instance = DescriptorTest()

        # Verify the descriptor returns the same method (not bound to the instance)
        assert instance.descriptor_method is method  # type: ignore[misc]

        # Verify it's not bound to the instance
        assert instance.descriptor_method.__self__ is None  # type: ignore[misc]

        # Create a method with is_binding=True
        binding_method = self.create_method_object(is_binding=True)

        # Create a class with the method as a descriptor
        class BindingDescriptorTest:
            descriptor_method = binding_method

        # Create an instance of the class
        binding_instance = BindingDescriptorTest()

        # Verify the descriptor returns the same method (bound to the instance)
        assert binding_instance.descriptor_method is binding_method  # type: ignore[misc]

        # Verify it's bound to the instance
        assert binding_instance.descriptor_method.__self__ is binding_instance  # type: ignore[misc]

    @pytest.mark.parametrize(
        ("setup", "validator"),
        [
            (
                lambda: setup_slotted_linked(),
                lambda loaded: loaded[0]._extra == 1 and loaded[0].__self__ is loaded[1],
            ),
            (
                lambda: SlottedMethod(init=False),
                lambda loaded: loaded.__wrapped__ is None and loaded.__self__ is None and not hasattr(loaded, "_extra"),
            ),
            (
                lambda: setup_slotted_cleared(),
                lambda loaded: loaded._extra == 1 and loaded.__wrapped__ is None and loaded.__self__ is None,
            ),
        ],
    )
    def test_pickling_scenarios(self, setup: Any, validator: Any) -> None:
        """Tests pickling of different method scenarios.

        Args:
            setup: Function that returns the object(s) to pickle.
            validator: Function that validates the loaded object(s).
        """
        data = setup()
        dump = pickle.dumps(data)
        loaded = pickle.loads(dump)
        assert validator(loaded)

    def test_bind_to_attribute_none_instance(self) -> None:
        """Tests bind_to_attribute with None instance."""
        method = self.UnitTestClass(lambda: None)
        with pytest.raises(AttributeError):
            method.bind_to_attribute(None)

    def test_weak_reference(self) -> None:
        """Tests that the method maintains a weak reference to the bound instance."""
        # Create a method
        method = self.create_method_object()

        # Create a new scope to control the lifetime of the instance
        def inner_scope() -> weakref.ReferenceType[Any]:
            # Create a local instance
            local_instance = self.create_bind_target()

            # Bind the method to the local instance
            method.__self__ = local_instance  # type: ignore[attr-defined]

            # Verify it's bound to the correct instance
            assert method.__self__ is local_instance  # type: ignore[attr-defined]

            # Return a weak reference to the local instance
            return weakref.ref(local_instance)

        # Get a weak reference to the local instance
        weak_ref = inner_scope()

        # Force garbage collection
        gc.collect()

        # Verify the local instance has been garbage collected
        assert weak_ref() is None

        # Verify the method's bound instance is now None
        assert method.__self__ is None  # type: ignore[attr-defined]

    def test_descriptor_protocol(self, test_method_object: BaseMethod) -> None:
        """Tests that the callable implements the descriptor protocol for method binding.

        This test only varifies that the descriptor returns a bound method. This method may be overwritten to include
        validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
        """

        class BindTarget:
            new_method: Any = test_method_object

        instance = BindTarget()
        assert isinstance(instance.new_method, self.UnitTestClass)
        assert instance.new_method.__self__ is instance

    @pytest.mark.parametrize("is_binding", [True, False])
    def test_bind_self(self, test_bind_target: ConcreteBindTarget, is_binding: bool) -> None:
        """Tests that the method can be bound to an instance.

        This test verifies that a bound method is returned and that it functions correctly.

        Args:
            test_bind_target: A fixture providing an instance to bind the method to.
            is_binding: Whether the method should be binding.
        """
        # Create a method
        method = cast(BaseMethod, self.create_method_object(is_binding=is_binding))

        # Bind the method to the target
        bound_method = method.bind_self(test_bind_target, self.BindTargetClass)

        # Verify it's the same method (not a new instance)
        assert bound_method is method

        if is_binding:
            # Verify it's bound to the correct instance
            assert bound_method.__self__ is test_bind_target
            assert bound_method.__owner__ is self.BindTargetClass

            # Verify it returns the expected result when called
            result = bound_method(3)
            assert result == (5, test_bind_target)  # (3 + 2, instance)
        else:
            # Verify it's not bound to the instance
            assert bound_method.__self__ is None

    @pytest.mark.parametrize("name", [None, "custom_method"])
    @pytest.mark.parametrize("use_owner_kwarg", [False, True])
    def test_bind_to_attribute(self, name: str | None, use_owner_kwarg: bool) -> None:
        """Tests that the method can be bound to an instance and set as an attribute.

        This test verifies that a bound method is returned and bound to the target instance's attribute,
        and that it functions correctly.
        """
        # Call the parent test method
        super().test_bind_to_attribute(name, use_owner_kwarg)

        # Create a method and a bind target
        method = cast(BaseMethod, self.create_method_object())
        bind_target = self.create_bind_target()

        # Bind the method to the target and set it as an attribute
        assert method.__wrapped__ is not None
        if name:
            bound_method = method.bind_to_attribute(bind_target, self.BindTargetClass, name=name)
            expected_name = name
        else:
            bound_method = method.bind_to_attribute(bind_target, self.BindTargetClass)
            expected_name = method.__wrapped__.__name__

        # Verify it's the same method (not a new instance)
        assert bound_method is method

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is bind_target
        assert bound_method.__owner__ is self.BindTargetClass

        # Verify it's set as an attribute on the instance
        assert method.__wrapped__ is not None
        assert hasattr(bind_target, expected_name)

        # Verify it returns the expected result when called through the attribute
        result = getattr(bind_target, expected_name)(3)
        assert result == (5, bind_target)  # (3 + 2, instance)

    def test_call_binding_no_get_method(self) -> None:
        """Tests call_binding when the wrapped object has no __get__ method."""

        class CallableNoGet:
            def __call__(self, instance: Any, x: int, y: int) -> tuple[Any, int]:
                return instance, x + y

        c = CallableNoGet()
        # Verify no __get__
        assert not hasattr(c, "__get__")

        bind_target = self.create_bind_target()
        method = self.UnitTestClass(c, instance=bind_target)

        # This calls call_binding internally when called
        result = method(3, 4)

        assert result == (bind_target, 7)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
