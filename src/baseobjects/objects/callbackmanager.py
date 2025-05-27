""" callbackmanager.py
An object which manages and executes callback functions with conditions and callers.
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
from asyncio import create_task, Task, gather, wait_for, shield
from collections.abc import Callable, Iterable
from collections import deque
from functools import partial
from typing import ClassVar, Any, NamedTuple

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject, BaseReducible
from ..functions import MethodMultiplexer


# Definitions #
# Classes #
class ConditionalCallbackEntry(NamedTuple):
    """An entry in a callback manager's registry."""

    callback: Callable
    condition: Callable
    caller: Callable


class CallbackScheduler(BaseObject):
    # Class Methods #
    default_schedule: ClassVar[str] = "schedule_callbacks"
    default_schedule_async: ClassVar[str] = "schedule_singleton_async_callbacks_async"

    # Attributes #
    callback_map: list[tuple[Callable, deque], ...]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        callback_map: Iterable[tuple[Callable, deque]] | None = None,
        schedule: Callable | str | None = None,
        schedule_async: Callable | str | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Attributes #
        self.callback_map = []

        self.schedule = MethodMultiplexer(instance=self, select=self.default_schedule)
        self.schedule_async = MethodMultiplexer(instance=self, select=self.default_schedule_async)

        # Parent Initialization #
        super().__init__()

        # Construction #
        if init:
            self.construct(callback_map, schedule, schedule_async, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        callback_map: list[tuple[Callable, deque]] | None = None,
        schedule: Callable | str | None = None,
        schedule_async: Callable | str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            callback_map:
            *args: Positional arguments which may be used for inheritance.
            **kwargs: Keyword arguments which may be used for inheritance.
        """
        if callback_map is not None:
            self.callback_map.extend(callback_map)

        if isinstance(schedule, str):
            self.schedule.select(schedule)
        elif schedule is not None:
            self.schedule.add_function(schedule.__name__, schedule)

        if isinstance(schedule_async, str):
            self.schedule_async.select(schedule_async)
        elif schedule_async is not None:
            self.schedule_async.add_function(schedule_async.__name__, schedule_async)

        super().construct(*args, **kwargs)

    # Scheduling
    def add_schedule_function(self, name: str, func: Callable) -> None:
        self.schedule.add_function(name, func)

    def add_schedule_async_function(self, name: str, func: Callable) -> None:
        self.schedule_async.add_function(name, func)

    def schedule_callbacks(self) -> None:
        """Schedules the evaluation of the callback functions."""
        for callback, _ in self.callback_map:
            callback()

    def schedule_async_callbacks(self) -> None:
        for callback_async, tasks in self.callback_map:
            callback_task = create_task(callback_async())
            callback_task.add_done_callback(tasks.remove)
            tasks.append(callback_task)

    async def schedule_async_callbacks_async(self) -> None:
        """Asynchronously, schedules the evaluation of the callback functions."""
        self.schedule_async_callbacks()

    def schedule_singleton_async_callbacks(self) -> None:
        for callback_async, tasks in self.callback_map:
            if len(tasks) < 1:
                callback_task = create_task(callback_async())
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)

    async def schedule_singleton_async_callbacks_async(self) -> None:
        """Asynchronously, schedules the evaluation of the callback functions."""
        self.schedule_singleton_async_callbacks()


class CallbackManager(BaseReducible):
    """An object which manages and executes callback functions with conditions and callers.

    The CallbackManager class allows the registration, formatting, scheduling, and execution of synchronous and
    asynchronous callback functions. It supports default conditions and callers to streamline callback
    registration and ensures organized management of callback and task entries.

    Attributes:
        default_condition: The default condition to evaluate callbacks, set to "true_condition" by default.
        default_caller: The default caller name for callbacks, set to "evaluate_callback" by default.
        callbacks: A dictionary storing registered synchronous ConditionalCallbackEntry objects.
        callbacks_async: A dictionary storing registered asynchronous ConditionalCallbackEntry objects.
        max_callback_tasks: The maximum number of callback tasks of each type allowed simultaneously.
        scheduler_tasks: A dictionary storing tasks related to scheduling operations.
        caller_tasks: A dictionary storing tasks related to caller operations.
        callback_tasks: A dictionary storing tasks related to callback executions.
        tasks: A ChainMap combining scheduler, caller, and callback task dictionaries.

    Args:
        callbacks: The CallbackEntries to add to the registry.
        callbacks_async: The async CallbackEntries to add to the registry.
        *args: Positional arguments which may be used for inheritance.
        default_condition: The default condition to use when registering callbacks.
        default_caller: The default caller to use when registering callbacks.
        **kwargs: Keyword arguments which may be used for inheritance.
    """
    # Attributes #
    default_condition: str = "true_condition"
    default_caller: str = "call_conditional"

    callbacks: dict[str, Callable]
    callbacks_async: dict[str, Callable]
    conditional_callbacks: dict[str, Callable]
    conditional_callbacks_async: dict[str, Callable]

    scheduler_type: type = CallbackScheduler
    schedulers: dict[str, CallbackScheduler]

    max_callback_tasks: int = 1
    tasks: dict[str, deque[Task]]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        callbacks: dict[str, ConditionalCallbackEntry] | None = None,
        callbacks_async: dict[str, ConditionalCallbackEntry] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_caller: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Attributes #
        self.callbacks = {}
        self.callbacks_async = {}
        self.conditional_callbacks = {}
        self.conditional_callbacks_async = {}

        self.schedulers = {}

        self.tasks = {}

        # Parent Initialization #
        super().__init__()

        # Construction #
        if init:
            self.construct(
                callbacks,
                callbacks_async,
                *args,
                default_condition=default_condition,
                default_caller=default_caller,
                **kwargs,
            )

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Gets the object's state for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()

        for name in ("callbacks", "callbacks_async", "scheduler_tasks", "caller_tasks", "callback_tasks", "tasks"):
            if name in state:
                del state[name]

        return state

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object.
        """
        super().__setstate__(state)
        self.callbacks = {}
        self.callbacks_async = {}
        self.tasks = {}

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        callbacks: dict[str, ConditionalCallbackEntry] | None = None,
        callbacks_async: dict[str, ConditionalCallbackEntry] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_caller: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            callbacks: The CallbackEntries to add to the registry.
            callbacks_async: The async CallbackEntries to add to the registry.
            *args: Positional arguments which may be used for inheritance.
            default_condition: The default condition to use when registering callbacks.
            default_caller: The default caller to use when registering callbacks.
            **kwargs: Keyword arguments which may be used for inheritance.
        """
        if default_condition is not None:
            self.default_condition = default_condition

        if default_caller is not None:
            self.default_caller = default_caller

        if callbacks is not None:
            self.callbacks.update(callbacks)

        if callbacks_async is not None:
            self.callbacks_async.update(callbacks_async)

        super().construct(*args, **kwargs)

    # Callback Creation
    def format_conditional_callback(
        self,
        callback: Callable,
        condition: Callable | str | None = None,
        caller: Callable | str | None = None,
        *args: Any,
        callback_kwargs: dict[str, Any] | None = None,
        condition_kwargs: dict[str, Any] | None = None,
        caller_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ConditionalCallbackEntry:
        """Formats a callback entry.

        Args:
            callback: The callback function.
            condition: The condition function or name.
            caller: The caller function or name.
            *args: Positional arguments which may be used for inheritance.
            callback_kwargs: Keyword arguments for the callback.
            condition_kwargs: Keyword arguments for the condition.
            caller_kwargs: Keyword arguments for the caller.
            **kwargs: Keyword arguments which may be used for inheritance.

        Returns:
            A formatted callback entry.
        """
        if condition is None:
            condition = getattr(self, self.default_condition)
        elif isinstance(condition, str):
            condition = getattr(self, condition)

        if caller is None:
            caller = getattr(self, self.default_caller)
        elif isinstance(caller, str):
            caller = getattr(self, caller)

        if callback_kwargs is not None:
            callback = partial(callback, **callback_kwargs)

        if condition_kwargs is not None:
            condition = partial(condition, **condition_kwargs)

        if caller_kwargs is not None:
            caller = partial(caller, **caller_kwargs)

        return ConditionalCallbackEntry(callback, condition, caller)

    def create_conditional_callback(
        self,
        callback: Callable,
        condition: Callable,
        caller: Callable,
        task_name: str | None = None,
    ) -> Callable:
        if task_name is None:
            return partial(caller, condition, callback)
        else:
            task_name = f"{task_name}_conditional_callback"
            if (tasks := self.tasks.get(task_name, None)) is None:
                self.tasks[task_name] = tasks = deque()
            return partial(caller, condition, callback, tasks)

    def create_scheduler(
        self,
        type_: type[CallbackScheduler] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> CallbackScheduler:
        if type_ is None:
            type_ = self.scheduler_type

        return type_(*args, **kwargs)

    def create_conditional_scheduler(
        self,
        condition_names: Iterable[str],
        type_: type[CallbackScheduler] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> CallbackScheduler:
        if type_ is None:
            type_ = self.scheduler_type

        callback_map = deque()
        for name in condition_names:
            callback = self.conditional_callbacks_async[name]
            task_name = f"{name}_conditional_caller"
            if (tasks := self.tasks.get(task_name, None)) is None:
                self.tasks[task_name] = tasks = deque()
            callback_map.append((callback, tasks))

        return type_(callback_map, *args, **kwargs)

    # Callback Registration
    def register_callback(self, name: str, callback: Callable, is_async: bool = False) -> None:
        if is_async:
            self.callbacks_async[name] = callback
        else:
            self.callbacks[name] = callback

    def register_callbacks(
        self,
        callbacks: dict[str, Callable] | Iterable[tuple[str, Callable]] | None = None,
        callbacks_async: dict[str, Callable] | Iterable[tuple[str, Callable]]  | None = None,
    ) -> None:
        """Registers synchronous and asynchronous callbacks.

        Args:
            callbacks: A dictionary of synchronous callback configurations.
            callbacks_async: A dictionary of asynchronous callback configurations.
        """
        if callbacks:
            self.callbacks.update(callbacks)

        if callbacks_async:
            self.callbacks_async.update(callbacks_async)

    def register_conditional_callback(
        self,
        name: str,
        callback: Callable,
        condition: Callable | str | None = None,
        caller: Callable | str | None = None,
        *args: Any,
        callback_kwargs: dict[str, Any] | None = None,
        condition_kwargs: dict[str, Any] | None = None,
        caller_kwargs: dict[str, Any] | None = None,
        is_async: bool = False,
        **kwargs: Any,
    ) -> None:
        # Format Callback, Condition, and Caller
        callback, condition, caller = self.format_conditional_callback(
            callback,
            condition,
            caller,
            *args,
            callback_kwargs=callback_kwargs,
            condition_kwargs=condition_kwargs,
            caller_kwargs=caller_kwargs,
            **kwargs,
        )

        # Register
        if is_async:
            self.conditional_callbacks_async[name] = self.create_conditional_callback(callback, condition, caller, name)
        else:
            self.conditional_callbacks[name] = self.create_conditional_callback(callback, condition, caller)

    def register_conditional_callbacks(
        self,
        callbacks: dict[str, Any] | Iterable[tuple[str, Any]] | None = None,
        callbacks_async: dict[str, Any] | Iterable[tuple[str, Any]] | None = None,
    ) -> None:
        """Registers synchronous and asynchronous callbacks.

        Args:
            callbacks: A dictionary of synchronous callback configurations.
            callbacks_async: A dictionary of asynchronous callback configurations.
        """
        # Register Callbacks
        if callbacks:
            if isinstance(callbacks, dict):
                callbacks = callbacks.items()

            creation_iter = (
                (n, self.create_conditional_callback(*self.format_conditional_callback(**kwargs)))
                for n, kwargs in callbacks
            )
            self.conditional_callbacks.update(creation_iter)

        # Register Async Callbacks
        if callbacks_async:
            if isinstance(callbacks_async, dict):
                callbacks_async = callbacks_async.items()

            creation_iter = (
                (n, self.create_conditional_callback(*self.format_conditional_callback(**kwargs), task_name=n))
                for n, kwargs in callbacks_async
            )
            self.conditional_callbacks_async.update(creation_iter)

    def register_scheduler(
        self,
        name: str,
        scheduler: CallbackScheduler | None = None,
        type_: type[CallbackScheduler] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.schedulers[name] = self.create_scheduler(type_, *args, **kwargs) if scheduler is None else scheduler

    def register_conditional_scheduler(
        self,
        name: str,
        scheduler: CallbackScheduler | None = None,
        condition_names: Iterable[str] | None = None,
        type_: type[CallbackScheduler] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if scheduler is None:
            if condition_names is None:
                raise ValueError("condition_names must be provided if scheduler is None.")

            self.schedulers[name] = self.create_conditional_scheduler(condition_names, type_, *args, **kwargs)
        else:
            self.schedulers[name] = scheduler

    def register_scheduler_callback(self, name: str, scheduler: CallbackScheduler | str) -> None:
        task_name = f"{name}_scheduler"
        if (tasks := self.tasks.get(task_name, None)) is None:
            self.tasks[name] = tasks = deque()

        if isinstance(scheduler, str):
            scheduler = self.schedulers[scheduler]

        self.callbacks[name] = partial(self.start_scheduler, scheduler, tasks)
        self.callbacks_async[name] = partial(self.start_scheduler_async, scheduler, tasks)

    # Callback Management
    def map_conditionals_to_scheduler(self, name: str, condition_names: Iterable[str]) -> None:
        callback_map = deque()
        for c_name in condition_names:
            callback = self.conditional_callbacks_async[c_name]
            task_name = f"{c_name}_conditional_caller"
            if (tasks := self.tasks.get(task_name, None)) is None:
                self.tasks[task_name] = tasks = deque()
            callback_map.append((callback, tasks))

        self.schedulers[name].callback_map.extend(callback_map)

    # Callback Conditions
    @staticmethod
    def true_condition() -> bool:
        """A method for a callback condition that always returns True.

        Returns:
            bool: Always returns True.
        """
        return True

    @staticmethod
    async def true_condition_async() -> bool:
        """An async method for a callback condition that always returns True.

        Returns:
            bool: Always returns True.
        """
        return True

    # Callback Calling
    def call_callback(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: Keyword arguments to pass to the callback function.
        """
        self.callbacks[name](*args, **kwargs)

    async def call_callback_async(self, name: str, *args: Any, **kwargs: Any) -> None:
        """Asynchronously executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: Keyword arguments to pass to the callback function.
        """
        await self.callbacks_async[name](*args, **kwargs)

    def call(self, callback) -> None:
        callback()

    async def call_async(self, callback) -> None:
        await callback()

    # Conditional Callback Calling
    def call_conditional(self, condition: Callable, callback: Callable) -> None:
        """Evaluates the callback function if the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
        """
        if condition():
            callback()

    async def call_conditional_async(self, condition_async: Callable, callback_async: Callable) -> None:
        """Asynchronously evaluates the callback function if the callback condition is met.

        Args:
            condition_async: The condition to evaluate the callback function.
            callback_async: The callback function to evaluate.
        """
        if await condition_async():
            await callback_async()

    def call_while_condition(self, condition: Callable, callback: Callable) -> None:
        """Evaluates the callback function while the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
        """
        while condition():
            callback()

    async def call_while_condition_async(
        self,
        condition_async: Callable,
        callback_async: Callable,
        tasks: deque,
    ) -> None:
        while (checked := await condition_async()) or tasks:
            # Add Callback Tasks and Await Them
            if len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = create_task(callback_async())
                tasks.append(callback_task)
            else:
                await next(iter(tasks))

    async def call_while_condition_task_async(
        self,
        condition_async: Callable,
        callback_async: Callable,
        tasks: deque,
    ) -> None:
        while (checked := await condition_async()) or tasks:
            # Add Callback Tasks and Await Them
            if len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = await callback_async()
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)
            else:
                await next(iter(tasks))

    # Callback Scheduling
    def start_scheduler(self, scheduler: CallbackScheduler, tasks: deque, *args: Any, **kwargs: Any) -> None:
        """Starts the scheduler for callback execution and management.

        This method initiates and starts a scheduler if it's not already running. Specifically, it ensures that the
        schedule of evaluations is managed asynchronously. It stores the reference to the created task in a dictionary
        for tracking and adds a callback that will handle cleanup after the task completion.
        """
        # Check if scheduler is running
        if not tasks:
            # Create Scheduler
            scheduler_task = create_task(scheduler.schedule_async(*args, **kwargs))  # Create scheduling task.
            scheduler_task.add_done_callback(tasks.remove)  # Remove task from tasks deque when done.
            tasks.append(scheduler_task)  # Add task to tasks deque.

    async def start_scheduler_async(self, scheduler: CallbackScheduler, tasks: deque, *args: Any, **kwargs: Any) -> None:
        """Asynchronously starts the scheduler for callback execution and management.

        This method initiates and starts a scheduler if it's not already running. Specifically, it ensures that the
        schedule of evaluations is managed asynchronously. It stores the reference to the created task in a dictionary
        for tracking and adds a callback that will handle cleanup after the task completion.
        """
        self.start_scheduler(scheduler, tasks, *args, **kwargs)

    # Task Management
    def join_tasks(self) -> None:
        """Joins all currently scheduled tasks."""
        for tasks in self.tasks.values():
            for task in tasks:
                while not task.done():
                    pass

    async def join_tasks_async(self, timeout: float | None = None) -> None:
        """Asynchronously joins all currently scheduled tasks."""
        all_tasks = deque()
        for tasks in self.tasks.values():
            for task in tasks:
                all_tasks.append(shield(task))

        if timeout is None:
            await gather(*all_tasks)
        else:
            await wait_for(gather(*all_tasks), timeout=timeout)

    def cancel_tasks(self) -> None:
        """Cancels all currently scheduled tasks."""
        for tasks in self.tasks.values():
            for task in tasks:
                task.cancel()
