""" callbackmanager.py
An object which manages and executes callback functions with conditions and evaluators.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from asyncio import create_task, Task
from collections.abc import Callable
from collections import deque, ChainMap
from functools import partial
from typing import Any, NamedTuple

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class CallbackEntry(NamedTuple):
    """An entry in a callback manager's registry."""

    callback: Callable
    condition: Callable
    evaluator: Callable


class CallbackManager(BaseObject):
    """An object which manages and executes callback functions with conditions and evaluators.

    The CallbackManager class allows the registration, formatting, scheduling, and execution of synchronous and
    asynchronous callback functions. It supports default conditions and evaluators to streamline callback
    registration and ensures organized management of callback and task entries.

    Attributes:
        default_condition: The default condition to evaluate callbacks, set to "true_condition" by default.
        default_evaluator: The default evaluator name for callbacks, set to "evaluate_callback" by default.
        callbacks: A dictionary storing registered synchronous CallbackEntry objects.
        callbacks_async: A dictionary storing registered asynchronous CallbackEntry objects.
        max_callback_tasks: The maximum number of callback tasks of each type allowed simultaneously.
        scheduler_tasks: A dictionary storing tasks related to scheduling operations.
        evaluator_tasks: A dictionary storing tasks related to evaluator operations.
        callback_tasks: A dictionary storing tasks related to callback executions.
        tasks: A ChainMap combining scheduler, evaluator, and callback task dictionaries.

    Args:
        callbacks: The CallbackEntries to add to the registry.
        callbacks_async: The async CallbackEntries to add to the registry.
        *args: Positional arguments which may be used for inheritance.
        default_condition: The default condition to use when registering callbacks.
        default_evaluator: The default evaluator to use when registering callbacks.
        **kwargs: Keyword arguments which may be used for inheritance.
    """
    # Attributes #
    default_condition: str = "true_condition"
    default_evaluator: str = "evaluate_callback"

    callbacks: dict[str, CallbackEntry]
    callbacks_async: dict[str, CallbackEntry]

    max_callback_tasks: int = 1
    scheduler_tasks: dict[str, Task]
    evaluator_tasks: dict[str, Task]
    callback_tasks: dict[str, Task]
    tasks: ChainMap[str, Task]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        callbacks: dict[str, CallbackEntry] | None = None,
        callbacks_async: dict[str, CallbackEntry] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_evaluator: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Attributes #
        self.callbacks = {}
        self.callbacks_async = {}

        self.scheduler_tasks = {}
        self.evaluator_tasks = {}
        self.callback_tasks = {}
        self.tasks = ChainMap(self.scheduler_tasks, self.evaluator_tasks, self.callback_tasks)

        # Parent Attributes #
        super().__init__()

        # Construction #
        if init:
            self.construct(
                callbacks,
                callbacks_async,
                *args,
                default_condition=default_condition,
                default_evaluator=default_evaluator,
                **kwargs,
            )

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object.

        Returns:
            A dictionary of this object's attributes.
        """
        state = super().__getstate__()

        for name in ("callbacks", "callbacks_async", "scheduler_tasks", "evaluator_tasks", "callback_tasks", "tasks"):
            if name in state:
                del state[name]

        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        super().__setstate__(state)
        self.callbacks = {}
        self.callbacks_async = {}
        self.scheduler_tasks = {}
        self.evaluator_tasks = {}
        self.callback_tasks = {}
        self.tasks = ChainMap(self.scheduler_tasks, self.evaluator_tasks, self.callback_tasks)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        callbacks: dict[str, CallbackEntry] | None = None,
        callbacks_async: dict[str, CallbackEntry] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_evaluator: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            callbacks: The CallbackEntries to add to the registry.
            callbacks_async: The async CallbackEntries to add to the registry.
            *args: Positional arguments which may be used for inheritance.
            default_condition: The default condition to use when registering callbacks.
            default_evaluator: The default evaluator to use when registering callbacks.
            **kwargs: Keyword arguments which may be used for inheritance.
        """
        if default_condition is not None:
            self.default_condition = default_condition

        if default_evaluator is not None:
            self.default_evaluator = default_evaluator

        if callbacks is not None:
            self.callbacks.update(callbacks)

        if callbacks_async is not None:
            self.callbacks_async.update(callbacks_async)

        super().construct(*args, **kwargs)

    # Callback Registration
    def format_callback(
        self,
        callback: Callable,
        condition: Callable | str | None = None,
        evaluator: Callable | str | None = None,
        *args: Any,
        callback_kwargs: dict[str, Any] | None = None,
        condition_kwargs: dict[str, Any] | None = None,
        evaluator_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> CallbackEntry:
        """Formats a callback entry.

        Args:
            callback: The callback function.
            condition: The condition function or name.
            evaluator: The evaluator function or name.
            *args: Positional arguments which may be used for inheritance.
            callback_kwargs: Keyword arguments for the callback.
            condition_kwargs: Keyword arguments for the condition.
            evaluator_kwargs: Keyword arguments for the evaluator.
            **kwargs: Keyword arguments which may be used for inheritance.

        Returns:
            A formatted callback entry.
        """
        if condition is None:
            condition = getattr(self, self.default_condition)
        elif isinstance(condition, str):
            condition = getattr(self, condition)

        if evaluator is None:
            evaluator = getattr(self, self.default_evaluator)
        elif isinstance(evaluator, str):
            evaluator = getattr(self, evaluator)

        if callback_kwargs is not None:
            callback = partial(callback, **callback_kwargs)

        if condition_kwargs is not None:
            condition = partial(condition, **condition_kwargs)

        if evaluator_kwargs is not None:
            evaluator = partial(evaluator, **evaluator_kwargs)

        return CallbackEntry(callback, condition, evaluator)

    def register_callbacks(
        self,
        callbacks: dict[str, dict[str, Any]] | None = None,
        callbacks_async: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        """Registers synchronous and asynchronous callbacks.

        Args:
            callbacks: A dictionary of synchronous callback configurations.
            callbacks_async: A dictionary of asynchronous callback configurations.
        """
        if callbacks:
            self.callbacks.update((n, self.format_callback(**c_kwargs)) for n, c_kwargs in callbacks.items())
        if callbacks_async:
            self.callbacks_async.update(
                (n, self.format_callback(**c_kwargs)) for n, c_kwargs in callbacks_async.items()
            )

    async def register_callbacks_async(
        self,
        callbacks: dict[str, dict[str, Any]] | None = None,
        callbacks_async: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        """Asynchronously registers synchronous and asynchronous callbacks.

        Args:
            callbacks: A dictionary of synchronous callback configurations.
            callbacks_async: A dictionary of asynchronous callback configurations.
        """
        if callbacks:
            self.callbacks.update((n, self.format_callback(**c_kwargs)) for n, c_kwargs in callbacks.items())
        if callbacks_async:
            self.callbacks_async.update(
                (n, self.format_callback(**c_kwargs)) for n, c_kwargs in callbacks_async.items()
            )

    # Callback Condition
    def true_condition(self) -> bool:
        """A method for a callback condition that always returns True.

        Returns:
            bool: Always returns True.
        """
        return True

    async def true_condition_async(self) -> bool:
        """An async method for a callback condition that always returns True.

        Returns:
            bool: Always returns True.
        """
        return True

    # Callback Execution
    def execute_callback(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: The keyword arguments to pass to the callback function.
        """
        self.callbacks[name][0](*args, **kwargs)

    async def execute_callback_async(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Asynchronously executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: The keyword arguments to pass to the callback function.
        """
        await self.callbacks_async[name][0](*args, **kwargs)

    def schedule_callback(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Schedules a callback by creating and storing an asyncio task for the specified callback.

        Args:
            name: The name of the callback to be scheduled.
            *args: The positional arguments to pass to the callback function.
            **kwargs: The keyword arguments to pass to the callback function.
        """
        self.callback_tasks[f"callback_execution_{name}"] = create_task(self.callbacks_async[name][0](*args, **kwargs))

    async def schedule_callback_async(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Asynchronously schedules a callback by creating and storing an asyncio task for the specified callback.

        Args:
            name: The name of the callback to be scheduled.
            *args: The positional arguments to pass to the callback function.
            **kwargs: The keyword arguments to pass to the callback function.
        """
        self.callback_tasks[f"callback_execution_{name}"] = create_task(self.callbacks_async[name][0](*args, **kwargs))

    # Callback Scheduling
    def start_scheduler(self) -> None:
        """Starts the scheduler for callback execution and management.

        This method initiates and starts a scheduler if it's not already running. Specifically, it ensures that the
        schedule of evaluations is managed asynchronously. It stores the reference to the created task in a dictionary
        for tracking and adds a callback that will handle cleanup after the task completion.
        """
        # Check if scheduler is running
        if not self.scheduler_tasks:
            # Create scheduler
            scheduler = create_task(self.schedule_evaluations_async())
            self.scheduler_tasks["callback_scheduling_task"] = scheduler
            # Add task callback to remove task when done
            scheduler.add_done_callback(partial(self._remove_scheduler, name="callback_scheduling_task"))

    async def start_scheduler_async(self) -> None:
        """Asynchronously starts the scheduler for callback execution and management.

        This method initiates and starts a scheduler if it's not already running. Specifically, it ensures that the
        schedule of evaluations is managed asynchronously. It stores the reference to the created task in a dictionary
        for tracking and adds a callback that will handle cleanup after the task completion.
        """
        # Check if scheduler is running
        if not self.scheduler_tasks:
            # Create scheduler
            scheduler = create_task(self.schedule_evaluations_async())
            self.scheduler_tasks["callback_scheduling_task"] = scheduler
            # Add task callback to remove task when done
            scheduler.add_done_callback(partial(self._remove_scheduler, name="callback_scheduling_task"))

    def _remove_scheduler(self, task: Task, name: str) -> None:
        """Removes a scheduler task by its name.

        Args:
            task: The Task instance to be removed, unused but required.
            name: The name of the task to be removed.
        """
        if name in self.scheduler_tasks:
            del self.scheduler_tasks[name]

    def schedule_evaluations(self) -> None:
        """Schedules the evaluation of the callback functions."""
        for check, callback in self.callbacks.values():
            self.evaluate_callbacks(check, callback)

    async def schedule_evaluations_async(self) -> None:
        """Asynchronously schedules the evaluation of the callback functions."""
        for name, (callback, condition, evaluate) in self.callbacks_async.items():
            # Check if evaluator is running
            if name not in self.evaluator_tasks:
                # Create evaluator
                self.evaluator_tasks[name] = callback_evaluator = create_task(evaluate(condition, callback))
                # Add task callback to remove task when done
                callback_evaluator.add_done_callback(partial(self._remove_evaluator, name=name))

    def _remove_evaluator(self, task: Task, name: str) -> None:
        """Removes an evaluator task by its name.

        Args:
            task: The Task instance to be removed, unused but required.
            name: The name of the task to be removed.
        """
        if name in self.evaluator_tasks:
            del self.evaluator_tasks[name]

    # Callback Evaluation
    def evaluate_callback(self, condition: Callable, callback: Callable) -> None:
        """Evaluates the callback function if the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
        """
        if condition():
            callback()

    async def evaluate_callback_async(self, condition_async: Callable, callback_async: Callable) -> None:
        """Asynchronously evaluates the callback function if the callback condition is met.

        Args:
            condition_async: The condition to evaluate the callback function.
            callback_async: The callback function to evaluate.
        """
        if await condition_async():
            await callback_async()

    def evaluate_callbacks(self, condition: Callable, callback: Callable) -> None:
        """Evaluates the callback function while the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
        """
        while condition():
            callback()

    async def evaluate_callbacks_async(self, condition_async: Callable, callback_async: Callable) -> None:
        """Asynchronously evaluates the callback function while the callback condition is met.

        Args:
            condition_async: The condition to evaluate the callback function.
            callback_async: The callback function to evaluate.
        """
        # Create Callback Tasks
        callback_tasks = deque()
        while (checked := await condition_async()) or callback_tasks:
            if len(callback_tasks) < self.max_callback_tasks and checked:
                # Create Evaluate Task
                callback_task = create_task(callback_async())
                callback_tasks.append(callback_task)
                # Add to collective task tracking
                key = f"callback_evaluation_{callback_task.get_name()}"
                self.callback_tasks[key] = callback_task
                # Have the new task remove its reference when it's done
                callback_task.add_done_callback(partial(self._remove_callback, name=key))
            else:
                await callback_tasks.popleft()

    async def evaluate_task_callbacks_async(self, condition_async: Callable, callback_async: Callable) -> None:
        """Asynchronously evaluates the callback function as tasks while the callback condition is met.

        Args:
            condition_async: The condition to evaluate the callback function.
            callback_async: The callback function to evaluate.
        """
        # Create Callback Tasks
        callback_tasks = deque()
        while (checked := await condition_async()) or callback_tasks:
            if len(callback_tasks) < self.max_callback_tasks and checked:
                # Create Evaluate Task
                callback_task = await callback_async()
                callback_tasks.append(callback_task)
                # Add to collective task tracking
                key = f"callback_evaluation_{callback_task.get_name()}"
                self.callback_tasks[key] = callback_task
                # Have the new task remove its reference when it's done
                callback_task.add_done_callback(partial(self._remove_callback, name=key))
            else:
                await callback_tasks.popleft()

    def _remove_callback(self, task: Task, name: str) -> None:
        """Removes a callback task by its name.

        Args:
            task: The Task instance to be removed, unused but required.
            name: The name of the task to be removed.
        """
        if name in self.callback_tasks:
            del self.callback_tasks[name]

    # Task Canceling
    def cancel_schedulers(self) -> None:
        """Cancels all currently scheduled callback scheduler tasks."""
        for task in self.scheduler_tasks.values():
            task.cancel()
        self.scheduler_tasks.clear()

    def cancel_evaluations(self) -> None:
        """Cancels all currently scheduled callback evaluation tasks."""
        for task in self.evaluator_tasks.values():
            task.cancel()
        self.evaluator_tasks.clear()

    def cancel_callbacks(self) -> None:
        """Cancels all currently scheduled callback tasks."""
        for task in self.callback_tasks.values():
            task.cancel()
        self.callback_tasks.clear()

    def cancel_tasks(self) -> None:
        """Cancels all currently scheduled tasks."""
        for task in self.tasks.values():
            task.cancel()
        self.scheduler_tasks.clear()
        self.evaluator_tasks.clear()
        self.callback_tasks.clear()
