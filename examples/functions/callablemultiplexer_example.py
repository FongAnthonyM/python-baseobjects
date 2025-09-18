#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from typing import Any, Dict, List, Optional, Tuple

# Third-Party Packages #
from baseobjects.functions import CallableMultiplexer, FunctionMultiplexer, MethodMultiplexer, FunctionRegistry

# Local Packages #


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


class OperationsProcessor:
    """A class that uses CallableMultiplexer to process operations.
    
    This class demonstrates how CallableMultiplexer can be used to select
    between different operations at runtime.
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
        
        # Create a registry for our functions
        self.registry = FunctionRegistry()
        
        # Add math operations to the registry
        self.registry["add"] = self.math_ops.add
        self.registry["subtract"] = self.math_ops.subtract
        self.registry["multiply"] = self.math_ops.multiply
        self.registry["divide"] = self.math_ops.divide
        
        # Add string operations to the registry
        self.registry["uppercase"] = self.string_ops.uppercase
        self.registry["lowercase"] = self.string_ops.lowercase
        self.registry["capitalize"] = self.string_ops.capitalize
        self.registry["reverse"] = self.string_ops.reverse
        
        # Create a CallableMultiplexer with our registry
        self.multiplexer = CallableMultiplexer(registry=self.registry, instance=self)
        
        # Default to the add operation
        self.multiplexer.select("add")
    
    def process(self, *args: Any, **kwargs: Any) -> Any:
        """Process the input using the currently selected operation.
        
        Args:
            *args: Positional arguments for the operation.
            **kwargs: Keyword arguments for the operation.
            
        Returns:
            The result of the operation.
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
    
    def get_current_operation(self) -> str:
        """Get the name of the currently selected operation.
        
        Returns:
            The name of the currently selected operation.
        """
        return self.multiplexer.selected
    
    def list_operations(self) -> List[str]:
        """List all available operations.
        
        Returns:
            A list of operation names.
        """
        return list(self.registry.keys())



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
    registry["power"] = lambda a, b: a ** b
    multiplexer.select("power")
    result = multiplexer(a, b)
    print(f"\nAdded and selected function: 'power'")
    print(f"multiplexer({a}, {b}) = {result}")
    
    # Add and select a function in one step
    multiplexer.add_select_function("divide", lambda a, b: a / b if b != 0 else float('inf'))
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


def operations_processor_example():
    """Demonstrates using CallableMultiplexer in a practical application."""
    print("OperationsProcessor Example:\n")
    
    # Create a processor
    processor = OperationsProcessor("Math and String Processor")
    
    # Show available operations
    print(f"Available operations: {processor.list_operations()}")
    print(f"Current operation: {processor.get_current_operation()}")
    
    # Process some data with the default operation (add)
    a, b = 10, 5
    result = processor.process(a, b)
    print(f"\nProcessing with default operation 'add':")
    print(f"processor.process({a}, {b}) = {result}")
    
    # Change the operation and process again
    processor.set_operation("multiply")
    result = processor.process(a, b)
    print(f"\nChanged operation to 'multiply':")
    print(f"processor.process({a}, {b}) = {result}")
    
    # Try a string operation
    text = "hello world"
    processor.set_operation("uppercase")
    result = processor.process(text)
    print(f"\nChanged operation to 'uppercase':")
    print(f"processor.process('{text}') = '{result}'")
    
    # Try another string operation
    processor.set_operation("capitalize")
    result = processor.process(text)
    print(f"\nChanged operation to 'capitalize':")
    print(f"processor.process('{text}') = '{result}'")
    
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
            self.data = {
                "numbers": [1, 2, 3, 4, 5],
                "text": "Hello World",
                "mixed": [10, "abc", 30, "xyz"]
            }
            
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
        return {
            "numbers": len(self.data["numbers"]),
            "text": len(self.data["text"]),
            "mixed": len(self.data["mixed"])
        }
    
    # Add the method to the instance
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
    # Basic usage of CallableMultiplexer
    basic_callable_multiplexer()
    
    # Compare the different multiplexer types
    multiplexer_types_comparison()
    
    # Using CallableMultiplexer in a practical application
    operations_processor_example()
    
    # Demonstrating dynamic method selection with CallableMultiplexer
    dynamic_method_selection()
    
    # Demonstrating dynamic method selection with MethodMultiplexer
    dynamic_method_multiplexer_example()
