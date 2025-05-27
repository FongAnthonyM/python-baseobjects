#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basetimedcache_performance.py
Performance tests for the basetimedcache module in the baseobjects package.
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
from src.baseobjects.cachingtools.caches.basetimedcache import BaseTimedCacheCallable, BaseTimedCache
from tests.bases.performance.base_performance import ClassPerformanceTest, StatsMicro


# Definitions #
# Functions #
def func(*args, **kwargs):
    return None

# Classes #
class BaseCachePerformanceTest(ClassPerformanceTest):
    """Base Performance Test for the Timed Cache classes."""
    speed_tolerance = 7500

    _func_time: float = timeit.timeit(lambda: func(1,2,3), number=10000000)
    func_speed: float = _func_time / 10000000 * 1000000

    def create_test_object(self):
        """Create the class to be tested."""
        class ExampleClass:
            """A simple class to run performance tests with."""

            def original_method(self, *args, **kwargs):
                return None

            @self.class_
            def default_method(self, *args, **kwargs):
                return None

            @self.class_(instanced=True)
            def instanced_method(self, *args, **kwargs):
                return None

            @self.class_(lifetime=0.0000001)
            def lifetime_method(self, *args, **kwargs):
                return None

        return ExampleClass()

    def test_caching_function_performance(self):
        """Test the performance of the caching function."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func)
        callable_obj.is_timed = False

        # First call to populate cache
        callable_obj(4, 5, 6)

        def cached_call():
            callable_obj(4, 5, 6)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = self.func_speed
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_decorator_overhead(self):
        """Test the overhead of using the decorator."""
        decorator = self.class_
        @decorator
        def func(*args, **kwargs):
            return None

        # First call to populate cache
        func(1, 2, 3)

        def decorated_call():
            func(4, 5, 6)

        mean_new = timeit.timeit(decorated_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = self.func_speed
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache decorator call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_caching_method_performance(self):
        """Test the performance of the caching method."""
        # Create a simple function to wrap
        caching_obj = self.create_test_object()

        caching_obj.default_method(4, 5, 6)  # Populate cache

        def cached_call():
            caching_obj.default_method(4, 5, 6)

        def direct_call():
            caching_obj.original_method(4, 5, 6)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = timeit.timeit(direct_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache method call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_caching_instanced_performance(self):
        """Test the performance of the caching method."""
        # Create a simple function to wrap
        caching_obj = self.create_test_object()

        caching_obj.instanced_method(4, 5, 6)  # Populate cache

        def cached_call():
            caching_obj.instanced_method(4, 5, 6)

        def direct_call():
            caching_obj.original_method(4, 5, 6)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = timeit.timeit(direct_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache instanced call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_lifetime_expiration(self):
        """Test the performance impact of lifetime expiration."""
        decorator = self.class_
        @decorator(lifetime=0.0000001)  # Very short lifetime for testing
        def func(*args, **kwargs):
            return None

        # First call to populate cache
        func(1, 2, 3)

        def expired_call():
            func(4, 5, 6)  # Different args, but should use same cache

        mean_new = timeit.timeit(expired_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = self.func_speed
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache expired call speed {new_c_units:.3f} cu {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_different_args_performance(self):
        """Test the performance of the caching method."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func)

        # First call to populate cache
        callable_obj(0)

        def cached_call():
            number = randint(1, 1000000)
            callable_obj(number)

        def direct_call():
            number = randint(1, 1000000)
            func(number)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = timeit.timeit(direct_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} cache call speed {new_c_units:.3f} cu {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_clear_cache_performance(self):
        """Test the performance of the caching function."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func, cache_method="clear_cache")

        # First call to populate cache
        callable_obj(4, 5, 6)

        def cached_call():
            callable_obj(4, 5, 6)

        mean_new = timeit.timeit(cached_call, number=self.timeit_runs) / self.timeit_runs * 1000000
        new_c_units = mean_new / self.call_speed
        mean_old = self.func_speed
        percent = (mean_new / mean_old) * 100

        print(f"\n{self.class_.__name__} clear cache call speed {new_c_units:.3f} cu or {mean_new:.3f} μs "
              f"\nIt took {percent:.3f}% of the time of a direct call.")
        assert percent < self.speed_tolerance  # A slower performance is expected, but not unreasonably high

    def test_caching_profile(self):
        """Profile the caching method."""
        # Create a simple function to wrap
        def func(*args, **kwargs):
            return None

        callable_obj = self.class_(func)
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
