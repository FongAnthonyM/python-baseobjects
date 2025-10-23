#!/usr/bin/env python
"""parse_parenthese_test.py
Tests for the parse_parentheses function in the baseobjects package.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations import parse_parentheses


# Definitions #
# Classes #
class TestParseParentheses:
    """Test the parse_parentheses function.

    This class tests the functionality of the parse_parentheses function, which parses expressions with parentheses and
    returns a nested list of extracted elements.
    """

    # Instance Methods #
    # Tests
    def test_string_parse_parentheses(self) -> None:
        """Test parsing a string expression with parentheses.

        This test verifies that the parse_parentheses function correctly parses a string expression with nested
        parentheses into a structured list format.
        """
        string = "((first(inner))(second)(wrong(thing)))"
        result = parse_parentheses(string)

        # Expected structure: [[[['first', ['inner']], ['second'], ['wrong', ['thing']]]]]
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == 3

        # Check first element: ['first', ['inner']]
        assert isinstance(result[0][0], list)
        assert len(result[0][0]) == 2
        assert result[0][0][0] == "first"
        assert isinstance(result[0][0][1], list)
        assert result[0][0][1][0] == "inner"

        # Check second element: ['second']
        assert isinstance(result[0][1], list)
        assert len(result[0][1]) == 1
        assert result[0][1][0] == "second"

        # Check third element: ['wrong', ['thing']]
        assert isinstance(result[0][2], list)
        assert len(result[0][2]) == 2
        assert result[0][2][0] == "wrong"
        assert isinstance(result[0][2][1], list)
        assert result[0][2][1][0] == "thing"

    def test_bytes_parse_parentheses(self) -> None:
        """Test parsing a bytes expression with parentheses.

        This test verifies that the parse_parentheses function correctly parses a bytes expression with nested
        parentheses into a structured list format.
        """
        bytes_expr = b"((first\xff(inner'('))(second)(wrong(thing)))"
        result = parse_parentheses(bytes_expr)

        # Verify the structure is as expected
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == 3

        # Check first element
        assert isinstance(result[0][0], list)
        assert len(result[0][0]) >= 1

        # Check second element
        assert isinstance(result[0][1], list)
        assert len(result[0][1]) == 1
        assert result[0][1][0] == b"second"

        # Check third element
        assert isinstance(result[0][2], list)
        assert len(result[0][2]) == 2
        assert result[0][2][0] == b"wrong"
        assert isinstance(result[0][2][1], list)
        assert result[0][2][1][0] == b"thing"

    def test_unbalanced_parentheses(self) -> None:
        """Test parsing an expression with unbalanced parentheses.

        This test verifies that the parse_parentheses function raises a ValueError when parsing an expression with
        unbalanced parentheses.
        """
        # Test with unmatched opening parenthesis
        with pytest.raises(ValueError, match="Unbalanced parentheses"):
            parse_parentheses("(test")

        # Test with unmatched closing parenthesis
        with pytest.raises(ValueError, match="Unbalanced parentheses"):
            parse_parentheses("test)")

    def test_filtering(self) -> None:
        """Test filtering elements during parsing.

        This test verifies that the parse_parentheses function correctly filters elements based on the include and
        exclude parameters.
        """
        string = "(first(inner))(second)(third)"

        # Test with include set
        include_result = parse_parentheses(string, include={"first", "third"})
        assert "first" in str(include_result)
        assert "third" in str(include_result)
        assert "second" not in str(include_result)

        # Test with exclude set
        exclude_result = parse_parentheses(string, exclude={"second"})
        assert "first" in str(exclude_result)
        assert "third" in str(exclude_result)
        assert "second" not in str(exclude_result)

    def test_casting(self) -> None:
        """Test casting elements during parsing.

        This test verifies that the parse_parentheses function correctly applies the casting function to transform
        elements.
        """
        string = "(123)(456)(789)"

        # Define a casting function to convert strings to integers
        def cast_to_int(s: str) -> int:
            return int(s)

        result = parse_parentheses(string, cast=cast_to_int)

        # Verify that elements were cast to integers
        for sublist in result:
            assert isinstance(sublist[0], int)

        # Verify specific values
        assert 123 in [sublist[0] for sublist in result]
        assert 456 in [sublist[0] for sublist in result]
        assert 789 in [sublist[0] for sublist in result]

    def test_empty_expression(self) -> None:
        """Test parsing an empty expression.

        This test verifies that the parse_parentheses function correctly handles empty expressions.
        """
        # Test with an empty string
        result = parse_parentheses("")
        assert result == []

        # Test with a string containing only whitespace
        result = parse_parentheses("   ")
        assert result == []

    def test_nested_empty_parentheses(self) -> None:
        """Test parsing expressions with nested empty parentheses.

        This test verifies that the parse_parentheses function correctly handles expressions with nested empty
        parentheses.
        """
        # Test with empty parentheses
        result = parse_parentheses("()")
        assert result == [[]]

        # Test with nested empty parentheses
        result = parse_parentheses("(())")
        assert result == [[[]]]

        # Test with multiple empty parentheses
        result = parse_parentheses("()()()")
        assert result == [[], [], []]

        # Test with a mix of empty and non-empty parentheses
        result = parse_parentheses("(test)()(nested())")
        assert result[0][0] == "test"
        assert result[1] == []
        assert result[2][0] == "nested"
        assert result[2][1] == []

    # This would be useful for parsing expressions with different types of parentheses, but it's not currently
    # supported.
    # def test_different_parentheses_types(self) -> None:
    #     """Test parsing expressions with different types of parentheses.
    #
    #     This test verifies that the parse_parentheses function correctly handles expressions with different types of
    #     parentheses when custom open and close characters are specified.
    #     """
    #     # Test with square brackets
    #     result = parse_parentheses("[test][nested[inner]]", open_char="[", close_char="]")
    #     assert result[0][0] == "test"
    #     assert result[1][0] == "nested"
    #     assert result[1][1][0] == "inner"
    #
    #     # Test with curly braces
    #     result = parse_parentheses("{test}{nested{inner}}", open_char="{", close_char="}")
    #     assert result[0][0] == "test"
    #     assert result[1][0] == "nested"
    #     assert result[1][1][0] == "inner"
    #
    #     # Test with angle brackets
    #     result = parse_parentheses("<test><nested<inner>>", open_char="<", close_char=">")
    #     assert result[0][0] == "test"
    #     assert result[1][0] == "nested"
    #     assert result[1][1][0] == "inner"
    #
    # def test_escaped_parentheses(self) -> None:
    #     """Test parsing expressions with escaped parentheses.
    #
    #     This test verifies that the parse_parentheses function correctly handles expressions with escaped parentheses
    #     when an escape character is specified.
    #     """
    #     # Test with escaped parentheses
    #     result = parse_parentheses(r"(test\(\))(normal)", escape_char="\\")
    #     assert result[0][0] == r"test\(\)"
    #     assert result[1][0] == "normal"
    #
    #     # Test with escaped escape character
    #     result = parse_parentheses(r"(test\\)(normal)", escape_char="\\")
    #     assert result[0][0] == r"test\\"
    #     assert result[1][0] == "normal"
    #
    # def test_custom_delimiters(self) -> None:
    # """Test parsing with custom delimiters.
    #
    #     This test verifies that the parse_parentheses function correctly handles expressions with custom delimiters.
    #     """
    #     # Test with custom delimiters
    #     result = parse_parentheses("(test,nested,items)", delimiters=",")
    #     assert result[0][0] == "test"
    #     assert result[0][1] == "nested"
    #     assert result[0][2] == "items"
    #
    #     # Test with multiple custom delimiters
    #     result = parse_parentheses("(test,nested;items)", delimiters=",;")
    #     assert result[0][0] == "test"
    #     assert result[0][1] == "nested"
    #     assert result[0][2] == "items"

    def test_large_expression(self) -> None:
        """Test parsing a very large expression.

        This test verifies that the parse_parentheses function can handle large expressions without performance issues.
        """
        # Create a large expression with many nested parentheses
        large_expr = "(" * 100 + "test" + ")" * 100

        # Parse the large expression
        result = parse_parentheses(large_expr)

        # Verify the result has the expected structure
        assert len(result) == 1
        current = result
        for _ in range(100):
            current = current[0]
        assert current[0] == "test"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
