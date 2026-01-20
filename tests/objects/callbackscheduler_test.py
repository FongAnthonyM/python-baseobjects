#!/usr/bin/env python
"""callbackscheduler_coverage_test.py
Test for the CallbackScheduler class to improve coverage.
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
from collections import deque
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.objects import CallbackScheduler
from baseobjects.testsuite.objects.callbackschedulertestsuite import CallbackSchedulerTestSuite


# Classes #
class TestCallbackScheduler(CallbackSchedulerTestSuite):
    """Tests the CallbackScheduler class."""

    UnitTestClass = CallbackScheduler

    def test_init_no_construct(self) -> None:
        """Tests initialization without construction."""
        obj = self.UnitTestClass(init=False)
        assert obj.callback_map == []

    def test_construct_with_strings(self) -> None:
        """Tests construction with string arguments for methods."""
        scheduler = self.UnitTestClass(schedule="schedule_callbacks", schedule_async="schedule_async_callbacks")
        assert scheduler.schedule.selected == "schedule_callbacks"
        assert scheduler.schedule_async.selected == "schedule_async_callbacks"

    def test_construct_with_callables(self) -> None:
        """Tests construction with callable arguments."""

        def my_schedule(*args: Any, **kwargs: Any) -> None:
            pass

        def my_schedule_async(*args: Any, **kwargs: Any) -> None:
            pass

        scheduler = self.UnitTestClass(schedule=my_schedule, schedule_async=my_schedule_async)
        assert my_schedule.__name__ in scheduler.schedule.registry
        assert my_schedule_async.__name__ in scheduler.schedule_async.registry

    def test_construct_with_callback_map(self) -> None:
        """Tests construction with a callback map."""
        tasks: deque[Any] = deque()

        def my_callback(*args: Any, **kwargs: Any) -> None:
            pass

        callback_map = [(my_callback, tasks)]

        scheduler = self.UnitTestClass(callback_map=callback_map)
        assert len(scheduler.callback_map) == 1
        assert scheduler.callback_map[0][0] == my_callback


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
