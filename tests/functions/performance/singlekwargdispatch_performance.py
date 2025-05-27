#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" singlekwargdispatch_performance.py
Performance tests for the singlekwargdispatchmethod and singlekwargdispatch classes in the baseobjects package.
"""
# Future Imports #
from __future__ import annotations

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from functools import singledispatchmethod
import timeit
from typing import Type, Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions.singlekwargdispatch import singlekwargdispatch
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Single Kwarg Dispatch
class TestSingleKwargDispatch(ClassPerformanceTest):
    """Test the performance of the singlekwargdispatch class.

    This class tests the performance of the singlekwargdispatch class, which extends singledispatch
    to allow kwargs to be used for dispatching.
    """
    # Class Definitions #
    class DispatchTestClass:
        """A class with methods for testing."""

        def normal_arg_method(self, arg: Any = None, **kwargs):
            """A normal method."""
            if isinstance(arg, int):
                return f"Integer: {arg}"
            elif isinstance(arg, str):
                return f"String: {arg}"
            else:
                return f"Default: {arg}"

        def normal_kwarg_method(self, arg: Any = None, kwarg: int | str | None = None, **kwargs):
            """A normal method with a kwarg."""
            if isinstance(kwarg, int):
                return f"Integer: {kwarg}"
            elif isinstance(kwarg, str):
                return f"String: {kwarg}"
            else:
                return f"Default: {kwarg}"

        @singledispatchmethod
        def functools_dispatch(self, arg: Any = None, **kwargs):
            """functools variation of dispatching method with a kwarg."""
            return f"Default: {arg}"

        @functools_dispatch.register
        def _(self, arg: int, **kwargs):
            """Process an integer."""
            return f"Integer: {arg}"

        @functools_dispatch.register(str)
        def _(self, arg: str, **kwargs):
            """Process a string."""
            return f"String: {arg}"

        @singlekwargdispatch
        def dispatch_arg(self, arg: int | str, **kwargs):
            """Default implementation."""
            return f"Default: {arg}"

        @dispatch_arg.register
        def _(self, arg: int, **kwargs):
            """Process an integer."""
            return f"Integer: {arg}"

        @dispatch_arg.register(str)
        def _(self, arg: str, **kwargs):
            """Process a string."""
            return f"String: {arg}"

        @singlekwargdispatch(kwarg="kwarg")
        def dispatch_kwarg(self, arg: Any = None, kwarg: int | str | None = None, **kwargs):
            """Default implementation with specific kwarg."""
            return f"Default: {kwarg}"

        @dispatch_kwarg.register
        def _(self, arg: Any = None, kwarg: int = 0, **kwargs):
            """Process an integer value."""
            return f"Integer: {kwarg}"

        @dispatch_kwarg.register(str)
        def _(self, arg: Any = None, kwarg: int | str | None = None, **kwargs):
            """Process a string value."""
            return f"String: {kwarg}"

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> TestSingleKwargDispatch.DispatchTestClass:
        """Create a test class instance for use in tests.

        Returns:
            DispatchTestClass: An instance of the test class.
        """
        return self.DispatchTestClass()

    # Tests
    def test_dispatch_call_speed_with_arg(self, test_class_instance: TestSingleKwargDispatch.DispatchTestClass) -> None:
        """Test the performance of the dispatch_call method with a positional argument.

        This test compares the speed of singlekwargdispatch.dispatch_call() with a normal singledispatchmethod.

        Args:
            test_class_instance: A fixture providing a DispatchTestClass instance.
        """
        arg = 42

        # Define the performance test functions
        def call_single_kwarg_dispatch() -> None:
            test_class_instance.dispatch_arg(arg)

        def call_single_dispatch() -> None:
            test_class_instance.functools_dispatch(arg)

        def call_normal_dispatch() -> None:
            test_class_instance.normal_arg_method(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_single_kwarg_dispatch, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_single_dispatch, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Calculate the mean time in microseconds for the baseline implementation
        baseline_time = timeit.timeit(call_normal_dispatch, number=self.timeit_runs)
        mean_baseline = baseline_time / self.timeit_runs * 1000000

        # Print the performance comparison
        print(f"\nBaseline: {mean_baseline:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"Old: {mean_old:.3f} μs")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_dispatch_call_speed_with_kwarg(self, test_class_instance: TestSingleKwargDispatch.DispatchTestClass) -> None:
        """Test the performance of the dispatch_call method with a keyword argument.

        This test compares the speed of singlekwargdispatch.dispatch_call() with a manual type check and dispatch.

        Args:
            test_class_instance: A fixture providing a DispatchTestClass instance.
        """
        arg = 42

        # Define the performance test functions
        def call_single_kwarg_dispatch() -> None:
            test_class_instance.dispatch_kwarg(kwarg=arg)

        def call_single_dispatch() -> None:
            test_class_instance.functools_dispatch(arg)

        def call_normal_dispatch() -> None:
            test_class_instance.normal_arg_method(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_single_kwarg_dispatch, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_single_dispatch, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Calculate the mean time in microseconds for the baseline implementation
        baseline_time = timeit.timeit(call_normal_dispatch, number=self.timeit_runs)
        mean_baseline = baseline_time / self.timeit_runs * 1000000

        # Print the performance comparison
        print(f"\nBaseline: {mean_baseline:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"Old: {mean_old:.3f} μs")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])