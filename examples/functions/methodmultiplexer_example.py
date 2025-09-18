#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""methodmultiplexer_example.py
An example of how to create and use MethodMultiplexer.

This example demonstrates:
1. Creating and using MethodMultiplexer for method-based multiplexing with automatic binding
2. Registering methods in the multiplexer
3. Selecting which method to use at runtime
"""

# Imports #
# Standard Libraries #
from typing import Any, Dict, List, Optional, Tuple

# Third-Party Packages #
from baseobjects.functions import MethodMultiplexer, FunctionRegistry

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


# Main #
if __name__ == "__main__":
    # Using MethodMultiplexer in a practical application
    method_processor_example()
