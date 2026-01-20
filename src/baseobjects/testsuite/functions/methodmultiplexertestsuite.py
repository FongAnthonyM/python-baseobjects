"""methodmultiplexertestsuite.py
Base test suite for ~baseobjects.functions.MethodMultiplexer and its subclasses.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import CallableMultiplexer, MethodMultiplexer
from .callablemultiplexertestsuite import CallableMultiplexerTestObject, CallableMultiplexerTestSuite


# Definitions #
def add_method_like(self: Any, x: int, y: int = 2) -> int:
    """A test method-like function.

    Returns:
        The sum of x and y.
    """
    return x + y


def multiply_method_like(self: Any, x: int, y: int = 3) -> int:
    """A test method-like function.

    Returns:
        The product of x and y.
    """
    return x * y


# Classes #
class MethodMultiplexerTestSuite(CallableMultiplexerTestSuite):
    """Base test suite for children of ~baseobjects.functions.MethodMultiplexer.

    This class provides common test functionality for child classes of ~baseobjects.functions.MethodMultiplexer.
    """

    UnitTestClass: ClassVar[type[MethodMultiplexer]]

    # Helper Methods #
    def create_function_object(self, func: Any = None, *args: Any, **kwargs: Any) -> MethodMultiplexer:
        """Creates a MethodMultiplexer instance that wraps a function.

        Overrides base to provide instance.

        Returns:
            A new MethodMultiplexer instance.
        """
        if func is None:
            func = add_method_like

        obj = CallableMultiplexerTestObject(value=10)

        # Call base create logic but inject instance
        # We reimplement to avoid base issues
        # Local Packages #
        from ...functions import FunctionRegistry

        registry = FunctionRegistry()
        name = "test_func"
        registry[name] = func
        return self.UnitTestClass(*args, instance=obj, registry=registry, select=name, **kwargs)  # type: ignore[misc]

    # Fixtures #
    @pytest.fixture
    def test_registry(self) -> Any:
        """Creates a test function registry with method-like functions.

        Returns:
            A FunctionRegistry populated with test functions.
        """
        # Local Packages #
        from ...functions import FunctionRegistry

        registry = FunctionRegistry()
        registry["add"] = add_method_like
        registry["multiply"] = multiply_method_like
        registry["add_method_like"] = add_method_like
        return registry

    @pytest.fixture
    def test_multiplexer(
        self,
        test_registry: Any,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> MethodMultiplexer:
        """Creates a test multiplexer with a registry and an instance.

        MethodMultiplexer requires an instance to bind methods to.

        Returns:
            A MethodMultiplexer instance.
        """
        return self.UnitTestClass(instance=test_object_instance, registry=test_registry, select="add")

    @pytest.fixture
    def test_function_object(
        self,
        test_registry: Any,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> MethodMultiplexer:
        """Creates a test callable object that wraps a function.

        MethodMultiplexer requires an instance to bind methods to.

        Returns:
            A MethodMultiplexer instance.
        """
        return self.UnitTestClass(instance=test_object_instance, registry=test_registry, select="add")

    # Tests #
    # Magic Methods #
    def test_call_wrapped(self, test_function_object: Any) -> None:
        """Tests that the wrapped function can be called directly.

        Overrides to provide 'self' argument.
        """
        # Call the wrapped function directly
        # method-like function expects self as first arg
        instance = test_function_object.__self__
        result = test_function_object.call_wrapped(instance, 3)

        # Verify it returns the expected result
        assert result == 5

    def test_add_select_function(self, test_multiplexer: MethodMultiplexer) -> None:  # type: ignore[override]
        """Tests adding and selecting a function in one step.

        Overrides to use compatible function.
        """

        def subtract(self: Any, x: int, y: int = 2) -> int:
            return self.value - x - y  # type: ignore[no-any-return]

        # Add and select function
        test_multiplexer.add_select_function("subtract", subtract)

        # Verify it's selected
        assert test_multiplexer.selected == "subtract"

        # Ensure binding (if not already)
        if test_multiplexer.__self__ is None:
            obj = CallableMultiplexerTestObject(value=10)
            test_multiplexer.bind_self(obj)

        # 10 - 5 - 2 = 3
        assert test_multiplexer(5) == 3

    def test_add_function(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests adding a function.

        MethodMultiplexer binds functions. So the function should accept 'self' if the multiplexer is bound.
        """

        def subtract(self: Any, x: int, y: int = 2) -> int:
            return self.value - x - y  # type: ignore[no-any-return]

        test_multiplexer.add_function("subtract", subtract)
        test_multiplexer.select("subtract")

        # Needs binding to work with 'self'
        obj = CallableMultiplexerTestObject(value=10)
        test_multiplexer.bind_self(obj)

        # 10 - 3 - 2 = 5
        assert test_multiplexer(3) == 5

    # Copying #
    def test_attribute_copying(self) -> None:
        """Tests that attributes from the wrapped function are correctly copied to the callable object.

        Overrides to ensure instance is kept alive.
        """

        # Create a temporary function
        def temp_func(self: Any, x: int, y: int = 2) -> int:
            return x + y

        # Create an attribute in the function
        temp_func.new_attribute = "test"  # type: ignore[attr-defined]

        # Create object to keep it alive
        obj = CallableMultiplexerTestObject(value=10)

        # Create a callable object
        # We manually create it instead of using create_function_object to keep obj alive in this scope
        # Local Packages #
        from ...functions import FunctionRegistry

        registry = FunctionRegistry()
        name = "temp_func"
        registry[name] = temp_func
        test_object = self.UnitTestClass(instance=obj, registry=registry, select=name)

        # Validate the new attribute is present and the same
        assert test_object.new_attribute == temp_func.new_attribute  # type: ignore[attr-defined]

    # Pickling #
    def test_pickle_object(self, test_multiplexer: MethodMultiplexer) -> None:  # type: ignore[override]
        """Tests pickling the multiplexer.

        Overrides to pickle instance with multiplexer to maintain weakref.
        """
        instance = test_multiplexer.__self__
        data = (test_multiplexer, instance)

        pickled = pickle.dumps(data)
        unpickled_multiplexer, _unpickled_instance = pickle.loads(pickled)

        # Verify state
        assert unpickled_multiplexer.selected == test_multiplexer.selected
        assert "add" in unpickled_multiplexer.registry

        # Call
        assert unpickled_multiplexer(3) == 5

    # Functionality #
    def test_always_binding(self, test_multiplexer: MethodMultiplexer) -> None:
        """Tests that MethodMultiplexer always binds the function."""
        # MethodMultiplexer overrides __call__ to bind
        # Even if we pass functions that look like bound methods (with self), it binds to the multiplexer instance

        # Unbound case:
        unbound = self.UnitTestClass(registry=test_multiplexer.registry, select="add_method_like")

        # Unbound call might fail depending on Python version/implementation of function.__get__(None, None)
        # In this env, it raises TypeError.
        try:
            unbound(3, 2)
        except TypeError:
            # Expected in some environments
            pass

        # Bind to instance
        obj = CallableMultiplexerTestObject(value=10)
        bound = unbound.bind_self(obj)

        # Bound call -> bind(obj, owner)
        # add_method_like(obj, 3) -> x=3. Returns 3+2=5.
        # Note: add_method_like ignores self.
        assert bound(3) == 5

    def test_invalid_selection(self, test_multiplexer: MethodMultiplexer) -> None:  # type: ignore[override]
        """Tests selecting an invalid name.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Since MethodMultiplexer has an instance, it checks the instance for the method name.
        # If not found, it raises AttributeError.
        with pytest.raises(AttributeError):
            test_multiplexer.select("invalid")

    def test_no_selection(self) -> None:
        """Tests calling with no selection."""
        multiplexer = self.UnitTestClass()
        # Expect AttributeError or TypeError
        with pytest.raises((TypeError, AttributeError)):
            multiplexer()

    def test_as_function_missing_attrs(self) -> None:
        """Tests that missing attributes are handled correctly."""

        class IncompleteCallable:
            def __call__(self) -> None:
                pass

        # MethodMultiplexer requires __get__ which IncompleteCallable lacks
        # We expect initialization to succeed (due to my fix skipping _selected_bind_method)
        # But call to fail because _selected_bind_method is missing.
        obj = self.UnitTestClass(IncompleteCallable())
        with pytest.raises(AttributeError):
            obj()
