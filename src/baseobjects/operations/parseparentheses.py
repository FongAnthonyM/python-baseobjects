"""parseparentheses.py

"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections import deque
from functools import singledispatch
import re
from typing import Any, Generator, Iterable

# Third-Party Packages #

# Local Packages #


# Definitions #
# Regular Expressions #
rb_parentheses = rb"\(|\)"
rb_double_quote_group = rb'"((?:[^"]|\\.)*)(?<!\\)"' 
rb_single_quote_group = rb"'((?:[^']|\\.)*)(?<!\\)'"
rb_group_between_characters = rb"[^,'\"\(\)]+" 
rb_expression = rb"|".join((rb_parentheses, rb_double_quote_group, rb_single_quote_group, rb_group_between_characters))

r_parentheses = r"\(|\)"
r_double_quote_group = r'"((?:[^"]|\\.)*)(?<!\\)"' 
r_single_quote_group = r"'((?:[^']|\\.)*)(?<!\\)'"
r_group_between_characters = r"[^,'\"\(\)]+" 
r_expression = r"|".join((r_parentheses, r_double_quote_group, r_single_quote_group, r_group_between_characters))


# Functions #
@singledispatch
def parse_parentheses(expression: str | bytes | bytearray) -> dict[str, Any]:
    # Catch the general case for any unregistered types
    raise ValueError(f"{expression} is an invailid type")


@parse_parentheses.register
def _parse_parentheses(expression: str) -> dict[str, Any]:
    list_bank = deque([[]])
    for match_object in re.finditer(r_expression, expression):
        match (token := match_object[0]):
            case '(':
                new_list = []
                list_bank[-1].append(new_list)
                list_bank.append(new_list)
            case ')':
                try:
                    list_bank.pop()
                except IndexError:
                    raise ValueError("Unbalanced parentheses")
            case _:
                list_bank[-1].append(token.strip())
    if len(list_bank) > 1:
        raise ValueError("Unbalanced parentheses")
    return list_bank.pop()


@parse_parentheses.register(bytes)
@parse_parentheses.register(bytearray)
def _parse_parentheses(expression: bytes | bytearray) -> dict[str, Any]:
    list_bank = deque([[]])
    for match_object in re.finditer(rb_expression, expression):
        match (token := match_object[0]):
            case b'(':
                new_list = []
                list_bank[-1].append(new_list)
                list_bank.append(new_list)
            case b')':
                try:
                    list_bank.pop()
                except IndexError:
                    raise ValueError("Unbalanced parentheses")
            case _:
                list_bank[-1].append(token.strip())
    if len(list_bank) > 1:
        raise ValueError("Unbalanced parentheses")
    return list_bank.pop()


