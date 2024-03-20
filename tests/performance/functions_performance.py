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

import cProfile
import datetime
import functools
import io
import pstats
import time
import timeit

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects import BaseFunction
from src.baseobjects.functions import *
from .bases_performance import PerformanceTest, StatsMicro


# Definitions #
# Classes #
class TestFunctions(PerformanceTest):
    timeit_runs = 10000000
    profiling = True

    def test_basefunction_overhead(self):

        def some_function():
            return "10".find("1")

        wapper = BaseFunction(some_function)

        def new_eval():
            wapper()

        def old_eval():
            some_function()

        mean_new = timeit.timeit(new_eval, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_eval, number=self.timeit_runs) / self.timeit_runs * 1000000
        overhead = mean_new - mean_old
        new_c_units = overhead / self.call_speed

        print(f"\nBaseFunction Overhead {new_c_units:.3f} cu or {overhead:.3f} μs.")
        assert True

    def test_dynamicfunction_overhead(self):

        def some_function():
            return "10".find("1")

        wapper = DynamicFunction(some_function)

        def new_eval():
            wapper()

        def old_eval():
            some_function()

        mean_new = timeit.timeit(new_eval, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_eval, number=self.timeit_runs) / self.timeit_runs * 1000000
        overhead = mean_new - mean_old
        new_c_units = overhead / self.call_speed

        print(f"\nDynamicFunction Overhead {new_c_units:.3f} cu or {overhead:.3f} μs.")
        assert True

    @pytest.mark.skipif(not profiling, reason="not profiling")
    def test_basefunction_profile(self):
        def some_function():
            return None

        wapper = BaseFunction(some_function)

        pr = cProfile.Profile()
        pr.enable()

        wapper()

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    @pytest.mark.skipif(not profiling, reason="not profiling")
    def test_dynamicfunction_profile(self):
        def some_function():
            return None

        wapper = DynamicFunction(some_function)

        pr = cProfile.Profile()
        pr.enable()

        wapper()

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
