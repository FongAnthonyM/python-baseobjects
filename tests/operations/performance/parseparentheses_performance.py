#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""parseparentheses_performance.py
Performance tests_old_ for the parse_parentheses function in the baseobjects.operations package.
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
import re
import timeit
from collections import deque
from typing import Any, Callable, List, Set, Union

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.testsuite import BasePerformanceTestSuite
from src.baseobjects.operations import parse_parentheses


# Definitions #
# Functions #
def standard_parse_parentheses_str(
    expression: str,
    include: Set[str] = None,
    exclude: Set[str] = None,
    cast: Callable = lambda x: x,
) -> List[Any]:
    """Standard implementation of parse_parentheses for string input using a stack-based approach.

    Args:
        expression: The input expression containing parentheses to parse.
        include: A set of elements to include in the output. Defaults to None.
        exclude: A set of elements to exclude from the output. Defaults to None.
        cast: A function to apply to each extracted element for custom transformations.

    Returns:
        A nested list of parsed and optionally filtered and transformed elements.

    Raises:
        ValueError: If the parentheses in the input expression are unbalanced.
    """
    if exclude is None:
        exclude = set()

    # Regular expressions for tokenizing
    r_parentheses = r"\(|\)"
    r_double_quote_group = r'"((?:[^"]|\\.)*)(?<!\\)"'
    r_single_quote_group = r"'((?:[^']|\\.)*)(?<!\\)'"
    r_group_between_characters = r"[^,'\"\(\)]+"
    r_expression = r"|".join((r_parentheses, r_double_quote_group, r_single_quote_group, r_group_between_characters))

    # Stack to keep track of nested lists
    stack = deque([[]])

    # Parse the expression
    for match in re.finditer(r_expression, expression.strip()):
        token = match[0]
        if token == "(":
            # Start a new nested list
            new_list = []
            stack[-1].append(new_list)
            stack.append(new_list)
        elif token == ")":
            # End the current nested list
            try:
                stack.pop()
            except IndexError:
                raise ValueError("Unbalanced parentheses")
        elif (not include or token in include) and token not in exclude:
            # Add the token to the current list if it passes the filters
            stack[-1].append(cast(token.strip()))

    # Check for unbalanced parentheses
    if len(stack) != 1:
        raise ValueError("Unbalanced parentheses")

    return stack[0]


def standard_parse_parentheses_bytes(
    expression: Union[bytes, bytearray],
    include: Set[bytes] = None,
    exclude: Set[bytes] = None,
    cast: Callable = lambda x: x,
) -> List[Any]:
    """Standard implementation of parse_parentheses for bytes/bytearray input using a stack-based approach.

    Args:
        expression: The input expression containing parentheses to parse.
        include: A set of elements to include in the output. Defaults to None.
        exclude: A set of elements to exclude from the output. Defaults to None.
        cast: A function to apply to each extracted element for custom transformations.

    Returns:
        A nested list of parsed and optionally filtered and transformed elements.

    Raises:
        ValueError: If the parentheses in the input expression are unbalanced.
    """
    if exclude is None:
        exclude = set()

    # Regular expressions for tokenizing
    rb_parentheses = rb"\(|\)"
    rb_double_quote_group = rb'"((?:[^"]|\\.)*)(?<!\\)"'
    rb_single_quote_group = rb"'((?:[^']|\\.)*)(?<!\\)'"
    rb_group_between_characters = rb"[^,'\"\(\)]+"
    rb_expression = rb"|".join(
        (rb_parentheses, rb_double_quote_group, rb_single_quote_group, rb_group_between_characters)
    )

    # Stack to keep track of nested lists
    stack = deque([[]])

    # Parse the expression
    for match in re.finditer(rb_expression, expression.strip()):
        token = match[0]
        if token == b"(":
            # Start a new nested list
            new_list = []
            stack[-1].append(new_list)
            stack.append(new_list)
        elif token == b")":
            # End the current nested list
            try:
                stack.pop()
            except IndexError:
                raise ValueError("Unbalanced parentheses")
        elif (not include or token in include) and token not in exclude:
            # Add the token to the current list if it passes the filters
            stack[-1].append(cast(token.strip()))

    # Check for unbalanced parentheses
    if len(stack) != 1:
        raise ValueError("Unbalanced parentheses")

    return stack[0]


