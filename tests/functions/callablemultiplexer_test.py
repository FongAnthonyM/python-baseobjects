#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" callablemultiplexer_test.py
Tests for the CallableMultiplexer class in the baseobjects package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import CallableMultiplexer
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestCallableMultiplexer(ClassTest):
    """Test the CallableMultiplexer class.

    This class tests the functionality of the CallableMultiplexer class, which is a callable that selects between
    different functions or methods to be used as the call method.
    """

    # Class Definitions #
    class ExampleClass:
        """An example class for testing CallableMultiplexer.

        This class has methods that can be multiplexed by CallableMultiplexer.
        """
        def __init__(self) -> None:
            """Initialize with two CallableMultiplexer instances."""
            self.multiplex_method = CallableMultiplexer(instance=self, select="add")
            self.multiplex_method_2 = CallableMultiplexer(instance=self, select="multiply")
            self.multiplex_method_binding = CallableMultiplexer(instance=self, select="add", binding=True)

        def add(self, a: int, b: int) -> int:
            """Add two numbers.

            Args:
                a: The first number.
                b: The second number.

            Returns:
                The sum of a and b.
            """
            return a + b

        def multiply(self, a: int, b: int) -> int:
            """Multiply two numbers.

            Args:
                a: The first number.
                b: The second number.

            Returns:
                The product of a and b.
            """
            return a * b

        def variable_args(self, *args: int) -> int:
            """Sum a variable number of arguments.

            Args:
                *args: The numbers to sum.

            Returns:
                The sum of all arguments.
            """
            return sum(args)

        async def async_add(self, a: int, b: int) -> int:
            """Asynchronously add two numbers.

            Args:
                a: The first number.
                b: The second number.

            Returns:
                The sum of a and b.
            """
            return a + b

    # Attributes #
    class_: Type[CallableMultiplexer] = CallableMultiplexer

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CallableMultiplexer can be created.

        This test verifies that CallableMultiplexer instances can be created with various parameters.
        """
        # Create with no parameters
        multiplexer1 = self.class_()
        assert multiplexer1 is not None
        assert multiplexer1.registry is not None
        assert multiplexer1.selected is None

        # Create with select parameter
        example = self.ExampleClass()
        multiplexer2 = self.class_(instance=example, select="add")
        assert multiplexer2 is not None
        assert multiplexer2.selected == "add"
        assert multiplexer2(1, 2) == 3

    def test_select(self) -> None:
        """Test the select method of CallableMultiplexer.

        This test verifies that the select method correctly changes the selected function/method.
        """
        example = self.ExampleClass()

        # Test selecting "add"
        example.multiplex_method.select("add")
        assert example.multiplex_method.selected == "add"
        assert example.multiplex_method(1, 2) == 3

        # Test selecting "multiply"
        example.multiplex_method.select("multiply")
        assert example.multiplex_method.selected == "multiply"
        assert example.multiplex_method(1, 2) == 2

    def test_pickling(self) -> None:
        """Test pickling and unpickling of objects with CallableMultiplexer attributes.

        This test verifies that objects with CallableMultiplexer attributes can be pickled and unpickled correctly,
        preserving the selected function/method.
        """
        # Setup
        test_object = self.ExampleClass()
        assert test_object.multiplex_method.selected == "add"

        # Change selection and verify
        test_object.multiplex_method.select("multiply")
        assert test_object.multiplex_method.selected == "multiply"

        # Test Pickle
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)

        # Assert
        assert new_obj is not None
        assert hasattr(new_obj, "multiplex_method")
        assert hasattr(new_obj, "multiplex_method_2")
        assert new_obj.multiplex_method.__self__ is not None
        assert new_obj.multiplex_method_2.__self__ is not None
        assert new_obj.multiplex_method.selected == "multiply"
        assert new_obj.multiplex_method(1, 2) == 2

    def test_add_function(self) -> None:
        """Test adding a function to the registry.

        This test verifies that functions can be added to the registry and then selected.
        """
        multiplexer = self.class_()

        # Define a function to add
        def subtract(a: int, b: int) -> int:
            return a - b

        # Add the function and select it
        multiplexer.add_function("subtract", subtract)
        multiplexer.select("subtract")

        # Verify it works
        assert multiplexer.selected == "subtract"
        assert multiplexer(5, 3) == 2

    def test_add_select_function(self) -> None:
        """Test adding and selecting a function in one step.

        This test verifies that functions can be added and selected in one step.
        """
        multiplexer = self.class_()

        # Define a function to add
        def divide(a: int, b: int) -> float:
            return a / b

        # Add and select the function
        multiplexer.add_select_function("divide", divide)

        # Verify it works
        assert multiplexer.selected == "divide"
        assert multiplexer(6, 3) == 2.0

    def test_selected_property(self) -> None:
        """Test the selected property.

        This test verifies that the selected property correctly gets and sets the selected function/method.
        """
        example = self.ExampleClass()
        multiplexer = self.class_(instance=example)

        # Set using the property
        multiplexer.selected = "add"
        assert multiplexer.selected == "add"
        assert multiplexer(1, 2) == 3

        # Set using the property again
        multiplexer.selected = "multiply"
        assert multiplexer.selected == "multiply"
        assert multiplexer(1, 2) == 2

    def test_nonexistent_function(self) -> None:
        """Test selecting a non-existent function.

        This test verifies that selecting a non-existent function raises an AttributeError when it's selected.
        """
        example = self.ExampleClass()

        # Select a non-existent function
        with pytest.raises(AttributeError):
            example.multiplex_method.select("nonexistent")

    def test_binding_flag(self) -> None:
        """Test the binding flag.

        This test verifies that when binding=True, the multiplexer correctly binds the selected function to the
        instance.
        """
        example = self.ExampleClass()

        # Test with binding=True
        assert example.multiplex_method_binding(1, 2) == 3

        # Create a new multiplexer with binding=True
        multiplexer = self.class_(instance=example, select="add", binding=True)
        assert multiplexer(1, 2) == 3

        # Change the selection and verify it still works
        multiplexer.select("multiply")
        assert multiplexer(1, 2) == 2

    def test_variable_args(self) -> None:
        """Test with a method that takes a variable number of arguments.

        This test verifies that the multiplexer correctly handles methods with different signatures, including variable
        arguments.
        """
        example = self.ExampleClass()
        multiplexer = self.class_(instance=example)

        # Select the variable_args method
        multiplexer.select("variable_args")
        assert multiplexer.selected == "variable_args"

        # Call with different numbers of arguments
        assert multiplexer(1, 2, 3) == 6
        assert multiplexer(1, 2, 3, 4, 5) == 15
        assert multiplexer() == 0

    def test_bind_selected(self) -> None:
        """Test the bind_selected method.

        This test verifies that the bind_selected method correctly binds the selected function to a different object.
        """
        example1 = self.ExampleClass()
        example2 = self.ExampleClass()

        # Bind to a different object
        bound_method = example1.multiplex_method.bind_selected(example2)
        assert bound_method.__self__ is example2
        assert bound_method(1, 2) == 3

        # Modify the second object's add method
        example2.add = lambda a, b: a * b
        assert example2.add(1, 2) == 2

        # The bound method should still use the original function
        assert bound_method(1, 2) == 3

    def test_method_multiplexer(self) -> None:
        """Test the MethodMultiplexer subclass.

        This test verifies that the MethodMultiplexer correctly handles method selection and calling.
        """
        from src.baseobjects.functions import MethodMultiplexer

        example = self.ExampleClass()
        multiplexer = MethodMultiplexer(instance=example, select="add")

        # Test calling the method
        assert multiplexer(1, 2) == 3

        # Change the selection and verify it works
        multiplexer.select("multiply")
        assert multiplexer(1, 2) == 2


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
