#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dynamicdecorator_example.py
An example of how to create and use DynamicDecorator.

This example demonstrates:
1. Creating a DynamicDecorator object
2. Understanding how DynamicDecorator combines BaseDecorator and DynamicFunction
3. Runtime switching between different binding and callback functions
4. Creating custom DynamicDecorator subclasses
5. Overriding __get__ or __call__ methods for static binding or callback
6. Comparing DynamicDecorator with BaseDecorator
"""


# Imports #
# Standard Libraries #
import time
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

# Third-Party Packages #
from baseobjects.functions import DynamicDecorator, BaseDecorator, DynamicFunction
from baseobjects.bases import BaseCallable, BaseMethod
from baseobjects.typing import AnyCallable, GetObjectMethod

# Local Packages #


# Definitions #
# Classes #
class MultiModeDecorator(DynamicDecorator):
    """A decorator that can switch between different modes of operation at runtime.

    This class demonstrates how DynamicDecorator allows for runtime switching between different
    binding and callback functions.
    """

    def __init__(self, func: AnyCallable, mode: str = "normal"):
        """Initialize the multi-mode decorator.

        Args:
            func: The function to decorate.
            mode: The initial mode of operation ("normal", "debug", or "timing").
        """
        super().__init__(func)
        self.set_mode(mode)

    def normal_callback(self, *args: Any, **kwargs: Any) -> Any:
        """Normal mode: simply calls the wrapped function.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        print(f"[Normal Mode] Calling {self.__wrapped__.__name__}")
        return self.__wrapped__(*args, **kwargs)

    def debug_callback(self, *args: Any, **kwargs: Any) -> Any:
        """Debug mode: prints arguments and return value.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        print(f"[Debug Mode] Calling {self.__wrapped__.__name__} with args: {args}, kwargs: {kwargs}")
        result = self.__wrapped__(*args, **kwargs)
        print(f"[Debug Mode] {self.__wrapped__.__name__} returned: {result}")
        return result

    def timing_callback(self, *args: Any, **kwargs: Any) -> Any:
        """Timing mode: measures execution time.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        print(f"[Timing Mode] Calling {self.__wrapped__.__name__}")
        start_time = time.time()
        result = self.__wrapped__(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[Timing Mode] {self.__wrapped__.__name__} executed in {execution_time:.6f} seconds")
        return result

    def set_mode(self, mode: str) -> None:
        """Set the mode of operation.

        Args:
            mode: The mode to set ("normal", "debug", or "timing").

        Raises:
            ValueError: If the mode is not recognized.
        """
        if mode == "normal":
            self.call_method = "normal_callback"
        elif mode == "debug":
            self.call_method = "debug_callback"
        elif mode == "timing":
            self.call_method = "timing_callback"
        else:
            raise ValueError(f"Unknown mode: {mode}")


class StaticBindingDecorator(DynamicDecorator):
    """A decorator with static binding but dynamic callback.

    This class demonstrates how to override the __get__ method to use a static binding method
    while still allowing dynamic callback switching.
    """

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: GetObjectMethod = BaseCallable.bind_builtin  # Assigns __get__ to a previously defined method.

    def __init__(self, func: AnyCallable, callback_mode: str = "normal"):
        """Initialize the static binding decorator.

        Args:
            func: The function to decorate.
            callback_mode: The initial callback mode ("normal" or "verbose").
        """
        super().__init__(func)
        self.set_callback_mode(callback_mode)

    def normal_callback(self, *args: Any, **kwargs: Any) -> Any:
        """Normal callback: simply calls the wrapped function.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__wrapped__(*args, **kwargs)

    def verbose_callback(self, *args: Any, **kwargs: Any) -> Any:
        """Verbose callback: prints before and after calling the function.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        print(f"Calling {self.__wrapped__.__name__}...")
        result = self.__wrapped__(*args, **kwargs)
        print(f"Finished calling {self.__wrapped__.__name__}")
        return result

    def set_callback_mode(self, mode: str) -> None:
        """Set the callback mode.

        Args:
            mode: The mode to set ("normal" or "verbose").

        Raises:
            ValueError: If the mode is not recognized.
        """
        if mode == "normal":
            self.call_method = "normal_callback"
        elif mode == "verbose":
            self.call_method = "verbose_callback"
        else:
            raise ValueError(f"Unknown callback mode: {mode}")


class StaticCallbackDecorator(DynamicDecorator):
    """A decorator with static callback.

    This class demonstrates how to override the __call__ method to use a static callback method.
    """

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __call__: AnyCallable = BaseCallable.call_wrapped  # Assigns __call__ to a previously defined method.

    def __init__(self, func: AnyCallable):
        """Initialize the static callback decorator.

        Args:
            func: The function to decorate.
        """
        super().__init__(func)


class FullyStaticDecorator(DynamicDecorator):
    """A decorator with both static binding and static callback.

    This class demonstrates how to override both __get__ and __call__ methods to use static methods
    for both binding and callback. In this case, using BaseDecorator directly might be more efficient.
    """

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: GetObjectMethod = BaseCallable.bind_builtin  # Assigns __get__ to a previously defined method.
    __call__: AnyCallable = BaseCallable.call_wrapped  # Assigns __call__ to a previously defined method.


# Example Classes #
class Calculator:
    """A class with methods to demonstrate decorators."""

    @MultiModeDecorator
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    @StaticBindingDecorator
    def subtract(self, a: int, b: int) -> int:
        """Subtract b from a."""
        return a - b

    @StaticCallbackDecorator
    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    @FullyStaticDecorator
    def divide(self, a: int, b: int) -> float:
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


# Functions #
def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number recursively."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Example Sections #
def basic_dynamicdecorator_usage():
    """Demonstrates basic usage of DynamicDecorator."""
    print("Basic DynamicDecorator Usage:\n")

    # Create a DynamicDecorator directly
    dynamic_decorator = DynamicDecorator(fibonacci)

    # Call the decorated function
    result = dynamic_decorator(5)
    print(f"fibonacci(5) = {result} == 5")

    # Use as a decorator
    @DynamicDecorator
    def square(x):
        return x * x

    result = square(4)
    print(f"square(4) = {result} == 16")

    print()


def dynamicdecorator_vs_basedecorator():
    """Demonstrates the differences between DynamicDecorator and BaseDecorator."""
    print("DynamicDecorator vs BaseDecorator:\n")

    # Create both types of decorators
    dynamic_dec = DynamicDecorator(fibonacci)
    base_dec = BaseDecorator(fibonacci)

    # Show that both can be called directly
    dynamic_result = dynamic_dec(5)
    base_result = base_dec(5)
    print(f"Direct call:")
    print(f"dynamic_dec(5) = {dynamic_result} == 5")
    print(f"base_dec(5) = {base_result} == 5")

    # Show the class hierarchy
    print(f"\nClass hierarchy:")
    print(f"DynamicDecorator inherits from: {DynamicDecorator.__mro__[1:3]}")
    print(f"BaseDecorator inherits from: {BaseDecorator.__mro__[1:2]}")

    # Show the key difference: DynamicDecorator has call_method and bind_method attributes
    print(f"\nKey differences:")
    print(f"DynamicDecorator has call_method: {hasattr(dynamic_dec, 'call_method')}")
    print(f"DynamicDecorator has bind_method: {hasattr(dynamic_dec, 'bind_method')}")
    print(f"BaseDecorator has call_method: {hasattr(base_dec, 'call_method')}")
    print(f"BaseDecorator has bind_method: {hasattr(base_dec, 'bind_method')}")

    print()


def multimode_decorator_example():
    """Demonstrates a DynamicDecorator that can switch between different modes."""
    print("MultiMode Decorator Example:\n")

    # Create a decorated function
    multi_fib = MultiModeDecorator(fibonacci)

    # Try different modes
    print("Normal mode:")
    result = multi_fib(5)
    print(f"Result: {result} == 5\n")

    print("Debug mode:")
    multi_fib.set_mode("debug")
    result = multi_fib(5)
    print(f"Result: {result} == 5\n")

    print("Timing mode:")
    multi_fib.set_mode("timing")
    result = multi_fib(10)
    print(f"Result: {result} == 55\n")

    # Use with a class
    calculator = Calculator()

    print("Calculator add method (default normal mode):")
    result = calculator.add(5, 3)
    print(f"5 + 3 = {result} == 8\n")

    # Create a new instance with a different mode
    # For demonstration purposes, we'll create a new decorator instance
    debug_decorator = MultiModeDecorator(lambda a, b: a + b, mode="debug")

    print("Calculator add method (debug mode):")
    result = debug_decorator(10, 7)
    print(f"10 + 7 = {result} == 17")

    print()


def static_binding_example():
    """Demonstrates a DynamicDecorator with static binding but dynamic callback."""
    print("Static Binding Decorator Example:\n")

    calculator = Calculator()

    print("Default normal callback mode:")
    result = calculator.subtract(10, 4)
    print(f"10 - 4 = {result} == 6\n")

    # Create a new instance with a different callback mode
    verbose_decorator = StaticBindingDecorator(lambda a, b: a - b, callback_mode="verbose")

    print("Verbose callback mode:")
    result = verbose_decorator(20, 8)
    print(f"20 - 8 = {result} == 12")

    print()


def static_callback_example():
    """Demonstrates a DynamicDecorator with static callback."""
    print("Static Callback Decorator Example:\n")

    calculator = Calculator()

    print("Using calculator's multiply method:")
    result = calculator.multiply(5, 6)
    print(f"5 * 6 = {result} == 30\n")

    # Create a new instance to demonstrate static callback
    static_callback = StaticCallbackDecorator(lambda a, b: a * b)

    print("Using static callback decorator:")
    result = static_callback(7, 8)
    print(f"7 * 8 = {result} == 56")

    print()


def fully_static_example():
    """Demonstrates a DynamicDecorator with both static binding and callback."""
    print("Fully Static Decorator Example:\n")

    calculator = Calculator()

    print("Using fully static decorator:")
    result = calculator.divide(20, 4)
    print(f"20 / 4 = {result} == 5.0")

    # Show that it behaves like a regular method
    try:
        result = calculator.divide(10, 0)
    except ValueError as e:
        print(f"\nError handling works: {e}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of DynamicDecorator
    basic_dynamicdecorator_usage()

    # Compare DynamicDecorator with BaseDecorator
    dynamicdecorator_vs_basedecorator()

    # MultiMode decorator example
    multimode_decorator_example()

    # Static binding example
    static_binding_example()

    # Static callback example
    static_callback_example()

    # Fully static example
    fully_static_example()
