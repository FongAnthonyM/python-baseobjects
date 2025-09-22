"""basemethodtestsuite.py
Base class for test suites which test BaseMethod and its subclasses.

This module provides a base test suite for testing the BaseMethod class and its subclasses. It defines abstract methods
for testing the core functionality of method objects, including binding to instances, weak references, binding to
attributes, and non-binding methods. It inherits from BaseMethodTestSuite to include tests for the callable behavior of
methods.
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
import gc
import pickle
from typing import Any, Type
import weakref

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseMethod
from .basecallabletestsuite import BaseCallableTestSuite


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
    # Fixtures
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
        """Test that the method object can be called and correctly delegates to the wrapped method.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """

    @abstractmethod
    def test_as_function(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """

    @abstractmethod
    def test_call_wrapped(self, test_method_object: BaseMethod) -> None:
        """Test that the wrapped method can be called directly.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """

    @abstractmethod
    def test_call_binding(self, test_method_object: BaseMethod) -> None:
        """Test that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """

    def test_bind_self(self, test_bind_target: "BindTargetClass") -> None:
        """Test that the function can be bound to an instance to create a method.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        method_object = self.create_method_object()
        bound_method = method_object.bind_self(test_bind_target, self.BindTargetClass)
        assert bound_method is method_object
        assert bound_method.__self__ is test_bind_target

        unbound_method_object = self.create_method_object(is_binding=False)
        unbound_method = unbound_method_object.bind_self(test_bind_target, self.BindTargetClass)
        assert unbound_method is unbound_method_object
        assert unbound_method.__self__ is None

    def test_bind_to_attribute(self) -> None:
        """Test that the method can be bound to an instance and set as an attribute.

        This test only varifies that a bound method is returned and bound to the target instance's attribute. This
        method may be overwritten to include validation that the method functions as intended.
        """
        method_object = self.create_method_object()
        new_bind_target = self.create_bind_target()
        bound_method = method_object.bind_to_attribute(new_bind_target, self.BindTargetClass)
        assert method_object is bound_method
        assert bound_method.__self__ is new_bind_target
        assert hasattr(new_bind_target, method_object.__wrapped__.__name__)

        new_method_object = self.create_method_object()
        bound_method_named = new_method_object.bind_to_attribute(
            new_bind_target,
            self.BindTargetClass,
            name="named_method",
        )
        assert bound_method_named is new_method_object
        assert bound_method_named.__self__ is new_bind_target
        assert hasattr(new_bind_target, "named_method")

        assert bound_method_named is not bound_method
        assert bound_method_named.__wrapped__ is bound_method.__wrapped__

    def test_descriptor_protocol(self, test_method_object: BaseMethod) -> None:
        """Test that the method implements the descriptor protocol for method binding.

        This test only varifies that the descriptor returns a bound method. This method may be overwritten to include
        validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        method_object = self.create_method_object()

        class BindTarget:
            new_method = method_object

        instance = BindTarget()
        assert instance.new_method is method_object
        assert instance.new_method.__self__ is instance

    def test_weak_reference(self) -> None:
        """Test that the method maintains a weak reference to the bound instance."""
        # Create a method
        method = self.create_method_object()

        # Create a new scope to control the lifetime of the instance
        def inner_scope():
            # Create a local instance
            local_instance = self.create_bind_target()

            # Bind the method to the local instance
            method.__self__ = local_instance

            # Verify it's bound to the correct instance
            assert method.__self__ is local_instance

            # Return a weak reference to the local instance
            return weakref.ref(local_instance)

        # Get a weak reference to the local instance
        weak_ref = inner_scope()

        # Force garbage collection
        gc.collect()

        # Verify the local instance has been garbage collected
        assert weak_ref() is None

        # Verify the method's bound instance is now None
        assert method.__self__ is None
