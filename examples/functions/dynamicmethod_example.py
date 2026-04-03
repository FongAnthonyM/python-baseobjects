#!/usr/bin/env python
"""dynamicmethod_example.py
An example of how to create and use DynamicMethod.

This example demonstrates:
1. Creating a DynamicMethod object
2. Understanding how DynamicMethod differs from DynamicCallable and DynamicFunction
3. Using DynamicMethod with different binding and calling methods
4. Creating custom DynamicMethod subclasses
5. Using DynamicMethod as a descriptor
6. Method binding behavior and self parameter handling
"""

# Imports #
# Standard Libraries #
from dataclasses import dataclass
from typing import Any

# Source Packages #
from baseobjects.functions import DynamicCallable, DynamicFunction, DynamicMethod


# Definitions #
# Classes #
@dataclass
class PickleClass:
    """A class used for pickling demonstration."""

    name: str


class CustomDynamicMethod(DynamicMethod):
    """A custom implementation of DynamicMethod with additional binding and calling methods.

    This class demonstrates how to extend DynamicMethod with custom binding and calling methods.
    """

    def bind_with_prefix(self, instance: Any, owner: Any = None) -> Any:
        """A custom binding method that adds a prefix to the callable.

        Args:
            instance: The instance to bind to.
            owner: The owner class.

        Returns:
            A callable that adds a prefix to the result.
        """

        # Creates a new callable that adds a prefix
        def prefixed_callable(*args: Any, **kwargs: Any) -> Any:
            assert self.__wrapped__ is not None
            result = self.__wrapped__(instance, *args, **kwargs)
            if isinstance(result, str):
                return f"[Prefixed] {result}"
            return result

        return prefixed_callable

    def call_with_logging(self, instance: Any, *args: Any, **kwargs: Any) -> Any:
        """A custom calling method that logs the call.

        Args:
            instance: The instance the method is bound to.
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        assert self.__wrapped__ is not None
        print(f"Calling {self.__wrapped__.__name__} on {instance} with args: {args}, kwargs: {kwargs}")
        result = self.__wrapped__(instance, *args, **kwargs)
        print(f"Result: {result}")
        return result

    def call_with_validation(self, instance: Any, *args: Any, **kwargs: Any) -> Any:
        """A custom calling method that validates the arguments.

        Args:
            instance: The instance the method is bound to.
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

        assert self.__wrapped__ is not None
        return self.__wrapped__(instance, *args, **kwargs)


class NonWrappingDynamicMethod(DynamicMethod):
    """A custom non-wrapping implementation of DynamicMethod that defines functionality directly.

    This class demonstrates how to extend DynamicMethod without relying on a wrapped function. Instead, it implements
    its own functionality directly through custom methods registered with the call_multiplexer.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes the NonWrappingDynamicMethod.

        This constructor initializes the object without requiring a wrapped function. It registers custom methods with
        the call_multiplexer and sets a default call method.

        Args:
            *args: Arguments for the parent class.
            **kwargs: Keyword arguments for the parent class.
        """
        # Initializes with no wrapped function
        super().__init__(None, *args, **kwargs)

        # Sets the default call method
        self.call_method = "greet"

    def greet(self, instance: Any, name: str) -> str:
        """Greet a person using the instance's name.

        Args:
            instance: The instance the method is bound to.
            name: The name of the person to greet.

        Returns:
            A greeting message.
        """
        return f"Hello, {name}! I'm {instance.name}!"

    def farewell(self, instance: Any, name: str) -> str:
        """Say goodbye to a person using the instance's name.

        Args:
            instance: The instance the method is bound to.
            name: The name of the person to say goodbye to.

        Returns:
            A farewell message.
        """
        return f"Goodbye, {name}! From {instance.name}."

    def introduce(self, instance: Any, title: str = "") -> str:
        """Introduce the instance.

        Args:
            instance: The instance the method is bound to.
            title: An optional title for the introduction.

        Returns:
            An introduction message.
        """
        if title:
            return f"I am {title} {instance.name}."
        return f"I am {instance.name}."


