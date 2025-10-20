#!/usr/bin/env python
"""dynamiccallable_example.py
An example of how to create and use DynamicCallable.

This example demonstrates:
1. Creating a DynamicCallable object
2. Understanding the binding and calling multiplexers
3. Changing the binding and calling methods at runtime
4. Customizing the behavior of DynamicCallable
5. Using DynamicCallable as a descriptor
6. Creating a DynamicCallable subclass that defines functionality directly without wrapping
"""


# Imports #
# Standard Libraries #
from typing import Any
from collections.abc import Callable

# Source Packages #
from baseobjects.functions import DynamicCallable


# Definitions #
# Classes #
class WrappingDynamicCallable(DynamicCallable):
    """A custom wrapping implementation of DynamicCallable with additional binding and calling methods.

    This class demonstrates how to extend DynamicCallable with custom binding and calling methods.
    """

    def bind_with_prefix(self, instance: object, owner: type | None = None) -> Callable[..., Any]:
        """A custom binding method that adds a prefix to the callable.

        Args:
            instance: The instance to bind to.
            owner: The owner class.

        Returns:
            A callable that adds a prefix to the result.
        """

        # Create a new callable that adds a prefix
        def prefixed_callable(*args: Any, **kwargs: Any) -> Any:
            result = self.__wrapped__(instance, *args, **kwargs)
            if isinstance(result, str):
                return f"[Prefixed] {result}"
            return result

        return prefixed_callable

    def call_with_logging(self, *args: Any, **kwargs: Any) -> Any:
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

    def call_with_validation(self, *args: Any, **kwargs: Any) -> Any:
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
                msg = "None values are not allowed"
                raise ValueError(msg)

        for key, value in kwargs.items():
            if value is None:
                msg = f"None value for {key} is not allowed"
                raise ValueError(msg)

        return self.__wrapped__(*args, **kwargs)


