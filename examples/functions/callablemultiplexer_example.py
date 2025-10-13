#!/usr/bin/env python
"""callablemultiplexer_example.py
An example of how to create and use CallableMultiplexer, FunctionMultiplexer, and MethodMultiplexer.

This example demonstrates:
1. Creating and using CallableMultiplexer to select between different functions/methods
2. Using FunctionMultiplexer for function-based multiplexing
3. Using MethodMultiplexer for method-based multiplexing with automatic binding
4. Registering functions and methods in the multiplexer
5. Selecting which function/method to use at runtime
6. Understanding the differences between the three multiplexer types
"""


# Imports #
# Standard Libraries #

# Source Packages #
from baseobjects.functions import CallableMultiplexer, FunctionMultiplexer, FunctionRegistry, MethodMultiplexer


# Definitions #
# Classes #
class MathOperations:
    """A class with various mathematical operations.

    This class demonstrates how methods can be extracted and used in a multiplexer.
    """

    def add(self, a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of the two numbers.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract the second number from the first.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The difference between the two numbers.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of the two numbers.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide the first number by the second.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The quotient of the division.

        Raises:
            ValueError: If attempting to divide by zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class StringOperations:
    """A class with various string operations.

    This class demonstrates how methods can be extracted and used in a multiplexer.
    """

    def uppercase(self, text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: The text to convert.

        Returns:
            The text in uppercase.
        """
        return text.upper()

    def lowercase(self, text: str) -> str:
        """Convert text to lowercase.

        Args:
            text: The text to convert.

        Returns:
            The text in lowercase.
        """
        return text.lower()

    def capitalize(self, text: str) -> str:
        """Capitalize the first letter of each word in the text.

        Args:
            text: The text to capitalize.

        Returns:
            The capitalized text.
        """
        return text.title()

    def reverse(self, text: str) -> str:
        """Reverse the text.

        Args:
            text: The text to reverse.

        Returns:
            The reversed text.
        """
        return text[::-1]


# Functions #
# Example Sections #
def basic_callable_multiplexer():
    """Demonstrates basic usage of CallableMultiplexer."""
    print("Basic CallableMultiplexer Usage:\n")

    # Create a registry and add some functions
    registry = FunctionRegistry()
    registry["add"] = lambda a, b: a + b
    registry["subtract"] = lambda a, b: a - b
    registry["multiply"] = lambda a, b: a * b

    # Create a CallableMultiplexer with the registry
    multiplexer = CallableMultiplexer(registry=registry)

    # Select a function to use
    multiplexer.select("add")

    # Use the selected function
    a, b = 10, 5
    result = multiplexer(a, b)
    print(f"Selected function: 'add'")
    print(f"multiplexer({a}, {b}) = {result}")

    # Change the selected function
    multiplexer.select("multiply")
    result = multiplexer(a, b)
    print(f"\nSelected function: 'multiply'")
    print(f"multiplexer({a}, {b}) = {result}")

    # Add a new function and select it
    registry["power"] = lambda a, b: a**b
    multiplexer.select("power")
    result = multiplexer(a, b)
    print(f"\nAdded and selected function: 'power'")
    print(f"multiplexer({a}, {b}) = {result}")

    # Add and select a function in one step
    multiplexer.add_select_function("divide", lambda a, b: a / b if b != 0 else float("inf"))
    result = multiplexer(a, b)
    print(f"\nAdded and selected function: 'divide'")
    print(f"multiplexer({a}, {b}) = {result}")

    print()


def multiplexer_types_comparison():
    """Demonstrates the differences between the three multiplexer types."""
    print("Comparing Multiplexer Types:\n")

    # Create instances of operation classes
    math_ops = MathOperations()
    string_ops = StringOperations()

    # Create registries for our functions/methods
    registry1 = FunctionRegistry()
    registry2 = FunctionRegistry()
    registry3 = FunctionRegistry()

    # Add the same methods to all registries
    registry1["add"] = math_ops.add
    registry1["uppercase"] = string_ops.uppercase

    registry2["add"] = math_ops.add
    registry2["uppercase"] = string_ops.uppercase

    registry3["add"] = math_ops.add
    registry3["uppercase"] = string_ops.uppercase

    # Create the different multiplexer types
    callable_multiplexer = CallableMultiplexer(registry=registry1, instance=math_ops)
    function_multiplexer = FunctionMultiplexer(registry=registry2)
    method_multiplexer = MethodMultiplexer(registry=registry3, instance=math_ops)

    # Select the same function in all multiplexers
    callable_multiplexer.select("add")
    function_multiplexer.select("add")
    method_multiplexer.select("add")

    print("Using 'add' method with different multiplexers:")

    # CallableMultiplexer behavior depends on is_binding_wrapper
    print("\nCallableMultiplexer:")
    try:
        # This will fail because the method expects 'self' as the first argument
        # and is_binding_wrapper is False by default after select()
        result = callable_multiplexer(10, 5)
        print(f"Result: {result}")
    except TypeError as e:
        print(f"Error: {e}")

    # Set is_binding_wrapper to True to make it work like MethodMultiplexer
    callable_multiplexer.is_binding_wrapper = True
    result = callable_multiplexer(10, 5)
    print(f"After setting is_binding_wrapper=True, result: {result}")

    # FunctionMultiplexer doesn't bind methods
    print("\nFunctionMultiplexer:")
    try:
        # This will fail because the method expects 'self' as the first argument
        result = function_multiplexer(10, 5)
        print(f"Result: {result}")
    except TypeError as e:
        print(f"Error: {e}")

    # MethodMultiplexer automatically binds methods
    print("\nMethodMultiplexer:")
    result = method_multiplexer(10, 5)
    print(f"Result: {result}")

    # Now let's try with standalone functions
    print("\nUsing standalone functions with different multiplexers:")

    # Define a standalone function
    def standalone_add(a, b):
        return a + b

    # Add the function to all registries
    registry1["standalone_add"] = standalone_add
    registry2["standalone_add"] = standalone_add
    registry3["standalone_add"] = standalone_add

    # Select the function in all multiplexers
    callable_multiplexer.select("standalone_add")
    function_multiplexer.select("standalone_add")
    method_multiplexer.select("standalone_add")

    # CallableMultiplexer with is_binding_wrapper=False works with standalone functions
    callable_multiplexer.is_binding_wrapper = False
    print("\nCallableMultiplexer with standalone function:")
    result = callable_multiplexer(10, 5)
    print(f"Result: {result}")

    # FunctionMultiplexer works with standalone functions
    print("\nFunctionMultiplexer with standalone function:")
    result = function_multiplexer(10, 5)
    print(f"Result: {result}")

    # MethodMultiplexer tries to bind standalone functions
    print("\nMethodMultiplexer with standalone function:")
    try:
        result = method_multiplexer(10, 5)
        print(f"Result: {result}")
    except TypeError as e:
        print(f"Error: {e}")

    print()


def dynamic_method_selection():
    """Demonstrates dynamic method selection with CallableMultiplexer."""
    print("Dynamic Method Selection Example:\n")

    # Create a class with instance methods
    class DynamicProcessor:
        def __init__(self, name):
            self.name = name
            self.value = 0

            # Create a CallableMultiplexer for this instance
            self.multiplexer = CallableMultiplexer(instance=self)

            # No need to add methods to a registry, we'll use the instance's methods directly
            self.multiplexer.select("increment")

        def increment(self, amount=1):
            self.value += amount
            return self.value

        def decrement(self, amount=1):
            self.value -= amount
            return self.value

        def reset(self):
            old_value = self.value
            self.value = 0
            return old_value

        def process(self):
            # Call the currently selected method
            return self.multiplexer()

    # Create an instance
    processor = DynamicProcessor("Dynamic Processor")

    # Use the default selected method (increment)
    result = processor.process()
    print(f"Using default method 'increment':")
    print(f"processor.process() = {result}")
    print(f"Current value: {processor.value}")

    # Change the selected method to decrement
    processor.multiplexer.select("decrement")
    result = processor.process()
    print(f"\nChanged to method 'decrement':")
    print(f"processor.process() = {result}")
    print(f"Current value: {processor.value}")

    # Increment by a specific amount
    processor.multiplexer.select("increment")
    result = processor.multiplexer(5)  # Call with an argument
    print(f"\nCalling 'increment' with argument 5:")
    print(f"processor.multiplexer(5) = {result}")
    print(f"Current value: {processor.value}")

    # Reset the value
    processor.multiplexer.select("reset")
    result = processor.process()
    print(f"\nChanged to method 'reset':")
    print(f"processor.process() = {result}")
    print(f"Current value: {processor.value}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of CallableMultiplexer
    basic_callable_multiplexer()

    # Compare the different multiplexer types
    multiplexer_types_comparison()

    # Demonstrating dynamic method selection with CallableMultiplexer
    dynamic_method_selection()
