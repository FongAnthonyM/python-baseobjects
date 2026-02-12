"""basecallabletestsuite.py
Base class for test suites which test BaseCallable and its subclasses.

This module provides a base test suite for testing the BaseCallable class and its subclasses. It defines abstract
methods for testing the core functionality of callable objects, including instance creation, function calling, binding,
and coroutine support.
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
import asyncio
import copy
import pickle
from collections.abc import Callable
from types import MethodType
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseCallable
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Helper Functions #
def concrete_function(x: int, y: int = 2) -> int:
    """A simple test function that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        The sum of x and y
    """
    return x + y


def concrete_method(self: Any, x: int, y: int = 2) -> tuple[int, Any]:
    """A simple test method that adds two numbers and returns the instance.

    Args:
        self: The instance the method is bound to.
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        A tuple with the sum of x and y, and the instance
    """
    return x + y, self


async def concrete_coroutine(x: int, y: int = 2) -> int:
    """A simple test coroutine that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        The sum of x and y
    """
    await asyncio.sleep(0.001)  # Simulate some async work
    return x + y


async def concrete_coroutine_method(self: Any, x: int, y: int = 2) -> tuple[int, Any]:
    """A simple test coroutine that adds two numbers.

    Args:
        self: The instance the coroutine method is bound to.
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        A tuple with the sum of x and y, and the instance
    """
    await asyncio.sleep(0.001)  # Simulate some async work
    return x + y, self


class ConcreteBindTarget:
    """A test class for testing method binding."""

    # Attributes #
    value: int

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, value: int = 42) -> None:
        """Initializes the instance.

        Args:
            value: The initial value to set.
        """
        self.value = value

    # Instance Methods #
    # Constructors/Destructors
    def method(self, x: int) -> int:
        """A test method that returns the sum of self.value and x.

        Returns:
            The sum of self.value and x.
        """
        return self.value + x


# Classes #
class BaseCallableTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test BaseCallable and its subclasses.

    This class provides common functionality for test suites that test callable objects, including fixtures and test
    methods for verifying the behavior of BaseCallable objects. Subclasses should implement the abstract methods and set
    the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseCallable or a subclass.
    """

    # Attributes #
    UnitTestClass: type[BaseCallable]
    BindTargetClass: type[Any] = ConcreteBindTarget

    # Helper Methods #
    def create_bind_target(self, *args: Any, **kwargs: Any) -> Any:
        """Creates a test instance to bind methods to.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.BindTargetClass(*args, **kwargs)

    def create_function_object(
        self,
        func: Callable[..., Any] = concrete_function,
        *args: Any,
        **kwargs: Any,
    ) -> BaseCallable:
        """Creates a BaseCallable instance that wraps a function.

        Args:
            func: The function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.UnitTestClass(func, *args, **kwargs)

    def create_method_object(
        self,
        func: Callable[..., Any] = concrete_method,
        *args: Any,
        **kwargs: Any,
    ) -> BaseCallable:
        """Creates a BaseCallable instance that wraps a method.

        Args:
            func: The method to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.UnitTestClass(func, *args, **kwargs)

    def create_coroutine_object(
        self,
        func: Callable[..., Any] = concrete_coroutine,
        *args: Any,
        **kwargs: Any,
    ) -> BaseCallable:
        """Creates a BaseCallable instance that wraps a coroutine function.

        Args:
            func: The coroutine function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.UnitTestClass(func, *args, **kwargs)

    def create_coroutine_method_object(
        self,
        func: Callable[..., Any] = concrete_coroutine_method,
        *args: Any,
        **kwargs: Any,
    ) -> BaseCallable:
        """Creates a BaseCallable instance that wraps a coroutine method.

        Args:
            func: The coroutine method to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.UnitTestClass(func, *args, **kwargs)

    # Fixtures #
    @pytest.fixture
    def test_bind_target(self) -> Any:
        """Creates a test instance to bind methods to.

        Returns:
            Any: An instance to bind methods to.
        """
        return self.create_bind_target()

    @pytest.fixture
    def test_function_object(self) -> BaseCallable:
        """Creates a test callable object that wraps a function.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.create_function_object()

    @pytest.fixture
    def test_method_object(self) -> BaseCallable:
        """Creates a test callable object that wraps a method.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.create_method_object()

    @pytest.fixture
    def test_coroutine_object(self) -> BaseCallable:
        """Creates a test callable object that wraps a coroutine function.

        Returns:
            BaseCallable: An instance of the test class that wraps a coroutine function.
        """
        return self.create_coroutine_object()

    @pytest.fixture
    def test_coroutine_method_object(self) -> BaseCallable:
        """Creates a test callable object that wraps a coroutine method.

        Returns:
            BaseCallable: An instance of the test class that wraps a coroutine function.
        """
        return self.create_coroutine_method_object()

    @pytest.fixture
    def test_object(self, test_function_object: BaseCallable, *args: Any, **kwargs: Any) -> BaseCallable:
        """Creates a test object.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseCallable: An instance of the test class.
        """
        return test_function_object

    # Tests #
    # Magic Methods #
    def test_call(self, test_function_object: BaseCallable) -> None:
        """Tests that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: BaseCallable) -> None:
        """Tests that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test function
        instance = self.UnitTestClass(concrete_function, *args, **kwargs)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has the correct wrapped function
        assert instance.__func__ is concrete_function

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: BaseCallable, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of the callable object.

        This test verifies that copy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseCallable instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: BaseCallable,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deep copy behavior of the callable object.

        This test verifies that deepcopy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseCallable instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, type(test_object))
        assert obj_deepcopy.__func__ is test_object.__func__

    # Pickling #
    def test_init_false_pickling(self) -> None:
        """Tests pickling of an object initialized with init=False."""
        obj = self.UnitTestClass(init=False)
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.__wrapped__ is None

    def test_pickling(self, test_object: BaseCallable) -> None:
        """Tests pickling and unpickling of the callable object.

        This test verifies that the object can be pickled and unpickled correctly, and that the unpickled object
        has the same wrapped function. This method may be overwritten to include validation beyond checking that the
        function is correct.

        Args:
            test_object: A fixture providing a BaseCallable instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, type(test_object))
        assert unpickled.__func__ is test_object.__func__

    # Functionality #
    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method."""

        class MyClass:
            def method(self) -> str:
                return "bound"

        inst = MyClass()
        bound = inst.method
        obj = self.UnitTestClass(bound)
        assert obj() == "bound"

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False)
        obj.construct()
        assert obj.__func__ is None

    def test_as_function(self, test_function_object: BaseCallable) -> None:
        """Tests that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

        # Verify it has the correct attributes
        assert func.__name__ == test_function_object.__name__  # type: ignore[attr-defined]
        assert func.__doc__ == test_function_object.__doc__
        assert func.__wrapped__ is test_function_object  # type: ignore[attr-defined]

    def test_binding(self, test_method_object: BaseCallable, test_bind_target: Any) -> None:
        """Tests that the function can be bound to an instance to create a method.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.__get__(test_bind_target, self.BindTargetClass)
        assert bound_method.__self__ is test_bind_target

    def test_bind_builtin(self, test_method_object: BaseCallable, test_bind_target: Any) -> None:
        """Tests that the callable object can be bound to an instance using the builtin method.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind_builtin(test_bind_target, self.BindTargetClass)
        assert isinstance(bound_method, MethodType)
        assert bound_method.__func__ is test_method_object
        assert bound_method.__self__ is test_bind_target

    def test_bind_wrapped(self, test_method_object: BaseCallable, test_bind_target: Any) -> None:
        """Tests that the wrapped function can be bound to an instance.

        This test verifies that a bound method is returned and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind_wrapped(test_bind_target, self.BindTargetClass)
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

        # Verify it works
        result = bound_method(3)
        assert result == (5, test_bind_target)

    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property."""
        # Test with standard function
        obj = self.create_function_object()
        assert not obj.is_coroutine

        # Test with coroutine function
        coro_obj = self.create_coroutine_object()
        assert coro_obj.is_coroutine

        # Test marker is None check
        obj_none = self.UnitTestClass()
        assert obj_none._is_coroutine_marker is None
        assert obj_none.is_coroutine is False

    def test_as_function_coroutine(self) -> None:
        """Tests as_function with a coroutine."""
        coro_obj = self.create_coroutine_object()
        wrapped = coro_obj.as_function()

        # Standard Libraries #
        import inspect

        assert inspect.iscoroutinefunction(wrapped)
        loop = asyncio.new_event_loop()
        res = loop.run_until_complete(wrapped(1))
        assert res == 3  # 1 + 2 (default y)
        loop.close()

    def test_bind_builtin_instance_none(self, test_function_object: BaseCallable) -> None:
        """Tests bind_builtin with None instance."""
        ret = test_function_object.bind_builtin(None)
        assert ret is test_function_object

    def test_func_setter_none(self, test_function_object: BaseCallable) -> None:
        """Tests setting __func__ to None.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        assert test_function_object.__wrapped__ is not None
        test_function_object.__func__ = None

        # Setter sets __wrapped__ to None.
        assert test_function_object.__wrapped__ is None
        assert test_function_object._is_coroutine_marker is None  # type: ignore[unreachable]

    def test_func_deleter(self, test_function_object: BaseCallable) -> None:
        """Tests deleting __func__.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """
        del test_function_object.__func__

        # After deletion, accessing __wrapped__ returns the class attribute default (None)
        assert test_function_object.__wrapped__ is None
        assert test_function_object._is_coroutine_marker is None
