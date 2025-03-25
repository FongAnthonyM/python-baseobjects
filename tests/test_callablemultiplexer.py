#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_callablemultiplexer.py
Tests callablemultiplexer
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
import pickle

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.functions import CallableMultiplexer


# Definitions #
# Classes #
class TestSingleKwargDispatchMethod:
    class ExampleClass:
        def __init__(self):
            self.multiplex_method = CallableMultiplexer(instance=self, select="add")
            self.multiplex_method_2 = CallableMultiplexer(instance=self, select="multiply")

        def add(self, a: int, b: int) -> int:
            return a + b

        def multiply(self, a: int, b: int) -> int:
            return a * b

    def test_select(self):
        example = self.ExampleClass()
        example.multiplex_method.select("add")
        assert example.multiplex_method(1, 2) == 3

        example.multiplex_method.select("multiply")
        assert example.multiplex_method(1, 2) == 2

    def test_pickling(self):
        # Setup
        test_object = self.ExampleClass()
        assert test_object.multiplex_method.selected == "add"

        test_object.multiplex_method.select("multiply")
        assert test_object.multiplex_method.selected == "multiply"

        # Test Pickle
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)

        # Assert
        assert all((new_obj, new_obj.multiplex_method.__self__, new_obj.multiplex_method_2.__self__))
        assert new_obj.multiplex_method.selected == "multiply"
        assert new_obj.multiplex_method(1, 2) == 2

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
