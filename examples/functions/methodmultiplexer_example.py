#!/usr/bin/env python
"""methodmultiplexer_example.py
An example of how to create and use MethodMultiplexer.

This example demonstrates:
1. Creating and using MethodMultiplexer for method-based multiplexing with automatic binding
2. Registering methods in the multiplexer
3. Selecting which method to use at runtime
"""


# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.functions import FunctionRegistry, MethodMultiplexer


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


class MethodProcessor:
    """A class that uses MethodMultiplexer to process operations.

    This class demonstrates how MethodMultiplexer can be used to select
    between different methods at runtime.
    """

    def __init__(self, name: str) -> None:
        """Initialize the processor with a name.

        Args:
            name: The name of the processor.
        """
        self.name = name

        # Create instances of operation classes
        self.math_ops = MathOperations()
        self.string_ops = StringOperations()

        # Create a registry for our methods
        self.registry = FunctionRegistry()

        # Add methods to the registry
        self.registry["add"] = self.math_ops.add
        self.registry["subtract"] = self.math_ops.subtract
        self.registry["uppercase"] = self.string_ops.uppercase
        self.registry["lowercase"] = self.string_ops.lowercase

        # Create a MethodMultiplexer with our registry
        # The instance parameter is important for method binding
        self.multiplexer = MethodMultiplexer(registry=self.registry, instance=self)

        # Default to the add operation
        self.multiplexer.select("add")

    def process(self, *args: Any, **kwargs: Any) -> Any:
        """Process the input using the currently selected method.

        Args:
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            The result of the method.
        """
        return self.multiplexer(*args, **kwargs)

    def set_operation(self, operation_name: str) -> None:
        """Set the operation to use for processing.

        Args:
            operation_name: The name of the operation to use.

        Raises:
            KeyError: If the operation is not in the registry.
        """
        if operation_name not in self.registry:
            raise KeyError(f"Operation '{operation_name}' not found in registry")

        self.multiplexer.select(operation_name)


# Functions #
def method_processor_example():
    """Demonstrates using MethodMultiplexer in a practical application."""
    print("MethodProcessor Example:\n")

    # Create a processor
    processor = MethodProcessor("Method Processor")

    # Process some data with the default operation (add)
    a, b = 10, 5
    result = processor.process(a, b)
    print(f"Processing with default operation 'add':")
    print(f"processor.process({a}, {b}) = {result}")

    # Change the operation and process again
    processor.set_operation("subtract")
    result = processor.process(a, b)
    print(f"\nChanged operation to 'subtract':")
    print(f"processor.process({a}, {b}) = {result}")

    # Try a string operation
    text = "HELLO WORLD"
    processor.set_operation("lowercase")
    result = processor.process(text)
    print(f"\nChanged operation to 'lowercase':")
    print(f"processor.process('{text}') = '{result}'")

    print()


def dynamic_method_multiplexer_example():
    """Demonstrates MethodMultiplexer's ability to dynamically select methods from the instance it wraps.

    This example highlights how MethodMultiplexer can directly access and bind methods from the wrapped
    instance without needing to add them to a registry first.
    """
    print("Dynamic Method Selection with MethodMultiplexer:\n")

    # Create a class with various methods that we'll dynamically select between
    class DataProcessor:
        def __init__(self, name):
            self.name = name
            self.data = {"numbers": [1, 2, 3, 4, 5], "text": "Hello World", "mixed": [10, "abc", 30, "xyz"]}

            # Create a MethodMultiplexer that wraps this instance
            # Note: We don't provide a registry - we'll select methods directly from the instance
            self.method_selector = MethodMultiplexer(instance=self)

            # Set a default method
            self.method_selector.select("sum_numbers")

        # Define various processing methods that we'll select between
        def sum_numbers(self):
            """Sum all numbers in the numbers list."""
            return sum(self.data["numbers"])

        def average_numbers(self):
            """Calculate the average of numbers in the numbers list."""
            numbers = self.data["numbers"]
            return sum(numbers) / len(numbers)

        def reverse_text(self):
            """Reverse the text string."""
            return self.data["text"][::-1]

        def uppercase_text(self):
            """Convert the text to uppercase."""
            return self.data["text"].upper()

        def extract_numbers(self):
            """Extract only the numbers from the mixed list."""
            return [item for item in self.data["mixed"] if isinstance(item, int)]

        def extract_strings(self):
            """Extract only the strings from the mixed list."""
            return [item for item in self.data["mixed"] if isinstance(item, str)]

        # Method to add new data
        def add_number(self, number):
            """Add a number to the numbers list."""
            self.data["numbers"].append(number)
            return self.data["numbers"]

        # Method to process using the currently selected method
        def process(self):
            """Process data using the currently selected method."""
            return self.method_selector()

        # Method to change the selected method
        def set_processor(self, method_name):
            """Change the processing method.

            Args:
                method_name: Name of the method to select.
            """
            self.method_selector.select(method_name)
            return f"Selected method: {method_name}"

    # Create an instance of our processor
    processor = DataProcessor("Dynamic Method Processor")

    # Show initial data
    print(f"Initial data:")
    print(f"Numbers: {processor.data['numbers']}")
    print(f"Text: '{processor.data['text']}'")
    print(f"Mixed: {processor.data['mixed']}")

    # Process with the default method (sum_numbers)
    result = processor.process()
    print(f"\nUsing default method 'sum_numbers':")
    print(f"processor.process() = {result}")

    # Change to a different method and process again
    processor.set_processor("average_numbers")
    result = processor.process()
    print(f"\nChanged to method 'average_numbers':")
    print(f"processor.process() = {result}")

    # Try a text processing method
    processor.set_processor("uppercase_text")
    result = processor.process()
    print(f"\nChanged to method 'uppercase_text':")
    print(f"processor.process() = '{result}'")

    # Try a method that processes the mixed data
    processor.set_processor("extract_numbers")
    result = processor.process()
    print(f"\nChanged to method 'extract_numbers':")
    print(f"processor.process() = {result}")

    # Add a new number using the method_selector directly
    processor.method_selector.select("add_number")
    result = processor.method_selector(10)  # Call with an argument
    print(f"\nCalling 'add_number' with argument 10:")
    print(f"processor.method_selector(10) = {result}")

    # Now the sum should be different
    processor.set_processor("sum_numbers")
    result = processor.process()
    print(f"\nBack to 'sum_numbers' after adding a number:")
    print(f"processor.process() = {result}")

    # Try a method that doesn't exist in the registry but exists in the instance
    processor.set_processor("extract_strings")
    result = processor.process()
    print(f"\nUsing 'extract_strings' method (not in registry, but in instance):")
    print(f"processor.process() = {result}")

    # Demonstrate that we can dynamically add methods to the instance and select them
    print("\nDynamically adding a new method to the instance:")

    # Add a new method to the instance
    def count_items(self):
        """Count the number of items in each data category."""
        return {"numbers": len(self.data["numbers"]), "text": len(self.data["text"]), "mixed": len(self.data["mixed"])}

    # Add the method to the instance
    # Standard Libraries #
    import types

    processor.count_items = types.MethodType(count_items, processor)

    # Select and use the new method
    processor.set_processor("count_items")
    result = processor.process()
    print(f"Added and selected 'count_items' method:")
    print(f"processor.process() = {result}")

    print()


# Main #
if __name__ == "__main__":
    # Using MethodMultiplexer in a practical application
    method_processor_example()

    # Demonstrating dynamic method selection with MethodMultiplexer
    dynamic_method_multiplexer_example()
