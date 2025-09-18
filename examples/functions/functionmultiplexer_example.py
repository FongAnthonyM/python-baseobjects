#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""functionmultiplexer_example.py
An example of how to create and use FunctionMultiplexer.

This example demonstrates:
1. Creating and using FunctionMultiplexer for function-based multiplexing
2. Registering functions in the multiplexer
3. Selecting which function to use at runtime
"""

# Imports #
# Standard Libraries #
from typing import Any, Dict, List, Optional, Tuple

# Third-Party Packages #
from baseobjects.functions import FunctionMultiplexer, FunctionRegistry

# Local Packages #


# Definitions #
# Classes #
class FunctionProcessor:
    """A class that uses FunctionMultiplexer to process operations.
    
    This class demonstrates how FunctionMultiplexer can be used to select
    between different functions at runtime.
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the processor with a name.
        
        Args:
            name: The name of the processor.
        """
        self.name = name
        
        # Create a registry for our functions
        self.registry = FunctionRegistry()
        
        # Add standalone functions to the registry
        self.registry["add"] = lambda a, b: a + b
        self.registry["subtract"] = lambda a, b: a - b
        self.registry["multiply"] = lambda a, b: a * b
        self.registry["divide"] = lambda a, b: a / b if b != 0 else float('inf')
        
        # Create a FunctionMultiplexer with our registry
        self.multiplexer = FunctionMultiplexer(registry=self.registry)
        
        # Default to the add operation
        self.multiplexer.select("add")
    
    def process(self, *args: Any, **kwargs: Any) -> Any:
        """Process the input using the currently selected function.
        
        Args:
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
            
        Returns:
            The result of the function.
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
def function_processor_example():
    """Demonstrates using FunctionMultiplexer in a practical application."""
    print("FunctionProcessor Example:\n")
    
    # Create a processor
    processor = FunctionProcessor("Function Processor")
    
    # Process some data with the default operation (add)
    a, b = 10, 5
    result = processor.process(a, b)
    print(f"Processing with default operation 'add':")
    print(f"processor.process({a}, {b}) = {result}")
    
    # Change the operation and process again
    processor.set_operation("multiply")
    result = processor.process(a, b)
    print(f"\nChanged operation to 'multiply':")
    print(f"processor.process({a}, {b}) = {result}")
    
    # Try division with zero
    processor.set_operation("divide")
    result = processor.process(a, 0)
    print(f"\nTrying division by zero:")
    print(f"processor.process({a}, 0) = {result}")
    
    print()


# Main #
if __name__ == "__main__":
    # Using FunctionMultiplexer in a practical application
    function_processor_example()