class ExampleClass:
    """A class to demonstrate using DynamicMethod as a descriptor."""

    def __init__(self, name: str) -> None:
        """Initializes the object."""
        self.name = name

    def greet(self, name: str) -> str:
        """A method that greets a person.

        Returns:
            The greeting string.
        """
        return f"Hello, {name}! I'm {self.name}!"

    # Creates a DynamicMethod as a class attribute
    dynamic_greeter = DynamicMethod(greet)

    # Creates a custom DynamicMethod as a class attribute
    custom_greeter = CustomDynamicMethod(greet)

    # Creates a non-wrapping DynamicMethod as a class attribute
    nonwrapping_greeter = NonWrappingDynamicMethod()


class MethodComparisonClass:
    """A class to demonstrate the differences between various method types."""

    def __init__(self, name: str) -> None:
        """Initializes the object."""
        self.name = name

    def regular_method(self, message: str) -> str:
        """A regular instance method.

        Returns:
            The formatted message.
        """
        return f"{self.name} says: {message}"

    # Creates different types of dynamic methods
    dynamic_method = DynamicMethod(regular_method)
    dynamic_function = DynamicFunction(regular_method)
    dynamic_callable = DynamicCallable(regular_method)


# Functions #
def method_function(self: Any, message: str) -> str:
    """A function designed to be used as a method.

    Args:
        self: The instance the method is bound to.
        message: A message to include.

    Returns:
        A formatted message.
    """
    return f"{self.name} says: {message}"


# Example Sections #
def basic_dynamicmethod_usage() -> None:
    """Demonstrates basic usage of DynamicMethod."""
    print("Basic DynamicMethod Usage:\n")

    # Creates a DynamicMethod with a method function
    dynamic_method = DynamicMethod(method_function)

    # Creates an instance to bind the method to
    @dataclass
    class SimpleClass:
        name: str

    instance = SimpleClass("Alice")

    # Binds the method to the instance
    bound_method = dynamic_method.__get__(instance, SimpleClass)

    # Calls the bound method
    result = bound_method("Hello, world!")
    print("Bound method call:")
    print(f"bound_method('Hello, world!') = {result}")

    # Checks the current bind method
    print(f"\nCurrent bind method: {dynamic_method.bind_method}")

    # Checks the current call method
    print(f"Current call method: {dynamic_method.call_method}")

    # Creates a DynamicMethod with no function
    empty_dynamic = DynamicMethod()

    # Sets the function after creation
    empty_dynamic.__func__ = method_function

    # Binds and call the method
    bound_empty = empty_dynamic.__get__(instance, SimpleClass)
    result = bound_empty("Hello from empty method!")
    print("\nSetting function after creation:")
    print(f"bound_empty('Hello from empty method!') = {result}")

    print()


def dynamicmethod_vs_others() -> None:
    """Demonstrates the differences between DynamicMethod, DynamicFunction, and DynamicCallable."""
    print("DynamicMethod vs DynamicFunction vs DynamicCallable:\n")

    # Creates an instance of the comparison class
    comparison = MethodComparisonClass("John")

    # Use the regular method
    regular_result = comparison.regular_method("Regular message")
    print("Regular method:")
    print(f"comparison.regular_method('Regular message') = {regular_result}")

    # Use the DynamicMethod
    dynamic_method_result = comparison.dynamic_method("Dynamic method message")
    print("\nDynamicMethod:")
    print(f"comparison.dynamic_method('Dynamic method message') = {dynamic_method_result}")

    # Use the DynamicFunction
    try:
        dynamic_function_result = comparison.dynamic_function("Dynamic function message")
        print("\nDynamicFunction:")
        print(f"comparison.dynamic_function('Dynamic function message') = {dynamic_function_result}")
    except Exception as e:
        print(f"\nDynamicFunction error: {e}")
        print("Note: DynamicFunction doesn't automatically pass self as the first argument.")

        # Gets the bound function and call it manually with self
        bound_function = comparison.dynamic_function
        dynamic_function_result = bound_function(comparison, "Dynamic function message")
        print(
            f"Manual call with self: bound_function(comparison, 'Dynamic function message') = "
            f"{dynamic_function_result}",
        )

    # Use the DynamicCallable
    try:
        dynamic_callable_result = comparison.dynamic_callable("Dynamic callable message")
        print("\nDynamicCallable:")
        print(f"comparison.dynamic_callable('Dynamic callable message') = {dynamic_callable_result}")
    except Exception as e:
        print(f"\nDynamicCallable error: {e}")
        print("Note: DynamicCallable doesn't automatically pass self as the first argument.")

        # Gets the bound callable and call it manually with self
        bound_callable = comparison.dynamic_callable
        dynamic_callable_result = bound_callable(comparison, "Dynamic callable message")
        print(
            f"Manual call with self: bound_callable(comparison, 'Dynamic callable message') = "
            f"{dynamic_callable_result}",
        )

    # Shows the class hierarchy
    print("\nClass hierarchy:")
    print(f"DynamicMethod inherits from: {DynamicMethod.__mro__[1:3]}")
    print(f"DynamicFunction inherits from: {DynamicFunction.__mro__[1:3]}")
    print(f"DynamicCallable inherits from: {DynamicCallable.__mro__[1:2]}")

    print()


