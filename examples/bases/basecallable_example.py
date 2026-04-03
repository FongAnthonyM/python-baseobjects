#!/usr/bin/env python
"""basecallable_example.py
An example of how to use BaseCallable, BaseMethod, and BaseFunction classes.

This example demonstrates:
1. Creating callable objects with BaseCallable
2. Creating method-like objects with BaseMethod
3. Creating function-like objects with BaseFunction
4. Binding callables to instances and attributes
5. Converting callables to regular functions
6. Working with coroutines
"""

# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.bases import BaseCallable, BaseFunction, BaseMethod


# Classes #
class Calculator:
    """A simple calculator class to demonstrate BaseCallable functionality."""

    def __init__(self, initial_value: int = 0) -> None:
        """Initializes the calculator with an initial value.

        Args:
            initial_value: The starting value for calculations
        """
        self.value = initial_value

    def add(self, x: int) -> int:
        """Adds a value to the calculator's current value.

        Args:
            x: The value to add

        Returns:
            The new calculator value
        """
        self.value += x
        return self.value

    def multiply(self, x: int) -> int:
        """Multiplies the calculator's current value by a factor.

        Args:
            x: The multiplication factor

        Returns:
            The new calculator value
        """
        self.value *= x
        return self.value


class CustomCallable(BaseCallable):
    """A custom callable that doubles its input."""

    def __init__(self) -> None:
        """Initializes with a function that doubles its input."""
        super().__init__(lambda x: x * 2)


class CustomMethod(BaseMethod):
    """A custom method that formats a greeting."""

    def __init__(self, instance: Any = None) -> None:
        """Initializes with a greeting formatter function.

        Args:
            instance: The instance to bind to
        """
        super().__init__(lambda self, name: f"Hello, {name}! Your value is {self.value}.", instance)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the underlying method.

        Returns:
            The result of the call.
        """
        return self.call_binding(*args, **kwargs)


class CustomFunction(BaseFunction):
    """A custom function that formats a message."""

    def __init__(self) -> None:
        """Initializes with a message formatter function."""
        super().__init__(lambda name, message: f"{name} says: {message}")


# Example Sections #
def basic_basecallable_example() -> None:
    """Demonstrates basic usage of BaseCallable."""
    print("\nBasic BaseCallable Example:")

    # Creates a BaseCallable with a lambda function
    double = BaseCallable(lambda x: x * 2)
    result = double(5)
    print(f"Double 5: {result} == 10")

    # Creates a BaseCallable with a regular function
    def square(x: int) -> int:
        return x * x

    square_callable = BaseCallable(square)
    result = square_callable(4)
    print(f"Square 4: {result} == 16")

    # Creates a custom callable
    custom = CustomCallable()
    result = custom(7)
    print(f"Custom double 7: {result} == 14")


def basemethod_example() -> None:
    """Demonstrates usage of BaseMethod."""
    print("\nBaseMethod Example:")

    # Creates a calculator instance
    calc = Calculator(10)

    # Creates a BaseMethod from the calculator's add method
    add_method = BaseMethod(calc.add, calc)
    result = add_method(5)
    print(f"Calculator add 5: {result} == 15")
    print(f"Calculator value: {calc.value} == 15")

    # Creates a BaseMethod from the calculator's multiply method
    multiply_method = BaseMethod(calc.multiply, calc)
    result = multiply_method(2)
    print(f"Calculator multiply by 2: {result} == 30")
    print(f"Calculator value: {calc.value} == 30")

    # Creates a custom method
    custom_method = CustomMethod(calc)
    greeting = custom_method("Alice")
    print(f"Custom greeting: {greeting} == 'Hello, Alice! Your value is 30.'")


def basefunction_example() -> None:
    """Demonstrates usage of BaseFunction."""
    print("\nBaseFunction Example:")

    # Creates a BaseFunction with a lambda
    format_message = BaseFunction(lambda name, message: f"{name} says: {message}")
    result = format_message("Bob", "Hello!")
    print(f"Formatted message: {result} == 'Bob says: Hello!'")

    # Creates a custom function
    custom_function = CustomFunction()
    result = custom_function("Charlie", "Good day!")
    print(f"Custom function: {result} == 'Charlie says: Good day!'")


def binding_example() -> None:
    """Demonstrates binding callables to instances and attributes."""
    print("\nBinding Example:")

    # Creates a calculator instance
    calc = Calculator(5)

    # Defines a standalone function
    def increment(self: Calculator, amount: int) -> int:
        self.value += amount
        return self.value

    # Creates a BaseFunction and bind it to the calculator
    increment_func = BaseFunction(increment)
    bound_increment = increment_func.bind(calc)
    result = bound_increment(3)
    print(f"Bound increment by 3: {result} == 8")
    print(f"Calculator value: {calc.value} == 8")

    # Binds a function to an attribute
    def reset(self: Calculator, value: int = 0) -> int:
        self.value = value
        return self.value

    reset_func = BaseFunction(reset)
    reset_func.bind_to_attribute(calc, name="reset")
    result = calc.reset(10)  # type: ignore
    print(f"Reset to 10: {result} == 10")
    print(f"Calculator value: {calc.value} == 10")


def conversion_example() -> None:
    """Demonstrates converting callables to regular functions."""
    print("\nConversion Example:")

    # Creates a BaseCallable
    double = BaseCallable(lambda x: x * 2)

    # Converts to a regular function
    double_func = double.as_function()
    result = double_func(6)
    print(f"Converted function double 6: {result} == 12")

    # Creates a BaseMethod
    calc = Calculator(10)
    add_method = BaseMethod(calc.add, calc)

    # Converts to a regular function
    add_func = add_method.as_function()
    result = add_func(5)
    print(f"Converted method add 5: {result} == 15")
    print(f"Calculator value: {calc.value} == 15")


# Main #
if __name__ == "__main__":
    # Runs examples
    basic_basecallable_example()
    basemethod_example()
    basefunction_example()
    binding_example()
    conversion_example()
