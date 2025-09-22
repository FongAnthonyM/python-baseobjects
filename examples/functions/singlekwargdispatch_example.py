#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""singlekwargdispatch_example.py
An example of how to create and use singlekwargdispatch.

This example demonstrates:
1. Basic usage of singlekwargdispatch
2. Positional dispatching based on the type of the first argument
3. Keyword dispatching based on a specific keyword argument
4. Flexible keyword dispatching where the dispatching keyword is not the first argument
5. Registering multiple implementations for different types
6. Using singlekwargdispatch to wrap standalone functions
"""

# Imports #
# Standard Libraries #
from typing import Any, Dict, List, Union

# Third-Party Packages #
from baseobjects.functions import singlekwargdispatch

# Local Packages #


# Definitions #
# Standalone Functions with singlekwargdispatch #
@singlekwargdispatch
def convert_value(value: Any) -> str:
    """Convert a value to a string representation.

    This is the default implementation that converts any value to a string.

    Args:
        value: The value to convert.

    Returns:
        The string representation of the value.
    """
    return f"Default: {str(value)}"


@convert_value.register
def _(value: int) -> str:
    """Convert an integer to a string representation.

    Args:
        value: The integer to convert.

    Returns:
        The string representation of the integer.
    """
    return f"Integer: {value} (hex: {hex(value)})"


@convert_value.register
def _(value: float) -> str:
    """Convert a float to a string representation.

    Args:
        value: The float to convert.

    Returns:
        The string representation of the float.
    """
    return f"Float: {value:.4f} (scientific: {value:.2e})"


@convert_value.register
def _(value: str) -> str:
    """Convert a string to a formatted representation.

    Args:
        value: The string to convert.

    Returns:
        The formatted representation of the string.
    """
    return f"String: '{value}' (length: {len(value)})"


@convert_value.register(tuple)
@convert_value.register(list)
def _(value) -> str:
    """Convert a list to a string representation.

    Args:
        value: The list to convert.

    Returns:
        The string representation of the list.
    """
    return f"List: {value} (length: {len(value)}, sum: {sum(value) if all(isinstance(x, (int, float)) for x in value) else 'N/A'})"


@singlekwargdispatch(kwarg="format_as")
def format_data(data: Any, format_as: Any = None, precision: int = 2) -> str:
    """Format data based on the format_as parameter.

    This is the default implementation that returns a simple string representation.

    Args:
        data: The data to format.
        format_as: The type to format the data as.
        precision: The precision for numeric formatting.

    Returns:
        The formatted data as a string.
    """
    return f"Data: {data} (default format, precision: {precision})"


@format_data.register
def _(data: Any, format_as: str, precision: int = 2) -> str:
    """Format data as a string with specified formatting.

    Args:
        data: The data to format.
        format_as: The string format type.
        precision: The precision for numeric formatting.

    Returns:
        The formatted data as a string.
    """
    if format_as.lower() == "json":
        import json

        try:
            return f"JSON: {json.dumps(data, indent=precision)}"
        except (TypeError, ValueError):
            return f"Cannot convert {type(data).__name__} to JSON"
    elif format_as.lower() == "table":
        if isinstance(data, dict):
            rows = [f"| {k} | {v} |" for k, v in data.items()]
            header = "| Key | Value |"
            separator = "|-----|-------|"
            return "Table:\n" + "\n".join([header, separator] + rows)
        else:
            return f"Cannot format {type(data).__name__} as table"
    else:
        return f"String format: {str(data)}"


@format_data.register
def _(data: Any, format_as: int, precision: int = 2) -> str:
    """Format data with integer formatting options.

    Args:
        data: The data to format.
        format_as: The integer format option (1=decimal, 2=hex, 3=binary).
        precision: The precision for numeric formatting.

    Returns:
        The formatted data as a string.
    """
    if isinstance(data, (int, float)):
        if format_as == 1:
            return f"Decimal: {data:.{precision}f}"
        elif format_as == 2:
            if isinstance(data, int):
                return f"Hexadecimal: {hex(data)}"
            else:
                return f"Hexadecimal: {hex(int(data))}"
        elif format_as == 3:
            if isinstance(data, int):
                return f"Binary: {bin(data)}"
            else:
                return f"Binary: {bin(int(data))}"
        else:
            return f"Unknown format option: {format_as}"
    else:
        return f"Cannot apply numeric formatting to {type(data).__name__}"


# Classes #
class Shape:
    """Base class for shapes."""

    pass


class Circle(Shape):
    """A circle shape."""

    def __init__(self, radius: float):
        """Initialize a circle with a radius.

        Args:
            radius: The radius of the circle.
        """
        self.radius = radius

    def __str__(self) -> str:
        return f"Circle(radius={self.radius})"


class Rectangle(Shape):
    """A rectangle shape."""

    def __init__(self, width: float, height: float):
        """Initialize a rectangle with width and height.

        Args:
            width: The width of the rectangle.
            height: The height of the rectangle.
        """
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"


class Triangle(Shape):
    """A triangle shape."""

    def __init__(self, base: float, height: float):
        """Initialize a triangle with base and height.

        Args:
            base: The base of the triangle.
            height: The height of the triangle.
        """
        self.base = base
        self.height = height

    def __str__(self) -> str:
        return f"Triangle(base={self.base}, height={self.height})"


class ShapeProcessor:
    """A class that processes shapes using singlekwargdispatch."""

    @singlekwargdispatch
    def calculate_area(self, shape: Shape) -> float:
        """Calculate the area of a shape.

        This is the default implementation that raises NotImplementedError.

        Args:
            shape: The shape to calculate the area of.

        Raises:
            NotImplementedError: If the shape type is not supported.
        """
        raise NotImplementedError(f"Area calculation not implemented for {type(shape).__name__}")

    @calculate_area.register
    def _(self, shape: Circle) -> float:
        """Calculate the area of a circle.

        Args:
            shape: The circle to calculate the area of.

        Returns:
            The area of the circle.
        """
        import math

        return math.pi * shape.radius**2

    @calculate_area.register
    def _(self, shape: Rectangle) -> float:
        """Calculate the area of a rectangle.

        Args:
            shape: The rectangle to calculate the area of.

        Returns:
            The area of the rectangle.
        """
        return shape.width * shape.height

    @calculate_area.register
    def _(self, shape: Triangle) -> float:
        """Calculate the area of a triangle.

        Args:
            shape: The triangle to calculate the area of.

        Returns:
            The area of the triangle.
        """
        return 0.5 * shape.base * shape.height


class DataProcessor:
    """A class that processes data using singlekwargdispatch with keyword arguments."""

    @singlekwargdispatch(kwarg="data")
    def process(self, prefix: str, data: Any) -> str:
        """Process data based on its type.

        This is the default implementation that converts the data to a string.

        Args:
            prefix: A prefix to add to the processed data.
            data: The data to process.

        Returns:
            The processed data as a string.
        """
        return f"{prefix}: {str(data)}"

    @process.register
    def _(self, prefix: str, data: int) -> str:
        """Process integer data.

        Args:
            prefix: A prefix to add to the processed data.
            data: The integer data to process.

        Returns:
            The processed integer data.
        """
        return f"{prefix}: Integer {data} (squared = {data ** 2})"

    @process.register
    def _(self, prefix: str, data: float) -> str:
        """Process float data.

        Args:
            prefix: A prefix to add to the processed data.
            data: The float data to process.

        Returns:
            The processed float data.
        """
        return f"{prefix}: Float {data:.2f} (doubled = {data * 2:.2f})"

    @process.register
    def _(self, prefix: str, data: str) -> str:
        """Process string data.

        Args:
            prefix: A prefix to add to the processed data.
            data: The string data to process.

        Returns:
            The processed string data.
        """
        return f"{prefix}: String '{data}' (length = {len(data)})"

    @process.register
    def _(self, prefix: str, data: list) -> str:
        """Process list data.

        Args:
            prefix: A prefix to add to the processed data.
            data: The list data to process.

        Returns:
            The processed list data.
        """
        return f"{prefix}: List {data} (length = {len(data)})"

    @process.register
    def _(self, prefix: str, data: dict) -> str:
        """Process dictionary data.

        Args:
            prefix: A prefix to add to the processed data.
            data: The dictionary data to process.

        Returns:
            The processed dictionary data.
        """
        return f"{prefix}: Dict {data} (keys = {list(data.keys())})"


class MultiParameterProcessor:
    """A class that processes data using singlekwargdispatch with multiple parameters."""

    @singlekwargdispatch(kwarg="format_type")
    def format_data(self, value: Any, description: str, format_type: Any) -> str:
        """Format data based on the format_type.

        This is the default implementation that returns a simple string representation.

        Args:
            value: The value to format.
            description: A description of the value.
            format_type: The type of formatting to apply.

        Returns:
            The formatted data as a string.
        """
        return f"{description}: {value} (default format)"

    @format_data.register
    def _(self, value: Any, description: str, format_type: str) -> str:
        """Format data with a string format type.

        Args:
            value: The value to format.
            description: A description of the value.
            format_type: The string format type.

        Returns:
            The formatted data as a string.
        """
        if format_type.lower() == "uppercase":
            return f"{description.upper()}: {str(value).upper()}"
        elif format_type.lower() == "lowercase":
            return f"{description.lower()}: {str(value).lower()}"
        else:
            return f"{description}: {value} (unknown string format: {format_type})"

    @format_data.register
    def _(self, value: Any, description: str, format_type: int) -> str:
        """Format data with an integer format type.

        Args:
            value: The value to format.
            description: A description of the value.
            format_type: The integer format type (specifies padding).

        Returns:
            The formatted data as a string.
        """
        return f"{description.ljust(format_type)}: {value}"

    @format_data.register
    def _(self, value: Any, description: str, format_type: bool) -> str:
        """Format data with a boolean format type.

        Args:
            value: The value to format.
            description: A description of the value.
            format_type: If True, adds extra formatting.

        Returns:
            The formatted data as a string.
        """
        if format_type:
            return f"*** {description} *** : {value}"
        else:
            return f"{description}: {value}"


# Example Sections #
def function_singlekwargdispatch_example():
    """Demonstrates using singlekwargdispatch as a function."""
    print("Dispatching Function Examples:\n")

    # Positional dispatching with functions
    print("Positional function dispatching:")

    # Integer
    result = convert_value(42)
    print(result)

    # Float
    result = convert_value(3.14159)
    print(result)

    # String
    result = convert_value("Hello, world!")
    print(result)

    # Tuple
    result = convert_value((1, 2, 3, 4, 5))
    print(result)

    # List
    result = convert_value([1, 2, 3, 4, 5])
    print(result)

    # Default case (tuple)
    result = convert_value((1, 2, 3))
    print(result)

    # Keyword dispatching with functions
    print("\nKeyword function dispatching:")

    # Default case
    result = format_data(42)
    print(result)

    # String format_as (JSON)
    data = {"name": "John", "age": 30, "city": "New York"}
    result = format_data(data, format_as="json", precision=4)
    print(result)

    # String format_as (Table)
    result = format_data(data, format_as="table")
    print(result)

    # Integer format_as (Decimal)
    result = format_data(42.5678, format_as=1, precision=3)
    print(result)

    # Integer format_as (Hex)
    result = format_data(255, format_as=2)
    print(result)

    # Integer format_as (Binary)
    result = format_data(15, format_as=3)
    print(result)

    # Try with incompatible data type
    result = format_data("not a number", format_as=2)
    print(result)

    print()


def method_singlekwargdispatch_example():
    """Demonstrates usage of singlekwargdispatch as a method."""
    print("Dispatching Method Examples:\n")

    # Positional dispatching with methods
    print("Positional method dispatching:")

    # Create a shape processor
    processor = ShapeProcessor()

    # Create some shapes
    circle = Circle(radius=5)
    rectangle = Rectangle(width=4, height=6)
    triangle = Triangle(base=3, height=8)

    # Calculate areas using positional dispatching
    print("Calculating areas using positional dispatching:")

    # Circle area
    area = processor.calculate_area(circle)
    print(f"Area of {circle} = {area:.2f}")

    # Rectangle area
    area = processor.calculate_area(rectangle)
    print(f"Area of {rectangle} = {area:.2f}")

    # Triangle area
    area = processor.calculate_area(triangle)
    print(f"Area of {triangle} = {area:.2f}")

    # Try with an unsupported shape type
    print("\nTrying with an unsupported shape type:")
    try:
        area = processor.calculate_area(Shape())
        print(f"Area = {area}")
    except NotImplementedError as e:
        print(f"Error: {e}")

    # Keyword dispatching with method
    print("Keyword method dispatching:\n")

    # Create processor

    processor = DataProcessor()

    # Integer
    result = processor.process(prefix="Result", data=42)
    print(result)

    # Float
    result = processor.process(prefix="Result", data=3.14159)
    print(result)

    # String
    result = processor.process(prefix="Result", data="Hello, world!")
    print(result)

    # List
    result = processor.process(prefix="Result", data=[1, 2, 3, 4, 5])
    print(result)

    # Dictionary
    result = processor.process(prefix="Result", data={"name": "John", "age": 30})
    print(result)

    # Default case (tuple)
    result = processor.process(prefix="Result", data=(1, 2, 3))
    print(result)

    print()


def flexible_keyword_dispatching_example():
    """Demonstrates singlekwargdispatch with the dispatching keyword not as the first argument."""
    print("Flexible Keyword Dispatching Example:\n")

    # Create a multi-parameter processor
    processor = MultiParameterProcessor()

    # Process data with different format types
    print("Processing data with different format types:")

    # String format type (uppercase)
    result = processor.format_data(value=42, description="The answer", format_type="uppercase")
    print(result)

    # String format type (lowercase)
    result = processor.format_data(value="Mixed CASE Text", description="Sample Text", format_type="lowercase")
    print(result)

    # Integer format type (padding)
    result = processor.format_data(value=3.14159, description="Pi", format_type=15)
    print(result)

    # Boolean format type (True)
    result = processor.format_data(value="Important information", description="Alert", format_type=True)
    print(result)

    # Boolean format type (False)
    result = processor.format_data(value="Regular information", description="Info", format_type=False)
    print(result)

    # Default case
    result = processor.format_data(value="Some data", description="Data", format_type=None)
    print(result)

    print()


# Main #
if __name__ == "__main__":
    # Using singlekwargdispatch as a function
    function_singlekwargdispatch_example()

    # Using singlekwargdispatch as a method with positional arguments
    method_singlekwargdispatch_example()

    # Using singlekwargdispatch with the dispatching keyword not as the first argument
    flexible_keyword_dispatching_example()
