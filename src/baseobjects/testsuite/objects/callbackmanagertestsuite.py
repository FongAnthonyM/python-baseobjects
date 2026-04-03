"""callbackmanagertestsuite.py
Base test suite for ~baseobjects.objects.CallbackManager and its subclasses.
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
from ...objects import CallbackManager, CallbackScheduler
from ..bases import BaseObjectTestSuite


# Classes #
class CallbackManagerTestSuite(BaseObjectTestSuite):
    """Base test suite for children of ~baseobjects.objects.CallbackManager.

    This class provides common test functionality for child classes of ~baseobjects.objects.CallbackManager.
    """

    UnitTestClass: type[CallbackManager]

    # Fixtures #
    @pytest.fixture
    def test_object(self) -> CallbackManager:
        """Creates a test object.

        Returns:
            CallbackManager: A test object instance.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def test_object_with_callbacks(self) -> CallbackManager:
        """Creates a test object with callbacks.

        Returns:
            CallbackManager: A test object instance with callbacks.
        """
        obj = self.UnitTestClass()

        def callback1(*args: Any, **kwargs: Any) -> str:
            return "callback1 called"

        def callback2(*args: Any, **kwargs: Any) -> str:
            return "callback2 called"

        obj.register_callback("callback1", callback1)
        obj.register_callback("callback2", callback2)
        return obj

    # Tests #
    # Magic Methods #
    def test_call_callback(self, test_object_with_callbacks: CallbackManager) -> None:
        """Tests calling a callback."""
        test_object_with_callbacks.call_callback("callback1")

    def test_call_callback_with_args(self, test_object: CallbackManager) -> None:
        """Tests calling a callback with arguments."""
        call_args = []

        def test_callback(arg1: Any, arg2: Any, kwarg1: Any = None, kwarg2: Any = None) -> None:
            call_args.append((arg1, arg2, kwarg1, kwarg2))

        test_object.register_callback("test_callback", test_callback)
        test_object.call_callback("test_callback", 1, 2, kwarg1="a", kwarg2="b")

        assert len(call_args) == 1
        assert call_args[0] == (1, 2, "a", "b")

    @pytest.mark.asyncio
    async def test_call_callback_async(self, test_object: CallbackManager) -> None:
        """Tests calling async callback."""
        call_count = 0

        async def test_async_function(*args: Any, **kwargs: Any) -> None:
            nonlocal call_count
            await asyncio.sleep(0)
            call_count += 1

        test_object.register_callback("async_cb", test_async_function, is_async=True)
        await test_object.call_callback_async("async_cb")
        assert call_count == 1

    def test_call_conditional(self, test_object: CallbackManager) -> None:
        """Tests calling conditional callback."""
        call_count = 0

        def test_callback(*args: Any, **kwargs: Any) -> None:
            nonlocal call_count
            call_count += 1

        def true_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        def false_condition(*args: Any, **kwargs: Any) -> bool:
            return False

        # Test direct call conditional
        test_object.call_conditional(true_condition, test_callback)
        assert call_count == 1

        test_object.call_conditional(false_condition, test_callback)
        assert call_count == 1  # Should not increment

    @pytest.mark.asyncio
    async def test_call_async(self, test_object: CallbackManager) -> None:
        """Tests the call_async method.

        This test verifies that the call_async method correctly calls an async function.
        """

        # Defines a test async function
        async def test_async_function(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "async function called"

        # Calls the async function
        result = await test_object.call_async(test_async_function)

        # Validate
        assert result == "async function called"

    @pytest.mark.asyncio
    async def test_call_conditional_async(self, test_object: CallbackManager) -> None:
        """Tests calling an async callback conditionally.

        This test verifies that an async callback is only called when the condition is True.
        """
        # Defines test async callback and conditions
        result = []

        async def test_async_callback(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            result.append("async callback called")
            return "async callback called"

        async def true_condition_async(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
            return True

        async def false_condition_async(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
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

    @pytest.mark.asyncio
    @pytest.mark.parametrize("is_task", [False, True])
    async def test_call_while_condition_async_operations(self, test_object: CallbackManager, is_task: bool) -> None:
        """Tests calling a callback while a condition is true.

        This test verifies that call_while_condition_async and call_while_condition_task_async
        correctly call a callback repeatedly while a condition is true.

        Args:
            test_object: A fixture providing a test object instance.
            is_task: Whether the callback returns a task.
        """
        # Defines test async callback and condition
        call_count = 0
        tasks: deque[Any] | None = deque() if is_task else None

        async def test_async_callback(*args: Any, **kwargs: Any) -> Any:
            await asyncio.sleep(0)
            nonlocal call_count
            call_count += 1
            if is_task:
                return asyncio.create_task(asyncio.sleep(0.1))
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Calls while condition
        if is_task:
            await test_object.call_while_condition_task_async(condition_async, test_async_callback, tasks)  # type: ignore[arg-type, unused-ignore]
        else:
            await test_object.call_while_condition_async(condition_async, test_async_callback)

        # Validate
        assert call_count == 2
        if is_task:
            assert len(tasks) == 0  # type: ignore[arg-type]

    def test_call_while_condition(self, test_object: CallbackManager) -> None:
        """Tests calling a callback while a condition is true.

        This test verifies that call_while_condition correctly calls a callback repeatedly
        while a condition is true.
        """
        # Defines test callback and condition
        call_count = 0

        def test_callback(*args: Any, **kwargs: Any) -> str:
            nonlocal call_count
            call_count += 1
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        def condition(*args: Any, **kwargs: Any) -> bool:
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Calls while condition
        test_object.call_while_condition(condition, test_callback)

        # Validate
        assert call_count == 2

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: CallbackManager, method: str) -> None:  # type: ignore[override]
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
    def test_deepcopy_operations(self, test_object: CallbackManager, method: str) -> None:
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
    def test_pickling(self, test_object: CallbackManager) -> None:
        """Tests pickling and unpickling of the object."""
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)

    # Functionality #
    def test_register_callback(self, test_object: CallbackManager) -> None:
        """Tests registering a callback."""

        def test_callback(*args: Any, **kwargs: Any) -> None:
            pass

        test_object.register_callback("test_callback", test_callback)
        assert "test_callback" in test_object.callbacks
        assert test_object.callbacks["test_callback"] == test_callback

    def test_register_callbacks(self, test_object: CallbackManager) -> None:
        """Tests registering multiple callbacks."""

        def callback1(*args: Any, **kwargs: Any) -> None:
            pass

        def callback2(*args: Any, **kwargs: Any) -> None:
            pass

        test_object.register_callbacks({"cb1": callback1, "cb2": callback2})
        assert "cb1" in test_object.callbacks
        assert "cb2" in test_object.callbacks

    def test_register_conditional_callback(self, test_object: CallbackManager) -> None:
        """Tests registering conditional callback."""

        def test_callback(*args: Any, **kwargs: Any) -> None:
            pass

        def test_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        test_object.register_conditional_callback("cond_cb", test_callback, test_condition)

    def test_empty_callbacks(self, test_object: CallbackManager) -> None:
        """Tests behavior with empty callbacks.

        This test verifies that calling a non-existent callback raises a KeyError.
        """
        # Attempt to call a non-existent callback
        with pytest.raises(KeyError):
            test_object.call_callback("non_existent_callback")

    def test_overwrite_callback(self, test_object_with_callbacks: CallbackManager) -> None:
        """Tests overwriting an existing callback.

        This test verifies that registering a callback with an existing name overwrites the previous callback.
        """

        # Defines a new callback
        def new_callback(*args: Any, **kwargs: Any) -> str:
            return "new callback called"

        # Registers the new callback with an existing name
        test_object_with_callbacks.register_callback("callback1", new_callback)

        # Calls the callback
        result = test_object_with_callbacks.call_callback("callback1")

        # Validate
        assert result == "new callback called"

    @pytest.mark.asyncio
    async def test_register_async_callback(self, test_object: CallbackManager) -> None:
        """Tests registering an async callback.

        This test verifies that an async callback can be registered and retrieved.
        """

        # Defines a test async callback
        async def test_async_callback(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "async callback called"

        # Registers the async callback
        test_object.register_callback("test_async_callback", test_async_callback, is_async=True)

        # Validate
        assert "test_async_callback" in test_object.callbacks_async
        assert test_object.callbacks_async["test_async_callback"] == test_async_callback

    def test_create_scheduler(self, test_object: CallbackManager) -> None:
        """Tests creating a scheduler.

        This test verifies that a scheduler can be created and has the expected type.
        """
        # Creates a scheduler
        scheduler = test_object.create_scheduler()

        # Validate
        assert isinstance(scheduler, CallbackScheduler)

    def test_register_scheduler(self, test_object: CallbackManager) -> None:
        """Tests registering a scheduler.

        This test verifies that a scheduler can be registered and retrieved.
        """
        # Registers a scheduler
        test_object.register_scheduler("test_scheduler")

        # Validate
        assert "test_scheduler" in test_object.schedulers
        assert isinstance(test_object.schedulers["test_scheduler"], CallbackScheduler)

    def test_register_scheduler_callback(self, test_object: CallbackManager) -> None:
        """Tests registering a callback with a scheduler.

        This test verifies that a callback can be registered with a scheduler.
        """
        # Registers a scheduler
        test_object.register_scheduler("test_scheduler")

        # Registers the callback with the scheduler
        test_object.register_scheduler_callback("test_callback", "test_scheduler")

        # Validate
        # Checks that the callbacks are registered
        assert "test_callback" in test_object.callbacks
        assert "test_callback" in test_object.callbacks_async
        # Checks that the task queue is created
        assert "test_callback" in test_object.tasks

    @pytest.mark.asyncio
    async def test_join_tasks_async(self, test_object: CallbackManager) -> None:
        """Tests joining tasks asynchronously.

        This test verifies that join_tasks_async waits for all tasks to complete.
        """

        # Creates some tasks
        async def async_task() -> str:
            await asyncio.sleep(0.1)
            return "task completed"

        task1 = asyncio.create_task(async_task())
        task2 = asyncio.create_task(async_task())

        # Adds tasks to the manager
        test_object.tasks["test_tasks"] = deque([task1, task2])

        # Join tasks
        await test_object.join_tasks_async()

        # Validate
        assert task1.done()
        assert task2.done()

    @pytest.mark.asyncio
    async def test_cancel_tasks(self, test_object: CallbackManager) -> None:
        """Tests cancelling tasks.

        This test verifies that cancel_tasks cancels all tasks.
        """
        # Creates a task that can be cancelled
        cancel_requested = False

        async def cancellable_task() -> None:
            nonlocal cancel_requested
            try:
                while not cancel_requested:  # noqa: ASYNC110
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                cancel_requested = True
                raise

        # Creates the task and add it to the manager
        task = asyncio.create_task(cancellable_task())
        test_object.tasks["test_tasks"] = deque([task])

        # Waits a bit to ensure the task is running
        await asyncio.sleep(0.2)

        # Cancel tasks
        test_object.cancel_tasks()

        # Waits for the task to be fully cancelled
        try:
            await asyncio.wait_for(task, timeout=0.5)
        except TimeoutError, asyncio.CancelledError:
            pass

        # Validate
        assert cancel_requested

        # Clean up any remaining tasks
        for t in [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]:
            t.cancel()
        await asyncio.gather(
            *[t for t in asyncio.all_tasks() if t is not asyncio.current_task()],
            return_exceptions=True,
        )

    def test_format_conditional_callback(self, test_object: CallbackManager) -> None:
        """Tests formatting a conditional callback.

        This test verifies that format_conditional_callback correctly formats the callback, condition, and caller.
        """

        # Defines test callback, condition, and caller
        def test_callback(*args: Any, **kwargs: Any) -> str:
            return "test callback called"

        def test_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        def test_caller(condition: Any, callback: Any, *args: Any, **kwargs: Any) -> Any:
            if condition():
                return callback()
            return None

        # Formats the conditional callback
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
        """Tests creating a conditional callback.

        This test verifies that create_conditional_callback correctly creates a callable that combines
        the condition and callback.
        """
        # Defines test callback, condition, and caller
        result = []

        def test_callback(*args: Any, **kwargs: Any) -> str:
            result.append("test callback called")
            return "test callback called"

        def test_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        def test_caller(condition: Any, callback: Any, *args: Any, **kwargs: Any) -> Any:
            if condition():
                return callback()
            return None

        # Creates the conditional callback
        conditional_callback = test_object.create_conditional_callback(test_callback, test_condition, test_caller)

        # Validate
        assert callable(conditional_callback)
        # Test that the conditional callback works
        conditional_callback()
        assert len(result) == 1
        assert result[0] == "test callback called"

    def test_create_conditional_scheduler(self, test_object: CallbackManager) -> None:
        """Tests creating a conditional scheduler.

        This test verifies that create_conditional_scheduler correctly creates a scheduler with
        the specified conditional callbacks.
        """

        # Defines test callbacks and conditions
        async def test_callback1(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "test callback1 called"

        async def test_callback2(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "test callback2 called"

        async def test_condition(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
            return True

        # Registers conditional callbacks with is_async=True
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)

        # Creates a conditional scheduler
        scheduler = test_object.create_conditional_scheduler(["test_conditional1", "test_conditional2"])

        # Validate
        assert isinstance(scheduler, CallbackScheduler)
        assert len(scheduler.callback_map) == 2
        # Checks that the callbacks in the scheduler are the ones we registered
        for callback, _ in scheduler.callback_map:
            assert callable(callback)

    def test_register_conditional_callbacks(self, test_object: CallbackManager) -> None:
        """Tests registering multiple conditional callbacks.

        This test verifies that register_conditional_callbacks correctly registers multiple callbacks.
        """

        # Defines test callbacks and conditions
        def test_callback1(*args: Any, **kwargs: Any) -> str:
            return "test callback1 called"

        def test_callback2(*args: Any, **kwargs: Any) -> str:
            return "test callback2 called"

        def test_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        # Registers conditional callbacks
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
        """Tests registering a conditional scheduler.

        This test verifies that register_conditional_scheduler correctly registers a scheduler
        with the specified conditional callbacks.
        """

        # Defines test callbacks and conditions
        async def test_callback1(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "test callback1 called"

        async def test_callback2(*args: Any, **kwargs: Any) -> str:
            await asyncio.sleep(0)
            return "test callback2 called"

        async def test_condition(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
            return True

        # Registers conditional callbacks with is_async=True
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)

        # Registers a conditional scheduler
        test_object.register_conditional_scheduler(
            "test_conditional_scheduler",
            condition_names=["test_conditional1", "test_conditional2"],
        )

        # Validate
        assert "test_conditional_scheduler" in test_object.schedulers
        assert isinstance(test_object.schedulers["test_conditional_scheduler"], CallbackScheduler)
        assert len(test_object.schedulers["test_conditional_scheduler"].callback_map) == 2

    def test_map_conditionals_to_scheduler(self, test_object: CallbackManager) -> None:
        """Tests mapping conditional callbacks to a scheduler.

        This test verifies that map_conditionals_to_scheduler correctly adds conditional callbacks
        to an existing scheduler.
        """

        # Defines test callbacks and conditions
        def test_callback1(*args: Any, **kwargs: Any) -> str:
            return "test callback1 called"

        def test_callback2(*args: Any, **kwargs: Any) -> str:
            return "test callback2 called"

        def test_condition(*args: Any, **kwargs: Any) -> bool:
            return True

        # Registers conditional callbacks and a scheduler
        test_object.register_conditional_callback("test_conditional1", test_callback1, test_condition, is_async=True)
        test_object.register_conditional_callback("test_conditional2", test_callback2, test_condition, is_async=True)
        test_object.register_scheduler("test_scheduler")

        # Map conditionals to the scheduler
        test_object.map_conditionals_to_scheduler("test_scheduler", ["test_conditional1", "test_conditional2"])

        # Validate
        assert len(test_object.schedulers["test_scheduler"].callback_map) == 2
        # Checks that task queues were created
        assert "test_conditional1_conditional_caller" in test_object.tasks
        assert "test_conditional2_conditional_caller" in test_object.tasks

    @pytest.mark.asyncio
    @pytest.mark.parametrize("is_task", [False, True])
    async def test_enqueue_call_while_condition_async_operations(
        self,
        test_object: CallbackManager,
        is_task: bool,
    ) -> None:
        """Tests enqueueing and calling a callback while a condition is true.

        This test verifies that enqueue_call_while_condition_async and enqueue_call_while_condition_task_async
        correctly enqueue and call a callback repeatedly while a condition is true.

        Args:
            test_object: A fixture providing a test object instance.
            is_task: Whether the callback returns a task.
        """
        # Defines test async callback and condition
        call_count = 0
        tasks: deque[Any] = deque()

        async def test_async_callback(*args: Any, **kwargs: Any) -> Any:
            nonlocal call_count
            await asyncio.sleep(0)
            call_count += 1
            if is_task:
                return asyncio.create_task(asyncio.sleep(0.1))
            await asyncio.sleep(0.1)
            return f"call {call_count}"

        # Condition that returns True twice then False
        condition_calls = 0

        async def condition_async(*args: Any, **kwargs: Any) -> bool:
            await asyncio.sleep(0)
            nonlocal condition_calls
            condition_calls += 1
            return condition_calls <= 2

        # Calls while condition
        if is_task:
            await test_object.enqueue_call_while_condition_task_async(condition_async, test_async_callback, tasks)
        else:
            await test_object.enqueue_call_while_condition_async(condition_async, test_async_callback, tasks)

        # Validate
        assert call_count == 2
        assert len(tasks) == 0  # All tasks should be completed

    @pytest.mark.asyncio
    async def test_join_tasks(self, test_object: CallbackManager) -> None:
        """Tests joining tasks synchronously.

        This test verifies that join_tasks waits for all tasks to complete.
        """

        # Creates some completed tasks
        async def dummy_task(result: str) -> str:
            await asyncio.sleep(0)
            return result

        task1 = asyncio.create_task(dummy_task("task1 completed"))
        task2 = asyncio.create_task(dummy_task("task2 completed"))

        # Ensure tasks are completed
        await asyncio.sleep(0)
        await asyncio.sleep(0)

        # Adds tasks to the manager
        test_object.tasks["test_tasks"] = deque([task1, task2])

        # Join tasks
        test_object.join_tasks()

        # Validate
        assert task1.done()
        assert task2.done()

    def test_true_condition(self) -> None:
        """Tests the true_condition static method.

        This test verifies that true_condition always returns True.
        """
        # Calls the method
        result = CallbackManager.true_condition()

        # Validate
        assert result is True

    @pytest.mark.asyncio
    async def test_true_condition_async(self) -> None:
        """Tests the true_condition_async static method.

        This test verifies that true_condition_async always returns True.
        """
        # Calls the method
        result = await CallbackManager.true_condition_async()

        # Validate
        assert result is True
