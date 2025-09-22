#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""callbackmanager_test.py
Test for the CallbackManager class.

This module provides tests for the CallbackManager class, which is a class that manages callbacks
and provides functionality for registering, calling, and scheduling callbacks.
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
import copy
import pickle
import asyncio
from typing import Any, Dict, Callable
from collections import deque

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects import CallbackManager, CallbackScheduler
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Classes #
class TestCallbackManager(BaseObjectTestSuite):
    """Test the CallbackManager class.

    This class tests the functionality of the CallbackManager class, which manages callbacks
    and provides functionality for registering, calling, and scheduling callbacks.
    """

    # Attributes #
    TestClass = CallbackManager

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> CallbackManager:
        """Create a test object.

        Returns:
            CallbackManager: A test CallbackManager instance.
        """
        return self.TestClass()

    @pytest.fixture
    def test_object_with_callbacks(self) -> CallbackManager:
        """Create a test object with some callbacks registered.

        Returns:
            CallbackManager: A test CallbackManager instance with callbacks.
        """

        def callback1(*args, **kwargs):
            return "callback1 called"

        def callback2(*args, **kwargs):
            return "callback2 called"

        manager = self.TestClass()
        manager.register_callback("callback1", callback1)
        manager.register_callback("callback2", callback2)
        return manager

    # Tests
    def test_copy(self, test_object: CallbackManager) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.callbacks == test_object.callbacks
        assert obj_copy.callbacks_async == test_object.callbacks_async
        assert obj_copy.tasks == test_object.tasks

    def test_copy_method(self, test_object: CallbackManager) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.callbacks == test_object.callbacks
        assert obj_copy.callbacks_async == test_object.callbacks_async
        assert obj_copy.tasks == test_object.tasks

    def test_deepcopy(self, test_object: CallbackManager) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Deep Copy Object
        obj_deepcopy = copy.deepcopy(test_object)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.callbacks == test_object.callbacks
        assert obj_deepcopy.callbacks is not test_object.callbacks
        assert obj_deepcopy.callbacks_async == test_object.callbacks_async
        assert obj_deepcopy.callbacks_async is not test_object.callbacks_async
        assert obj_deepcopy.tasks == test_object.tasks
        assert obj_deepcopy.tasks is not test_object.tasks

    def test_deepcopy_method(self, test_object: CallbackManager) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Deep Copy Object
        obj_deepcopy = test_object.deepcopy()

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.callbacks == test_object.callbacks
        assert obj_deepcopy.callbacks is not test_object.callbacks
        assert obj_deepcopy.callbacks_async == test_object.callbacks_async
        assert obj_deepcopy.callbacks_async is not test_object.callbacks_async
        assert obj_deepcopy.tasks == test_object.tasks
        assert obj_deepcopy.tasks is not test_object.tasks

    def test_pickling(self, test_object: CallbackManager) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)
        assert unpickled.callbacks == test_object.callbacks
        assert unpickled.callbacks_async == test_object.callbacks_async
        assert unpickled.tasks == test_object.tasks

    # CallbackManager Specific Tests
    def test_register_callback(self, test_object: CallbackManager) -> None:
        """Test registering a callback.

        This test verifies that a callback can be registered and retrieved.
        """

        # Define a test callback
        def test_callback(*args, **kwargs):
            return "test callback called"

        # Register the callback
        test_object.register_callback("test_callback", test_callback)

        # Validate
        assert "test_callback" in test_object.callbacks
        assert test_object.callbacks["test_callback"] == test_callback

    def test_register_callbacks(self, test_object: CallbackManager) -> None:
        """Test registering multiple callbacks.

        This test verifies that multiple callbacks can be registered and retrieved.
        """

        # Define test callbacks
        def callback1(*args, **kwargs):
            return "callback1 called"

        def callback2(*args, **kwargs):
            return "callback2 called"

        # Register callbacks
        callbacks = {"callback1": callback1, "callback2": callback2}
        test_object.register_callbacks(callbacks)

        # Validate
        assert "callback1" in test_object.callbacks
        assert "callback2" in test_object.callbacks
        assert test_object.callbacks["callback1"] == callback1
        assert test_object.callbacks["callback2"] == callback2

    def test_call_callback(self, test_object_with_callbacks: CallbackManager) -> None:
        """Test calling a registered callback.

        This test verifies that a registered callback can be called and returns the expected result.
        """
        # Call the callback
        result = test_object_with_callbacks.call_callback("callback1")

        # Validate
        assert result == "callback1 called"

    def test_call_callback_with_args(self, test_object: CallbackManager) -> None:
        """Test calling a callback with arguments.

        This test verifies that a callback can be called with arguments and they are passed correctly.
        """

        # Define a test callback that uses arguments
        def test_callback(arg1, arg2, kwarg1=None, kwarg2=None):
            return f"{arg1}, {arg2}, {kwarg1}, {kwarg2}"

        # Register the callback
        test_object.register_callback("test_callback", test_callback)

        # Call the callback with arguments
        result = test_object.call_callback("test_callback", "value1", "value2", kwarg1="key1", kwarg2="key2")

        # Validate
        assert result == "value1, value2, key1, key2"

    def test_register_conditional_callback(self, test_object: CallbackManager) -> None:
        """Test registering a conditional callback.

        This test verifies that a conditional callback can be registered and retrieved.
        """

        # Define test callback and condition
        def test_callback(*args, **kwargs):
            return "test callback called"

        def test_condition(*args, **kwargs):
            return True

        # Register the conditional callback
        test_object.register_conditional_callback("test_conditional", test_callback, test_condition)

        # Validate
        assert "test_conditional" in test_object.conditional_callbacks
        assert callable(test_object.conditional_callbacks["test_conditional"])

    def test_call_conditional(self, test_object: CallbackManager) -> None:
        """Test calling a callback conditionally.

        This test verifies that a callback is only called when the condition is True.
        """
        # Define test callback and conditions
        result = []

        def test_callback(*args, **kwargs):
            result.append("test callback called")
            return "test callback called"

        def true_condition(*args, **kwargs):
            return True

        def false_condition(*args, **kwargs):
            return False

        # Test with true condition
        test_object.call_conditional(true_condition, test_callback)
        assert len(result) == 1
        assert result[0] == "test callback called"

        # Clear result for next test
        result.clear()

        # Test with false condition
        test_object.call_conditional(false_condition, test_callback)
        assert len(result) == 0

    def test_empty_callbacks(self, test_object: CallbackManager) -> None:
        """Test behavior with empty callbacks.

        This test verifies that calling a non-existent callback raises a KeyError.
        """
        # Attempt to call a non-existent callback
        with pytest.raises(KeyError):
            test_object.call_callback("non_existent_callback")

    def test_overwrite_callback(self, test_object_with_callbacks: CallbackManager) -> None:
        """Test overwriting an existing callback.

        This test verifies that registering a callback with an existing name overwrites the previous callback.
        """

        # Define a new callback
        def new_callback(*args, **kwargs):
            return "new callback called"

        # Register the new callback with an existing name
        test_object_with_callbacks.register_callback("callback1", new_callback)

        # Call the callback
        result = test_object_with_callbacks.call_callback("callback1")

        # Validate
        assert result == "new callback called"

    # Async Tests
    @pytest.mark.asyncio
    async def test_register_async_callback(self, test_object: CallbackManager) -> None:
        """Test registering an async callback.

        This test verifies that an async callback can be registered and retrieved.
        """

        # Define a test async callback
        async def test_async_callback(*args, **kwargs):
            return "async callback called"

        # Register the async callback
        test_object.register_callback("test_async_callback", test_async_callback, is_async=True)

        # Validate
        assert "test_async_callback" in test_object.callbacks_async
        assert test_object.callbacks_async["test_async_callback"] == test_async_callback

    @pytest.mark.asyncio
    async def test_call_callback_async(self, test_object: CallbackManager) -> None:
        """Test calling an async callback.

        This test verifies that an async callback can be called and returns the expected result.
        """

        # Define a test async callback
        async def test_async_callback(*args, **kwargs):
            return "async callback called"

        # Register the async callback
        test_object.register_callback("test_async_callback", test_async_callback, is_async=True)

        # Call the async callback
        result = await test_object.call_callback_async("test_async_callback")

        # Validate
        assert result == "async callback called"

    @pytest.mark.asyncio
    async def test_call_async(self, test_object: CallbackManager) -> None:
        """Test the call_async method.

        This test verifies that the call_async method correctly calls an async function.
        """

        # Define a test async function
        async def test_async_function(*args, **kwargs):
            return "async function called"

        # Call the async function
        result = await test_object.call_async(test_async_function)

        # Validate
        assert result == "async function called"

    @pytest.mark.asyncio
    async def test_call_conditional_async(self, test_object: CallbackManager) -> None:
        """Test calling an async callback conditionally.

        This test verifies that an async callback is only called when the condition is True.
        """
        # Define test async callback and conditions
        result = []

        async def test_async_callback(*args, **kwargs):
            result.append("async callback called")
            return "async callback called"

        async def true_condition_async(*args, **kwargs):
            return True

        async def false_condition_async(*args, **kwargs):
            return False

        # Test with true condition
        await test_object.call_conditional_async(true_condition_async, test_async_callback)
        assert len(result) == 1
        assert result[0] == "async callback called"

        # Clear result for next test
        result.clear()

        # Test with false condition
        await test_object.call_conditional_async(false_condition_async, test_async_callback)
        assert len(result) == 0

    # Scheduler Tests
    def test_create_scheduler(self, test_object: CallbackManager) -> None:
        """Test creating a scheduler.

        This test verifies that a scheduler can be created and has the expected type.
        """
        # Create a scheduler
        scheduler = test_object.create_scheduler()

        # Validate
        assert isinstance(scheduler, CallbackScheduler)

    def test_register_scheduler(self, test_object: CallbackManager) -> None:
        """Test registering a scheduler.

        This test verifies that a scheduler can be registered and retrieved.
        """
        # Register a scheduler
        test_object.register_scheduler("test_scheduler")

        # Validate
        assert "test_scheduler" in test_object.schedulers
        assert isinstance(test_object.schedulers["test_scheduler"], CallbackScheduler)

    def test_register_scheduler_callback(self, test_object: CallbackManager) -> None:
        """Test registering a callback with a scheduler.

        This test verifies that a callback can be registered with a scheduler.
        """
        # Register a scheduler
        test_object.register_scheduler("test_scheduler")

        # Register the callback with the scheduler
        test_object.register_scheduler_callback("test_callback", "test_scheduler")

        # Validate
        # Check that the callbacks are registered
        assert "test_callback" in test_object.callbacks
        assert "test_callback" in test_object.callbacks_async
        # Check that the task queue is created
        assert "test_callback" in test_object.tasks

    # Task Management Tests
    @pytest.mark.asyncio
    async def test_call_while_condition_async(self, test_object: CallbackManager) -> None:
        """Test calling a callback while a condition is true.

        This test verifies that a callback is called repeatedly while a condition is true.
        """
        # Define test async callback and condition
        call_count = 0

        async def test_async_callback(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args, **kwargs):
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Call while condition
        await test_object.call_while_condition_async(condition_async, test_async_callback)

        # Validate
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_join_tasks_async(self, test_object: CallbackManager) -> None:
        """Test joining tasks asynchronously.

        This test verifies that join_tasks_async waits for all tasks to complete.
        """

        # Create some tasks
        async def async_task():
            await asyncio.sleep(0.1)
            return "task completed"

        task1 = asyncio.create_task(async_task())
        task2 = asyncio.create_task(async_task())

        # Add tasks to the manager
        test_object.tasks["test_tasks"] = deque([task1, task2])

        # Join tasks
        await test_object.join_tasks_async()

        # Validate
        assert task1.done()
        assert task2.done()

    @pytest.mark.asyncio
    async def test_cancel_tasks(self, test_object: CallbackManager) -> None:
        """Test cancelling tasks.

        This test verifies that cancel_tasks cancels all tasks.
        """
        # Create a task that can be cancelled
        cancel_requested = False

        async def cancellable_task():
            nonlocal cancel_requested
            try:
                while not cancel_requested:
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                cancel_requested = True
                raise

        # Create the task and add it to the manager
        task = asyncio.create_task(cancellable_task())
        test_object.tasks["test_tasks"] = deque([task])

        # Wait a bit to ensure the task is running
        await asyncio.sleep(0.2)

        # Cancel tasks
        test_object.cancel_tasks()

        # Wait for the task to be fully cancelled
        try:
            await asyncio.wait_for(task, timeout=0.5)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass

        # Validate
        assert cancel_requested

        # Clean up any remaining tasks
        for t in [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]:
            t.cancel()
        await asyncio.gather(
            *[t for t in asyncio.all_tasks() if t is not asyncio.current_task()], return_exceptions=True
        )

    def test_format_conditional_callback(self, test_object: CallbackManager) -> None:
        """Test formatting a conditional callback.

        This test verifies that format_conditional_callback correctly formats the callback, condition, and caller.
        """

        # Define test callback, condition, and caller
        def test_callback(*args, **kwargs):
            return "test callback called"

        def test_condition(*args, **kwargs):
            return True

        def test_caller(condition, callback, *args, **kwargs):
            if condition():
                return callback()
            return None

        # Format the conditional callback
        callback, condition, caller = test_object.format_conditional_callback(
            test_callback,
            test_condition,
            test_caller,
            callback_kwargs={"key1": "value1"},
            condition_kwargs={"key2": "value2"},
            caller_kwargs={"key3": "value3"},
        )

        # Validate
        assert callable(callback)
        assert callable(condition)
        assert callable(caller)
        # Test that the callback works
        assert caller(condition, callback) == "test callback called"

    def test_create_conditional_callback(self, test_object: CallbackManager) -> None:
        """Test creating a conditional callback.

        This test verifies that create_conditional_callback correctly creates a callable that combines
        the condition and callback.
        """
        # Define test callback, condition, and caller
        result = []

        def test_callback(*args, **kwargs):
            result.append("test callback called")
            return "test callback called"

        def test_condition(*args, **kwargs):
            return True

        def test_caller(condition, callback, *args, **kwargs):
            if condition():
                return callback()
            return None

        # Create the conditional callback
        conditional_callback = test_object.create_conditional_callback(test_callback, test_condition, test_caller)

        # Validate
        assert callable(conditional_callback)
        # Test that the conditional callback works
        conditional_callback()
        assert len(result) == 1
        assert result[0] == "test callback called"

    def test_create_conditional_scheduler(self, test_object: CallbackManager) -> None:
        """Test creating a conditional scheduler.

        This test verifies that create_conditional_scheduler correctly creates a scheduler with
        the specified conditional callbacks.
        """

        # Define test callbacks and conditions
        async def test_callback1(*args, **kwargs):
            return "test callback1 called"

        async def test_callback2(*args, **kwargs):
            return "test callback2 called"

        async def test_condition(*args, **kwargs):
            return True

        # Register conditional callbacks with is_async=True
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)

        # Create a conditional scheduler
        scheduler = test_object.create_conditional_scheduler(["test_conditional1", "test_conditional2"])

        # Validate
        assert isinstance(scheduler, CallbackScheduler)
        assert len(scheduler.callback_map) == 2
        # Check that the callbacks in the scheduler are the ones we registered
        for callback, _ in scheduler.callback_map:
            assert callable(callback)

    def test_register_conditional_callbacks(self, test_object: CallbackManager) -> None:
        """Test registering multiple conditional callbacks.

        This test verifies that register_conditional_callbacks correctly registers multiple callbacks.
        """

        # Define test callbacks and conditions
        def test_callback1(*args, **kwargs):
            return "test callback1 called"

        def test_callback2(*args, **kwargs):
            return "test callback2 called"

        def test_condition(*args, **kwargs):
            return True

        # Register conditional callbacks
        callbacks = [
            ("test_conditional1", {"callback": test_callback1, "condition": test_condition}),
            ("test_conditional2", {"callback": test_callback2, "condition": test_condition}),
        ]
        test_object.register_conditional_callbacks(callbacks)

        # Validate
        assert "test_conditional1" in test_object.conditional_callbacks
        assert "test_conditional2" in test_object.conditional_callbacks
        assert callable(test_object.conditional_callbacks["test_conditional1"])
        assert callable(test_object.conditional_callbacks["test_conditional2"])

    def test_register_conditional_scheduler(self, test_object: CallbackManager) -> None:
        """Test registering a conditional scheduler.

        This test verifies that register_conditional_scheduler correctly registers a scheduler
        with the specified conditional callbacks.
        """

        # Define test callbacks and conditions
        async def test_callback1(*args, **kwargs):
            return "test callback1 called"

        async def test_callback2(*args, **kwargs):
            return "test callback2 called"

        async def test_condition(*args, **kwargs):
            return True

        # Register conditional callbacks with is_async=True
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)

        # Register a conditional scheduler
        test_object.register_conditional_scheduler(
            "test_conditional_scheduler", condition_names=["test_conditional1", "test_conditional2"]
        )

        # Validate
        assert "test_conditional_scheduler" in test_object.schedulers
        assert isinstance(test_object.schedulers["test_conditional_scheduler"], CallbackScheduler)
        assert len(test_object.schedulers["test_conditional_scheduler"].callback_map) == 2

    def test_map_conditionals_to_scheduler(self, test_object: CallbackManager) -> None:
        """Test mapping conditional callbacks to a scheduler.

        This test verifies that map_conditionals_to_scheduler correctly adds conditional callbacks
        to an existing scheduler.
        """

        # Define test callbacks and conditions
        def test_callback1(*args, **kwargs):
            return "test callback1 called"

        def test_callback2(*args, **kwargs):
            return "test callback2 called"

        def test_condition(*args, **kwargs):
            return True

        # Register conditional callbacks and a scheduler
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)
        test_object.register_scheduler("test_scheduler")

        # Map conditionals to the scheduler
        test_object.map_conditionals_to_scheduler("test_scheduler", ["test_conditional1", "test_conditional2"])

        # Validate
        assert len(test_object.schedulers["test_scheduler"].callback_map) == 2
        # Check that task queues were created
        assert "test_conditional1_conditional_caller" in test_object.tasks
        assert "test_conditional2_conditional_caller" in test_object.tasks

    def test_call_while_condition(self, test_object: CallbackManager) -> None:
        """Test calling a callback while a condition is true.

        This test verifies that call_while_condition correctly calls a callback repeatedly
        while a condition is true.
        """
        # Define test callback and condition
        call_count = 0

        def test_callback(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        def condition(*args, **kwargs):
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Call while condition
        test_object.call_while_condition(condition, test_callback)

        # Validate
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_call_while_condition_task_async(self, test_object: CallbackManager) -> None:
        """Test calling a task-returning callback while a condition is true.

        This test verifies that call_while_condition_task_async correctly calls a callback
        that returns a task repeatedly while a condition is true.
        """
        # Define test async callback and condition
        call_count = 0
        tasks = deque()

        async def test_async_callback(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return asyncio.create_task(asyncio.sleep(0.1))

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args, **kwargs):
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Call while condition
        await test_object.call_while_condition_task_async(condition_async, test_async_callback, tasks)

        # Validate
        assert call_count == 2
        assert len(tasks) == 0  # All tasks should be completed

    @pytest.mark.asyncio
    async def test_enqueue_call_while_condition_async(self, test_object: CallbackManager) -> None:
        """Test enqueueing and calling a callback while a condition is true.

        This test verifies that enqueue_call_while_condition_async correctly enqueues and calls
        a callback repeatedly while a condition is true.
        """
        # Define test async callback and condition
        call_count = 0
        tasks = deque()

        async def test_async_callback(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args, **kwargs):
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Call while condition
        await test_object.enqueue_call_while_condition_async(condition_async, test_async_callback, tasks)

        # Validate
        assert call_count == 2
        assert len(tasks) == 0  # All tasks should be completed

    @pytest.mark.asyncio
    async def test_enqueue_call_while_condition_task_async(self, test_object: CallbackManager) -> None:
        """Test enqueueing and calling a task-returning callback while a condition is true.

        This test verifies that enqueue_call_while_condition_task_async correctly enqueues and calls
        a callback that returns a task repeatedly while a condition is true.
        """
        # Define test async callback and condition
        call_count = 0
        tasks = deque()

        async def test_async_callback(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return asyncio.create_task(asyncio.sleep(0.1))

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args, **kwargs):
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Call while condition
        await test_object.enqueue_call_while_condition_task_async(condition_async, test_async_callback, tasks)

        # Validate
        assert call_count == 2
        assert len(tasks) == 0  # All tasks should be completed

    @pytest.mark.asyncio
    async def test_join_tasks(self, test_object: CallbackManager) -> None:
        """Test joining tasks synchronously.

        This test verifies that join_tasks waits for all tasks to complete.
        """
        # Create some completed tasks
        task1 = asyncio.Future()
        task1.set_result("task1 completed")
        task2 = asyncio.Future()
        task2.set_result("task2 completed")

        # Add tasks to the manager
        test_object.tasks["test_tasks"] = deque([task1, task2])

        # Join tasks
        test_object.join_tasks()

        # Validate
        assert task1.done()
        assert task2.done()

    def test_true_condition(self) -> None:
        """Test the true_condition static method.

        This test verifies that true_condition always returns True.
        """
        # Call the method
        result = CallbackManager.true_condition()

        # Validate
        assert result is True

    @pytest.mark.asyncio
    async def test_true_condition_async(self) -> None:
        """Test the true_condition_async static method.

        This test verifies that true_condition_async always returns True.
        """
        # Call the method
        result = await CallbackManager.true_condition_async()

        # Validate
        assert result is True


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
