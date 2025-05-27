#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedlrucache_performance.py
Performance tests for the timedlrucache module in the baseobjects package.
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
import datetime
import functools
import io
import pstats
from random import randint
import time
import timeit
from typing import Any, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedlrucache import TimedLRUCache
from tests.bases.performance.base_performance import StatsMicro
from tests.cachingtools.performance.performance_basetimedcache import BaseCachePerformanceTest


# Definitions #
# Classes #
class TestTimedLRUCache(BaseCachePerformanceTest):
    """Performance tests for the TimedLRUCache class.

    This class tests the performance of the TimedLRUCache class.
    """
    class_ = TimedLRUCache
    zero_time = datetime.timedelta(0)

    def test_compare_with_python_lru_cache(self):
        """Compare the performance of TimedLRUCache with Python's built-in lru_cache.

        This test compares the performance of TimedLRUCache against Python's built-in
        functools.lru_cache for the same operations.
        """
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        # Create both cache versions
        timedlru_cache = self.class_(func, maxsize=100)
        python_lru_cache = functools.lru_cache(maxsize=100)(func)

        # First call to populate caches
        timedlru_cache(4, 5, 6)
        python_lru_cache(4, 5, 6)

        def timedlru_call():
            timedlru_cache(4, 5, 6)

        def python_lru_call():
            python_lru_cache(4, 5, 6)

        # Measure performance
        timedlru_time = timeit.timeit(timedlru_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        python_lru_time = timeit.timeit(python_lru_call, number=self.timeit_runs) / self.timeit_runs * 1000000

        # Calculate relative performance
        timedlru_c_units = timedlru_time / self.call_speed
        python_lru_c_units = python_lru_time / self.call_speed
        percent = (timedlru_time / python_lru_time) * 100

        print(f"\nTimedLRUCache call speed: {timedlru_c_units:.3f} cu or {timedlru_time:.3f} μs")
        print(f"Python's lru_cache call speed: {python_lru_c_units:.3f} cu or {python_lru_time:.3f} μs")
        print(f"TimedLRUCache took {percent:.3f}% of the time of Python's lru_cache.")

        # We don't assert here as this is just a comparison, not a pass/fail test

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

    def test_lru_eviction_performance(self):
        """Test the performance impact of LRU cache eviction."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, maxsize=2)

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

    def test_lru_access_pattern_performance(self):
        """Test the performance with different access patterns."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, maxsize=10)

        # Fill the cache
        for i in range(10):
            callable_obj(i)

        def sequential_access():
            # Access items in sequential order
            for i in range(10):
                callable_obj(i)

        def random_access():
            # Access items in a non-sequential order that exercises the LRU functionality
            callable_obj(5)
            callable_obj(2)
            callable_obj(8)
            callable_obj(1)
            callable_obj(9)
            callable_obj(3)
            callable_obj(7)
            callable_obj(0)
            callable_obj(6)
            callable_obj(4)

        mean_seq = timeit.timeit(sequential_access, number=1000) / 1000 * 1000000
        mean_rand = timeit.timeit(random_access, number=1000) / 1000 * 1000000

        # Compare the two access patterns
        percent = (mean_rand / mean_seq) * 100

        print(f"\nRandom access pattern took {percent:.3f}% of the time of sequential access pattern.")
        print(f"Sequential: {mean_seq:.3f} μs, Random: {mean_rand:.3f} μs")
        assert True  # Just measuring, not enforcing a specific performance level

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

    def test_cache_miss_performance_comparison(self):
        """Compare cache miss performance between TimedLRUCache and Python's lru_cache.

        This test compares how both caches perform when there are cache misses.
        """
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        # Create both cache versions with small size to force misses
        timedlru_cache = self.class_(func, maxsize=10)
        python_lru_cache = functools.lru_cache(maxsize=10)(func)

        def timedlru_miss():
            # Generate random numbers to ensure cache misses
            for i in range(20):
                timedlru_cache(randint(1, 1000))

        def python_lru_miss():
            # Generate random numbers to ensure cache misses
            for i in range(20):
                python_lru_cache(randint(1, 1000))

        # Measure performance (fewer runs due to more work per run)
        timedlru_time = timeit.timeit(timedlru_miss, number=1000) / 1000 * 1000000
        python_lru_time = timeit.timeit(python_lru_miss, number=1000) / 1000 * 1000000

        # Calculate relative performance
        percent = (timedlru_time / python_lru_time) * 100

        print(f"\nTimedLRUCache cache miss performance: {timedlru_time:.3f} μs")
        print(f"Python's lru_cache cache miss performance: {python_lru_time:.3f} μs")
        print(f"TimedLRUCache took {percent:.3f}% of the time of Python's lru_cache for cache misses.")

    def test_access_pattern_comparison(self):
        """Compare different access patterns between TimedLRUCache and Python's lru_cache.

        This test compares how both caches perform with different access patterns.
        """
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        # Create both cache versions
        timedlru_cache = self.class_(func, maxsize=100)
        python_lru_cache = functools.lru_cache(maxsize=100)(func)

        # Fill the caches with initial values
        for i in range(100):
            timedlru_cache(i)
            python_lru_cache(i)

        # Test sequential access pattern
        def timedlru_sequential():
            for i in range(100):
                timedlru_cache(i)

        def python_lru_sequential():
            for i in range(100):
                python_lru_cache(i)

        # Test random access pattern
        def timedlru_random():
            for _ in range(100):
                timedlru_cache(randint(0, 99))

        def python_lru_random():
            for _ in range(100):
                python_lru_cache(randint(0, 99))

        # Measure sequential access performance (fewer runs due to more work per run)
        timedlru_seq_time = timeit.timeit(timedlru_sequential, number=100) / 100 * 1000000
        python_lru_seq_time = timeit.timeit(python_lru_sequential, number=100) / 100 * 1000000

        # Measure random access performance (fewer runs due to more work per run)
        timedlru_rand_time = timeit.timeit(timedlru_random, number=100) / 100 * 1000000
        python_lru_rand_time = timeit.timeit(python_lru_random, number=100) / 100 * 1000000

        # Calculate relative performance
        seq_percent = (timedlru_seq_time / python_lru_seq_time) * 100
        rand_percent = (timedlru_rand_time / python_lru_rand_time) * 100

        print(f"\nSequential access pattern:")
        print(f"TimedLRUCache: {timedlru_seq_time:.3f} μs")
        print(f"Python's lru_cache: {python_lru_seq_time:.3f} μs")
        print(f"TimedLRUCache took {seq_percent:.3f}% of the time of Python's lru_cache.")

        print(f"\nRandom access pattern:")
        print(f"TimedLRUCache: {timedlru_rand_time:.3f} μs")
        print(f"Python's lru_cache: {python_lru_rand_time:.3f} μs")
        print(f"TimedLRUCache took {rand_percent:.3f}% of the time of Python's lru_cache.")

    def test_different_cache_sizes_comparison(self):
        """Compare performance with different cache sizes between TimedLRUCache and Python's lru_cache.

        This test compares how both caches perform with different cache sizes.
        """
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        # Test different cache sizes
        cache_sizes = [10, 100, 1000]

        for size in cache_sizes:
            # Create both cache versions
            timedlru_cache = self.class_(func, maxsize=size)
            python_lru_cache = functools.lru_cache(maxsize=size)(func)

            # Fill the caches with initial values (up to size)
            for i in range(size):
                timedlru_cache(i)
                python_lru_cache(i)

            def timedlru_call():
                # Access a mix of cached values
                for i in range(min(size, 100)):  # Limit to 100 calls for larger sizes
                    timedlru_cache(i)

            def python_lru_call():
                # Access a mix of cached values
                for i in range(min(size, 100)):  # Limit to 100 calls for larger sizes
                    python_lru_cache(i)

            # Measure performance (fewer runs for larger sizes)
            runs = 100 if size > 100 else 1000
            timedlru_time = timeit.timeit(timedlru_call, number=runs) / runs * 1000000
            python_lru_time = timeit.timeit(python_lru_call, number=runs) / runs * 1000000

            # Calculate relative performance
            percent = (timedlru_time / python_lru_time) * 100

            print(f"\nCache size: {size}")
            print(f"TimedLRUCache: {timedlru_time:.3f} μs")
            print(f"Python's lru_cache: {python_lru_time:.3f} μs")
            print(f"TimedLRUCache took {percent:.3f}% of the time of Python's lru_cache.")



# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
