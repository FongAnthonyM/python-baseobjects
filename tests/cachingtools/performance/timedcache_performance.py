#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedcache_performance.py
Performance tests for the timedcache module in the baseobjects package.
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
import cProfile
import io
import pstats
from random import randint
import timeit

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedcache import TimedCache
from tests.bases.performance.base_performance import StatsMicro
from tests.cachingtools.performance.performance_basetimedcache import BaseCachePerformanceTest


# Definitions #
# Classes #
class TestTimedCache(BaseCachePerformanceTest):
    """Performance tests for the TimedCache class.

    This class tests the performance of the TimedCache class.
    """
    class_ = TimedCache

    def test_limited_cache_performance(self):
        """Test the performance of the limited_cache method."""

        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, maxsize=100)

        # First call to populate cache
        callable_obj(4, 5, 6)

        def cached_call():
            callable_obj(4, 5, 6)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = self.func_speed
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} limited cache call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_cache_eviction_performance(self):
        """Test the performance impact of cache eviction."""

        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, maxsize=1)

        # First call to populate cache
        callable_obj(0)

        def cached_call():
            number = randint(1, 1000000)
            callable_obj(number)

        def direct_call():
            number = randint(1, 1000000)
            func(number)

        mean_new = timeit.timeit(cached_call, number=100) / 100 * 1000000  # Fewer runs due to more work
        new_c_units = mean_new / self.call_speed
        mean_old = timeit.timeit(direct_call, number=100) / 100 * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache eviction call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_limited_cache_profile(self):
        """Profile the limited caching method."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, maxsize=1)
        callable_obj(1, 2, 3)  # Populate cache

        pr = cProfile.Profile()
        pr.enable()

        callable_obj(4, 5, 6)

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
