#!/usr/bin/env python
"""parseparentheses_example.py
An example of how to use the parse_parentheses function.

This example demonstrates:
1. Basic usage of parse_parentheses
2. Parsing nested parentheses
3. Filtering parsed elements
4. Casting parsed elements to different types
5. Handling different input types (str, bytes)
6. Practical applications for parentheses parsing
"""


# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.operations import parse_parentheses

# Example Sections #


def basic_usage_example() -> None:
    """Demonstrates basic usage of parse_parentheses."""
    print("\nBasic parse_parentheses Usage:")

    # Simple expression with parentheses
    expression = "a (b c) d"

    # Parse the expression
    result = parse_parentheses(expression)

    print(f"Expression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['a', ['b', 'c'], 'd']")

    # Another simple example
    expression = "function(arg1, arg2)"
    result = parse_parentheses(expression)

    print(f"\nExpression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['function', ['arg1', 'arg2']]")


def nested_parentheses_example() -> None:
    """Demonstrates parsing expressions with nested parentheses."""
    print("\nNested Parentheses Example:")

    # Expression with nested parentheses
    expression = "a (b (c d) e) f"

    # Parse the expression
    result = parse_parentheses(expression)

    print(f"Expression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['a', ['b', ['c', 'd'], 'e'], 'f']")

    # More complex nested expression
    expression = "function(arg1, nested_func(arg2, arg3), arg4)"
    result = parse_parentheses(expression)

    print(f"\nExpression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['function', ['arg1', 'nested_func', ['arg2', 'arg3'], 'arg4']]")

    # Deeply nested expression
    expression = "a (b (c (d (e))))"
    result = parse_parentheses(expression)

    print(f"\nExpression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['a', ['b', ['c', ['d', ['e']]]]]")


def filtering_example() -> None:
    """Demonstrates filtering parsed elements."""
    print("\nFiltering Example:")

    # Expression with various elements
    expression = "function(arg1, 123, 'string', True)"

    # Parse with include filter (only include certain elements)
    include_set = {"function", "arg1", "True"}
    result_include = parse_parentheses(expression, include=include_set)

    print(f"Expression: '{expression}'")
    print(f"Include set: {include_set}")
    print(f"Parsed result with include filter: {result_include}")
    print("Expected: ['function', ['arg1', 'True']]")

    # Parse with exclude filter (exclude certain elements)
    exclude_set = {"123", "string"}
    result_exclude = parse_parentheses(expression, exclude=exclude_set)

    print(f"\nExpression: '{expression}'")
    print(f"Exclude set: {exclude_set}")
    print(f"Parsed result with exclude filter: {result_exclude}")
    print("Expected: ['function', ['arg1', 'True']]")

    # Combine include and exclude filters
    include_set = {"function", "arg1", "123", "True"}
    exclude_set = {"123"}
    result_combined = parse_parentheses(expression, include=include_set, exclude=exclude_set)

    print(f"\nExpression: '{expression}'")
    print(f"Include set: {include_set}")
    print(f"Exclude set: {exclude_set}")
    print(f"Parsed result with combined filters: {result_combined}")
    print("Expected: ['function', ['arg1', 'True']]")


def casting_example() -> None:
    """Demonstrates casting parsed elements to different types."""
    print("\nCasting Example:")

    # Expression with numeric values
    expression = "calculate(1, 2, 3, 4)"

    # Defines a cast function to convert strings to integers where possible
    def cast_to_int(s: str) -> int | str:
        try:
            return int(s)
        except ValueError:
            return s

    # Parse with casting
    result = parse_parentheses(expression, cast=cast_to_int)

    print(f"Expression: '{expression}'")
    print(f"Parsed result with int casting: {result}")
    print("Expected: ['calculate', [1, 2, 3, 4]]")

    # Expression with mixed types
    expression = "mixed(1, 2.5, 'text', True)"

    # Defines a more complex cast function
    def smart_cast(s: str) -> int | float | bool | str:
        s = s.strip()
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                if s.lower() == "true":
                    return True
                elif s.lower() == "false":
                    return False
                else:
                    return s

    # Parse with smart casting
    result = parse_parentheses(expression, cast=smart_cast)

    print(f"\nExpression: '{expression}'")
    print(f"Parsed result with smart casting: {result}")
    print("Expected: ['mixed', [1, 2.5, 'text', True]]")


def different_input_types_example() -> None:
    """Demonstrates parsing different input types."""
    print("\nDifferent Input Types Example:")

    # String input (default)
    str_expression = "function(arg1, arg2)"
    str_result = parse_parentheses(str_expression)

    print(f"String expression: '{str_expression}'")
    print(f"Parsed result: {str_result}")
    print("Expected: ['function', ['arg1', 'arg2']]")

    # Bytes input
    bytes_expression = b"function(arg1, arg2)"
    bytes_result = parse_parentheses(bytes_expression)

    print(f"\nBytes expression: {bytes_expression!r}")
    print(f"Parsed result: {bytes_result}")
    print("Expected: [b'function', [b'arg1', b'arg2']]")

    # Bytearray input
    bytearray_expression = bytearray(b"function(arg1, arg2)")
    bytearray_result = parse_parentheses(bytearray_expression)

    print(f"\nBytearray expression: {bytearray_expression}")
    print(f"Parsed result: {bytearray_result}")
    print("Expected: [b'function', [b'arg1', b'arg2']]")


