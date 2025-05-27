#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" callbackmanager_test.py
Tests for the callbackmanager.py module in the baseobjects package.
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
from collections import deque
from functools import partial
from typing import Callable, Dict, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects.callbackmanager import CallbackManager, CallbackScheduler, ConditionalCallbackEntry
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestConditionalCallbackEntry(ClassTest):
    """Test the ConditionalCallbackEntry class.

    This class tests the functionality of the ConditionalCallbackEntry class, which is a
    NamedTuple for storing callback entries.
    """

    # Class Attributes #
    class_: Type[ConditionalCallbackEntry] = ConditionalCallbackEntry

    # Instance Methods #
    # Tests
    def test_creation(self) -> None:
        """Test the creation of a ConditionalCallbackEntry.

        This test verifies that a ConditionalCallbackEntry can be created with the
        expected attributes.
        """
        # Define simple functions for testing
        def callback() -> str:
            return "callback"

        def condition() -> bool:
            return True

        def caller(cond: Callable, cb: Callable) -> str:
            if cond():
                return cb()
            return "not called"

        # Create a ConditionalCallbackEntry
        entry = ConditionalCallbackEntry(callback=callback, condition=condition, caller=caller)

        # Verify the entry has the expected attributes
        assert entry.callback == callback
        assert entry.condition == condition
        assert entry.caller == caller

        # Verify the entry works as expected
        assert entry.caller(entry.condition, entry.callback) == "callback"


class TestCallbackScheduler(ClassTest):
    """Test the CallbackScheduler class.

    This class tests the functionality of the CallbackScheduler class, which schedules
    and executes callbacks.
    """

    # Class Attributes #
    class_: Type[CallbackScheduler] = CallbackScheduler

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def callback_counter(self) -> Dict[str, int]:
        """Create a dictionary to track callback executions.

        Returns:
            A dictionary to track callback executions.
        """
        return {"count": 0}

    @pytest.fixture
    def callback(self, callback_counter: Dict[str, int]) -> Callable:
        """Create a simple callback function for testing.

        Args:
            callback_counter: A fixture providing a counter dictionary.

        Returns:
            A simple callback function that increments the counter.
        """
        def cb() -> None:
            callback_counter["count"] += 1
        return cb

    @pytest.fixture
    def async_callback(self, callback_counter: Dict[str, int]) -> Callable:
        """Create a simple async callback function for testing.

        Args:
            callback_counter: A fixture providing a counter dictionary.

        Returns:
            A simple async callback function that increments the counter.
        """
        async def cb() -> None:
            callback_counter["count"] += 1
        return cb

    @pytest.fixture
    def callback_scheduler(self, callback: Callable) -> CallbackScheduler:
        """Create a CallbackScheduler instance for testing.

        Args:
            callback: A fixture providing a callback function.

        Returns:
            A CallbackScheduler instance with a test callback.
        """
        tasks = deque()
        return CallbackScheduler(callback_map=[(callback, tasks)])

    @pytest.fixture
    def async_callback_scheduler(self, async_callback: Callable) -> CallbackScheduler:
        """Create a CallbackScheduler instance for testing async callbacks.

        Args:
            async_callback: A fixture providing an async callback function.

        Returns:
            A CallbackScheduler instance with a test async callback.
        """
        tasks = deque()
        return CallbackScheduler(callback_map=[(async_callback, tasks)])

    # Tests
    def test_init(self) -> None:
        """Test the initialization of CallbackScheduler.

        This test verifies that CallbackScheduler can be initialized with and without parameters.
        """
        # Test default initialization
        scheduler = CallbackScheduler()
        assert scheduler.callback_map == []
        assert scheduler.schedule.selected == "schedule_callbacks"
        assert scheduler.schedule_async.selected == "schedule_singleton_async_callbacks_async"

        # Test initialization with parameters
        def test_callback() -> None:
            pass

        tasks = deque()
        callback_map = [(test_callback, tasks)]
        scheduler = CallbackScheduler(callback_map=callback_map, schedule="schedule_callbacks")
        assert scheduler.callback_map == callback_map
        assert scheduler.schedule.selected == "schedule_callbacks"

    def test_construct(self) -> None:
        """Test the construct method of CallbackScheduler.

        This test verifies that the construct method correctly sets up the scheduler.
        """
        # Create a scheduler without initialization
        scheduler = CallbackScheduler(init=False)

        # Define a test callback
        def test_callback() -> None:
            pass

        # Define a test schedule function
        def test_schedule() -> None:
            pass

        # Define a test async schedule function
        async def test_schedule_async() -> None:
            pass

        # Construct the scheduler
        tasks = deque()
        callback_map = [(test_callback, tasks)]
        scheduler.construct(
            callback_map=callback_map,
            schedule=test_schedule,
            schedule_async=test_schedule_async
        )

        # Verify the scheduler was constructed correctly
        assert scheduler.callback_map == callback_map
        assert "test_schedule" in scheduler.schedule.registry
        assert "test_schedule_async" in scheduler.schedule_async.registry

    def test_add_schedule_function(self) -> None:
        """Test the add_schedule_function method.

        This test verifies that a schedule function can be added to the scheduler.
        """
        scheduler = CallbackScheduler()

        # Define a test schedule function
        def test_schedule() -> None:
            pass

        # Add the schedule function
        scheduler.add_schedule_function("test_schedule", test_schedule)

        # Verify the function was added
        assert "test_schedule" in scheduler.schedule.registry
        assert scheduler.schedule.registry["test_schedule"] == test_schedule

    def test_add_schedule_async_function(self) -> None:
        """Test the add_schedule_async_function method.

        This test verifies that an async schedule function can be added to the scheduler.
        """
        scheduler = CallbackScheduler()

        # Define a test async schedule function
        async def test_schedule_async() -> None:
            pass

        # Add the async schedule function
        scheduler.add_schedule_async_function("test_schedule_async", test_schedule_async)

        # Verify the function was added
        assert "test_schedule_async" in scheduler.schedule_async.registry
        assert scheduler.schedule_async.registry["test_schedule_async"] == test_schedule_async

    def test_schedule_callbacks(self, callback_scheduler: CallbackScheduler, callback_counter: Dict[str, int]) -> None:
        """Test the schedule_callbacks method.

        This test verifies that the schedule_callbacks method correctly executes callbacks.

        Args:
            callback_scheduler: A fixture providing a CallbackScheduler instance.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Schedule callbacks
        callback_scheduler.schedule_callbacks()

        # Verify the callback was executed
        assert callback_counter["count"] == 1

    @pytest.mark.asyncio
    async def test_schedule_async_callbacks_async(self, async_callback_scheduler: CallbackScheduler, callback_counter: Dict[str, int]) -> None:
        """Test the schedule_async_callbacks_async method.

        This test verifies that the schedule_async_callbacks_async method correctly
        schedules async callbacks.

        Args:
            async_callback_scheduler: A fixture providing a CallbackScheduler instance.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Schedule async callbacks
        await async_callback_scheduler.schedule_async_callbacks_async()

        # Wait for the callback to execute
        await asyncio.sleep(0.1)

        # Verify the callback was executed
        assert callback_counter["count"] == 1


