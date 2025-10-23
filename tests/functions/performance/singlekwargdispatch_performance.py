#!/usr/bin/env python
"""singlekwargdispatch_performance.py
Performance tests for the singlekwargdispatchmethod and singlekwargdispatch classes in the baseobjects.functions package.
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


# Standard Libraries #
import timeit

# Imports #
from functools import singledispatchmethod
from typing import Any, Type, Union

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions.singlekwargdispatch import singlekwargdispatch
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestSingleKwargDispatchPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the singlekwargdispatch class.

    This test suite measures the performance of various operations on singlekwargdispatch objects
    and compares them with standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
    """

    # Class Definitions #
    class DispatchTestClass:
        """A class with methods for testing."""

        def normal_arg_method(self, arg: Any = None, **kwargs) -> str:
            """A normal method."""
            if isinstance(arg, int):
                return f"Integer: {arg}"
            elif isinstance(arg, str):
                return f"String: {arg}"
            else:
                return f"Default: {arg}"

        def normal_kwarg_method(self, arg: Any = None, kwarg: int | str | None = None, **kwargs) -> str:
            """A normal method with a kwarg."""
            if isinstance(kwarg, int):
                return f"Integer: {kwarg}"
            elif isinstance(kwarg, str):
                return f"String: {kwarg}"
            else:
                return f"Default: {kwarg}"

        @singledispatchmethod
        def functools_dispatch(self, arg: Any = None, **kwargs) -> str:
            """Functools variation of dispatching method with a kwarg."""
            return f"Default: {arg}"

        @functools_dispatch.register
        def _(self, arg: int, **kwargs) -> str:
            """Process an integer."""
            return f"Integer: {arg}"

        @functools_dispatch.register(str)
        def _(self, arg: str, **kwargs) -> str:
            """Process a string."""
            return f"String: {arg}"

        @singlekwargdispatch
        def dispatch_arg(self, arg: int | str, **kwargs) -> str:
            """Default implementation."""
            return f"Default: {arg}"

        @dispatch_arg.register
        def _(self, arg: int, **kwargs) -> str:
            """Process an integer."""
            return f"Integer: {arg}"

        @dispatch_arg.register(str)
        def _(self, arg: str, **kwargs) -> str:
            """Process a string."""
            return f"String: {arg}"

        @singlekwargdispatch(kwarg="kwarg")
        def dispatch_kwarg(self, arg: Any = None, kwarg: int | str | None = None, **kwargs) -> str:
            """Default implementation with specific kwarg."""
            return f"Default: {kwarg}"

        @dispatch_kwarg.register
        def _(self, arg: Any = None, kwarg: int = 0, **kwargs) -> str:
            """Process an integer value."""
            return f"Integer: {kwarg}"

        @dispatch_kwarg.register(str)
        def _(self, arg: Any = None, kwarg: int | str | None = None, **kwargs) -> str:
            """Process a string value."""
            return f"String: {kwarg}"

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> TestSingleKwargDispatchPerformance.DispatchTestClass:
        """Create a test class instance for use in tests.

        Returns:
            DispatchTestClass: An instance of the test class.
        """
        return self.DispatchTestClass()

    # Tests
    def test_dispatch_call_speed_with_arg(
        self,
        test_class_instance: TestSingleKwargDispatchPerformance.DispatchTestClass,
    ) -> None:
        """Test the performance of the dispatch_call method with a positional argument.

        This test compares the speed of singlekwargdispatch.dispatch_call() with a normal singledispatchmethod
        and a manual type check implementation.

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

        # Calculate the mean time in microseconds for the singlekwargdispatch implementation
        new_time = timeit.timeit(call_single_kwarg_dispatch, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the singledispatchmethod implementation
        old_time = timeit.timeit(call_single_dispatch, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent_to_old = (mean_new / mean_old) * 100

        # Calculate the mean time in microseconds for the manual type check implementation
        baseline_time = timeit.timeit(call_normal_dispatch, number=self.timeit_runs)
        mean_baseline = baseline_time / self.timeit_runs * 1000000
        percent_to_baseline = (mean_new / mean_baseline) * 100

        # Print the performance comparison
        print(
            f"\nManual type check: {mean_baseline:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"singledispatchmethod: {mean_old:.3f} μs ({(mean_old / mean_baseline):.3f}% of manual type check time)")
        print(
            f"singlekwargdispatch with arg: {mean_new:.3f} μs ({percent_to_baseline:.3f}% of manual type check time, {percent_to_old:.3f}% of singledispatchmethod time)",
        )
        assert percent_to_old < self.speed_tolerance

    def test_dispatch_call_speed_with_kwarg(
        self,
        test_class_instance: TestSingleKwargDispatchPerformance.DispatchTestClass,
    ) -> None:
        """Test the performance of the dispatch_call method with a keyword argument.

        This test compares the speed of singlekwargdispatch.dispatch_call() with a keyword argument
        against a manual type check implementation and singledispatchmethod.

        Args:
            test_class_instance: A fixture providing a DispatchTestClass instance.
        """
        arg = 42

        # Define the performance test functions
        def call_single_kwarg_dispatch() -> None:
            test_class_instance.dispatch_kwarg(kwarg=arg)

        def call_normal_kwarg_dispatch() -> None:
            test_class_instance.normal_kwarg_method(kwarg=arg)

        def call_single_dispatch() -> None:
            # singledispatchmethod doesn't support kwarg dispatch, so we use arg
            test_class_instance.functools_dispatch(arg)

        # Calculate the mean time in microseconds for the singlekwargdispatch implementation
        new_time = timeit.timeit(call_single_kwarg_dispatch, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the manual type check implementation
        baseline_time = timeit.timeit(call_normal_kwarg_dispatch, number=self.timeit_runs)
        mean_baseline = baseline_time / self.timeit_runs * 1000000
        percent_to_baseline = (mean_new / mean_baseline) * 100

        # Calculate the mean time in microseconds for the singledispatchmethod implementation
        old_time = timeit.timeit(call_single_dispatch, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent_to_old = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nManual type check with kwarg: {mean_baseline:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"singledispatchmethod with arg: {mean_old:.3f} μs ({(mean_old / mean_baseline):.3f}% of manual type check time)",
        )
        print(
            f"singlekwargdispatch with kwarg: {mean_new:.3f} μs ({percent_to_baseline:.3f}% of manual type check time, {percent_to_old:.3f}% of singledispatchmethod time)",
        )
        assert percent_to_baseline < self.speed_tolerance * 2  # Allow more overhead for kwarg dispatch

    def test_edge_case_multiple_types(
        self,
        test_class_instance: TestSingleKwargDispatchPerformance.DispatchTestClass,
    ) -> None:
        """Test the performance with an edge case of multiple registered types.

        This test measures the performance overhead when dispatching with many registered types.

        Args:
            test_class_instance: A fixture providing a DispatchTestClass instance.
        """

        # Create a class with many registered types
        class ManyTypesDispatch:
            @singlekwargdispatch
            def dispatch(self, arg: Any, **kwargs) -> str:
                """Default implementation."""
                return f"Default: {arg}"

            @dispatch.register
            def _(self, arg: int, **kwargs) -> str:
                return f"Integer: {arg}"

            @dispatch.register(str)
            def _(self, arg: str, **kwargs) -> str:
                return f"String: {arg}"

            @dispatch.register(list)
            def _(self, arg: list, **kwargs) -> str:
                return f"List: {arg}"

            @dispatch.register(dict)
            def _(self, arg: dict, **kwargs) -> str:
                return f"Dict: {arg}"

            @dispatch.register(tuple)
            def _(self, arg: tuple, **kwargs) -> str:
                return f"Tuple: {arg}"

            @dispatch.register(set)
            def _(self, arg: set, **kwargs) -> str:
                return f"Set: {arg}"

            @dispatch.register(bool)
            def _(self, arg: bool, **kwargs) -> str:
                return f"Bool: {arg}"

            @dispatch.register(float)
            def _(self, arg: float, **kwargs) -> str:
                return f"Float: {arg}"

            @dispatch.register(complex)
            def _(self, arg: complex, **kwargs) -> str:
                return f"Complex: {arg}"

            @singledispatchmethod
            def functools_dispatch(self, arg: Any, **kwargs) -> str:
                """Default implementation."""
                return f"Default: {arg}"

            @functools_dispatch.register
            def _(self, arg: int, **kwargs) -> str:
                return f"Integer: {arg}"

            @functools_dispatch.register(str)
            def _(self, arg: str, **kwargs) -> str:
                return f"String: {arg}"

            @functools_dispatch.register(list)
            def _(self, arg: list, **kwargs) -> str:
                return f"List: {arg}"

            @functools_dispatch.register(dict)
            def _(self, arg: dict, **kwargs) -> str:
                return f"Dict: {arg}"

            @functools_dispatch.register(tuple)
            def _(self, arg: tuple, **kwargs) -> str:
                return f"Tuple: {arg}"

            @functools_dispatch.register(set)
            def _(self, arg: set, **kwargs) -> str:
                return f"Set: {arg}"

            @functools_dispatch.register(bool)
            def _(self, arg: bool, **kwargs) -> str:
                return f"Bool: {arg}"

            @functools_dispatch.register(float)
            def _(self, arg: float, **kwargs) -> str:
                return f"Float: {arg}"

            @functools_dispatch.register(complex)
            def _(self, arg: complex, **kwargs) -> str:
                return f"Complex: {arg}"

        many_types = ManyTypesDispatch()

        # Define the performance test functions
        def call_single_kwarg_dispatch() -> None:
            many_types.dispatch(42)
            many_types.dispatch("test")
            many_types.dispatch([1, 2, 3])
            many_types.dispatch({"a": 1})
            many_types.dispatch((1, 2))

        def call_single_dispatch() -> None:
            many_types.functools_dispatch(42)
            many_types.functools_dispatch("test")
            many_types.functools_dispatch([1, 2, 3])
            many_types.functools_dispatch({"a": 1})
            many_types.functools_dispatch((1, 2))

        # Calculate the mean time in microseconds for the singlekwargdispatch implementation
        new_time = timeit.timeit(call_single_kwarg_dispatch, number=self.timeit_runs // 100)
        mean_new = new_time / (self.timeit_runs // 100) * 1000000

        # Calculate the mean time in microseconds for the singledispatchmethod implementation
        old_time = timeit.timeit(call_single_dispatch, number=self.timeit_runs // 100)
        mean_old = old_time / (self.timeit_runs // 100) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nsingledispatchmethod with many types: {mean_old:.3f} μs")
        print(f"singlekwargdispatch with many types: {mean_new:.3f} μs ({percent:.3f}% of singledispatchmethod time)")
        assert percent < self.speed_tolerance * 1.5  # Allow more overhead for many types

    def test_edge_case_nested_dispatch(
        self,
        test_class_instance: TestSingleKwargDispatchPerformance.DispatchTestClass,
    ) -> None:
        """Test the performance with an edge case of nested dispatch.

        This test measures the performance overhead when using nested dispatch methods.

        Args:
            test_class_instance: A fixture providing a DispatchTestClass instance.
        """

        # Create a class with nested dispatch
        class NestedDispatch:
            @singlekwargdispatch
            def outer_dispatch(self, arg: Any, **kwargs):
                """Default outer implementation."""
                return self.inner_dispatch(arg)

            @outer_dispatch.register
            def _(self, arg: int, **kwargs) -> str:
                """Process an integer in outer."""
                return f"Outer Integer: {self.inner_dispatch(arg)}"

            @singlekwargdispatch
            def inner_dispatch(self, arg: Any, **kwargs) -> str:
                """Default inner implementation."""
                return f"Default: {arg}"

            @inner_dispatch.register
            def _(self, arg: int, **kwargs) -> str:
                """Process an integer in inner."""
                return f"Inner Integer: {arg}"

            @singledispatchmethod
            def outer_functools(self, arg: Any, **kwargs):
                """Default outer implementation."""
                return self.inner_functools(arg)

            @outer_functools.register
            def _(self, arg: int, **kwargs) -> str:
                """Process an integer in outer."""
                return f"Outer Integer: {self.inner_functools(arg)}"

            @singledispatchmethod
            def inner_functools(self, arg: Any, **kwargs) -> str:
                """Default inner implementation."""
                return f"Default: {arg}"

            @inner_functools.register
            def _(self, arg: int, **kwargs) -> str:
                """Process an integer in inner."""
                return f"Inner Integer: {arg}"

        nested = NestedDispatch()

        # Define the performance test functions
        def call_nested_kwarg_dispatch() -> None:
            nested.outer_dispatch(42)

        def call_nested_functools_dispatch() -> None:
            nested.outer_functools(42)

        # Calculate the mean time in microseconds for the nested singlekwargdispatch
        new_time = timeit.timeit(call_nested_kwarg_dispatch, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the nested singledispatchmethod
        old_time = timeit.timeit(call_nested_functools_dispatch, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNested singledispatchmethod: {mean_old:.3f} μs")
        print(f"Nested singlekwargdispatch: {mean_new:.3f} μs ({percent:.3f}% of nested singledispatchmethod time)")
        assert percent < self.speed_tolerance * 1.5  # Allow more overhead for nested dispatch


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
