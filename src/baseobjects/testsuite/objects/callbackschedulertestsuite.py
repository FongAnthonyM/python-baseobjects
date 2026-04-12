"""callbackschedulertestsuite.py
Base test suite for ~baseobjects.objects.CallbackScheduler and its subclasses.

This module contains the base test suite for ~baseobjects.objects.CallbackScheduler and its subclasses.
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
import asyncio
import copy
import pickle
from collections import deque
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...objects import CallbackScheduler
from ..bases import BaseObjectTestSuite


# Classes #
class CallbackSchedulerTestSuite(BaseObjectTestSuite):
    """Base test suite for children of ~baseobjects.objects.CallbackScheduler.

    This class provides common test functionality for child classes of ~baseobjects.objects.CallbackScheduler.
    """

    UnitTestClass: type[CallbackScheduler]

    # Fixtures #
    @pytest.fixture
    def test_object(self) -> CallbackScheduler:
        """Creates a test object.

        Returns:
            CallbackScheduler: A test object instance.
        """
        return self.UnitTestClass()

    # Tests #
    # Magic Methods #
    @pytest.mark.parametrize("is_async", [False, True])
    def test_add_schedule_function_operations(self, test_object: CallbackScheduler, is_async: bool) -> None:
        """Tests adding a schedule function.

        This test verifies that add_schedule_function and add_schedule_async_function correctly add
        functions to the scheduler registry.

        Args:
            test_object: A fixture providing a test object instance.
            is_async: Whether the function is async.
        """
        if is_async:

            async def my_func(*args: Any, **kwargs: Any) -> None:
                pass

            test_object.add_schedule_async_function("my_func", my_func)
            assert "my_func" in test_object.schedule_async.registry
        else:

            def my_func(*args: Any, **kwargs: Any) -> None:  # type: ignore[misc]
                pass

            test_object.add_schedule_function("my_func", my_func)
            assert "my_func" in test_object.schedule.registry

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: CallbackScheduler, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ("copy" or "method").
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)

    @pytest.mark.parametrize("method", ["deepcopy", "method"])
    def test_deepcopy_operations(self, test_object: CallbackScheduler, method: str) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ("deepcopy" or "method").
        """
        # Deep Copy Object
        if method == "deepcopy":
            obj_deepcopy = copy.deepcopy(test_object)
        else:
            obj_deepcopy = test_object.deepcopy()

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)

    # Pickling #
    def test_pickling(self, test_object: CallbackScheduler) -> None:
        """Tests pickling and unpickling of the object."""
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)

    # Functionality #
    def test_schedule_callbacks(self, test_object: CallbackScheduler) -> None:
        """Tests scheduling callbacks."""
        tasks: deque = deque()  # type: ignore[type-arg]
        call_count = 0

        def my_callback() -> None:
            nonlocal call_count
            call_count += 1

        test_object.callback_map.append((my_callback, tasks))
        test_object.schedule_callbacks()
        assert call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize("is_async_call", [False, True])
    async def test_schedule_async_callbacks_operations(
        self,
        test_object: CallbackScheduler,
        is_async_call: bool,
    ) -> None:
        """Tests scheduling async callbacks.

        This test verifies that schedule_async_callbacks and schedule_async_callbacks_async correctly schedule
        async callbacks.

        Args:
            test_object: A fixture providing a test object instance.
            is_async_call: Whether to use the async version of the scheduler method.
        """
        tasks: deque = deque()  # type: ignore[type-arg]
        fut = asyncio.Future()  # type: ignore[var-annotated]

        async def my_callback() -> None:
            await asyncio.sleep(0)
            fut.set_result(True)

        test_object.callback_map.append((my_callback, tasks))

        if is_async_call:
            await test_object.schedule_async_callbacks_async()
        else:
            test_object.schedule_async_callbacks()

        await asyncio.sleep(0)
        assert len(tasks) == 1

        await tasks[0]
        assert fut.result()
        await asyncio.sleep(0)
        assert len(tasks) == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize("is_async_call", [False, True])
    async def test_schedule_singleton_async_callbacks_operations(
        self,
        test_object: CallbackScheduler,
        is_async_call: bool,
    ) -> None:
        """Tests scheduling singleton async callbacks.

        This test verifies that schedule_singleton_async_callbacks and schedule_singleton_async_callbacks_async
        correctly schedule singleton async callbacks.

        Args:
            test_object: A fixture providing a test object instance.
            is_async_call: Whether to use the async version of the scheduler method.
        """
        tasks: deque = deque()  # type: ignore[type-arg]
        counter = 0

        async def my_callback() -> None:
            nonlocal counter
            counter += 1
            await asyncio.sleep(0.01)

        test_object.callback_map.append((my_callback, tasks))

        # Helper to call the method
        async def schedule() -> None:
            if is_async_call:
                await test_object.schedule_singleton_async_callbacks_async()
            else:
                test_object.schedule_singleton_async_callbacks()

        # Schedule once
        await schedule()
        assert len(tasks) == 1

        # Schedule again immediately (should not add another task because singleton)
        await schedule()
        assert len(tasks) == 1

        await tasks[0]
        assert counter == 1

        # After completion, task removes itself
        await asyncio.sleep(0)
        assert len(tasks) == 0

        # Schedule again (should add new task)
        await schedule()
        assert len(tasks) == 1
        await tasks[0]
        assert counter == 2
