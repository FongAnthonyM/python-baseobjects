"""baseperformancetestsuite.py
Base class for test suites which test the performance.
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
from pstats import Stats, f8, func_std_string
import timeit
from typing import Any

# Third-Party Packages #

# Local Packages #
from .basetestsuite import BaseTestSuite


# Definitions #
# Classes #
class BasePerformanceTestSuite(BaseTestSuite):
    """Base class for test suites which test performance.

    This class provides common functionality for performance test suites, including attributes for benchmarking.

    Attributes:
        _base_time: The time it takes to run a simple function call 10 million times.
        call_speed: The speed of a simple function call in microseconds.
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
    """

    # Attributes #
    _base_time: float = timeit.timeit(lambda: None, number=10000000)
    call_speed: float = _base_time / 10  # (_base_time / 10,000,000) * 1,000,000 simplified

    timeit_runs: int = 100000
    speed_tolerance: float = 150.0


# Performance Profiler
class StatsMicro(Stats):
    """A subclass of Stats from pstats that prints times in microseconds instead of seconds.

    This class overrides the print_stats and print_line methods to display times in microseconds, which is more
    appropriate for performance testing of small functions.
    """
    def print_stats(self, *amount: Any) -> "StatsMicro":
        """Print the statistics for the profiled code.

        Args:
            *amount: Optional restrictions on what to print.

        Returns:
            StatsMicro: Self for method chaining.
        """
        for filename in self.files:
            print(filename, file=self.stream)
        if self.files:
            print(file=self.stream)
        indent = " " * 8
        for func in self.top_level:
            print(indent, func_std_string(func), file=self.stream)

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

    def print_line(self, func: Any) -> None:  # hack: should print percentages
        """Print a single line of statistics.

        Args:
            func: The function for which to print statistics.
        """
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
