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
import timeit

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools import *
from .bases_performance import ClassPerformanceTest, StatsMicro


# Definitions #
# Classes #
class TestCachingObject(ClassPerformanceTest):
    class_ = CachingObject
    zero_time = datetime.timedelta(0)

    class CachingTestObject(CachingObject):
        def __init__(self, a=1, init=True):
            super().__init__()
            self.a = a

        @property
        def proxy(self):
            return self.get_proxy.caching_call()

        @timed_keyless_cache_method(lifetime=2, call_method="clearing_call", collective=False)
        def get_proxy(self):
            return datetime.datetime.now()

        def normal(self):
            return datetime.datetime.now()

        def printer(self):
            print(self.a)

    def test_cache_bypass_speed(self):
        cacher = TestCachingObject.CachingTestObject()

        def new_access():
            cacher.get_proxy()

        def old_access():
            cacher.normal()

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_cached_speed(self):
        cacher = TestCachingObject.CachingTestObject()

        cacher.proxy

        def new_access():
            cacher.proxy

        def old_access():
            cacher.a

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_cached_profile(self):
        cacher = TestCachingObject.CachingTestObject()
        cacher.proxy

        pr = cProfile.Profile()
        pr.enable()

        cacher.proxy

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    def test_functool_speed(self):
        x = 1

        @functools.lru_cache
        def proxy(a=None):
            return datetime.datetime.now()

        proxy()

        def new_access():
            proxy()

        def old_access():
            x

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_functool_profile(self):
        @functools.lru_cache
        def proxy(a=None):
            return datetime.datetime.now()

        proxy()

        pr = cProfile.Profile()
        pr.enable()

        proxy()

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
