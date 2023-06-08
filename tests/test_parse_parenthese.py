""" test_parse_parenthese.py

"""
# Package Header #
from src.baseobjects.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import abc
import pathlib

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations import parse_parentheses


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""

    class_ = None
    timeit_runs = 100000
    speed_tolerance = 200

    def test_instance_creation(self):
        pass


class TestParseParentheses:
    def test_string_parse_parentheses(self):
        string = "((first(inner))(second)(wrong(thing)))"
        out = parse_parentheses(string)
        assert True

    def test_bytes_parse_parentheses(self):
        string = b"((first\xff(inner'('))(second)(wrong(thing)))"
        out = parse_parentheses(string)
        assert True


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
