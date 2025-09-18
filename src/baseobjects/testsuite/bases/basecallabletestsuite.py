"""basecallabletestsuite.py
Base class for test suites which test BaseCallable and its subclasses.

This module provides a base test suite for testing the BaseCallable class and its subclasses. It defines
abstract methods for testing the core functionality of callable objects, including instance creation,
function calling, attribute copying, binding, and coroutine support.
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
from abc import abstractmethod
import copy
from typing import Any, Type, Callable

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
    TestClass: Type[BaseCallable]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function_object(self) -> BaseCallable:
        """Create a test callable object that wraps a function.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.TestClass(example_function)

    @pytest.fixture
    def test_method_object(self) -> BaseCallable:
        """Create a test callable object that wraps a function.

        Returns:
            BaseCallable: An instance of the test class that wraps a function.
        """
        return self.TestClass(example_method)

    @pytest.fixture
    def test_coroutine_object(self) -> BaseCallable:
        """Create a test callable object that wraps a coroutine function.

        Returns:
            BaseCallable: An instance of the test class that wraps a coroutine function.
        """
        return self.TestClass(example_coroutine)

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

        This test verifies that copy creates a new object with the same wrapped function.

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

        This test verifies that copy creates a new object with the same wrapped function.

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

        This test verifies that deepcopy creates a new object with the same wrapped function.

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

        This test verifies that deepcopy creates a new object with the same wrapped function.

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
        has the same wrapped function.

        Args:
            test_object: A fixture providing a BaseCallable instance.
        """
        import pickle

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
    def test_bind_builtin(self, test_method_object: BaseCallable) -> None:
        """Test that the callable object can be bound to an instance using the builtin method.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
        """

    @abstractmethod
    def test_bind_wrapped(self, test_method_object: BaseCallable) -> None:
        """Test that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: BaseCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseCallable instance that wraps a function.
        """

    @abstractmethod
    def test_coroutine(self, test_coroutine_object: BaseCallable) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a BaseCallable instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: BaseCallable) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a BaseCallable instance that wraps a coroutine function.
        """
