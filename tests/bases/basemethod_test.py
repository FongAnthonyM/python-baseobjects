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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseMethod
from src.baseobjects.testsuite.bases import BaseMethodTestSuite, ExampleBindTarget, example_method


# Classes #
class TestBaseMethod(BaseMethodTestSuite):
    """Test the BaseMethod class.

    This class tests the functionality of the BaseMethod class, which extends BaseCallable to create
    method-like callable objects that maintain a reference to the instance they're bound to.
    """

    # Attributes #
    TestClass: Type[BaseMethod] = BaseMethod

    # Instance Methods #
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test method
        instance = self.TestClass(example_method)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct wrapped function
        assert instance.__func__ is example_method

        # Verify it has no bound instance by default
        assert instance.__self__ is None

        # Create an instance with a test method and a bound instance
        bind_target = self.create_bind_target()
        bound_instance = self.TestClass(example_method, instance=bind_target, owner=self.BindTargetClass)

        # Verify it has the correct bound instance
        assert bound_instance.__self__ is bind_target
        assert bound_instance.__owner__ is self.BindTargetClass

    def test_call(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be called and correctly delegates to the wrapped method.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Create a bind target
        bind_target = self.create_bind_target()

        # Bind the method to the target
        test_method_object.__self__ = bind_target

        # Call the method
        result = test_method_object(3)

        # Verify it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Call with different arguments
        result = test_method_object(3, 4)

        # Verify it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    def test_as_function(self, test_method_object: BaseMethod) -> None:
        """Test that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Create a bind target
        bind_target = self.create_bind_target()

        # Bind the method to the target
        test_method_object.__self__ = bind_target

        # Convert to a standard Python function
        func = test_method_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == (5, bind_target)  # (3 + 2, instance)
        assert func(3, 4) == (7, bind_target)  # (3 + 4, instance)

        # Verify it has the correct attributes
        assert func.__name__ == test_method_object.__name__
        assert func.__doc__ == test_method_object.__doc__
        assert func.__wrapped__ is test_method_object

    def test_call_wrapped(self, test_method_object: BaseMethod) -> None:
        """Test that the wrapped method can be called directly.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Create a bind target
        bind_target = self.create_bind_target()

        # Call the wrapped method directly
        result = test_method_object.call_wrapped(bind_target, 3)

        # Verify it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Call with different arguments
        result = test_method_object.call_wrapped(bind_target, 3, 4)

        # Verify it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    def test_call_binding(self, test_method_object: BaseMethod) -> None:
        """Test that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Create a bind target
        bind_target = self.create_bind_target()

        # Bind the method to the target
        test_method_object.__self__ = bind_target
        test_method_object.__owner__ = self.BindTargetClass

        # Call the method using call_binding
        result = test_method_object.call_binding(3)

        # Verify it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Call with different arguments
        result = test_method_object.call_binding(3, 4)

        # Verify it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    def test_bind_self(self, test_bind_target: ExampleBindTarget) -> None:
        """Test that the method can be bound to an instance.

        This test verifies that a bound method is returned and that it functions correctly.

        Args:
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Call the parent test method
        super().test_bind_self(test_bind_target)

        # Create a method
        method = self.create_method_object()

        # Bind the method to the target
        bound_method = method.bind_self(test_bind_target, self.BindTargetClass)

        # Verify it's the same method (not a new instance)
        assert bound_method is method

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is test_bind_target
        assert bound_method.__owner__ is self.BindTargetClass

        # Verify it returns the expected result when called
        result = bound_method(3)
        assert result == (5, test_bind_target)  # (3 + 2, instance)

        # Test with is_binding=False
        unbound_method = self.create_method_object(is_binding=False)
        unbound_result = unbound_method.bind_self(test_bind_target, self.BindTargetClass)

        # Verify it's the same method (not a new instance)
        assert unbound_result is unbound_method

        # Verify it's not bound to the instance
        assert unbound_result.__self__ is None

    def test_bind_to_attribute(self) -> None:
        """Test that the method can be bound to an instance and set as an attribute.

        This test verifies that a bound method is returned and bound to the target instance's attribute,
        and that it functions correctly.
        """
        # Call the parent test method
        super().test_bind_to_attribute()

        # Create a method and a bind target
        method = self.create_method_object()
        bind_target = self.create_bind_target()

        # Bind the method to the target and set it as an attribute
        bound_method = method.bind_to_attribute(bind_target, self.BindTargetClass)

        # Verify it's the same method (not a new instance)
        assert bound_method is method

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is bind_target
        assert bound_method.__owner__ is self.BindTargetClass

        # Verify it's set as an attribute on the instance
        assert hasattr(bind_target, method.__wrapped__.__name__)

        # Verify it returns the expected result when called through the attribute
        method_name = method.__wrapped__.__name__
        result = getattr(bind_target, method_name)(3)
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Test with a custom name
        new_method = self.create_method_object()
        new_bind_target = self.create_bind_target()
        bound_method_named = new_method.bind_to_attribute(
            new_bind_target,
            self.BindTargetClass,
            name="custom_method",
        )

        # Verify it's set as an attribute with the custom name
        assert hasattr(new_bind_target, "custom_method")

        # Verify it returns the expected result when called through the attribute
        result = new_bind_target.custom_method(3)
        assert result == (5, new_bind_target)  # (3 + 2, instance)

    def test_descriptor_protocol(self, test_method_object: BaseMethod) -> None:
        """Test that the method implements the descriptor protocol for method binding.

        This test verifies that the descriptor returns a bound method and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Call the parent test method
        super().test_descriptor_protocol(test_method_object)

        # Create a class with the method as a descriptor
        method = self.create_method_object()

        class DescriptorTest:
            descriptor_method = method

        # Create an instance of the class
        instance = DescriptorTest()

        # Verify the descriptor returns the same method (not a new instance)
        assert instance.descriptor_method is method

        # Verify it's bound to the correct instance
        assert instance.descriptor_method.__self__ is instance

        # Verify it returns the expected result when called
        result = instance.descriptor_method(3)
        assert result == (5, instance)  # (3 + 2, instance)

    def test_weak_reference(self) -> None:
        """Test that the method maintains a weak reference to the bound instance."""
        # Call the parent test method
        super().test_weak_reference()

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

    def test_pickling_with_instance(self) -> None:
        """Test pickling and unpickling of the method object with a bound instance."""
        # Create a method and a bind target
        method = self.create_method_object()
        bind_target = self.create_bind_target()

        # Bind the method to the target
        method.__self__ = bind_target
        method.__owner__ = self.BindTargetClass

        # Pickle and unpickle the method and bind target (need a strong reference to the bind target)
        items = (method, bind_target)
        pickled = pickle.dumps(items)
        unpickled_method, unpickled_bind_target = pickle.loads(pickled)

        # Verify the unpickled method is a new instance
        assert unpickled_method is not method

        # Verify it has the correct wrapped function
        assert unpickled_method.__func__ is method.__func__

        # Verify it's bound to the correct instance
        assert unpickled_method.__self__ is not bind_target
        assert unpickled_method.__self__ is unpickled_bind_target
        assert unpickled_method.__owner__ is self.BindTargetClass

        # Verify it returns the expected result when called
        result = unpickled_method(3)
        assert result == (5, unpickled_bind_target)  # (3 + 2, instance)

    def test_is_binding_flag(self) -> None:
        """Test the is_binding flag."""
        # Create a method with is_binding=False
        method = self.create_method_object(is_binding=False)

        # Verify the flag is set correctly
        assert method.is_binding is False

        # Create a class with the method as a descriptor
        class DescriptorTest:
            descriptor_method = method

        # Create an instance of the class
        instance = DescriptorTest()

        # Verify the descriptor returns the same method (not bound to the instance)
        assert instance.descriptor_method is method

        # Verify it's not bound to the instance
        assert instance.descriptor_method.__self__ is None

        # Create a method with is_binding=True
        binding_method = self.create_method_object(is_binding=True)

        # Create a class with the method as a descriptor
        class BindingDescriptorTest:
            descriptor_method = binding_method

        # Create an instance of the class
        binding_instance = BindingDescriptorTest()

        # Verify the descriptor returns the same method (bound to the instance)
        assert binding_instance.descriptor_method is binding_method

        # Verify it's bound to the instance
        assert binding_instance.descriptor_method.__self__ is binding_instance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
