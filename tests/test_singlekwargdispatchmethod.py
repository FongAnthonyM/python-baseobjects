#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_singlekwargdispatchmethod.py
Tests singlekwargdispatchmethod
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

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.functions import singlekwargdispatch


# Definitions #
# Classes #
class TestSingleKwargDispatchMethod:
    class ExampleClass:
        @singlekwargdispatch
        def first_overload(self, a, b=None):
            return None

        @first_overload.register
        def _(self, a: int, b: None = None):
            return a + 1

        @first_overload.register
        def _(self, a: str):
            return True

        @singlekwargdispatch(kwarg="a")
        def second_overload(self, a, b=None):
            return None

        @second_overload.register
        def _(self, a: int, b: None = None):
            return a + 1

        @second_overload.register
        def _(self, a: str):
            return True

    def test_arg(self):
        example = self.ExampleClass()
        assert example.first_overload(1) == 2
        assert example.first_overload("Any")

    def test_first_kwarg(self):
        example = self.ExampleClass()
        assert example.first_overload(a=1) == 2
        assert example.first_overload(a="Any")

    def test_specific_kwarg(self):
        example = self.ExampleClass()
        assert example.second_overload(b=None, a=1) is not None
        assert example.second_overload(a="Any")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