def error_handling_example() -> None:
    """Demonstrates error handling with parse_parentheses."""
    print("\nError Handling Example:")

    # Unbalanced parentheses (missing closing parenthesis)
    unbalanced_expression = "function(arg1, arg2"

    print(f"Unbalanced expression (missing closing parenthesis): '{unbalanced_expression}'")
    try:
        result = parse_parentheses(unbalanced_expression)
        print(f"Parsed result: {result}")
    except ValueError as e:
        print(f"ValueError: {e}")
        print("Expected: ValueError about unbalanced parentheses")

    # Unbalanced parentheses (extra closing parenthesis)
    unbalanced_expression = "function(arg1, arg2))"

    print(f"\nUnbalanced expression (extra closing parenthesis): '{unbalanced_expression}'")
    try:
        result = parse_parentheses(unbalanced_expression)
        print(f"Parsed result: {result}")
    except ValueError as e:
        print(f"ValueError: {e}")
        print("Expected: ValueError about unbalanced parentheses")

    # Invalid input type
    invalid_input = 123

    print(f"\nInvalid input type (int): {invalid_input}")
    try:
        result = parse_parentheses(invalid_input)
        print(f"Parsed result: {result}")
    except ValueError as e:
        print(f"ValueError: {e}")
        print("Expected: ValueError about unsupported input type")


def quoted_strings_example() -> None:
    """Demonstrates handling quoted strings in expressions."""
    print("\nQuoted Strings Example:")

    # Expression with quoted strings
    expression = "function(\"quoted string\", 'another quoted string')"

    # Parse the expression
    result = parse_parentheses(expression)

    print(f"Expression: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['function', ['\"quoted string\"', \"'another quoted string'\"]]")

    # Expression with escaped quotes
    expression = 'function("string with \\"escaped\\" quotes")'

    # Parse the expression
    result = parse_parentheses(expression)

    print(f"\nExpression with escaped quotes: '{expression}'")
    print(f"Parsed result: {result}")
    print("Expected: ['function', ['\"string with \\\"escaped\\\" quotes\"']]")


def practical_example() -> None:
    """Demonstrates a practical use case for parse_parentheses."""
    print("\nPractical Example - Simple Expression Evaluator:")

    # Defines a simple expression evaluator
    def evaluate_expression(expr: str) -> float:
        # Parse the expression
        parsed = parse_parentheses(expr)

        # Evaluate the parsed expression
        return float(evaluate_parsed(parsed))

    def evaluate_parsed(parsed: Any) -> float:
        if not parsed:
            return 0.0

        if isinstance(parsed, list):
            if not parsed:
                return 0.0

            # If it's a list, evaluate it recursively
            if len(parsed) == 1 and isinstance(parsed[0], (int, float, str)):
                # Single value in list
                return evaluate_parsed(parsed[0])

            # Operator handling
            op = parsed[0]
            if op == "+":
                return float(sum(evaluate_parsed(item) for item in parsed[1:]))
            elif op == "*":
                result: float = 1.0
                for item in parsed[1:]:
                    result *= evaluate_parsed(item)
                return result
            elif op == "-":
                if len(parsed) == 2:
                    return -evaluate_parsed(parsed[1])
                elif len(parsed) > 2:
                    return evaluate_parsed(parsed[1]) - float(sum(evaluate_parsed(item) for item in parsed[2:]))
                else:
                    return 0.0
            elif op == "/":
                if len(parsed) < 3:
                    return 1.0
                div_result: float = evaluate_parsed(parsed[1])
                for item in parsed[2:]:
                    val = evaluate_parsed(item)
                    if val != 0:
                        div_result /= val
                return div_result

            # If the first element is a list, evaluate it
            if isinstance(op, list):
                return evaluate_parsed(op)

        # If it's a number (as a string or number), convert it
        try:
            return float(parsed)
        except (ValueError, TypeError):
            pass

        return 0.0

    # Test the evaluator with some expressions
    expressions = [
        "(+ 1 2 3)",
        "(* 2 3 4)",
        "(- 10 5 2)",
        "(/ 20 2 2)",
        "(+ 1 (* 2 3) (- 10 5))",
        "(* (+ 1 2) (- 10 5))",
    ]

    for expr in expressions:
        result = evaluate_expression(expr)
        print(f"Expression: '{expr}'")
        print(f"Evaluated result: {result}")

        # Calculates expected result for verification
        expected: float | str
        if expr == "(+ 1 2 3)":
            expected = 1 + 2 + 3
        elif expr == "(* 2 3 4)":
            expected = 2 * 3 * 4
        elif expr == "(- 10 5 2)":
            expected = 10 - 5 - 2
        elif expr == "(/ 20 2 2)":
            expected = 20 / 2 / 2
        elif expr == "(+ 1 (* 2 3) (- 10 5))":
            expected = 1 + (2 * 3) + (10 - 5)
        elif expr == "(* (+ 1 2) (- 10 5))":
            expected = (1 + 2) * (10 - 5)
        else:
            expected = "unknown"

        print(f"Expected: {expected}")
        print()


# Main #
if __name__ == "__main__":
    # Runs examples
    basic_usage_example()
    nested_parentheses_example()
    filtering_example()
    casting_example()
    different_input_types_example()
    error_handling_example()
    quoted_strings_example()
    practical_example()
