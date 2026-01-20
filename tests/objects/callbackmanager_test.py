#!/usr/bin/env python
"""callbackmanager_test.py
Test for the CallbackManager class.

This module provides tests for the CallbackManager class, which is a class that manages callbacks and provides
functionality for registering, calling, and scheduling callbacks.
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
import pickle
import unittest.mock
from collections import deque
from typing import Any
from unittest.mock import MagicMock

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.objects import CallbackManager, CallbackScheduler
from baseobjects.testsuite.objects import CallbackManagerTestSuite


# Definitions #
# Classes #
class SlotCM(CallbackManager):
    """A CallbackManager subclass with slots for testing."""

    __slots__ = ("extra",)

    def __init__(self) -> None:
        """Initializes the SlotCM."""
        super().__init__()
        self.extra = 1


class TestCallbackManager(CallbackManagerTestSuite):
    """Test the CallbackManager class.

    This class tests the functionality of the CallbackManager class, which manages callbacks and provides functionality
    for registering, calling, and scheduling callbacks.
    """

    # Attributes #
    UnitTestClass = CallbackManager

    # Instance Methods #

    # Tests
    def test_register_and_call_callback(self) -> None:
        """Tests registering and calling a callback."""
        cm = CallbackManager()
        called = False

        def cb() -> None:
            nonlocal called
            called = True

        cm.register_callback("test", cb)
        cm.call_callback("test")
        assert called

    def test_callbacks_dict(self) -> None:
        """Tests accessing the callbacks dictionary."""
        cm = CallbackManager()

        def cb() -> None:
            pass

        cm.register_callback("test", cb)
        assert "test" in cm.callbacks
        assert cm.callbacks["test"] is cb

    def test_clear_callbacks(self) -> None:
        """Tests clearing callbacks."""
        cm = CallbackManager()
        cm.register_callback("test", lambda: None)
        cm.callbacks.clear()
        assert len(cm.callbacks) == 0

    def test_init_no_construct(self) -> None:
        """Tests initialization without construction."""
        cm = CallbackManager(init=False)
        assert cm.callbacks == {}
        assert cm.schedulers == {}

    def test_construct_args(self) -> None:
        """Tests construction with arguments."""
        cm = CallbackManager(
            default_condition="true_condition",
            default_caller="call",
            callbacks={"a": lambda: 1},
            callbacks_async={"b": lambda: 2},
        )
        assert cm.default_condition == "true_condition"
        assert cm.default_caller == "call"
        assert "a" in cm.callbacks
        assert "b" in cm.callbacks_async

    def test_format_conditional_callback_defaults(self) -> None:
        """Tests format_conditional_callback with defaults."""
        cm = CallbackManager(default_condition="true_condition", default_caller="call")
        _cb, cond, caller = cm.format_conditional_callback(lambda: None)
        assert cond == cm.true_condition
        assert caller == cm.call

    def test_format_conditional_callback_strings(self) -> None:
        """Tests format_conditional_callback with strings."""
        cm = CallbackManager()
        _cb, cond, caller = cm.format_conditional_callback(lambda: None, condition="true_condition", caller="call")
        assert cond == cm.true_condition
        assert caller == cm.call

    def test_create_conditional_callback_existing_task(self) -> None:
        """Tests create_conditional_callback reusing an existing task queue."""
        cm = CallbackManager()
        tasks: deque[Any] = deque()
        cm.tasks["my_task_conditional_callback"] = tasks
        cm.create_conditional_callback(lambda: None, lambda: True, lambda c, cb: cb(), task_name="my_task")
        assert cm.tasks["my_task_conditional_callback"] is tasks

    def test_create_scheduler_with_type(self) -> None:
        """Tests create_scheduler with a specific type."""
        cm = CallbackManager()
        sched = cm.create_scheduler(type_=CallbackScheduler)
        assert isinstance(sched, CallbackScheduler)

    def test_create_conditional_scheduler_with_type_and_existing_task(self) -> None:
        """Tests create_conditional_scheduler with type and existing task."""
        cm = CallbackManager()
        tasks: deque[Any] = deque()
        cm.tasks["cond1_conditional_caller"] = tasks

        async def cb() -> None:
            pass

        cm.register_conditional_callback("cond1", cb, is_async=True)
        sched = cm.create_conditional_scheduler(["cond1"], type_=CallbackScheduler)
        assert isinstance(sched, CallbackScheduler)
        assert cm.tasks["cond1_conditional_caller"] is tasks

    def test_register_callbacks_none(self) -> None:
        """Tests register_callbacks with None."""
        cm = CallbackManager()
        cm.register_callbacks(callbacks=None, callbacks_async=None)

    def test_register_callbacks_async(self) -> None:
        """Tests register_callbacks with async callbacks."""
        # Cover line 556
        cm = CallbackManager()
        cm.register_callbacks(callbacks_async={"a": lambda: 1})
        assert "a" in cm.callbacks_async

    def test_register_conditional_callbacks_dict(self) -> None:
        """Tests register_conditional_callbacks with a dictionary."""
        cm = CallbackManager()
        cm.register_conditional_callbacks(
            callbacks={"c1": {"callback": lambda: None, "condition": lambda: True}},
            callbacks_async={"c2": {"callback": lambda: None, "condition": lambda: True}},
        )
        assert "c1" in cm.conditional_callbacks
        assert "c2" in cm.conditional_callbacks_async

    def test_register_conditional_callbacks_iterable(self) -> None:
        """Tests register_conditional_callbacks with an iterable."""
        # Cover 633->636 (false branch of isinstance dict)
        cm = CallbackManager()
        cm.register_conditional_callbacks(
            callbacks_async=[("c3", {"callback": lambda: None, "condition": lambda: True})],
        )
        assert "c3" in cm.conditional_callbacks_async

    def test_register_conditional_callbacks_none(self) -> None:
        """Tests register_conditional_callbacks with None."""
        cm = CallbackManager()
        cm.register_conditional_callbacks(callbacks=None, callbacks_async=None)

    def test_register_conditional_scheduler_error(self) -> None:
        """Tests register_conditional_scheduler error handling."""
        cm = CallbackManager()
        with pytest.raises(ValueError):
            cm.register_conditional_scheduler("name", scheduler=None, condition_names=None)

    def test_register_conditional_scheduler_existing(self) -> None:
        """Tests register_conditional_scheduler with existing scheduler."""
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_conditional_scheduler("name", scheduler=sched)
        assert cm.schedulers["name"] is sched

    def test_register_scheduler_callback_existing_task_and_str_scheduler(self) -> None:
        """Tests register_scheduler_callback with existing task and string scheduler name."""
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_scheduler("my_sched", sched)

        tasks: deque[Any] = deque()
        cm.tasks["cb_name_scheduler"] = tasks

        cm.register_scheduler_callback("cb_name", "my_sched")

        # It should reuse tasks
        assert cm.tasks["cb_name_scheduler"] is tasks
        assert "cb_name" in cm.callbacks

    def test_register_scheduler_callback_with_object(self) -> None:
        """Tests register_scheduler_callback with a scheduler object."""
        # Cover 717->720 (scheduler is not str)
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_scheduler_callback("cb_name", sched)
        assert "cb_name" in cm.callbacks

    @pytest.mark.asyncio
    async def test_start_scheduler_execution(self) -> None:
        """Tests starting scheduler execution."""
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_scheduler("my_sched", sched)
        cm.register_scheduler_callback("start_it", "my_sched")

        cm.call_callback("start_it")
        tasks = cm.tasks["start_it"]
        assert len(tasks) == 1

        # Call again to cover "if not tasks" false branch (already running)
        cm.call_callback("start_it")
        assert len(tasks) == 1  # Should not add another task

        for t in tasks:
            t.cancel()

    @pytest.mark.asyncio
    async def test_start_scheduler_async_execution(self) -> None:
        """Tests starting scheduler execution asynchronously."""
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_scheduler("my_sched", sched)
        cm.register_scheduler_callback("start_it", "my_sched")

        await cm.call_callback_async("start_it")
        tasks = cm.tasks["start_it"]
        assert len(tasks) == 1
        await asyncio.sleep(0)
        for t in tasks:
            t.cancel()

    def test_map_conditionals_to_scheduler_existing_task(self) -> None:
        """Tests map_conditionals_to_scheduler with existing tasks."""
        cm = CallbackManager()
        sched = CallbackScheduler()
        cm.register_scheduler("my_sched", sched)

        async def cb() -> None:
            pass

        cm.register_conditional_callback("c1", cb, is_async=True)
        tasks: deque[Any] = deque()
        cm.tasks["c1_conditional_caller"] = tasks
        cm.map_conditionals_to_scheduler("my_sched", ["c1"])
        assert cm.tasks["c1_conditional_caller"] is tasks
        assert len(sched.callback_map) == 1

    def test_call_sync(self) -> None:
        """Tests synchronous call."""
        cm = CallbackManager()
        called = False

        def cb() -> None:
            nonlocal called
            called = True

        cm.call(cb)
        assert called

    @pytest.mark.asyncio
    @pytest.mark.parametrize("use_tasks", [False, True])
    async def test_call_while_condition_async_tasks(self, use_tasks: bool) -> None:
        """Tests call_while_condition_async with task usage."""
        cm = CallbackManager()

        async def cond() -> bool:
            await asyncio.sleep(0)
            return False

        async def cb() -> None:
            await asyncio.sleep(0)

        tasks: deque[Any] | None = deque() if use_tasks else None
        await cm.call_while_condition_async(cond, cb, tasks=tasks)

    @pytest.mark.asyncio
    async def test_call_while_condition_async_max_tasks_zero(self) -> None:
        """Tests call_while_condition_async with max_callback_tasks=0."""
        # Cover 894->890
        cm = CallbackManager()
        cm.max_callback_tasks = 0

        # Need condition to be True then False to avoid infinite loop
        count = 0

        async def cond() -> bool:
            nonlocal count
            await asyncio.sleep(0)
            count += 1
            return count < 2

        async def cb() -> None:
            await asyncio.sleep(0)

        await cm.call_while_condition_async(cond, cb, tasks=None)

    @pytest.mark.asyncio
    async def test_enqueue_call_while_condition_async_none_tasks(self) -> None:
        """Tests enqueue_call_while_condition_async with no tasks."""
        cm = CallbackManager()

        async def cond() -> bool:
            await asyncio.sleep(0)
            return False

        async def cb() -> None:
            await asyncio.sleep(0)

        await cm.enqueue_call_while_condition_async(cond, cb, tasks=None)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("use_tasks", [False, True])
    async def test_call_while_condition_task_async_tasks(self, use_tasks: bool) -> None:
        """Tests call_while_condition_task_async with task usage."""
        cm = CallbackManager()

        async def cond() -> bool:
            await asyncio.sleep(0)
            return False

        async def cb() -> asyncio.Task[Any]:
            await asyncio.sleep(0)
            return asyncio.create_task(asyncio.sleep(0))

        tasks: deque[Any] | None = deque() if use_tasks else None
        await cm.call_while_condition_task_async(cond, cb, tasks=tasks)

    @pytest.mark.asyncio
    async def test_call_while_condition_task_async_max_tasks_zero(self) -> None:
        """Tests call_while_condition_task_async with max_callback_tasks=0."""
        cm = CallbackManager()
        cm.max_callback_tasks = 0
        count = 0

        async def cond() -> bool:
            nonlocal count
            await asyncio.sleep(0)
            count += 1
            return count < 2

        async def cb() -> asyncio.Task[Any]:
            await asyncio.sleep(0)
            return asyncio.create_task(asyncio.sleep(0))

        await cm.call_while_condition_task_async(cond, cb, tasks=None)

    @pytest.mark.asyncio
    async def test_enqueue_call_while_condition_task_async_none_tasks(self) -> None:
        """Tests enqueue_call_while_condition_task_async with no tasks."""
        cm = CallbackManager()

        async def cond() -> bool:
            await asyncio.sleep(0)
            return False

        async def cb() -> asyncio.Task[Any]:
            await asyncio.sleep(0)
            return asyncio.create_task(asyncio.sleep(0))

        await cm.enqueue_call_while_condition_task_async(cond, cb, tasks=None)

    def test_join_tasks_busy_wait(self) -> None:
        """Tests join_tasks with busy wait."""
        cm = CallbackManager()
        mock_task = MagicMock()
        mock_task.done.side_effect = [False, True]
        cm.tasks["mock"] = deque([mock_task])
        cm.join_tasks()
        assert mock_task.done.call_count == 2

    def test_pickling_with_slots(self) -> None:
        """Tests pickling with slots."""
        cm = SlotCM()
        pickled = pickle.dumps(cm)
        unpickled = pickle.loads(pickled)
        assert isinstance(unpickled, SlotCM)

    def test_getstate_fallthrough(self) -> None:
        """Tests getstate fallthrough."""
        # Cover 328->331 (no match)
        base_cls = CallbackManager.__base__
        with unittest.mock.patch.object(base_cls, "__getstate__", return_value=None):
            cm = CallbackManager()
            state = cm.__getstate__()
            assert state is None

    def test_register_scheduler_callback_reuse_tasks(self, test_object: CallbackManager) -> None:
        """Tests that register_scheduler_callback reuses existing task queue."""
        scheduler = CallbackScheduler()
        test_object.register_scheduler("my_sched", scheduler)

        # First registration
        test_object.register_scheduler_callback("cb_name", "my_sched")

        assert "cb_name" in test_object.tasks
        tasks1 = test_object.tasks["cb_name"]

        # Second registration
        test_object.register_scheduler_callback("cb_name", "my_sched")
        tasks2 = test_object.tasks["cb_name"]

        assert tasks1 is tasks2
        assert len(test_object.tasks) == 1

    def test_format_conditional_callback_kwargs(self, test_object: CallbackManager) -> None:
        """Tests format_conditional_callback with kwargs for components."""
        call_args = {}

        def my_callback(*args: Any, **kwargs: Any) -> None:
            call_args["callback"] = kwargs

        def my_condition(*args: Any, **kwargs: Any) -> bool:
            call_args["condition"] = kwargs
            return True

        def my_caller(condition: Any, callback: Any, *args: Any, **kwargs: Any) -> None:
            call_args["caller"] = kwargs
            if condition():
                callback()

        # Register with kwargs
        test_object.register_conditional_callback(
            "my_cond_cb",
            my_callback,
            my_condition,
            my_caller,
            callback_kwargs={"a": 1},
            condition_kwargs={"b": 2},
            caller_kwargs={"c": 3},
        )

        # Call it
        test_object.conditional_callbacks["my_cond_cb"]()

        assert call_args["callback"] == {"a": 1}
        assert call_args["condition"] == {"b": 2}
        assert call_args["caller"] == {"c": 3}

    @pytest.mark.parametrize(
        ("arg_name", "attr_name"),
        [
            ("callbacks", "conditional_callbacks"),
            ("callbacks_async", "conditional_callbacks_async"),
        ],
    )
    def test_register_conditional_callbacks_list_tuples(
        self, test_object: CallbackManager, arg_name: str, attr_name: str,
    ) -> None:
        """Tests register_conditional_callbacks with list of tuples."""

        def cb() -> None:
            pass

        def cond() -> bool:
            return True

        callbacks_list = [
            ("cb1", {"callback": cb, "condition": cond}),
            ("cb2", {"callback": cb, "condition": cond}),
        ]

        kwargs = {arg_name: callbacks_list}
        test_object.register_conditional_callbacks(**kwargs)

        target_dict = getattr(test_object, attr_name)
        assert "cb1" in target_dict
        assert "cb2" in target_dict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
