"""parseparentheses.py
Parses expressions with parentheses and returns a nested list of extracted elements.
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
from collections import deque
from typing import Any
from collections.abc import Callable

# Local Packages #
from ..functions import singlekwargdispatch

# Definitions #
# Regular Expressions #
rb_parentheses = rb"\(|\)"
rb_double_quote_group = rb'"((?:[^"]|\\.)*)(?<!\\)"'
rb_single_quote_group = rb"'((?:[^']|\\.)*)(?<!\\)'"
rb_group_between_characters = rb"[^, '\"\(\)]+"
rb_expression = rb"|".join((rb_parentheses, rb_double_quote_group, rb_single_quote_group, rb_group_between_characters))

r_parentheses = r"\(|\)"
r_double_quote_group = r'"((?:[^"]|\\.)*)(?<!\\)"'
r_single_quote_group = r"'((?:[^']|\\.)*)(?<!\\)'"
r_group_between_characters = r"[^, '\"\(\)]+"
r_expression = r"|".join((r_parentheses, r_double_quote_group, r_single_quote_group, r_group_between_characters))


# Functions #
def _no_cast(obj: Any) -> Any:
    """A helper function which does not the cast the input.

    Args:
        obj: The object to be returned unchanged.

    Returns:
        The same object that was provided as input.
    """
    return obj


@singlekwargdispatch
def parse_parentheses(
    expression: str | bytes | bytearray,
    include: set | None = None,
    exclude: set | None = None,
    cast: Callable = _no_cast,
) -> list[...]:
    """Parses expressions with parentheses and returns a nested list of extracted elements.

    This function uses a single-dispatch mechanism to handle parsing for various data types. If the type of the provided
    expression is not supported by any registered dispatch function, a ValueError is raised. Optional filtering can be
    applied by specifying `include` or `exclude` sets to control which elements are included or excluded. An optional
    casting function can be applied to transform the extracted elements.

    Args:
        expression: The input expression containing parentheses to parse.
        include: A set of elements to include in the output. Defaults to None.
        exclude: A set of elements to exclude from the output. Defaults to None.
        cast: A function to apply to each extracted element for custom transformations. Defaults to `_no_cast`.

    Returns:
        A nest list of parsed and optionally filtered and transformed elements.

    Raises:
        ValueError: If the type of the input expression is unsupported.
    """
    # Catch the general case for any unregistered types
    msg = f"parse_parentheses does not parse {expression} type."
    raise ValueError(msg)


@parse_parentheses.register(str)
def _parse_parentheses(
    expression: str,
    include: set | None = None,
    exclude: set | None = None,
    cast: Callable = _no_cast,
) -> list[...]:
    """Parses string expressions with parentheses and returns a nested list of extracted elements.

    This function is used to parse expressions with parentheses into a structured list format. Each open parenthesis '('
    denotes the start of a nested list, and each close parenthesis ')' indicates the end of the currently active list.
    Optional filtering can be applied by specifying `include` or `exclude` sets to control which elements are included
    or excluded. An optional casting function can be applied to transform the extracted elements.

    Args:
        expression: The input expression containing parentheses to parse.
        include: A set of elements to include in the output. Defaults to None.
        exclude: A set of elements to exclude from the output. Defaults to None.
        cast: A function to apply to each extracted element for custom transformations. Defaults to `_no_cast`.

    Returns:
        A nest list of parsed and optionally filtered and transformed elements.

    Raises:
        ValueError: If the parentheses in the input expression are unbalanced (either unmatched opening or closing
            parentheses).
    """
    if exclude is None:
        exclude = set()
    list_bank = deque([[]])
    for match_object in re.finditer(r_expression, expression.strip()):
        match (token := match_object[0]):
            case "(":
                new_list = []
                list_bank[-1].append(new_list)
                list_bank.append(new_list)
            case ")":
                try:
                    list_bank.pop()
                except IndexError:
                    msg = "Unbalanced parentheses"
                    raise ValueError(msg) from None
            case _ if (not include or token in include) and token not in exclude:
                list_bank[-1].append(cast(token.strip()))
    if len(list_bank) != 1:
        msg = "Unbalanced parentheses"
        raise ValueError(msg)
    return list_bank.pop()


@parse_parentheses.register(bytes)
@parse_parentheses.register(bytearray)
def _parse_parentheses(
    expression: bytes | bytearray,
    include: set | None = None,
    exclude: set | None = None,
    cast: Callable = _no_cast,
) -> list[...]:
    """Parses bytes or bytesarray expressions with parentheses and returns a nested list of extracted elements.

    This function is used to parse expressions with parentheses into a structured list format. Each open parenthesis '('
    denotes the start of a nested list, and each close parenthesis ')' indicates the end of the currently active list.
    Optional filtering can be applied by specifying `include` or `exclude` sets to control which elements are included
    or excluded. An optional casting function can be applied to transform the extracted elements.

    Args:
        expression: The input expression containing parentheses to parse.
        include: A set of elements to include in the output. Defaults to None.
        exclude: A set of elements to exclude from the output. Defaults to None.
        cast: A function to apply to each extracted element for custom transformations. Defaults to `_no_cast`.

    Returns:
        A nest list of parsed and optionally filtered and transformed elements.

    Raises:
        ValueError: If the parentheses in the input expression are unbalanced (either unmatched opening or closing
            parentheses).
    """
    if exclude is None:
        exclude = set()
    list_bank = deque([[]])
    for match_object in re.finditer(rb_expression, expression.strip()):
        match (token := match_object[0]):
            case b"(":
                new_list = []
                list_bank[-1].append(new_list)
                list_bank.append(new_list)
            case b")":
                try:
                    list_bank.pop()
                except IndexError:
                    msg = "Unbalanced parentheses"
                    raise ValueError(msg) from None
            case _ if (not include or token in include) and token not in exclude:
                list_bank[-1].append(cast(token.strip()))
    if len(list_bank) != 1:
        msg = "Unbalanced parentheses"
        raise ValueError(msg)
    return list_bank.pop()
