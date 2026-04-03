#!/usr/bin/env python
"""basecomposite_example.py
An example of how to create and use BaseComposite.

This example demonstrates:
1. Creating a composite class that inherits from BaseComposite
2. Adding components to a composite
3. Accessing components from a composite
4. Creating components with default types
5. Serialization and deserialization of composites with components
"""

# Imports #
# Standard Libraries #
import pickle
from typing import Any, ClassVar

# Source Packages #
from baseobjects.composition import BaseComponent, BaseComposite


# Definitions #
# Classes #
class MathComponent(BaseComponent):
    """A component that provides mathematical operations for a composite."""

    def add(self, a: int, b: int) -> int:
        """Adds two numbers and updates the composite's result.

        Args:
            a: First number to add.
            b: Second number to add.

        Returns:
            The sum of the two numbers.
        """
        result = a + b
        self.composite.result = result
        return result

    def subtract(self, a: int, b: int) -> int:
        """Subtracts b from a and updates the composite's result.

        Args:
            a: Number to subtract from.
            b: Number to subtract.

        Returns:
            The difference between a and b.
        """
        result = a - b
        self.composite.result = result
        return result

    def multiply(self, a: int, b: int) -> int:
        """Multiplies two numbers and updates the composite's result.

        Args:
            a: First number to multiply.
            b: Second number to multiply.

        Returns:
            The product of the two numbers.
        """
        result = a * b
        self.composite.result = result
        return result


