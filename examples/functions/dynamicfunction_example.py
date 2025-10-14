#!/usr/bin/env python
"""dynamicfunction_example.py
An example of how to create and use DynamicFunction.

This example demonstrates:
1. Creating a DynamicFunction object
2. Understanding how DynamicFunction differs from DynamicCallable
3. Using DynamicFunction with different call methods
4. Creating custom DynamicFunction subclasses
5. Using DynamicFunction as a descriptor
6. Converting between functions and methods
"""


# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.functions import DynamicCallable, DynamicFunction, DynamicMethod


# Definitions #
# Classes #
class CustomDynamicFunction(DynamicFunction):
    """A custom implementation of DynamicFunction with additional calling methods.

    This class demonstrates how to extend DynamicFunction with custom calling methods.
    """

    def call_with_logging(self, *args, **kwargs):
        """A custom calling method that logs the call.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        print(f"Calling {self.__wrapped__.__name__} with args: {args}, kwargs: {kwargs}")
        result = self.__wrapped__(*args, **kwargs)
        print(f"Result: {result}")
        return result

    def call_with_validation(self, *args, **kwargs):
        """A custom calling method that validates the arguments.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.

        Raises:
            ValueError: If any argument is None.
        """
        # Simple validation: check if any argument is None
        for arg in args:
            if arg is None:
                raise ValueError("None values are not allowed")

        for key, value in kwargs.items():
            if value is None:
                raise ValueError(f"None value for {key} is not allowed")

        return self.__wrapped__(*args, **kwargs)


class NonWrappingDynamicFunction(DynamicFunction):
    """A custom non-wrapping implementation of DynamicFunction that defines functionality directly.

    This class demonstrates how to extend DynamicFunction without relying on a wrapped function. Instead, it implements
    its own functionality directly through custom methods registered with the call_multiplexer.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the NonWrappingDynamicFunction.

        This constructor initializes the object without requiring a wrapped function. It registers custom methods with
        the call_multiplexer and sets a default call method.

        Args:
            *args: Arguments for the parent class.
            **kwargs: Keyword arguments for the parent class.
        """
        # Initialize with no wrapped function
        super().__init__(None, *args, **kwargs)

        # Set the default call method
        self.call_method = "add"

    def add(self, a, b):
        """Add two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of a and b.
        """
        return a + b

    def subtract(self, a, b):
        """Subtract b from a.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The difference between a and b.
        """
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of a and b.
        """
        return a * b

    def divide(self, a, b):
        """Divide a by b.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b


class ExampleClass:
    """A class to demonstrate using DynamicFunction as a descriptor."""

    def __init__(self, name):
        self.name = name

    def greet(self, name):
        """A method that greets a person."""
        return f"Hello, {name}! I'm {self.name}!"

    # Create a DynamicFunction as a class attribute
    dynamic_greeter = DynamicFunction(greet)

    # Create a custom DynamicFunction as a class attribute
    custom_greeter = CustomDynamicFunction(greet)


# Functions #
def example_function(a, b):
    """A simple function that adds two numbers."""
    return a + b


# Example Sections #
def basic_dynamicfunction_usage():
    """Demonstrates basic usage of DynamicFunction."""
    print("Basic DynamicFunction Usage:\n")

    # Create a DynamicFunction with a simple function
    dynamic_func = DynamicFunction(example_function)

    # Call the function using the default call method
    result = dynamic_func(5, 3)
    print("Default call method (call_wrapped):")
    print(f"dynamic_func(5, 3) = {result}")

    # Check the current call method
    print(f"\nCurrent call method: {dynamic_func.call_method}")

    # Check the current bind method
    print(f"Current bind method: {dynamic_func.bind_method}")

    # Create a DynamicFunction with no function
    empty_dynamic = DynamicFunction()

    # Set the function after creation
    empty_dynamic.__func__ = example_function

    # Call the function
    result = empty_dynamic(10, 20)
    print("\nSetting function after creation:")
    print(f"empty_dynamic(10, 20) = {result}")

    print()


def dynamicfunction_vs_dynamiccallable():
    """Demonstrates the differences between DynamicFunction and DynamicCallable."""
    print("DynamicFunction vs DynamicCallable:\n")

    # Create a DynamicFunction and a DynamicCallable with the same function
    dynamic_func = DynamicFunction(example_function)
    dynamic_callable = DynamicCallable(example_function)

    # Show that both can be called directly
    func_result = dynamic_func(7, 3)
    callable_result = dynamic_callable(7, 3)
    print("Direct call:")
    print(f"dynamic_func(7, 3) = {func_result}")
    print(f"dynamic_callable(7, 3) = {callable_result}")

    # Show the class hierarchy
    print("\nClass hierarchy:")
    print(f"DynamicFunction inherits from: {DynamicFunction.__mro__[1:3]}")
    print(f"DynamicCallable inherits from: {DynamicCallable.__mro__[1:2]}")

    # Show the method_type attribute
    print("\nMethod type:")
    print(f"DynamicFunction.method_type = {DynamicFunction.method_type}")

    # Create an instance of ExampleClass
    example = ExampleClass("John")

    # Use both as descriptors
    func_result = example.dynamic_greeter("Alice")
    print("\nUsing as descriptors:")
    print(f"example.dynamic_greeter('Alice') = {func_result}")

    print()


def custom_dynamicfunction_usage():
    """Demonstrates usage of a custom DynamicFunction with additional methods."""
    print("Custom DynamicFunction Usage:\n")

    # Create a custom DynamicFunction
    custom_func = CustomDynamicFunction(example_function)

    # Use the default call method
    result = custom_func(7, 3)
    print("Default call method (call_wrapped):")
    print(f"custom_func(7, 3) = {result}")

    # Switch to the custom call method with logging
    custom_func.call_method = "call_with_logging"
    result = custom_func(7, 3)

    # Switch to the custom call method with validation
    custom_func.call_method = "call_with_validation"
    print("\nUsing call_with_validation method:")
    try:
        result = custom_func(None, 3)
    except ValueError as e:
        print(f"Validation error: {e}")

    # Valid call with the validation method
    result = custom_func(7, 3)
    print(f"Valid call: custom_func(7, 3) = {result}")

    print()


def dynamicfunction_as_descriptor():
    """Demonstrates using DynamicFunction as a descriptor."""
    print("DynamicFunction as Descriptor:\n")

    # Create an instance of ExampleClass
    example = ExampleClass("John")

    # Use the DynamicFunction descriptor
    result = example.dynamic_greeter("Alice")
    print("Using dynamic_greeter descriptor:")
    print(f"example.dynamic_greeter('Alice') = {result}")

    # Examine the type of the bound method
    bound_method = example.dynamic_greeter
    print(f"\nType of bound method: {type(bound_method).__name__}")

    # Show that the bound method is an instance of DynamicMethod
    print(f"Is bound method a DynamicMethod? {isinstance(bound_method, DynamicMethod)}")

    # Use the custom DynamicFunction descriptor
    custom_func = example.custom_greeter.__func__  # The Dynamic function is wrapped by a Method
    custom_func.call_method = "call_with_logging"
    result = example.custom_greeter("Bob")

    print()


def nonwrapping_dynamicfunction_usage():
    """Demonstrates usage of a non-wrapping DynamicFunction with direct functionality."""
    print("Non-Wrapping DynamicFunction Usage:\n")

    # Create a non-wrapping DynamicFunction
    calculator = NonWrappingDynamicFunction()

    # Use the default call method (add)
    result = calculator(5, 3)
    print("Default call method (add):")
    print(f"calculator(5, 3) = {result}")

    # Switch to the subtract method
    calculator.call_method = "subtract"
    result = calculator(10, 4)
    print("\nUsing subtract method:")
    print(f"calculator(10, 4) = {result}")

    # Switch to the multiply method
    calculator.call_method = "multiply"
    result = calculator(6, 7)
    print("\nUsing multiply method:")
    print(f"calculator(6, 7) = {result}")

    # Switch to the divide method
    calculator.call_method = "divide"
    result = calculator(20, 5)
    print("\nUsing divide method:")
    print(f"calculator(20, 5) = {result}")

    # Test error handling
    try:
        result = calculator(10, 0)
    except ZeroDivisionError as e:
        print("\nError handling:")
        print(f"calculator(10, 0) raised: {e}")

    print()


def function_method_conversion():
    """Demonstrates conversion between functions and methods using DynamicFunction."""
    print("Function-Method Conversion:\n")

    # Create a class with a method
    class MethodContainer:
        def instance_method(self, x, y):
            return x * y + self.value

        def __init__(self, value):
            self.value = value

    # Create an instance of the class
    container = MethodContainer(10)

    # Create a DynamicFunction from the instance method
    method_func = DynamicFunction(container.instance_method)

    # This won't work correctly because the method needs 'self'
    try:
        result = method_func(5, 3)
        print("Trying to call method as function:")
        print(f"method_func(5, 3) = {result}")
    except TypeError as e:
        print(f"Error when calling method as function: {e}")

    # Create a function that can handle 'self' parameter
    def adaptable_function(self_or_x, y=None, z=None):
        """A function that can work both as a function and as a method.

        When called as a function: adaptable_function(x, y)
        When called as a method: instance.adaptable_function(y, z)
        """
        if z is None:
            # Called as a function: adaptable_function(x, y)
            x = self_or_x
            return x + y
        else:
            # Called as a method: instance.adaptable_function(y, z)
            return y + z + self_or_x.value

    # Create a DynamicFunction from the adaptable function
    dynamic_func = DynamicFunction(adaptable_function)

    # Call as a function
    result = dynamic_func(5, 3)
    print("\nCalling as a function:")
    print(f"dynamic_func(5, 3) = {result}")

    # Create a DynamicMethod from the DynamicFunction
    dynamic_method = dynamic_func.__get__(container, MethodContainer)

    # Call as a method
    result = dynamic_method(7, 3)
    print("\nCalling as a method:")
    print(f"dynamic_method(7, 3) = {result}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of DynamicFunction
    basic_dynamicfunction_usage()

    # DynamicFunction vs DynamicCallable
    dynamicfunction_vs_dynamiccallable()

    # Custom DynamicFunction usage
    custom_dynamicfunction_usage()

    # Using DynamicFunction as a descriptor
    dynamicfunction_as_descriptor()

    # Non-wrapping DynamicFunction usage
    nonwrapping_dynamicfunction_usage()

    # Function-Method conversion
    function_method_conversion()