def custom_dynamicmethod_usage() -> None:
    """Demonstrates usage of a custom DynamicMethod with additional methods."""
    print("Custom DynamicMethod Usage:\n")

    # Creates an instance of ConcreteClass
    example = ExampleClass("Sarah")

    # Use the custom DynamicMethod with default call method
    result = example.custom_greeter("Bob")
    print("Default call method (call_wrapped):")
    print(f"example.custom_greeter('Bob') = {result}")

    # Gets the DynamicMethod instance
    dynamic_method = example.custom_greeter.__func__

    # Switch to the custom call method with logging
    dynamic_method.call_method = "call_with_logging"
    result = example.custom_greeter("Charlie")

    # Switch to the custom call method with validation
    dynamic_method.call_method = "call_with_validation"
    print("\nUsing call_with_validation method:")
    try:
        result = example.custom_greeter(None)
    except ValueError as e:
        print(f"Validation error: {e}")

    # Valid call with the validation method
    result = example.custom_greeter("David")
    print(f"Valid call: example.custom_greeter('David') = {result}")

    # Switch to the custom bind method
    dynamic_method.bind_method = "bind_with_prefix"
    result = example.custom_greeter("Eve")
    print("\nUsing bind_with_prefix method:")
    print(f"example.custom_greeter('Eve') = {result}")

    print()


def dynamicmethod_as_descriptor() -> None:
    """Demonstrates using DynamicMethod as a descriptor."""
    print("DynamicMethod as Descriptor:\n")

    # Creates an instance of ConcreteClass
    example = ExampleClass("Michael")

    # Use the DynamicMethod descriptor
    result = example.dynamic_greeter("Alice")
    print("Using dynamic_greeter descriptor:")
    print(f"example.dynamic_greeter('Alice') = {result}")

    # Examine what happens during descriptor binding
    print("\nDescriptor binding process:")
    print("1. DynamicMethod.__get__ is called with instance and owner")
    print("2. bind_multiplexer is called with instance and owner")
    print("3. The selected bind method (bind_self) creates a bound method")
    print("4. When the bound method is called, it passes self automatically")

    # Shows that the bound method has access to instance attributes
    example.name = "Changed Name"
    result = example.dynamic_greeter("Bob")
    print("\nAfter changing instance attribute:")
    print(f"example.dynamic_greeter('Bob') = {result}")

    print()


def nonwrapping_dynamicmethod_usage() -> None:
    """Demonstrates usage of a non-wrapping DynamicMethod with direct functionality."""
    print("Non-Wrapping DynamicMethod Usage:\n")

    # Creates a non-wrapping DynamicMethod directly
    greeter = NonWrappingDynamicMethod()

    # Creates an instance to bind to
    @dataclass
    class Person:
        name: str

    person = Person("James")

    # Binds the method to the instance
    bound_greeter = greeter.__get__(person, Person)

    # Use the default call method (greet)
    result = bound_greeter("Alice")
    print("Default call method (greet):")
    print(f"bound_greeter('Alice') = {result}")

    # Switch to the farewell method
    greeter.call_method = "farewell"
    result = bound_greeter("Bob")
    print("\nUsing farewell method:")
    print(f"bound_greeter('Bob') = {result}")

    # Switch to the introduce method
    greeter.call_method = "introduce"
    result = bound_greeter()
    print("\nUsing introduce method:")
    print(f"bound_greeter() = {result}")

    # Use the introduce method with a title
    result = bound_greeter(title="Dr.")
    print(f"bound_greeter(title='Dr.') = {result}")

    print()


