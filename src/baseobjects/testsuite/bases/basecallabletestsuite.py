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
from abc import abstractmethod
from types import MethodType
from typing import Any, Type
from collections.abc import Callable

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseCallable
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Helper Functions #
def example_function(x: int, y: int = 2) -> int:
    """A simple test function that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        The sum of x and y
    """
    return x + y


def example_method(self, x: int, y: int = 2) -> tuple[int, Any]:
    """A simple test method that adds two numbers and returns the instance.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        A tuple with the sum of x and y, and the instance
    """
    return x + y, self


async def example_coroutine(x: int, y: int = 2) -> int:
    """A simple test coroutine that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        The sum of x and y
    """
    await asyncio.sleep(0.001)  # Simulate some async work
    return x + y


async def example_coroutine_method(self, x: int, y: int = 2) -> tuple[int, Any]:
    """A simple test coroutine that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        A tuple with the sum of x and y, and the instance
    """
    await asyncio.sleep(0.001)  # Simulate some async work
    return x + y, self


class ExampleBindTarget:
    """A test class for testing method binding."""

    # Attributes #
    value: int

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, value: int = 42):
        """Initialize the instance.

        Args:
            value: The initial value to set.
        """
        self.value = value

    # Instance Methods #
    # Constructors/Destructors
    def method(self, x: int) -> int:
        """A test method that returns the sum of self.value and x."""
        return self.value + x


# Classes #
class BaseCallableTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test BaseCallable and its subclasses.

    This class provides common functionality for test suites that test callable objects, including fixtures and
    test methods for verifying the behavior of BaseCallable objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseCallable or a subclass.
    """

    # Attributes #
    TestClass: type[BaseCallable]
    BindTargetClass: type[Any] = ExampleBindTarget

    # Instance Methods #
    def create_bind_target(self, *args: Any, **kwargs) -> Any:
        """Create a test instance to bind methods to.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.BindTargetClass(*args, **kwargs)

    def create_function_object(self, func: Callable[..., Any] = example_function, *args: Any, **kwargs: Any) -> Any:
        """Create a BaseCallable instance that wraps a function.

        Args:
            func: The function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.TestClass(func, *args, **kwargs)

    def create_method_object(self, func: Callable[..., Any] = example_method, *args: Any, **kwargs: Any) -> Any:
        """Create a BaseCallable instance that wraps a method.

        Args:
            func: The method to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.TestClass(func, *args, **kwargs)

    def create_coroutine_object(self, func: Callable[..., Any] = example_coroutine, *args: Any, **kwargs: Any) -> Any:
        """Create a BaseCallable instance that wraps a coroutine function.

        Args:
            func: The coroutine function to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.TestClass(func, *args, **kwargs)

    def create_coroutine_method_object(
        self,
        func: Callable[..., Any] = example_coroutine_method,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Create a BaseCallable instance that wraps a coroutine method.

        Args:
            func: The coroutine method to wrap.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.TestClass(func, *args, **kwargs)

    # Fixtures
    @pytest.fixture
    def test_bind_target(self) -> Any:
        """Create a test instance to bind methods to.

        Returns:
            Any: An instance to bind methods to.
        """
        return self.create_bind_target()

    @pytest.fixture
    def test_function_object(self) -> BaseCallable:
        """Create a test callable object that wraps a function.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.create_function_object()

    @pytest.fixture
    def test_method_object(self) -> BaseCallable:
        """Create a test callable object that wraps a method.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.create_method_object()

    @pytest.fixture
    def test_coroutine_object(self) -> BaseCallable:
        """Create a test callable object that wraps a coroutine function.

        Returns:
            BaseCallable: An instance of the test class that wraps a coroutine function.
        """
        return self.create_coroutine_object()

    @pytest.fixture
    def test_coroutine_method_object(self) -> BaseCallable:
        """Create a test callable object that wraps a coroutine method.

        Returns:
            BaseCallable: An instance of the test class that wraps a coroutine function.
        """
        return self.create_coroutine_method_object()

    @pytest.fixture
    def test_object(self, test_function_object: BaseCallable, *args: Any, **kwargs: Any) -> BaseCallable:
        """Create a test object.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseCallable: An instance of the test class.
        """
        return test_function_object

    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    def test_copy(self, test_object: BaseCallable) -> None:
        """Test the copy behavior of the callable object.

        This test verifies that copy creates a new object with the same wrapped function. This method may be overwritten
        to include validation beyond checking that the function is correct.

        Args:
            test_object: A fixture providing a BaseCallable instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__

    def test_copy_method(self, test_object: BaseCallable) -> None:
        """Test the copy method behavior of the callable object.

        This test verifies that copy creates a new object with the same wrapped function. This method may be overwritten
        to include validation beyond checking that the function is correct.

        Args:
            test_object: A fixture providing a BaseCallable instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__

    def test_deepcopy(self, test_object: BaseCallable, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the callable object.

        This test verifies that deepcopy creates a new object with the same wrapped function. This method may be
        overwritten to include validation beyond checking that the function is correct.

        Args:
            test_object: A fixture providing a BaseCallable instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, type(test_object))
        assert obj_deepcopy.__func__ is test_object.__func__

    def test_deepcopy_method(self, test_object: BaseCallable, memo: dict | None = None) -> None:
        """Test the deep copy method behavior of the callable object.

        This test verifies that deepcopy creates a new object with the same wrapped function. This method may be
        overwritten to include validation beyond checking that the function is correct.

        Args:
            test_object: A fixture providing a BaseCallable instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, type(test_object))
        assert obj_deepcopy.__func__ is test_object.__func__

    def test_pickling(self, test_object: BaseCallable) -> None:
        """Test pickling and unpickling of the callable object.

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

    @abstractmethod
    def test_call(self, test_function_object: BaseCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: BaseCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: BaseCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    def test_binding(self, test_method_object: BaseCallable, test_bind_target: "BindTargetClass") -> None:
        """Test that the function can be bound to an instance to create a method.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.__get__(test_bind_target, self.BindTargetClass)
        assert bound_method.__self__ is test_bind_target

    def test_bind_builtin(self, test_method_object: BaseCallable, test_bind_target: "BindTargetClass") -> None:
        """Test that the callable object can be bound to an instance using the builtin method.

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

    def test_bind_wrapped(self, test_method_object: BaseCallable, test_bind_target: "BindTargetClass") -> None:
        """Test that the wrapped function can be bound to an instance.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind_wrapped(test_bind_target, self.BindTargetClass)
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

    def test_descriptor_protocol(self, test_method_object: BaseCallable) -> None:
        """Test that the callable implements the descriptor protocol for method binding.

        This test only varifies that the descriptor returns a bound method. This method may be overwritten to include
        validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
        """

        class BindTarget:
            new_method = test_method_object

        instance = BindTarget()
        assert isinstance(instance.new_method, MethodType)
        assert instance.new_method.__self__ is instance

    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object."""

        # Create a temporary function
        def temp_func(x: int, y: int = 2) -> int:
            return x + y

        # Create an attribute in the function
        temp_func.new_attribute = "test"

        # Create a callable object
        test_object = self.TestClass(temp_func)

        # Validate the new attribute is present and the same
        assert test_object.new_attribute == temp_func.new_attribute
