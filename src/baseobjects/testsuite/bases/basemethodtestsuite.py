"""basemethodtestsuite.py
Base class for test suites which test BaseMethod and its subclasses.

This module provides a base test suite for testing the BaseMethod class and its subclasses. It defines
abstract methods for testing the core functionality of method objects, including binding to instances,
weak references, binding to attributes, and non-binding methods. It inherits from BaseMethodTestSuite
to include tests for the callable behavior of methods.
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
from abc import abstractmethod
import copy
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseMethod
from .basecallabletestsuite import BaseCallableTestSuite, example_method, example_coroutine


# Definitions #
# Classes #
class BaseMethodTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test BaseMethod and its subclasses.

    This class provides common functionality for test suites that test method objects, including fixtures and
    test methods for verifying the behavior of BaseMethod objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseMethod or a subclass.
    """

    # Attributes #
    TestClass: Type[BaseMethod]
    BindTargetClass: Type[Any]

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

    # Fixtures
    @pytest.fixture
    def test_bind_target(self) -> Any:
        """Create a test instance to bind methods to.

        Returns:
            Any: An instance to bind methods to.
        """
        return self.create_bind_target()

    @pytest.fixture
    def test_object(self, test_method_object: BaseMethod, *args: Any, **kwargs: Any) -> BaseMethod:
        """Create a test object.

        Args:
            test_method_object: A fixture providing a BaseMethod instance.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseMethod: A test object instance.
        """
        return test_method_object

    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    def test_copy(self, test_object: BaseMethod) -> None:
        """Test the copy behavior of the method object.

        This test verifies that copy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__
        assert obj_copy.__self__ is test_object.__self__

    def test_copy_method(self, test_object: BaseMethod) -> None:
        """Test the copy method behavior of the method object.

        This test verifies that copy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__
        assert obj_copy.__self__ is test_object.__self__

    def test_deepcopy(self, test_object: BaseMethod, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the method object.

        This test verifies that deepcopy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
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
        assert obj_deepcopy.__self__ is test_object.__self__

    def test_deepcopy_method(self, test_object: BaseMethod, memo: dict | None = None) -> None:
        """Test the deep copy method behavior of the method object.

        This test verifies that deepcopy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
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
        assert obj_deepcopy.__self__ is test_object.__self__

    def test_pickling(self, test_object: BaseMethod) -> None:
        """Test pickling and unpickling of the method object.

        This test verifies that the object can be pickled and unpickled correctly, and that the unpickled object
        has the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
        """
        import pickle

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, type(test_object))
        assert unpickled.__func__ is test_object.__func__
        assert unpickled.__self__ is test_object.__self__

    @abstractmethod
    def test_call(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be called and correctly delegates to the wrapped function.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a function.
        """

    @abstractmethod
    def test_bind_builtin(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be bound to an instance using the builtin method.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a function.
        """

    @abstractmethod
    def test_bind_wrapped(self, test_method_object: BaseMethod) -> None:
        """Test that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_method_object: BaseMethod) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a function.
        """

    @abstractmethod
    def test_coroutine(self, test_coroutine_object: BaseMethod) -> None:
        """Test that the method object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a BaseMethod instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: BaseMethod) -> None:
        """Test that the method object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a BaseMethod instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_binding(self, test_instance: Any) -> None:
        """Test that the method can be bound to an instance.

        Args:
            test_instance: A fixture providing an instance to bind the method to.
        """

    @abstractmethod
    def test_call_binding(self, test_object: BaseMethod) -> None:
        """Test that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_object: A fixture providing a bound BaseMethod instance.
        """

    @abstractmethod
    def test_weak_reference(self, test_instance: Any) -> None:
        """Test that the method maintains a weak reference to the bound instance.

        Args:
            test_instance: A fixture providing an instance to bind the method to.
        """

    @abstractmethod
    def test_bind_to_attribute(self) -> None:
        """Test that the method can be bound to an instance and set as an attribute."""

    @abstractmethod
    def test_non_binding_method(self, test_instance: Any) -> None:
        """Test that a method with is_binding=False does not bind to instances.

        Args:
            test_instance: A fixture providing an instance to attempt binding with.
        """