class LoggingComponent(BaseComponent):
    """A component that logs operations performed on a composite."""

    def __init__(self, composite: Any = None, init: bool = True, **kwargs: Any) -> None:
        """Initializes the LoggingComponent.

        Args:
            composite: The composite this component belongs to.
            init: Whether to initialize the component.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(composite=composite, init=init, **kwargs)
        self.log: list[str] = []

    def log_operation(self, operation: str, *args: Any) -> None:
        """Logs an operation performed on the composite.

        Args:
            operation: The name of the operation.
            *args: Arguments used in the operation.
        """
        log_entry = f"{operation}({', '.join(str(arg) for arg in args)}) = {self.composite.result}"
        self.log.append(log_entry)
        print(f"Logged: {log_entry}")

    def get_log(self) -> list[str]:
        """Gets the operation log.

        Returns:
            The list of logged operations.
        """
        return self.log

    def clear_log(self) -> None:
        """Clears the operation log."""
        self.log.clear()
        print("Log cleared")


class FormattingComponent(BaseComponent):
    """A component that formats the result of a composite."""

    def format_result(self, prefix: str = "Result: ", suffix: str = "") -> str:
        """Formats the composite's result with a prefix and suffix.

        Args:
            prefix: Text to prepend to the result.
            suffix: Text to append to the result.

        Returns:
            The formatted result.
        """
        formatted = f"{prefix}{self.composite.result}{suffix}"
        self.composite.formatted_result = formatted
        return formatted


class Calculator(BaseComposite):
    """A composite calculator that uses components for different operations.

    Attributes:
        result: The current calculation result.
        formatted_result: The formatted version of the result.
        default_component_types: Default components to create when initializing.
    """

    # Class Attributes #
    default_component_types: ClassVar[dict[str, tuple[type[BaseComponent], dict[str, Any]]]] = {
        "math": (MathComponent, {}),
        "logging": (LoggingComponent, {}),
    }

    # Attributes #
    result: int = 0
    formatted_result: str = ""


# Functions #
# Example Sections #
def basic_composite_usage() -> None:
    """Demonstrates basic usage of a composite with components."""
    print("Basic Composite Usage:\n")

    # Creates a calculator composite
    print("Creating a calculator composite...")
    calculator = Calculator()

    # The calculator automatically creates the default components
    print("Default components created:")
    for name, component in calculator.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Use the math component to perform calculations
    print("Using the math component to perform calculations...")
    math_component = calculator.components["math"]

    # Addition
    result = math_component.add(5, 3)
    print(f"5 + 3 = {result} == 8")
    assert calculator.result == 8

    # Subtraction
    result = math_component.subtract(10, 4)
    print(f"10 - 4 = {result} == 6")
    assert calculator.result == 6

    # Multiplication
    result = math_component.multiply(3, 7)
    print(f"3 * 7 = {result} == 21")
    assert calculator.result == 21
    print()


def adding_components() -> None:
    """Demonstrates adding components to a composite."""
    print("Adding Components to a Composite:\n")

    # Creates a calculator with only the math component
    print("Creating a calculator with custom component types...")
    calculator = Calculator(component_types={"math": (MathComponent, {})})

    print("Initial components:")
    for name, component in calculator.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Adds a formatting component
    print("Adding a formatting component...")
    calculator.add_component("formatting", FormattingComponent(composite=calculator))

    print("Components after addition:")
    for name, component in calculator.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Use the components together
    print("Using components together...")
    math_component = calculator.components["math"]
    formatting_component = calculator.components["formatting"]

    # Performs a calculation
    result = math_component.add(12, 30)
    print(f"12 + 30 = {result} == 42")

    # Formats the result
    formatted = formatting_component.format_result("The answer is: ", "!")
    print(f"Formatted result: {formatted} == 'The answer is: 42!'")
    assert calculator.formatted_result == "The answer is: 42!"
    print()


def component_creation_methods() -> None:
    """Demonstrates different ways to create components in a composite."""
    print("Component Creation Methods:\n")

    # Method 1: Using default_component_types
    print("Method 1: Using default_component_types class attribute...")
    calculator1 = Calculator()
    print("Components created from default_component_types:")
    for name, component in calculator1.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Method 2: Using component_types parameter
    print("Method 2: Using component_types parameter...")
    calculator2 = Calculator(component_types={"math": (MathComponent, {}), "formatting": (FormattingComponent, {})})
    print("Components created from component_types parameter:")
    for name, component in calculator2.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Method 3: Using create_component method
    print("Method 3: Using create_component method...")
    calculator3 = Calculator(component_types={})
    calculator3.create_component("math", MathComponent)
    calculator3.create_component("logging", LoggingComponent)
    print("Components created using create_component:")
    for name, component in calculator3.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Method 4: Using components parameter with pre-created components
    print("Method 4: Using components parameter with pre-created components...")
    math_component = MathComponent()
    logging_component = LoggingComponent()
    calculator4 = Calculator(components={"math": math_component, "logging": logging_component})
    print("Components added from components parameter:")
    for name, component in calculator4.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()


def component_interaction() -> None:
    """Demonstrates interaction between components in a composite."""
    print("Component Interaction in a Composite:\n")

    # Creates a calculator with math and logging components
    print("Creating a calculator with math and logging components...")
    calculator = Calculator()

    # Gets the components
    math_component = calculator.components["math"]
    logging_component = calculator.components["logging"]

    # Performs calculations and log them
    print("Performing calculations and logging them...")

    # Addition
    math_component.add(5, 3)
    logging_component.log_operation("add", 5, 3)

    # Subtraction
    math_component.subtract(10, 4)
    logging_component.log_operation("subtract", 10, 4)

    # Multiplication
    math_component.multiply(3, 7)
    logging_component.log_operation("multiply", 3, 7)

    # Gets the log
    print("\nRetrieving the operation log...")
    log = logging_component.get_log()
    print("Operation log:")
    for entry in log:
        print(f"  - {entry}")
    print()


def composite_serialization() -> None:
    """Demonstrates serialization and deserialization of composites with components."""
    print("Composite Serialization and Deserialization:\n")

    # Creates a calculator with components
    print("Creating a calculator with components...")
    calculator = Calculator()

    # Performs some operations
    print("Performing some operations...")
    math_component = calculator.components["math"]
    math_component.add(10, 20)
    print(f"Result: {calculator.result} == 30")

    # Adds a formatting component
    calculator.add_component("formatting", FormattingComponent(composite=calculator))
    formatting_component = calculator.components["formatting"]
    formatted = formatting_component.format_result("Answer: ")
    print(f"Formatted result: {formatted} == 'Answer: 30'")

    # Serialize the calculator
    print("\nSerializing the calculator...")
    serialized = pickle.dumps(calculator)
    print(f"Calculator serialized to {len(serialized)} bytes")

    # Deserialize to a new calculator
    print("\nDeserializing to a new calculator...")
    new_calculator = pickle.loads(serialized)

    # Checks the deserialized calculator
    print("Checking the deserialized calculator...")
    print(f"Result: {new_calculator.result} == 30")
    print(f"Formatted result: {new_calculator.formatted_result} == 'Answer: 30'")

    # Checks the components
    print("\nComponents in the deserialized calculator:")
    for name, component in new_calculator.components.items():
        print(f"  - {name}: {type(component).__name__}")

    # Use the deserialized calculator
    print("\nUsing the deserialized calculator...")
    math_component = new_calculator.components["math"]
    result = math_component.multiply(5, 6)
    print(f"5 * 6 = {result} == 30")

    formatting_component = new_calculator.components["formatting"]
    formatted = formatting_component.format_result("New answer: ")
    print(f"Formatted result: {formatted} == 'New answer: 30'")
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of a composite with components
    basic_composite_usage()

    # Adding components to a composite
    adding_components()

    # Different ways to create components in a composite
    component_creation_methods()

    # Interaction between components in a composite
    component_interaction()

    # Serialization and deserialization of composites with components
    composite_serialization()