def method_binding_behavior() -> None:
    """Demonstrates the method binding behavior of DynamicMethod."""
    print("Method Binding Behavior:\n")

    # Creates a class with a DynamicMethod
    class BindingExample:
        def __init__(self, name: str) -> None:
            """Initializes."""
            self.name = name

        def method(self, message: str) -> str:
            return f"{self.name}: {message}"

        dynamic_method = DynamicMethod(method)

    # Creates instances of the class
    instance1 = BindingExample("Instance 1")
    instance2 = BindingExample("Instance 2")

    # Shows that the method is bound to the correct instance
    result1 = instance1.dynamic_method("Hello")
    result2 = instance2.dynamic_method("Hello")
    print("Binding to different instances:")
    print(f"instance1.dynamic_method('Hello') = {result1}")
    print(f"instance2.dynamic_method('Hello') = {result2}")

    # Shows that the bound method keeps a reference to the instance
    bound_method = instance1.dynamic_method
    instance1.name = "Changed Instance 1"
    result = bound_method("After change")
    print("\nAfter changing instance attribute:")
    print(f"bound_method('After change') = {result}")

    # Creates a DynamicMethod with different bind methods
    class BindMethodsExample:
        def __init__(self, name: str) -> None:
            """Initializes."""
            self.name = name

        def method(self, message: str) -> str:
            return f"{self.name}: {message}"

        # Creates DynamicMethods with different bind methods
        default_bind = DynamicMethod(method)

        # Creates a DynamicMethod with custom bind method
        custom_bind = DynamicMethod(method)

        def __init_subclass__(cls, **kwargs: Any) -> None:
            # Change the bind method after class creation
            cls.custom_bind.bind_method = "bind_class"

    # Creates an instance of the class
    bind_example = BindMethodsExample("Bind Example")

    # Use the default bind method
    result = bind_example.default_bind("Default bind")
    print("\nDefault bind method (bind_self):")
    print(f"bind_example.default_bind('Default bind') = {result}")

    # Use the custom bind method
    try:
        result = bind_example.custom_bind("Custom bind")
        print("\nCustom bind method (bind_class):")
        print(f"bind_example.custom_bind('Custom bind') = {result}")
    except Exception as e:
        print(f"\nCustom bind method error: {e}")
        print("Note: bind_class is not implemented in this example.")

    print()


def pickling_dynamicmethod() -> None:
    """Demonstrates pickling and unpickling a DynamicMethod."""
    print("Pickling DynamicMethod:\n")

    # Standard Libraries #
    import pickle

    # Creates a DynamicMethod
    dynamic_method = DynamicMethod(method_function)

    # Creates an instance of the global PickleClass
    instance = PickleClass("Pickle Example")

    # Binds the method and test before pickling
    bound_method = dynamic_method.__get__(instance, PickleClass)
    result = bound_method("Before pickling")
    print("Before pickling:")
    print(f"bound_method('Before pickling') = {result}")

    # Pickle the DynamicMethod
    pickled = pickle.dumps(dynamic_method)

    # Unpickle the DynamicMethod
    unpickled = pickle.loads(pickled)

    # Binds the unpickled method and test
    bound_unpickled = unpickled.__get__(instance, PickleClass)
    result = bound_unpickled("After unpickling")
    print("\nAfter unpickling:")
    print(f"bound_unpickled('After unpickling') = {result}")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of DynamicMethod
    basic_dynamicmethod_usage()

    # DynamicMethod vs DynamicFunction vs DynamicCallable
    dynamicmethod_vs_others()

    # Custom DynamicMethod usage
    custom_dynamicmethod_usage()

    # Using DynamicMethod as a descriptor
    dynamicmethod_as_descriptor()

    # Non-wrapping DynamicMethod usage
    nonwrapping_dynamicmethod_usage()

    # Method binding behavior
    method_binding_behavior()

    # Pickling DynamicMethod
    pickling_dynamicmethod()