# Classes #
class TestParseParentheses(BasePerformanceTestSuite):
    """Test the performance of the parse_parentheses function.

    This class tests_old_ the performance of the parse_parentheses function, which parses expressions with parentheses and
    returns a nested list of extracted elements.
    """

    # Attributes #
    timeit_runs: int = 10000  # Reduced for more complex operations
    speed_tolerance: int = 150

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def simple_expression(self) -> str:
        """Create a simple expression for use in tests_old_.

        Returns:
            str: A simple expression with parentheses.
        """
        return "((first(inner))(second)(wrong(thing)))"

    @pytest.fixture
    def complex_expression(self) -> str:
        """Create a complex expression for use in tests_old_.

        Returns:
            str: A complex expression with many nested parentheses.
        """
        return "(" * 20 + "test" + ")" * 20 + "(second(nested(deep)))(third)(fourth(fifth))"

    @pytest.fixture
    def bytes_expression(self) -> bytes:
        """Create a bytes expression for use in tests_old_.

        Returns:
            bytes: A bytes expression with parentheses.
        """
        return b"((first\xff(inner'('))(second)(wrong(thing)))"

    @pytest.fixture
    def include_set(self) -> set:
        """Create an include set for use in tests_old_.

        Returns:
            set: A set of elements to include.
        """
        return {"first", "second", "third"}

    @pytest.fixture
    def exclude_set(self) -> set:
        """Create an exclude set for use in tests_old_.

        Returns:
            set: A set of elements to exclude.
        """
        return {"wrong", "thing"}

    @pytest.fixture
    def cast_function(self) -> Callable:
        """Create a cast function for use in tests_old_.

        Returns:
            Callable: A function to cast elements.
        """

        def cast_to_upper(s: str) -> str:
            if isinstance(s, str):
                return s.upper()
            return s

        return cast_to_upper

    # Tests
    def test_parse_parentheses_simple_speed(self, simple_expression: str) -> None:
        """Test the performance of parse_parentheses with a simple expression.

        This test compares the speed of parse_parentheses with a standard implementation for a simple expression.

        Args:
            simple_expression: A fixture providing a simple expression.
        """

        def custom_implementation() -> None:
            parse_parentheses(simple_expression)

        def standard_implementation() -> None:
            standard_parse_parentheses_str(simple_expression)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (parse_parentheses simple): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_parse_parentheses_complex_speed(self, complex_expression: str) -> None:
        """Test the performance of parse_parentheses with a complex expression.

        This test compares the speed of parse_parentheses with a standard implementation for a complex expression.

        Args:
            complex_expression: A fixture providing a complex expression.
        """

        def custom_implementation() -> None:
            parse_parentheses(complex_expression)

        def standard_implementation() -> None:
            standard_parse_parentheses_str(complex_expression)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (parse_parentheses complex): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_parse_parentheses_bytes_speed(self, bytes_expression: bytes) -> None:
        """Test the performance of parse_parentheses with a bytes expression.

        This test compares the speed of parse_parentheses with a standard implementation for a bytes expression.

        Args:
            bytes_expression: A fixture providing a bytes expression.
        """

        def custom_implementation() -> None:
            parse_parentheses(bytes_expression)

        def standard_implementation() -> None:
            standard_parse_parentheses_bytes(bytes_expression)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (parse_parentheses bytes): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_parse_parentheses_filtering_speed(
        self, simple_expression: str, include_set: set, exclude_set: set
    ) -> None:
        """Test the performance of parse_parentheses with filtering.

        This test compares the speed of parse_parentheses with a standard implementation when using include/exclude sets.

        Args:
            simple_expression: A fixture providing a simple expression.
            include_set: A fixture providing an include set.
            exclude_set: A fixture providing an exclude set.
        """

        def custom_implementation_include() -> None:
            parse_parentheses(simple_expression, include=include_set)

        def standard_implementation_include() -> None:
            standard_parse_parentheses_str(simple_expression, include=include_set)

        def custom_implementation_exclude() -> None:
            parse_parentheses(simple_expression, exclude=exclude_set)

        def standard_implementation_exclude() -> None:
            standard_parse_parentheses_str(simple_expression, exclude=exclude_set)

        # Calculate the mean time for include filtering
        include_new_time = timeit.timeit(custom_implementation_include, number=self.timeit_runs)
        include_old_time = timeit.timeit(standard_implementation_include, number=self.timeit_runs)

        # Calculate the mean time for exclude filtering
        exclude_new_time = timeit.timeit(custom_implementation_exclude, number=self.timeit_runs)
        exclude_old_time = timeit.timeit(standard_implementation_exclude, number=self.timeit_runs)

        # Calculate the average time for both filtering types
        new_avg_time = (include_new_time + exclude_new_time) / 2
        old_avg_time = (include_old_time + exclude_old_time) / 2

        # Convert to microseconds
        mean_new = new_avg_time / self.timeit_runs * 1000000
        mean_old = old_avg_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (parse_parentheses filtering): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)"
        )
        assert percent < self.speed_tolerance

    def test_parse_parentheses_casting_speed(self, simple_expression: str, cast_function: Callable) -> None:
        """Test the performance of parse_parentheses with casting.

        This test compares the speed of parse_parentheses with a standard implementation when using a cast function.

        Args:
            simple_expression: A fixture providing a simple expression.
            cast_function: A fixture providing a cast function.
        """

        def custom_implementation() -> None:
            parse_parentheses(simple_expression, cast=cast_function)

        def standard_implementation() -> None:
            standard_parse_parentheses_str(simple_expression, cast=cast_function)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (parse_parentheses casting): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
