#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package.
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
import copy
import pathlib
from pstats import Stats, f8, func_std_string
import timeit

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class StatsMicro(Stats):
    def print_stats(self, *amount):
        for filename in self.files:
            print(filename, file=self.stream)
        if self.files:
            print(file=self.stream)
        indent = " " * 8
        for func in self.top_level:
            print(indent, func_get_function_name(func), file=self.stream)

        print(indent, self.total_calls, "function calls", end=" ", file=self.stream)
        if self.total_calls != self.prim_calls:
            print("(%d primitive calls)" % self.prim_calls, end=" ", file=self.stream)
        print("in %.3f microseconds" % (self.total_tt * 1000000), file=self.stream)
        print(file=self.stream)
        width, list = self.get_print_list(amount)
        if list:
            self.print_title()
            for func in list:
                self.print_line(func)
            print(file=self.stream)
            print(file=self.stream)
        return self

    def print_line(self, func):  # hack: should print percentages
        cc, nc, tt, ct, callers = self.stats[func]
        c = str(nc)
        if nc != cc:
            c = c + "/" + str(cc)
        print(c.rjust(9), end=" ", file=self.stream)
        print(f8(tt * 1000000), end=" ", file=self.stream)
        if nc == 0:
            print(" " * 8, end=" ", file=self.stream)
        else:
            print(f8(tt / nc * 1000000), end=" ", file=self.stream)
        print(f8(ct * 1000000), end=" ", file=self.stream)
        if cc == 0:
            print(" " * 8, end=" ", file=self.stream)
        else:
            print(f8(ct / cc * 1000000), end=" ", file=self.stream)
        print(func_std_string(func), file=self.stream)


class ClassPerformanceTest(abc.ABC):
    """Default class tests that all classes should pass."""

    class_ = None
    timeit_runs = 100000
    speed_tolerance = 200

    def test_instance_creation(self):
        pass


class TestBaseObject(ClassPerformanceTest):
    """Test the BaseObject class which a subclass is created to test with."""

    class BaseTestObject(BaseObject):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class NormalObject(object):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class_ = BaseTestObject

    @pytest.fixture
    def test_object(self):
        return self.class_()

    def test_copy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_copy():
            copy.copy(normal)

        mean_new = timeit.timeit(test_object.copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_deepcopy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_deepcopy():
            copy.deepcopy(normal)

        mean_new = timeit.timeit(test_object.deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
