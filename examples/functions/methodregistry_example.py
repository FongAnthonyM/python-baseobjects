#!/usr/bin/env python
"""methodregistry_example.py
An example of how to create and use MethodRegistry.

This example demonstrates:
1. Creating a MethodRegistry with different initialization methods
2. Using MethodRegistry as a descriptor to bind methods to instances
3. Accessing and using methods from the registry
4. Comparing MethodRegistry with FunctionRegistry
5. Using MethodRegistry in practical applications
"""

# Imports #
# Standard Libraries #
from collections.abc import Callable
from typing import Any

# Source Packages #
from baseobjects.functions import FunctionRegistry, MethodRegistry


# Definitions #
# Classes #
class MathOperations:
    """A class with various mathematical operations.

    This class demonstrates how methods can be extracted and stored in a MethodRegistry.
    """

    def add(self, a: float, b: float) -> float:
        """Adds two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of the two numbers.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtracts the second number from the first.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The difference between the two numbers.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiplies two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The product of the two numbers.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divides the first number by the second.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The quotient of the division.

        Raises:
            ValueError: If attempting to divide by zero.
        """
        if b == 0:
            msg = "Cannot divide by zero"
            raise ValueError(msg)
        return a / b


class StringOperations:
    """A class with various string operations.

    This class demonstrates how methods can be extracted and stored in a MethodRegistry.
    """

    def uppercase(self, text: str) -> str:
        """Converts text to uppercase.

        Args:
            text: The text to convert.

        Returns:
            The text in uppercase.
        """
        return text.upper()

    def lowercase(self, text: str) -> str:
        """Converts text to lowercase.

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


class OperationsContainer:
    """A container class that uses MethodRegistry as a descriptor.

    This class demonstrates how MethodRegistry can be used as a descriptor
    to bind methods to instances.
    """

    # Defines a MethodRegistry as a class attribute
    # When accessed through an instance, it will return a BoundMethodRegistry
    methods = MethodRegistry()

    def __init__(self, name: str) -> None:
        """Initializes the container with a name.

        Args:
            name: The name of the container.
        """
        self.name = name

        # Initializes the methods registry with some methods
        # We'll use a separate instance variable to store the math_ops instance
        self.math_ops = MathOperations()

        # Adds methods to the registry
        # The methods will be bound to self.math_ops when accessed through self.methods
        # We wrap them to handle the double binding
        # (MethodRegistry binds to instance, and math_ops methods are already bound)
        self.methods["add"] = lambda obj, *args, **kwargs: self.math_ops.add(*args, **kwargs)
        self.methods["subtract"] = lambda obj, *args, **kwargs: self.math_ops.subtract(*args, **kwargs)
        self.methods["multiply"] = lambda obj, *args, **kwargs: self.math_ops.multiply(*args, **kwargs)
        self.methods["divide"] = lambda obj, *args, **kwargs: self.math_ops.divide(*args, **kwargs)

    def add_method(self, name: str, method: Callable[..., Any]) -> None:
        """Adds a method to the registry.

        Args:
            name: The name of the method.
            method: The method to add.
        """
        self.methods[name] = method

    def execute_method(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """Executes a method from the registry.

        Args:
            method_name: The name of the method to execute.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the method execution.

        Raises:
            KeyError: If the method is not in the registry.
        """
        if method_name not in self.methods:
            msg = f"Method '{method_name}' not found in registry"
            raise KeyError(msg)

        method = self.methods[method_name]
        return method(*args, **kwargs)

    def list_methods(self) -> list[str]:
        """List all methods in the registry.

        Returns:
            A list of method names.
        """
        return list(self.methods.keys())


class MultiOperationsContainer:
    """A container class that uses multiple MethodRegistry instances.

    This class demonstrates how multiple MethodRegistry instances can be used
    to organize methods by category.
    """

    # Defines separate MethodRegistry instances for different categories
    math_methods = MethodRegistry()
    string_methods = MethodRegistry()

    def __init__(self, name: str) -> None:
        """Initializes the container with a name.

        Args:
            name: The name of the container.
        """
        self.name = name

        # Initializes the method registries
        # We'll use separate instance variables to store the operations instances
        self.math_ops = MathOperations()
        self.string_ops = StringOperations()

        # Adds methods to the math registry
        # The methods will be bound to self.math_ops when accessed through self.math_methods
        self.math_methods["add"] = lambda obj, *args, **kwargs: self.math_ops.add(*args, **kwargs)
        self.math_methods["subtract"] = lambda obj, *args, **kwargs: self.math_ops.subtract(*args, **kwargs)
        self.math_methods["multiply"] = lambda obj, *args, **kwargs: self.math_ops.multiply(*args, **kwargs)
        self.math_methods["divide"] = lambda obj, *args, **kwargs: self.math_ops.divide(*args, **kwargs)

        # Adds methods to the string registry
        # The methods will be bound to self.string_ops when accessed through self.string_methods
        self.string_methods["uppercase"] = lambda obj, *args, **kwargs: self.string_ops.uppercase(*args, **kwargs)
        self.string_methods["lowercase"] = lambda obj, *args, **kwargs: self.string_ops.lowercase(*args, **kwargs)
        self.string_methods["capitalize"] = lambda obj, *args, **kwargs: self.string_ops.capitalize(*args, **kwargs)
        self.string_methods["reverse"] = lambda obj, *args, **kwargs: self.string_ops.reverse(*args, **kwargs)

    def execute_math_method(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """Executes a math method from the registry.

        Args:
            method_name: The name of the method to execute.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the method execution.

        Raises:
            KeyError: If the method is not in the registry.
        """
        if method_name not in self.math_methods:
            msg = f"Math method '{method_name}' not found in registry"
            raise KeyError(msg)

        method = self.math_methods[method_name]
        return method(*args, **kwargs)

    def execute_string_method(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """Executes a string method from the registry.

        Args:
            method_name: The name of the method to execute.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the method execution.

        Raises:
            KeyError: If the method is not in the registry.
        """
        if method_name not in self.string_methods:
            msg = f"String method '{method_name}' not found in registry"
            raise KeyError(msg)

        method = self.string_methods[method_name]
        return method(*args, **kwargs)

    def list_math_methods(self) -> list[str]:
        """List all math methods in the registry.

        Returns:
            A list of method names.
        """
        return list(self.math_methods.keys())

    def list_string_methods(self) -> list[str]:
        """List all string methods in the registry.

        Returns:
            A list of method names.
        """
        return list(self.string_methods.keys())


# Functions #
# Example Sections #
def basic_method_registry() -> None:
    """Demonstrates basic usage of MethodRegistry."""
    print("Basic MethodRegistry Usage:\n")

    # Creates a class with a MethodRegistry
    class Example:
        methods = MethodRegistry()

        def __init__(self, name: str) -> None:
            """Initializes."""
            self.name = name

    # Creates instances of the class
    instance1 = Example("Instance 1")
    instance2 = Example("Instance 2")

    # Shows that each instance has its own bound registry
    print("Each instance has its own bound registry:")
    print(f"instance1.methods is instance2.methods: {instance1.methods is instance2.methods}")
    print(f"Type of instance1.methods: {type(instance1.methods).__name__}")
    print(f"Type of Example.methods: {type(Example.methods).__name__}")

    # Adds methods to the registry
    print("\nAdding methods to the registry...")

    # Creates a MathOperations instance
    math_ops = MathOperations()

    # Adds methods to the class registry
    # Since MethodRegistry binds the method to the instance, we need to wrap the
    # already-bound methods to accept the instance (self) as the first argument
    Example.methods["add"] = lambda self, *args, **kwargs: math_ops.add(*args, **kwargs)
    Example.methods["subtract"] = lambda self, *args, **kwargs: math_ops.subtract(*args, **kwargs)

    # Checks the methods in each instance
    print(f"Methods in instance1: {list(instance1.methods.keys())}")
    print(f"Methods in instance2: {list(instance2.methods.keys())}")

    # Use methods from the registry
    print("\nUsing methods from the registry:")
    a, b = 10, 5

    # The methods are bound to the instance
    result1 = instance1.methods["add"](a, b)
    print(f"instance1.methods['add']({a}, {b}) = {result1}")

    result2 = instance2.methods["subtract"](a, b)
    print(f"instance2.methods['subtract']({a}, {b}) = {result2}")

    print()


def method_registry_vs_function_registry() -> None:
    """Demonstrates the difference between MethodRegistry and FunctionRegistry."""
    print("MethodRegistry vs FunctionRegistry:\n")

    # Creates a class with both registry types
    class Example:
        method_registry = MethodRegistry()
        function_registry = FunctionRegistry()

        def __init__(self, name: str) -> None:
            """Initializes."""
            self.name = name

    # Creates instances of the class
    instance1 = Example("Instance 1")
    instance2 = Example("Instance 2")

    # Creates operation instances
    math_ops = MathOperations()
    string_ops = StringOperations()

    # Adds methods to both registries
    # For MethodRegistry, we wrap to handle the bound instance
    Example.method_registry["add"] = lambda self, *args, **kwargs: math_ops.add(*args, **kwargs)
    Example.method_registry["uppercase"] = lambda self, *args, **kwargs: string_ops.uppercase(*args, **kwargs)

    Example.function_registry["add"] = math_ops.add
    Example.function_registry["uppercase"] = string_ops.uppercase

    # Compares the registries
    print("Registry types:")
    print(f"Type of Example.method_registry: {type(Example.method_registry).__name__}")
    print(f"Type of instance1.method_registry: {type(instance1.method_registry).__name__}")
    print(f"Type of Example.function_registry: {type(Example.function_registry).__name__}")
    print(f"Type of instance1.function_registry: {type(instance1.function_registry).__name__}")

    # Shows that method_registry instances are different for each instance
    print("\nRegistry instances:")
    same_method_registry = instance1.method_registry is instance2.method_registry
    print("method_registry same across instances:", same_method_registry)
    same_function_registry = instance1.function_registry is instance2.function_registry
    print("function_registry same across instances:", same_function_registry)

    # Use methods from both registries
    print("\nUsing methods from both registries:")
    a, b = 10, 5
    text = "hello world"

    # With MethodRegistry, the methods are bound to the instance
    # The 'self' parameter is automatically bound to the instance
    result1 = instance1.method_registry["add"](a, b)
    print(f"instance1.method_registry['add']({a}, {b}) = {result1}")

    result2 = instance1.method_registry["uppercase"](text)
    print(f"instance1.method_registry['uppercase']('{text}') = '{result2}'")

    # With FunctionRegistry, the methods are not bound to the instance
    try:
        # This will fail because the method expects 'self' as the first argument
        result3 = instance1.function_registry["add"](a, b)
        print(f"instance1.function_registry['add']({a}, {b}) = {result3}")
    except TypeError as e:
        print(f"Error with function_registry['add']: {e}")

    try:
        # This will fail because the method expects 'self' as the first argument
        result4 = instance1.function_registry["uppercase"](text)
        print(f"instance1.function_registry['uppercase']('{text}') = '{result4}'")
    except TypeError as e:
        print(f"Error with function_registry['uppercase']: {e}")

    # To make the function_registry work, we need to use static methods or functions
    # Let's define some static methods and functions
    print("\nUsing static methods and functions with function_registry:")

    # Defines static methods
    def static_add(a: float, b: float) -> float:
        """Adds two numbers without requiring an instance.

        Returns:
            The sum.
        """
        return a + b

    def static_uppercase(text: str) -> str:
        """Uppercase text without requiring an instance.

        Returns:
            The uppercase text.
        """
        return text.upper()

    # Adds the static methods to the function_registry
    Example.function_registry["static_add"] = static_add
    Example.function_registry["static_uppercase"] = static_uppercase

    # Now we can use them without passing 'self'
    result5 = instance1.function_registry["static_add"](a, b)
    print(f"instance1.function_registry['static_add']({a}, {b}) = {result5}")

    result6 = instance1.function_registry["static_uppercase"](text)
    print(f"instance1.function_registry['static_uppercase']('{text}') = '{result6}'")

    print()


def operations_container_example() -> None:
    """Demonstrates using MethodRegistry in a practical application."""
    print("OperationsContainer Example:\n")

    # Creates containers
    container1 = OperationsContainer("Container 1")
    container2 = OperationsContainer("Container 2")

    # Shows the initial methods
    print(f"Initial methods in {container1.name}: {container1.list_methods()}")

    # Executes some methods
    print("\nExecuting methods:")
    a, b = 10, 5

    result = container1.execute_method("add", a, b)
    print(f"{container1.name}.execute_method('add', {a}, {b}) = {result}")

    result = container1.execute_method("subtract", a, b)
    print(f"{container1.name}.execute_method('subtract', {a}, {b}) = {result}")

    result = container1.execute_method("multiply", a, b)
    print(f"{container1.name}.execute_method('multiply', {a}, {b}) = {result}")

    result = container1.execute_method("divide", a, b)
    print(f"{container1.name}.execute_method('divide', {a}, {b}) = {result}")

    # Adds a custom method to container2
    print(f"\nAdding a custom method to {container2.name}...")

    # Defines a method for the math_ops instance
    def power_method(self: Any, a: float, b: float) -> float:
        """Raise a to the power of b.

        Returns:
            The result of the power operation.
        """
        return float(a**b)

    # Adds the method to the math_ops instance
    container2.math_ops.power = power_method.__get__(container2.math_ops, MathOperations)  # type: ignore[attr-defined]

    # Adds the bound method to the registry
    # We need to wrap it to handle the double binding
    container2.add_method("power", lambda obj, *args: container2.math_ops.power(*args))  # type: ignore[attr-defined]

    # Shows the updated methods
    print(f"Methods in {container2.name}: {container2.list_methods()}")

    # Executes the custom method
    result = container2.execute_method("power", 2, 3)
    print(f"{container2.name}.execute_method('power', 2, 3) = {result}")

    # Try to execute a method that doesn't exist
    print("\nTrying to execute a method that doesn't exist:")
    try:
        result = container2.execute_method("nonexistent", 1, 2)
        print(f"Result: {result}")
    except KeyError as e:
        print(f"Error: {e}")

    print()


def multi_operations_container_example() -> None:
    """Demonstrates using multiple MethodRegistry instances in a class."""
    print("MultiOperationsContainer Example:\n")

    # Creates a container
    container = MultiOperationsContainer("Multi Container")

    # Shows the available methods
    print(f"Math methods: {container.list_math_methods()}")
    print(f"String methods: {container.list_string_methods()}")

    # Executes some math methods
    print("\nExecuting math methods:")
    a, b = 10, 5

    result = container.execute_math_method("add", a, b)
    print(f"execute_math_method('add', {a}, {b}) = {result}")

    result = container.execute_math_method("subtract", a, b)
    print(f"execute_math_method('subtract', {a}, {b}) = {result}")

    # Executes some string methods
    print("\nExecuting string methods:")
    text = "hello world"

    result = container.execute_string_method("uppercase", text)
    print(f"execute_string_method('uppercase', '{text}') = '{result}'")

    result = container.execute_string_method("capitalize", text)
    print(f"execute_string_method('capitalize', '{text}') = '{result}'")

    result = container.execute_string_method("reverse", text)
    print(f"execute_string_method('reverse', '{text}') = '{result}'")

    print()


def method_binding_example() -> None:
    """Demonstrates how MethodRegistry binds methods to instances."""
    print("Method Binding Example:\n")

    # Creates a class with instance methods
    class Example:
        def __init__(self, name: str, value: Any) -> None:
            """Initializes."""
            self.name = name
            self.value = value

            # Creates a MethodRegistry for this instance
            self.methods = MethodRegistry()

            # Adds instance methods to the registry
            self.methods["get"] = self.get_value
            self.methods["set"] = self.set_value

        def get_value(self) -> Any:
            return self.value

        def set_value(self, value: Any) -> Any:
            self.value = value
            return self.value

    # Creates instances with different values
    instance1 = Example("Instance 1", 10)
    instance2 = Example("Instance 2", 20)

    # Shows that the methods are bound to the correct instance
    print("Methods bound to instances:")

    # Gets values from both instances
    result1 = instance1.methods["get"]()
    result2 = instance2.methods["get"]()

    print(f"{instance1.name}.methods['get']() = {result1}")
    print(f"{instance2.name}.methods['get']() = {result2}")

    # Sets values on both instances
    new_value1 = 15
    new_value2 = 25

    result1 = instance1.methods["set"](new_value1)
    result2 = instance2.methods["set"](new_value2)

    print(f"\n{instance1.name}.methods['set']({new_value1}) = {result1}")
    print(f"{instance2.name}.methods['set']({new_value2}) = {result2}")

    # Verifies the values were updated
    print("\nUpdated values:")
    print(f"{instance1.name}.value = {instance1.value}")
    print(f"{instance2.name}.value = {instance2.value}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of MethodRegistry
    basic_method_registry()

    # Compares MethodRegistry with FunctionRegistry
    method_registry_vs_function_registry()

    # Using MethodRegistry in a practical application
    operations_container_example()

    # Using multiple MethodRegistry instances
    multi_operations_container_example()

    # Demonstrating method binding
    method_binding_example()