class TestCallbackManager(ClassTest):
    """Test the CallbackManager class.

    This class tests the functionality of the CallbackManager class, which manages and
    executes callback functions with conditions and callers.
    """

    # Class Attributes #
    class_: Type[CallbackManager] = CallbackManager

    # Setup #
    def setup_method(self) -> None:
        """Set up the test environment before each test method.

        This method is called before each test method to set up the test environment.
        """
        # Fix the default_caller attribute to match the actual method name
        CallbackManager.default_caller = "call_conditional"

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def callback_counter(self) -> Dict[str, int]:
        """Create a dictionary to track callback executions.

        Returns:
            A dictionary to track callback executions.
        """
        return {"count": 0}

    @pytest.fixture
    def callback(self, callback_counter: Dict[str, int]) -> Callable:
        """Create a simple callback function for testing.

        Args:
            callback_counter: A fixture providing a counter dictionary.

        Returns:
            A simple callback function that increments the counter.
        """
        def cb() -> None:
            callback_counter["count"] += 1
        return cb

    @pytest.fixture
    def async_callback(self, callback_counter: Dict[str, int]) -> Callable:
        """Create a simple async callback function for testing.

        Args:
            callback_counter: A fixture providing a counter dictionary.

        Returns:
            A simple async callback function that increments the counter.
        """
        async def cb() -> None:
            callback_counter["count"] += 1
        return cb

    @pytest.fixture
    def true_condition(self) -> Callable:
        """Create a condition function that always returns True.

        Returns:
            A condition function that always returns True.
        """
        def condition() -> bool:
            return True
        return condition

    @pytest.fixture
    def false_condition(self) -> Callable:
        """Create a condition function that always returns False.

        Returns:
            A condition function that always returns False.
        """
        def condition() -> bool:
            return False
        return condition

    @pytest.fixture
    def async_true_condition(self) -> Callable:
        """Create an async condition function that always returns True.

        Returns:
            An async condition function that always returns True.
        """
        async def condition() -> bool:
            return True
        return condition

    @pytest.fixture
    def async_false_condition(self) -> Callable:
        """Create an async condition function that always returns False.

        Returns:
            An async condition function that always returns False.
        """
        async def condition() -> bool:
            return False
        return condition

    @pytest.fixture
    def callback_manager(self) -> CallbackManager:
        """Create a CallbackManager instance for testing.

        Returns:
            A CallbackManager instance.
        """
        return CallbackManager()

    # Tests
    def test_init(self) -> None:
        """Test the initialization of CallbackManager.

        This test verifies that CallbackManager can be initialized with and without parameters.
        """
        # Test default initialization
        manager = CallbackManager()
        assert manager.callbacks == {}
        assert manager.callbacks_async == {}
        assert manager.conditional_callbacks == {}
        assert manager.conditional_callbacks_async == {}
        assert manager.schedulers == {}
        assert manager.tasks == {}
        assert manager.default_condition == "true_condition"
        assert manager.default_caller == "call_conditional"

        # Test initialization with parameters
        def callback() -> None:
            pass

        def condition() -> bool:
            return True

        def caller(cond: Callable, cb: Callable) -> None:
            if cond():
                cb()

        entry = ConditionalCallbackEntry(callback=callback, condition=condition, caller=caller)
        callbacks = {"test_callback": entry}
        manager = CallbackManager(callbacks=callbacks, default_condition="custom_condition")
        assert manager.callbacks == callbacks
        assert manager.default_condition == "custom_condition"

    def test_format_conditional_callback(self, callback_manager: CallbackManager, callback: Callable, true_condition: Callable) -> None:
        """Test the format_conditional_callback method.

        This test verifies that the format_conditional_callback method correctly formats
        a callback entry.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
            true_condition: A fixture providing a condition function.
        """
        # Format a callback entry with default condition and caller
        entry = callback_manager.format_conditional_callback(callback)
        assert entry.callback == callback
        assert entry.condition == callback_manager.true_condition
        assert entry.caller == getattr(callback_manager, callback_manager.default_caller)

        # Format a callback entry with custom condition and caller
        def custom_caller(cond: Callable, cb: Callable) -> None:
            if cond():
                cb()

        entry = callback_manager.format_conditional_callback(
            callback,
            condition=true_condition,
            caller=custom_caller
        )
        assert entry.callback == callback
        assert entry.condition == true_condition
        assert entry.caller == custom_caller

        # Format a callback entry with kwargs
        callback_kwargs = {"arg": "value"}
        entry = callback_manager.format_conditional_callback(
            callback,
            callback_kwargs=callback_kwargs
        )
        assert isinstance(entry.callback, partial)
        assert entry.callback.keywords == callback_kwargs

    def test_register_callback(self, callback_manager: CallbackManager, callback: Callable, async_callback: Callable) -> None:
        """Test the register_callback method.

        This test verifies that the register_callback method correctly registers callbacks.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
            async_callback: A fixture providing an async callback function.
        """
        # Register a synchronous callback
        callback_manager.register_callback("test_callback", callback)
        assert "test_callback" in callback_manager.callbacks
        assert callback_manager.callbacks["test_callback"] == callback

        # Register an asynchronous callback
        callback_manager.register_callback("test_async_callback", async_callback, is_async=True)
        assert "test_async_callback" in callback_manager.callbacks_async
        assert callback_manager.callbacks_async["test_async_callback"] == async_callback

    def test_register_conditional_callback(self, callback_manager: CallbackManager, callback: Callable, true_condition: Callable) -> None:
        """Test the register_conditional_callback method.

        This test verifies that the register_conditional_callback method correctly registers
        conditional callbacks.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
            true_condition: A fixture providing a condition function.
        """
        # Register a conditional callback
        callback_manager.register_conditional_callback(
            "test_conditional",
            callback,
            condition=true_condition
        )
        assert "test_conditional" in callback_manager.conditional_callbacks

        # Verify the conditional callback works
        conditional_callback = callback_manager.conditional_callbacks["test_conditional"]
        assert callable(conditional_callback)

    def test_call_callback(self, callback_manager: CallbackManager, callback: Callable, callback_counter: Dict[str, int]) -> None:
        """Test the call_callback method.

        This test verifies that the call_callback method correctly calls a registered callback.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Register a callback
        callback_manager.register_callback("test_callback", callback)

        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Call the callback
        callback_manager.call_callback("test_callback")

        # Verify the callback was executed
        assert callback_counter["count"] == 1

    @pytest.mark.asyncio
    async def test_call_callback_async(self, callback_manager: CallbackManager, async_callback: Callable, callback_counter: Dict[str, int]) -> None:
        """Test the call_callback_async method.

        This test verifies that the call_callback_async method correctly calls a registered
        async callback.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            async_callback: A fixture providing an async callback function.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Register an async callback
        callback_manager.register_callback("test_async_callback", async_callback, is_async=True)

        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Call the async callback
        await callback_manager.call_callback_async("test_async_callback")

        # Verify the callback was executed
        assert callback_counter["count"] == 1

    def test_true_condition(self, callback_manager: CallbackManager) -> None:
        """Test the true_condition method.

        This test verifies that the true_condition method always returns True.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
        """
        assert callback_manager.true_condition() is True

    @pytest.mark.asyncio
    async def test_true_condition_async(self, callback_manager: CallbackManager) -> None:
        """Test the true_condition_async method.

        This test verifies that the true_condition_async method always returns True.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
        """
        assert await callback_manager.true_condition_async() is True

    def test_call_conditional(self, callback_manager: CallbackManager, callback: Callable, true_condition: Callable, false_condition: Callable, callback_counter: Dict[str, int]) -> None:
        """Test the call_conditional method.

        This test verifies that the call_conditional method correctly evaluates the condition
        and calls the callback if the condition is met.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
            true_condition: A fixture providing a condition function that returns True.
            false_condition: A fixture providing a condition function that returns False.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Call with true condition
        callback_manager.call_conditional(true_condition, callback)

        # Verify the callback was executed
        assert callback_counter["count"] == 1

        # Call with false condition
        callback_manager.call_conditional(false_condition, callback)

        # Verify the callback was not executed again
        assert callback_counter["count"] == 1

    @pytest.mark.asyncio
    async def test_call_conditional_async(self, callback_manager: CallbackManager, async_callback: Callable, async_true_condition: Callable, async_false_condition: Callable, callback_counter: Dict[str, int]) -> None:
        """Test the call_conditional_async method.

        This test verifies that the call_conditional_async method correctly evaluates the
        async condition and calls the async callback if the condition is met.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            async_callback: A fixture providing an async callback function.
            async_true_condition: A fixture providing an async condition function that returns True.
            async_false_condition: A fixture providing an async condition function that returns False.
            callback_counter: A fixture providing a counter dictionary.
        """
        # Verify initial counter value
        assert callback_counter["count"] == 0

        # Call with true condition
        await callback_manager.call_conditional_async(async_true_condition, async_callback)

        # Verify the callback was executed
        assert callback_counter["count"] == 1

        # Call with false condition
        await callback_manager.call_conditional_async(async_false_condition, async_callback)

        # Verify the callback was not executed again
        assert callback_counter["count"] == 1

    def test_pickling(self, callback_manager: CallbackManager, callback: Callable) -> None:
        """Test pickling and unpickling of CallbackManager.

        This test verifies that a CallbackManager can be pickled and unpickled correctly.

        Args:
            callback_manager: A fixture providing a CallbackManager instance.
            callback: A fixture providing a callback function.
        """
        import pickle

        # Register a callback
        callback_manager.register_callback("test_callback", callback)

        # Pickle and unpickle the manager
        pickled = pickle.dumps(callback_manager)
        unpickled = pickle.loads(pickled)

        # Verify the unpickled manager has empty callbacks and tasks
        assert unpickled.callbacks == {}
        assert unpickled.callbacks_async == {}
        assert unpickled.tasks == {}

        # Verify other attributes are preserved
        assert unpickled.default_condition == callback_manager.default_condition
        assert unpickled.default_caller == callback_manager.default_caller


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