class NonWrappingDynamicCallable(DynamicCallable):
    """A custom non-wrapping implementation of DynamicCallable that defines functionality directly.

    This class demonstrates how to extend DynamicCallable without relying on a wrapped function. Instead, it implements
    its own functionality directly through custom methods registered with the call_multiplexer.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the NonWrappingDynamicCallable.

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

    def add(self, a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of a and b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The difference between a and b.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of a and b.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
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
            msg = "Cannot divide by zero"
            raise ZeroDivisionError(msg)
        return a / b


class ExampleClass:
    """A class to demonstrate using DynamicCallable as a descriptor."""

    def __init__(self, name) -> None:
        self.name = name

    def greet(self, name) -> str:
        """A static method that greets a person."""
        return f"Hello, {name}! I'm {self.name}!"

    # Create a DynamicCallable as a class attribute
    dynamic_greeter = DynamicCallable(greet)

    # Create a custom wrapping DynamicCallable as a class attribute
    custom_greeter = WrappingDynamicCallable(greet)


# Functions #
def example_function(a, b):
    """A simple function that adds two numbers."""
    return a + b


# Example Sections #
def basic_dynamiccallable_usage() -> None:
    """Demonstrates basic usage of DynamicCallable."""
    print("Basic DynamicCallable Usage:\n")

    # Create a DynamicCallable with a simple function
    dynamic_callable = DynamicCallable(example_function)

    # Call the function using the default call method
    result = dynamic_callable(5, 3)
    print("Default call method (call_wrapped):")
    print(f"dynamic_callable(5, 3) = {result}")

    # Check the current call method
    print(f"\nCurrent call method: {dynamic_callable.call_method}")

    # Check the current bind method
    print(f"Current bind method: {dynamic_callable.bind_method}")

    # Create a DynamicCallable with no function
    empty_dynamic = DynamicCallable()

    # Set the function after creation
    empty_dynamic.__func__ = example_function

    # Call the function
    result = empty_dynamic(10, 20)
    print("\nSetting function after creation:")
    print(f"empty_dynamic(10, 20) = {result}")

    print()


def wrapping_dynamiccallable_usage() -> None:
    """Demonstrates usage of a wrapping DynamicCallable with additional methods."""
    print("Wrapping DynamicCallable Usage:\n")

    # Create a wrapping DynamicCallable
    wrapping_dynamic = WrappingDynamicCallable(example_function)

    # Use the default call method
    result = wrapping_dynamic(7, 3)
    print("Default call method (call_wrapped):")
    print(f"wrapping_dynamic(7, 3) = {result}")

    # Switch to the wrapping call method with logging
    wrapping_dynamic.call_method = "call_with_logging"
    result = wrapping_dynamic(7, 3)

    # Switch to the wrapping call method with validation
    wrapping_dynamic.call_method = "call_with_validation"
    print("\nUsing call_with_validation method:")
    try:
        result = wrapping_dynamic(None, 3)
    except ValueError as e:
        print(f"Validation error: {e}")

    # Valid call with the validation method
    result = wrapping_dynamic(7, 3)
    print(f"Valid call: wrapping_dynamic(7, 3) = {result}")

    print()


def dynamiccallable_as_descriptor() -> None:
    """Demonstrates using DynamicCallable as a descriptor."""
    print("DynamicCallable as Descriptor:\n")

    # Create an instance of ExampleClass
    example = ExampleClass("John")

    # Use the DynamicCallable descriptor
    result = example.dynamic_greeter("Alice")
    print("Using dynamic_greeter descriptor:")
    print(f"example.dynamic_greeter('Alice') = {result}")

    # Use the wrapping DynamicCallable descriptor
    dynamic_callable = example.custom_greeter.__func__  # The Dynamic callable is wrapped by a Method
    dynamic_callable.call_method = "call_with_logging"
    result = example.custom_greeter("Bob")

    # Change the bind method of the wrapping greeter
    dynamic_callable.bind_method = "bind_with_prefix"
    result = example.custom_greeter("Charlie")
    print("\nUsing wrapping bind method:")
    print(f"example.wrapping_greeter('Charlie') = {result}")

    print()


def multiplexer_exploration() -> None:
    """Explores the multiplexers in DynamicCallable."""
    print("Multiplexer Exploration:\n")

    # Create a DynamicCallable
    dynamic_callable = DynamicCallable(example_function)

    # Examine the bind multiplexer
    print("Bind Multiplexer:")
    print(f"Type: {type(dynamic_callable.bind_multiplexer).__name__}")
    print(f"Selected method: {dynamic_callable.bind_multiplexer.selected}")
    print(f"Available methods: {list(dynamic_callable.bind_multiplexer.registry.keys())}")

    # Examine the call multiplexer
    print("\nCall Multiplexer:")
    print(f"Type: {type(dynamic_callable.call_multiplexer).__name__}")
    print(f"Selected method: {dynamic_callable.call_multiplexer.selected}")
    print(f"Available methods: {list(dynamic_callable.call_multiplexer.registry.keys())}")

    # Add a custom method to the call multiplexer
    def call_with_double(self, *args, **kwargs):
        """Double the result of the wrapped function."""
        result = dynamic_callable.__wrapped__(*args, **kwargs)
        return result * 2

    dynamic_callable.call_multiplexer.add_function("call_with_double", call_with_double)

    # Use the new method
    dynamic_callable.call_method = "call_with_double"
    result = dynamic_callable(5, 3)
    print("\nUsing custom call method 'call_with_double':")
    print(f"dynamic_callable(5, 3) = {result}")

    # Reset to default call method
    dynamic_callable.call_method = "call_wrapped"
    result = dynamic_callable(5, 3)
    print("\nReset to default call method:")
    print(f"dynamic_callable(5, 3) = {result}")

    print()


def nonwrapping_dynamiccallable_usage() -> None:
    """Demonstrates usage of a non-wrapping DynamicCallable with direct functionality."""
    print("Non-Wrapping DynamicCallable Usage:\n")

    # Create a non-wrapping DynamicCallable
    calculator = NonWrappingDynamicCallable()

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


def pickling_dynamiccallable() -> None:
    """Demonstrates pickling and unpickling a DynamicCallable."""
    print("Pickling DynamicCallable:\n")

    # Standard Libraries #
    import pickle

    # Create a DynamicCallable
    dynamic_callable = DynamicCallable(example_function)

    # Test before pickling
    result = dynamic_callable(2, 3)
    print("Before pickling:")
    print(f"dynamic_callable(2, 3) = {result}")

    # Pickle the DynamicCallable
    pickled = pickle.dumps(dynamic_callable)

    # Unpickle the DynamicCallable
    unpickled = pickle.loads(pickled)

    # Test after unpickling
    try:
        result = unpickled(2, 3)
        print("\nAfter unpickling:")
        print(f"unpickled(2, 3) = {result}")
    except Exception as e:
        print(f"\nError after unpickling: {e}")
        print("Note: Custom functions added to multiplexers cannot be pickled.")

        # Reset to default call method
        unpickled.call_method = "call_wrapped"
        result = unpickled(2, 3)
        print("\nAfter resetting to default call method:")
        print(f"unpickled(2, 3) = {result}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of DynamicCallable
    basic_dynamiccallable_usage()

    # Wrapping DynamicCallable usage
    wrapping_dynamiccallable_usage()

    # Using DynamicCallable as a descriptor
    dynamiccallable_as_descriptor()

    # Exploring the multiplexers
    multiplexer_exploration()

    # Non-wrapping DynamicCallable usage
    nonwrapping_dynamiccallable_usage()

    # Pickling DynamicCallable
    pickling_dynamiccallable()
