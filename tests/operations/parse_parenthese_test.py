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
from typing import Any

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Source Packages #
from baseobjects.operations import parse_parentheses


# Definitions #
# Classes #
class TestParseParentheses:
    """Tests the parse_parentheses function.

    This class tests the functionality of the parse_parentheses function, which parses expressions with parentheses and
    returns a nested list of extracted elements.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("text", "expected_structure"),
        [
            ("((first(inner))(second)(wrong(thing)))", ["first", "inner", "second", "wrong", "thing"]),
            (
                b"((first\xff(inner'('))(second)(wrong(thing)))",
                [b"first\xff", b"inner'('", b"second", b"wrong", b"thing"],
            ),
        ],
    )
    def test_parse_parentheses_structure(self, text: str | bytes, expected_structure: list[Any]) -> None:
        """Tests parsing expression with nested parentheses.

        This test verifies that the parse_parentheses function correctly parses expressions with nested parentheses
        into a structured list format for both string and bytes.
        """
        result = parse_parentheses(text)

        # Basic structure verification (length and type)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == 3

        # Check first element
        assert isinstance(result[0][0], list)
        # Check second element
        assert isinstance(result[0][1], list)
        # Check third element
        assert isinstance(result[0][2], list)

        if isinstance(text, str):
            assert result[0][1][0] == "second"
            assert result[0][2][0] == "wrong"
        else:
            assert result[0][1][0] == b"second"
            assert result[0][2][0] == b"wrong"

    @pytest.mark.parametrize(
        ("invalid_input", "error_match"),
        [
            ("(test", "Unbalanced parentheses"),
            ("test)", "Unbalanced parentheses"),
            ("))", "Unbalanced parentheses"),
            ("(", "Unbalanced parentheses"),
            (b"))", "Unbalanced parentheses"),
            (b"(", "Unbalanced parentheses"),
        ],
    )
    def test_unbalanced_parentheses(self, invalid_input: Any, error_match: str) -> None:
        """Tests parsing an expression with unbalanced parentheses.

        This test verifies that the parse_parentheses function raises a ValueError when parsing an expression with
        unbalanced parentheses.
        """
        with pytest.raises(ValueError, match=error_match):
            parse_parentheses(invalid_input)

    @pytest.mark.parametrize(
        ("expression", "expected"),
        [
            ("", []),
            ("   ", []),
            ("()", [[]]),
            ("(())", [[[]]]),
            ("()()()", [[], [], []]),
        ],
    )
    def test_empty_parentheses(self, expression: str, expected: list[Any]) -> None:
        """Tests parsing empty expressions and empty parentheses.

        This test verifies that the parse_parentheses function correctly handles empty expressions and nested empty
        parentheses.
        """
        result = parse_parentheses(expression)
        assert result == expected

    def test_nested_mixed_empty_parentheses(self) -> None:
        """Tests parsing expressions with a mix of empty and non-empty parentheses."""
        result = parse_parentheses("(test)()(nested())")
        assert result[0][0] == "test"
        assert result[1] == []
        assert result[2][0] == "nested"
        assert result[2][1] == []

    def test_parse_parentheses_unsupported_type(self) -> None:
        """Tests that parse_parentheses raises ValueError for unsupported types."""
        with pytest.raises((ValueError, TypeCheckError)):
            parse_parentheses(123)

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("start (middle) end", ["start", ["middle"], "end"]),
            ("no parentheses", ["no", "parentheses"]),
            ("start (middle (inner)) end", ["start", ["middle", ["inner"]], "end"]),
            ("start (first) middle (second) end", ["start", ["first"], "middle", ["second"], "end"]),
        ],
    )
    def test_basic_parsing_scenarios(self, text: str, expected: list[Any]) -> None:
        """Tests parsing basic string scenarios.

        This test verifies that the parse_parentheses function correctly parses strings with various parentheses
        configurations.
        """
        result = parse_parentheses(text)
        assert result == expected

    @pytest.mark.parametrize(
        ("text", "include", "exclude", "check_in", "check_not_in"),
        [
            ("(first(inner))(second)(third)", {"first", "third"}, None, ["first", "third"], ["second"]),
            ("(first(inner))(second)(third)", None, {"second"}, ["first", "third"], ["second"]),
            (b"foo bar", {b"bar"}, None, [b"bar"], [b"foo"]),
            (b"foo bar", None, {b"foo"}, [b"bar"], [b"foo"]),
        ],
    )
    def test_filtering(
        self,
        text: Any,
        include: set[Any] | None,
        exclude: set[Any] | None,
        check_in: list[Any],
        check_not_in: list[Any],
    ) -> None:
        """Tests filtering elements during parsing.

        This test verifies that the parse_parentheses function correctly filters elements based on the include and
        exclude parameters for both string and bytes.
        """
        kwargs = {}
        if include is not None:
            kwargs["include"] = include
        if exclude is not None:
            kwargs["exclude"] = exclude

        result = parse_parentheses(text, **kwargs)
        result_str = str(result)

        for item in check_in:
            assert (
                str(item) in result_str
                or (isinstance(item, (str, bytes)) and item in result)
                or (isinstance(result, list) and any(item in x if isinstance(x, list) else item == x for x in result))
            )

        for item in check_in:
            assert (
                str(item) in str(result)
                or (isinstance(item, bytes) and repr(item) in str(result))
                or (isinstance(item, bytes) and item in result)
            )

        for item in check_not_in:
            assert str(item) not in str(result)
            assert not isinstance(item, bytes) or item not in result

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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
