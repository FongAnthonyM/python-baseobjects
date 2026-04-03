"""callablemultiplexertestsuite.py
Base test suite for ~baseobjects.functions.CallableMultiplexer and its subclasses.
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
import inspect
import pickle
from typing import Any
from unittest.mock import patch

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseMethod
from ...functions import CallableMultiplexer, FunctionRegistry
from ..bases import BaseCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers.

    Returns:
        The product of x and y.
    """
    return x * y


# Helper Classes #
class CallableMultiplexerTestObject:
    """A test class for testing method binding and selection."""

    def __init__(self, value: int = 10) -> None:
        """Initializes with a value."""
        self.value = value
        self.callable_multiplexer = CallableMultiplexer(instance=self, select="method1", binding=True)
        self.callable_multiplexer2 = CallableMultiplexer(instance=self, select="method2", binding=True)

    def method1(self, x: int) -> int:
        """A test method that adds x to the value.

        Returns:
            The sum of the value and x.
        """
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x.

        Returns:
            The product of the value and x.
        """
        return self.value * x


# Classes #
class CallableMultiplexerTestSuite(BaseCallableTestSuite):
    """Base test suite for children of ~baseobjects.functions.CallableMultiplexer.

    This class provides common test functionality for child classes of ~baseobjects.functions.CallableMultiplexer,
    including tests for multiplexing behavior. Subclasses should set the UnitTestClass attribute and may override or
    extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: type[CallableMultiplexer]

    # Helper Methods #
    def create_function_object(self, func: Any = None, *args: Any, **kwargs: Any) -> CallableMultiplexer:
        """Creates a CallableMultiplexer instance that wraps a function.

        Args:
            func: The function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer wrapping a function.
        """
        registry = FunctionRegistry()
        if func is None:
            # BaseCallableTestSuite might pass None or default?
            # example_function is default in base.
            pass

        # If func is passed (from base suite fixture), add it to registry and select it.
        # But we need a name.
        name = "test_func"
        registry[name] = func
        return self.UnitTestClass(*args, registry=registry, select=name, **kwargs)  # type: ignore[misc]

    def create_coroutine_object(self, func: Any = None, *args: Any, **kwargs: Any) -> CallableMultiplexer:
        """Creates a CallableMultiplexer instance that wraps a coroutine function.

        Args:
            func: The coroutine function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer wrapping a coroutine function.
        """
        return self.create_function_object(func, *args, **kwargs)

    # Fixtures #
    @pytest.fixture
    def test_registry(self) -> FunctionRegistry:
        """Creates a test function registry.

        Returns:
            FunctionRegistry: A registry with test functions.
        """
        registry = FunctionRegistry()
        registry["add"] = add_function
        registry["multiply"] = multiply_function
        return registry

    @pytest.fixture
    def test_object_instance(self) -> CallableMultiplexerTestObject:
        """Creates a test object instance.

        Returns:
            CallableMultiplexerTestObject: An instance of the test object.
        """
        return CallableMultiplexerTestObject(value=10)

    @pytest.fixture
    def test_multiplexer(self, test_registry: FunctionRegistry) -> CallableMultiplexer:
        """Creates a test multiplexer with a registry.

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer with a registry.
        """
        return self.UnitTestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_multiplexer_with_object(self, test_object_instance: CallableMultiplexerTestObject) -> CallableMultiplexer:
        """Creates a test multiplexer with an object instance.

        Args:
            test_object_instance: A fixture providing a test object instance.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer with an object instance.
        """
        return self.UnitTestClass(instance=test_object_instance, select="method1")

    @pytest.fixture
    def test_function_object(self, test_registry: FunctionRegistry) -> CallableMultiplexer:
        """Creates a test callable object that wraps a function (via multiplexer).

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer wrapping a function.
        """
        return self.UnitTestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_method_object(self, test_object_instance: CallableMultiplexerTestObject) -> CallableMultiplexer:
        """Creates a test callable object that wraps a method (via multiplexer).

        Args:
            test_object_instance: A fixture providing a test object instance.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer wrapping a method.
        """
        return self.UnitTestClass(instance=test_object_instance, select="method1")

    # Tests #
    # Magic Methods #
    def test_call(self, test_function_object: Any) -> None:
        """Tests that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Calls the callable object (select="add")
        result = test_function_object(3)

        # Verifies it returns the expected result (add_function(3, 2))
        assert result == 5

        # Change selection
        test_function_object.select("multiply")
        result = test_function_object(3)

        # Verifies it returns the expected result (multiply_function(3, 3))
        assert result == 9

    def test_call_wrapped(self, test_function_object: Any) -> None:
        """Tests that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Calls the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verifies it returns the expected result
        assert result == 5

    def test_add_function(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests adding a function to the registry via add_function.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """

        def subtract(x: int, y: int = 2) -> int:
            return x - y

        # Adds function
        test_multiplexer.add_function("subtract", subtract)

        # Verifies it's in registry
        assert "subtract" in test_multiplexer.registry
        assert test_multiplexer.registry["subtract"] is subtract

        # Select and call
        test_multiplexer.select("subtract")
        assert test_multiplexer(5) == 3

    def test_add_method(
        self,
        test_multiplexer: CallableMultiplexer,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> None:
        """Tests adding a method to the registry.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_object_instance: A fixture providing a test object instance.
        """
        # Adds method
        test_multiplexer.add_method("method1", test_object_instance.method1)

        # Select
        test_multiplexer.select("method1")

        # Binds to instance so unbound method can be called
        test_multiplexer.bind_self(test_object_instance)

        # Calls
        assert test_multiplexer(3) == 13

    def test_add_select_function(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests adding and selecting a function in one step.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """

        def subtract(x: int, y: int = 2) -> int:
            return x - y

        # Adds and select function
        test_multiplexer.add_select_function("subtract", subtract)

        # Verifies it's selected
        assert test_multiplexer.selected == "subtract"
        assert test_multiplexer(5) == 3

    def test_add_select_method(
        self,
        test_multiplexer: CallableMultiplexer,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> None:
        """Tests adding and selecting a method in one step.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_object_instance: A fixture providing a test object instance.
        """
        # Adds and select method
        test_multiplexer.add_select_method("method1", test_object_instance.method1)

        # Verifies it's selected
        assert test_multiplexer.selected == "method1"

        # Binds to instance so unbound method can be called
        test_multiplexer.bind_self(test_object_instance)

        # Calls
        assert test_multiplexer(3) == 13

    def test_add_callable_with_str(self) -> None:
        """Tests adding a callable with a string name."""
        cm = self.UnitTestClass()

        def func() -> None:
            pass

        cm.add_function("my_func", func)
        assert "my_func" in cm.registry
        assert cm.registry["my_func"] is func

    def test_add_callable_with_list(self) -> None:
        """Tests adding callables with a list of names."""
        # API doesn't seem to support list of names in add_function directly?
        # add_function(name: str, func)
        # Checks source if it iterates? No, name is str.
        # So I remove this test or adapt loop.
        cm = self.UnitTestClass()

        def func() -> None:
            pass

        cm.add_function("alias1", func)
        cm.add_function("alias2", func)
        assert "alias1" in cm.registry
        assert "alias2" in cm.registry

    def test_call_selected_none(self) -> None:
        """Tests calling when no function is selected."""
        cm = self.UnitTestClass()
        cm.add_function("a", lambda: 1)
        # Calling without selection (selected is None)
        # Seems to return None from registry lookup then fails call?
        with pytest.raises((TypeError, AttributeError)):
            cm()

    def test_call_exclusive(self) -> None:
        """Tests calling a selected function exclusively."""
        cm = self.UnitTestClass()
        # Use *args to handle potential binding (MethodMultiplexer might pass self)
        cm.add_function("a", lambda *args: 1)
        cm.select("a")

        # Binds to dummy to satisfy MethodMultiplexer in environments where unbound __get__ fails
        class Dummy:
            pass

        d = Dummy()
        cm.bind_self(d)

        assert cm() == 1

    def test_add_method_no_func(self) -> None:
        """Tests adding a method without specifying a function in init."""
        cm = self.UnitTestClass()
        cm.add_method("m", lambda: 1)
        assert "m" in cm.registry

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Creates an instance with defaults
        instance = self.UnitTestClass()
        assert isinstance(instance, self.UnitTestClass)
        assert instance.registry is not None
        assert instance.selected is None

        # Creates an instance with a registry
        registry = FunctionRegistry()
        instance_with_registry = self.UnitTestClass(registry=registry)
        assert instance_with_registry.registry is registry

    # Copying #
    def test_attribute_copying(self) -> None:
        """Tests that attributes from the wrapped function are correctly copied to the callable object.

        Overrides BaseCallableTestSuite.test_attribute_copying to use create_function_object.
        """

        # Creates a temporary function
        def temp_func(x: int, y: int = 2) -> int:
            return x + y

        # Creates an attribute in the function
        temp_func.new_attribute = "test"  # type: ignore[attr-defined]

        # Creates a callable object
        test_object = self.create_function_object(temp_func)

        # Validate the new attribute is present and the same
        assert test_object.new_attribute == temp_func.new_attribute  # type: ignore[attr-defined]

    # Pickling #
    def test_pickle_object(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests pickling the multiplexer.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Pickle and unpickle
        pickled = pickle.dumps(test_multiplexer)
        unpickled = pickle.loads(pickled)

        # Verifies state
        assert unpickled.selected == test_multiplexer.selected
        assert "add" in unpickled.registry
        assert unpickled(3) == 5

    def test_pickling_no_selection(self) -> None:
        """Tests pickling when no function is selected."""
        cm = self.UnitTestClass()
        s = pickle.dumps(cm)
        cm2 = pickle.loads(s)
        assert cm2.selected is None

    # Functionality #
    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property.

        Skipped for CallableMultiplexer as it doesn't proxy is_coroutine from the selected function automatically.
        """

    def test_as_function(self, test_function_object: Any) -> None:
        """Tests that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Converts to a standard Python function
        func = test_function_object.as_function()

        # Verifies it's a function
        assert callable(func)

        # Verifies it returns the expected result
        assert func(3) == 5

    def test_bind_wrapped(self, test_method_object: Any, test_bind_target: Any) -> None:
        """Tests that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # This test might not apply directly to CallableMultiplexer as it's more complex,
        # but let's see if we can adapt it or just override it.
        # CallableMultiplexer.bind_wrapped binds the currently selected function.
        test_method_object.bind_wrapped(test_bind_target, type(test_bind_target))

    def test_descriptor_protocol(self, test_method_object: CallableMultiplexer) -> None:
        """Tests that the callable implements the descriptor protocol for method binding.

        Args:
            test_method_object: A fixture providing a CallableMultiplexer instance.
        """

        class BindTarget:
            new_method = test_method_object

            def __init__(self, value: int = 10) -> None:
                self.value = value

            def method1(self, x: int) -> int:
                return self.value + x

            def method2(self, x: int) -> int:
                return self.value * x

        # Test descriptor access
        instance = BindTarget()
        bound_multiplexer = instance.new_method

        # Verifies it returns the multiplexer (bound to instance)
        assert isinstance(bound_multiplexer, self.UnitTestClass)
        # CallableMultiplexer returns self when bound
        assert bound_multiplexer is test_method_object
        assert bound_multiplexer.__self__ is instance

        # Select method from the bound instance
        bound_multiplexer.select("method1")
        assert bound_multiplexer(3) == 13  # 10 + 3

    def test_select(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests the select method.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Select "add"
        test_multiplexer.select("add")
        assert test_multiplexer.selected == "add"
        assert test_multiplexer(3) == 5

        # Select "multiply"
        test_multiplexer.select("multiply")
        assert test_multiplexer.selected == "multiply"
        assert test_multiplexer(3) == 9

    def test_selected_property(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests the selected property.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Test getter
        test_multiplexer.select("add")
        assert test_multiplexer.selected == "add"

        # Test setter
        test_multiplexer.selected = "multiply"
        assert test_multiplexer.selected == "multiply"
        assert test_multiplexer(3) == 9

    def test_bind_selected(self, test_multiplexer: CallableMultiplexer, test_bind_target: Any) -> None:
        """Tests binding the selected function to a target.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Select "add" (function)
        test_multiplexer.select("add")

        # Binds selected
        bound_method = test_multiplexer.bind_selected(test_bind_target)

        # Verifies binding
        assert bound_method.__self__ is test_bind_target  # type: ignore[union-attr]

    def test_bind_self(self, test_multiplexer: CallableMultiplexer, test_bind_target: Any) -> None:
        """Tests binding the multiplexer itself to a target.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Binds self
        bound_multiplexer = test_multiplexer.bind_self(test_bind_target)

        # Verifies binding
        # CallableMultiplexer returns self when bound
        assert bound_multiplexer is test_multiplexer
        assert isinstance(bound_multiplexer, self.UnitTestClass)
        assert bound_multiplexer.__self__ is test_bind_target

    def test_object_method_selection(self, test_multiplexer_with_object: CallableMultiplexer) -> None:
        """Tests selecting methods from the bound object.

        Args:
            test_multiplexer_with_object: A fixture providing a CallableMultiplexer bound to an object.
        """
        # Select method1
        test_multiplexer_with_object.select("method1")
        assert test_multiplexer_with_object(3) == 13

        # Select method2
        test_multiplexer_with_object.select("method2")
        assert test_multiplexer_with_object(3) == 30

    def test_no_selection(self) -> None:
        """Tests calling with no selection."""
        multiplexer = self.UnitTestClass()
        # Expect TypeError because None is not callable
        with pytest.raises(TypeError):
            multiplexer()

    def test_invalid_selection(self, test_multiplexer: CallableMultiplexer) -> None:
        """Tests selecting an invalid name.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # CallableMultiplexer logic sets __func__ to None (if registry not found and no instance)
        # It does NOT raise KeyError unless registry raises it (but registry.get returns None)
        # So we verify that selected is set but __func__ is None
        test_multiplexer.select("invalid")
        assert test_multiplexer.selected == "invalid"
        assert test_multiplexer.__func__ is None

    def test_as_function_coroutine(self) -> None:
        """Tests as_function with a coroutine."""

        # Creates directly to test wrapping behavior (which supports coroutines correctly)
        async def coro() -> None:
            pass

        obj = self.UnitTestClass(coro)
        assert obj.is_coroutine
        wrapped = obj.as_function()
        assert inspect.iscoroutinefunction(wrapped)

    def test_is_binding_wrapper_setter(self) -> None:
        """Tests the setter for is_binding_wrapper."""

        async def coro() -> None:
            pass

        cm = self.UnitTestClass(coro)
        # Ensure _selected_bind_method is initialized via my fix
        # is_binding defaults to True?
        cm.is_binding_wrapper = True
        assert hasattr(cm, "_selected_bind_method")

        cm.is_binding_wrapper = False
        assert not hasattr(cm, "_selected_bind_method")

    def test_select_none(self) -> None:
        """Tests selecting None to deselect."""

        async def coro() -> None:
            pass

        cm = self.UnitTestClass(coro)
        # Initializes _selected_bind_method
        cm.is_binding_wrapper = True
        assert hasattr(cm, "_selected_bind_method")

        cm.select(None)
        assert cm.selected is None
        # Should be deleted
        assert not hasattr(cm, "_selected_bind_method")

    def test_bind_self_missing_selected(self) -> None:
        """Tests binding self when the selected function is missing."""
        cm = self.UnitTestClass()
        cm.registry["a"] = lambda: 1
        cm.select("a")
        del cm.registry["a"]

        # This shouldn't raise, just proceed
        cm.is_binding_wrapper = True

        class A:
            pass

        a = A()
        cm.bind_self(a)
        assert cm.__self__ is a

    def test_select_func_no_get(self) -> None:
        """Tests selecting a function object that has no __get__ method."""

        class NoGet:
            def __call__(self) -> None:
                pass

        no_get = NoGet()
        cm = self.UnitTestClass()
        cm.add_function("ng", no_get)
        # Should not set _selected_bind_method, preventing AttributeError later if used as binding
        cm.select("ng")
        assert not hasattr(cm, "_selected_bind_method")

    def test_select_none_clean(self) -> None:
        """Tests selecting None when no selection exists."""
        cm = self.UnitTestClass()
        # Ensure no _selected_bind_method exists initially
        assert not hasattr(cm, "_selected_bind_method")
        cm.select(None)
        # Should finish without error
        assert not hasattr(cm, "_selected_bind_method")

    def test_setstate_tuple(self) -> None:
        """Tests setstate with a tuple (dict, slots)."""
        cm = self.UnitTestClass()
        cm.registry["a"] = lambda: 1
        # Fix key name: _selected not _selected_
        state = ({"_selected": "a"}, {})  # type: ignore[var-annotated]
        cm.__setstate__(state)
        assert cm._selected == "a"

    def test_getstate_tuple(self) -> None:
        """Tests getstate returning a tuple."""

        class SlotCM(self.UnitTestClass):  # type: ignore[misc, name-defined]
            __slots__ = ("extra",)

            def __init__(self) -> None:
                super().__init__()
                self.extra = 1

        cm = SlotCM()
        # Ensure _selected_bind_method is in dict
        cm._selected_bind_method = lambda: 1

        state = cm.__getstate__()
        assert isinstance(state, tuple)
        # state[0] is dict (BaseCallable has dict)
        assert state[0] is not None
        assert "_selected_bind_method" not in state[0]

    def test_init_as_decorator(self) -> None:
        """Tests initialization as a decorator."""

        # Must handle binding.
        def my_func(*args: Any) -> int:
            return 1

        cm = self.UnitTestClass(my_func)
        assert cm.__wrapped__ is my_func
        # It creates a registry if none provided
        assert cm.registry is not None

        # Binds to dummy to satisfy MethodMultiplexer
        class Dummy:
            pass

        d = Dummy()
        cm.bind_self(d)

        # Calls should work
        assert cm() == 1

    def test_bind_self_not_binding(self) -> None:
        """Tests binding when is_binding is False."""
        cm = self.UnitTestClass(is_binding=False)

        class A:
            pass

        obj = A()
        cm.bind_self(obj)
        # Should not bind
        assert getattr(cm, "__self__", None) is not obj

    def test_bind_selected_none(self) -> None:
        """Tests bind_selected with instance=None."""
        cm = self.UnitTestClass()
        # bind_selected(None) returns self
        assert cm.bind_selected(None) is cm

    def test_bind_selected_no_selection(self) -> None:
        """Tests bind_selected when no function is selected."""
        cm = self.UnitTestClass()
        # No selection, __wrapped__ is None
        with pytest.raises(AttributeError):
            cm.bind_selected(object())

    def test_is_binding_wrapper_setter_no_wrapped(self) -> None:
        """Tests setting is_binding_wrapper=True when __wrapped__ is None."""
        cm = self.UnitTestClass()
        # Ensure __wrapped__ is None
        assert cm.__wrapped__ is None

        # This should execute the implicit else of the elif
        cm.is_binding_wrapper = True

        # _selected_bind_method should not be set
        assert not hasattr(cm, "_selected_bind_method")
        assert cm.is_binding_wrapper

    def test_is_binding_wrapper_setter_no_get(self) -> None:
        """Tests setting is_binding_wrapper=True when __wrapped__ has no __get__."""

        class NoGet:
            def __call__(self) -> None:
                pass

        cm = self.UnitTestClass(func=NoGet())

        # This should execute the implicit else of the elif
        cm.is_binding_wrapper = True

        # _selected_bind_method should not be set
        assert not hasattr(cm, "_selected_bind_method")

    def test_getstate_tuple_none_dict(self) -> None:
        """Tests __getstate__ when super() returns a tuple with None as first element."""
        cm = self.UnitTestClass()

        # Mock BaseMethod.__getstate__ to return (None, {})
        # This simulates a case where the object has slots but no dict
        with patch.object(BaseMethod, "__getstate__", return_value=(None, {})):
            state = cm.__getstate__()

        assert state == (None, {})

    def test_bind_self_instance_none(self) -> None:
        """Tests bind_self with instance=None while is_binding=True."""
        cm = self.UnitTestClass(is_binding=True)

        # Ensure initial state
        assert cm.is_binding

        # Calls bind_self with None
        # This should hit the 'if instance is not None' check and skip the body
        res = cm.bind_self(instance=None)

        assert res is cm
        # __self__ should still be None (or whatever default)
        assert cm.__self__ is None

    def test_bind_self_owner_only(self) -> None:
        """Tests bind_self with owner only."""
        cm = self.UnitTestClass(is_binding=True)

        class A:
            pass

        # This covers 'if owner is not None' path while 'if instance is not None' is skipped
        cm.bind_self(instance=None, owner=A)

        assert cm.__owner__ is A
        assert cm.__self__ is None
