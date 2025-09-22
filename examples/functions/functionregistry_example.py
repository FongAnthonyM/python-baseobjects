#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""functionregistry_example.py
An example of how to create and use FunctionRegistry.

This example demonstrates:
1. Creating a FunctionRegistry with different initialization methods
2. Adding functions to the registry
3. Retrieving and using functions from the registry
4. Updating the registry from objects and dictionaries
5. Using the registry in practical applications
"""

# Imports #
# Standard Libraries #
from typing import Any, Callable, Dict, List, Optional, Tuple

# Third-Party Packages #
from baseobjects.functions import FunctionRegistry

# Local Packages #


# Definitions #
# Classes #
class MathOperations:
    """A class with various mathematical operations.

    This class demonstrates how methods can be extracted and stored in a FunctionRegistry.
    """

    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of the two numbers.
        """
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract the second number from the first.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The difference between the two numbers.
        """
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of the two numbers.
        """
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
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

    @staticmethod
    def power(a: float, b: float) -> float:
        """Raise the first number to the power of the second.

        Args:
            a: The base number.
            b: The exponent.

        Returns:
            The result of raising a to the power of b.
        """
        return a**b


class StringOperations:
    """A class with various string operations.

    This class demonstrates how methods can be extracted and stored in a FunctionRegistry.
    """

    @staticmethod
    def uppercase(text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: The text to convert.

        Returns:
            The text in uppercase.
        """
        return text.upper()

    @staticmethod
    def lowercase(text: str) -> str:
        """Convert text to lowercase.

        Args:
            text: The text to convert.

        Returns:
            The text in lowercase.
        """
        return text.lower()

    @staticmethod
    def capitalize(text: str) -> str:
        """Capitalize the first letter of each word in the text.

        Args:
            text: The text to capitalize.

        Returns:
            The capitalized text.
        """
        return text.title()

    @staticmethod
    def reverse(text: str) -> str:
        """Reverse the text.

        Args:
            text: The text to reverse.

        Returns:
            The reversed text.
        """
        return text[::-1]


class Calculator:
    """A calculator that uses a FunctionRegistry to perform operations.

    This class demonstrates a practical application of FunctionRegistry.
    """

    def __init__(self) -> None:
        """Initialize the calculator with a function registry."""
        self.registry = FunctionRegistry()

        # Add basic operations
        self.registry.update(
            {
                "add": MathOperations.add,
                "subtract": MathOperations.subtract,
                "multiply": MathOperations.multiply,
                "divide": MathOperations.divide,
            }
        )

    def register_operation(self, name: str, operation: Callable) -> None:
        """Register a new operation.

        Args:
            name: The name of the operation.
            operation: The function that implements the operation.
        """
        self.registry[name] = operation

    def perform_operation(self, operation_name: str, *args: Any, **kwargs: Any) -> Any:
        """Perform an operation by name.

        Args:
            operation_name: The name of the operation to perform.
            *args: Positional arguments for the operation.
            **kwargs: Keyword arguments for the operation.

        Returns:
            The result of the operation.

        Raises:
            KeyError: If the operation is not registered.
        """
        if operation_name not in self.registry:
            raise KeyError(f"Operation '{operation_name}' not found in registry")

        operation = self.registry[operation_name]
        return operation(*args, **kwargs)

    def list_operations(self) -> List[str]:
        """List all registered operations.

        Returns:
            A list of operation names.
        """
        return list(self.registry.keys())


# Standalone functions for the registry
def square(x: float) -> float:
    """Calculate the square of a number.

    Args:
        x: The number to square.

    Returns:
        The square of the number.
    """
    return x * x


def cube(x: float) -> float:
    """Calculate the cube of a number.

    Args:
        x: The number to cube.

    Returns:
        The cube of the number.
    """
    return x * x * x


def factorial(n: int) -> int:
    """Calculate the factorial of a number.

    Args:
        n: The number to calculate the factorial of.

    Returns:
        The factorial of the number.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


# Functions #
# Example Sections #
def basic_function_registry():
    """Demonstrates basic usage of FunctionRegistry."""
    print("Basic FunctionRegistry Usage:\n")

    # Create an empty registry
    registry = FunctionRegistry()
    print(f"Created empty registry: {registry}")

    # Add functions to the registry
    print("\nAdding functions to the registry...")
    registry["add"] = MathOperations.add
    registry["square"] = square
    registry["factorial"] = factorial

    # Check the contents of the registry
    print(f"Registry now contains: {list(registry.keys())}")

    # Use functions from the registry
    print("\nUsing functions from the registry:")

    a, b = 10, 5
    result = registry["add"](a, b)
    print(f"add({a}, {b}) = {result}")

    x = 4
    result = registry["square"](x)
    print(f"square({x}) = {result}")

    n = 5
    result = registry["factorial"](n)
    print(f"factorial({n}) = {result}")

    print()


def registry_initialization():
    """Demonstrates different ways to initialize a FunctionRegistry."""
    print("FunctionRegistry Initialization:\n")

    # Initialize with a dictionary of functions
    print("Initializing with a dictionary of functions:")
    functions = {"add": MathOperations.add, "subtract": MathOperations.subtract, "multiply": MathOperations.multiply}
    registry1 = FunctionRegistry(functions=functions)
    print(f"Registry1 contains: {list(registry1.keys())}")

    # Initialize with an object
    print("\nInitializing with an object:")
    math_ops = MathOperations()
    registry2 = FunctionRegistry(object_=math_ops)
    print(f"Registry2 contains: {list(registry2.keys())}")

    # Initialize with multiple objects
    print("\nInitializing with multiple objects:")
    math_ops = MathOperations()
    string_ops = StringOperations()
    registry3 = FunctionRegistry(objects=[math_ops, string_ops])
    print(f"Registry3 contains: {list(registry3.keys())}")

    print()


def updating_registry():
    """Demonstrates updating a FunctionRegistry from different sources."""
    print("Updating FunctionRegistry:\n")

    # Create an empty registry
    registry = FunctionRegistry()
    print(f"Created empty registry: {registry}")

    # Update from a dictionary
    print("\nUpdating from a dictionary:")
    functions = {"square": square, "cube": cube}
    registry.update(functions)
    print(f"Registry now contains: {list(registry.keys())}")

    # Update from an object
    print("\nUpdating from an object:")
    math_ops = MathOperations()
    registry.update_from_object(math_ops)
    print(f"Registry now contains: {list(registry.keys())}")

    # Update from multiple objects
    print("\nUpdating from multiple objects:")
    string_ops = StringOperations()
    registry.update_from_objects(string_ops)
    print(f"Registry now contains: {list(registry.keys())}")

    print()


def calculator_example():
    """Demonstrates using FunctionRegistry in a practical application."""
    print("Calculator Example:\n")

    # Create a calculator
    calculator = Calculator()
    print(f"Created calculator with operations: {calculator.list_operations()}")

    # Perform some operations
    print("\nPerforming operations:")

    a, b = 10, 5

    result = calculator.perform_operation("add", a, b)
    print(f"add({a}, {b}) = {result}")

    result = calculator.perform_operation("subtract", a, b)
    print(f"subtract({a}, {b}) = {result}")

    result = calculator.perform_operation("multiply", a, b)
    print(f"multiply({a}, {b}) = {result}")

    result = calculator.perform_operation("divide", a, b)
    print(f"divide({a}, {b}) = {result}")

    # Register additional operations
    print("\nRegistering additional operations:")
    calculator.register_operation("power", MathOperations.power)
    calculator.register_operation("square", square)
    calculator.register_operation("cube", cube)

    print(f"Calculator now has operations: {calculator.list_operations()}")

    # Perform the new operations
    print("\nPerforming new operations:")

    result = calculator.perform_operation("power", 2, 3)
    print(f"power(2, 3) = {result}")

    result = calculator.perform_operation("square", 4)
    print(f"square(4) = {result}")

    result = calculator.perform_operation("cube", 3)
    print(f"cube(3) = {result}")

    # Try to perform an unregistered operation
    print("\nTrying to perform an unregistered operation:")
    try:
        result = calculator.perform_operation("factorial", 5)
        print(f"factorial(5) = {result}")
    except KeyError as e:
        print(f"Error: {e}")

    print()


def function_composition():
    """Demonstrates using FunctionRegistry for function composition."""
    print("Function Composition Example:\n")

    # Create a registry with some functions
    registry = FunctionRegistry(
        {"square": square, "cube": cube, "add": MathOperations.add, "multiply": MathOperations.multiply}
    )

    # Define a function that composes functions from the registry
    def compose_functions(function_names: List[str], initial_value: float) -> float:
        """Compose functions from the registry.

        Args:
            function_names: The names of the functions to compose.
            initial_value: The initial value to pass to the first function.

        Returns:
            The result of applying the functions in sequence.

        Raises:
            KeyError: If any function name is not in the registry.
        """
        result = initial_value
        for name in function_names:
            if name not in registry:
                raise KeyError(f"Function '{name}' not found in registry")

            func = registry[name]
            if name in ["add", "multiply"]:
                # These functions take two arguments, so we'll use 2 as the second argument
                result = func(result, 2)
            else:
                # These functions take one argument
                result = func(result)

        return result

    # Compose some functions
    print("Composing functions from the registry:")

    # square(3) = 9
    result = compose_functions(["square"], 3)
    print(f"square(3) = {result}")

    # cube(square(2)) = cube(4) = 64
    result = compose_functions(["square", "cube"], 2)
    print(f"cube(square(2)) = {result}")

    # add(square(3), 2) = add(9, 2) = 11
    result = compose_functions(["square", "add"], 3)
    print(f"add(square(3), 2) = {result}")

    # multiply(add(square(2), 2), 2) = multiply(add(4, 2), 2) = multiply(6, 2) = 12
    result = compose_functions(["square", "add", "multiply"], 2)
    print(f"multiply(add(square(2), 2), 2) = {result}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of FunctionRegistry
    basic_function_registry()

    # Different ways to initialize a FunctionRegistry
    registry_initialization()

    # Updating a FunctionRegistry from different sources
    updating_registry()

    # Using FunctionRegistry in a calculator
    calculator_example()

    # Using FunctionRegistry for function composition
    function_composition()
