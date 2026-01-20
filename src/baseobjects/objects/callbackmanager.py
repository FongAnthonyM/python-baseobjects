"""callbackmanager.py
An object which manages and executes callback functions with conditions and callers.

This module provides classes for managing callback functions with conditional execution. It includes functionality for
registering, formatting, and executing both synchronous and asynchronous callbacks. The module supports conditional
execution of callbacks, allowing callbacks to be executed only when specific conditions are met. It also provides task
management for asynchronous callbacks, including scheduling, cancellation, and joining of tasks.

The main classes in this module are:
- ConditionalCallbackEntry: A named tuple for storing callback entries with their conditions and callers
- CallbackScheduler: A class for scheduling and managing the execution of callbacks
- CallbackManager: The main class for registering and executing callbacks with conditions
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
from asyncio import Task, create_task, gather, shield
from collections import deque
from collections.abc import Iterable
from functools import partial
from typing import Any, ClassVar, NamedTuple

# Local Packages #
from ..bases import BaseObject, BaseReducible
from ..functions import MethodMultiplexer
from ..typing import AnyCallable


# Definitions #
# Classes #
class ConditionalCallbackEntry(NamedTuple):
    """An entry in a callback manager's registry.

    This named tuple represents a callback entry with its associated condition and caller functions. It is used by the
    CallbackManager to store and manage callback functions along with their execution conditions and caller methods.

    """

    callback: AnyCallable
    condition: AnyCallable
    caller: AnyCallable


class CallbackScheduler(BaseObject):
    """A scheduler for managing and executing callback functions.

    This class is responsible for scheduling and executing callback functions, particularly asynchronous callbacks. It
    maintains a mapping of callbacks to their associated task queues and provides methods for scheduling different types
    of callback executions.

    Attributes:
        callback_map: A list of tuples containing callback functions and their associated task queues.
        schedule: A method multiplexer for selecting and executing synchronous scheduling methods.
        schedule_async: A method multiplexer for selecting and executing asynchronous scheduling methods.
    """

    # Class Methods #
    default_schedule: ClassVar[str] = "schedule_callbacks"
    default_schedule_async: ClassVar[str] = "schedule_singleton_async_callbacks_async"

    # Attributes #
    callback_map: list[tuple[AnyCallable, deque[Any]]]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        callback_map: Iterable[tuple[AnyCallable, deque[Any]]] | None = None,
        schedule: AnyCallable | str | None = None,
        schedule_async: AnyCallable | str | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            callback_map: An iterable of tuples containing callback functions and their associated task queues.
            schedule: The scheduling function or method name to use for synchronous scheduling.
            schedule_async: The scheduling function or method name to use for asynchronous scheduling.
            *args: Additional positional arguments to pass to the parent class constructor.
            init: Whether to call the construct method during initialization.
            **kwargs: Additional keyword arguments to pass to the parent class constructor.
        """
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
        callback_map: Iterable[tuple[AnyCallable, deque[Any]]] | None = None,
        schedule: AnyCallable | str | None = None,
        schedule_async: AnyCallable | str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        This method sets up the callback map and configures the scheduling functions. It's called during initialization
        if init=True, or can be called manually to reinitialize the object.

        Args:
            callback_map: A list of tuples containing callback functions and their associated task queues.
            schedule: The scheduling function or method name to use for synchronous scheduling.
            schedule_async: The scheduling function or method name to use for asynchronous scheduling.
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
    def add_schedule_function(self, name: str, func: AnyCallable) -> None:
        """Adds a synchronous scheduling function to the scheduler.

        Args:
            name: The name to register the function under.
            func: The scheduling function to add.
        """
        self.schedule.add_function(name, func)

    def add_schedule_async_function(self, name: str, func: AnyCallable) -> None:
        """Adds an asynchronous scheduling function to the scheduler.

        Args:
            name: The name to register the function under.
            func: The asynchronous scheduling function to add.
        """
        self.schedule_async.add_function(name, func)

    def schedule_callbacks(self) -> None:
        """Schedules the evaluation of all callback functions.

        Executes all callback functions in the callback_map synchronously.
        """
        for callback, _ in self.callback_map:
            callback()

    def schedule_async_callbacks(self) -> None:
        """Schedules the evaluation of all asynchronous callback functions.

        Creates tasks for all asynchronous callbacks in the callback_map and adds them to their respective task queues.
        Each task is set up to remove itself from the queue when completed.
        """
        for callback_async, tasks in self.callback_map:
            callback_task = create_task(callback_async())
            callback_task.add_done_callback(tasks.remove)
            tasks.append(callback_task)

    async def schedule_async_callbacks_async(self) -> None:
        """Asynchronously schedules the evaluation of all callback functions.

        This is an async wrapper around schedule_async_callbacks that allows it to be called from async contexts.
        """
        self.schedule_async_callbacks()

    def schedule_singleton_async_callbacks(self) -> None:
        """Schedules the evaluation of asynchronous callbacks if they're not already running.

        Creates tasks for asynchronous callbacks only if there are no existing tasks for that callback in the task
        queue. This ensures only one instance of each callback is running at a time.
        """
        for callback_async, tasks in self.callback_map:
            if len(tasks) < 1:
                callback_task = create_task(callback_async())
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)

    async def schedule_singleton_async_callbacks_async(self) -> None:
        """Asynchronously schedules singleton evaluation of callback functions.

        This is an async wrapper around schedule_singleton_async_callbacks that allows it to be called from async
        contexts.
        """
        self.schedule_singleton_async_callbacks()


class CallbackManager(BaseReducible):
    """An object which manages and executes callback functions with conditions and callers.

    The CallbackManager class allows the registration, formatting, scheduling, and execution of synchronous and
    asynchronous callback functions. It supports default conditions and callers to streamline callback registration and
    ensures organized management of callback and task entries.

    Attributes:
        default_condition: The default condition to evaluate callbacks, set to "true_condition" by default.
        default_caller: The default caller name for callbacks, set to "evaluate_callback" by default.
        callbacks: A dictionary storing registered synchronous ConditionalCallbackEntry objects.
        callbacks_async: A dictionary storing registered asynchronous ConditionalCallbackEntry objects.
        conditional_callbacks: A dictionary storing registered synchronous ConditionalCallbackEntry objects.
        conditional_callbacks_async: A dictionary storing registered asynchronous ConditionalCallbackEntry objects.
        max_callback_tasks: The maximum number of callback tasks of each type allowed simultaneously.
        tasks: A dictionary storing tasks.

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

    callbacks: dict[str, AnyCallable]
    callbacks_async: dict[str, AnyCallable]
    conditional_callbacks: dict[str, AnyCallable]
    conditional_callbacks_async: dict[str, AnyCallable]

    scheduler_type: type = CallbackScheduler
    schedulers: dict[str, CallbackScheduler]

    max_callback_tasks: int = 1
    tasks: dict[str, deque[Task[Any]]]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        callbacks: dict[str, AnyCallable] | None = None,
        callbacks_async: dict[str, AnyCallable] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_caller: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Initializes internal registries and optionally constructs the instance using
        provided callback entries and defaults.

        Args:
            callbacks: Mapping of names to synchronous callback functions to register.
            callbacks_async: Mapping of names to asynchronous callback functions to register.
            *args: Additional positional arguments forwarded to construct for subclass initialization.
            default_condition: Default condition name used when registering callbacks.
                If provided, overrides the class default.
            default_caller: Default caller method name used when registering callbacks.
                If provided, overrides the class default.
            init: If True, call construct to finalize initialization with the provided arguments.
            **kwargs: Additional keyword arguments forwarded to construct for subclass initialization.
        """
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
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        names = ("callbacks", "callbacks_async", "scheduler_tasks", "caller_tasks", "callback_tasks", "tasks")

        match state:
            case dict():
                for name in names:
                    state.pop(name, None)
            case (dict() as state_dict, _):
                for name in names:
                    state_dict.pop(name, None)
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
        callbacks: dict[str, AnyCallable] | None = None,
        callbacks_async: dict[str, AnyCallable] | None = None,
        *args: Any,
        default_condition: str | None = None,
        default_caller: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            callbacks: The callback functions to add to the registry.
            callbacks_async: The async callback functions to add to the registry.
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
        callback: AnyCallable,
        condition: AnyCallable | str | None = None,
        caller: AnyCallable | str | None = None,
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
            condition = partial(condition, **condition_kwargs)  # type: ignore[arg-type, operator, misc]

        if caller_kwargs is not None:
            caller = partial(caller, **caller_kwargs)  # type: ignore[arg-type, operator, misc]

        return ConditionalCallbackEntry(callback, condition, caller)  # type: ignore[arg-type]

    def create_conditional_callback(
        self,
        callback: AnyCallable,
        condition: AnyCallable,
        caller: AnyCallable,
        task_name: str | None = None,
    ) -> AnyCallable:
        """Creates a conditional callback function.

        This method creates a partial function that combines a callback, condition, and caller.
        If a task_name is provided, it also creates a task queue for the callback and includes
        it in the partial function.

        Args:
            callback: The callback function to execute when the condition is met.
            condition: The condition function that determines if the callback should be executed.
            caller: The function responsible for calling the callback when the condition is met.
            task_name: Optional name for creating a task queue for this callback.

        Returns:
            A partial function that combines the condition, callback, and caller.
        """
        if task_name is None:
            return partial(caller, condition, callback)
        else:
            task_name = f"{task_name}_conditional_callback"
            if (tasks := self.tasks.get(task_name, None)) is None:
                self.tasks[task_name] = tasks = deque()
            return partial(caller, condition, callback, tasks=tasks)

    def create_scheduler(
        self,
        type_: type[CallbackScheduler] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> CallbackScheduler:
        """Creates a new callback scheduler instance.

        This method creates a new scheduler of the specified type or the default scheduler type if none is provided. The
        scheduler is responsible for managing and executing callbacks.

        Args:
            type_: The type of scheduler to create. If None, uses the default scheduler_type.
            *args: Positional arguments to pass to the scheduler constructor.
            **kwargs: Keyword arguments to pass to the scheduler constructor.

        Returns:
            A new CallbackScheduler instance.
        """
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
        """Creates a scheduler for conditional callbacks.

        This method creates a scheduler specifically for managing conditional callbacks. It maps the specified
        conditional callbacks to their task queues and creates a scheduler to manage them.

        Args:
            condition_names: An iterable of names of conditional callbacks to include in the scheduler.
            type_: The type of scheduler to create. If None, uses the default scheduler_type.
            *args: Positional arguments to pass to the scheduler constructor.
            **kwargs: Keyword arguments to pass to the scheduler constructor.

        Returns:
            A new CallbackScheduler instance configured for the specified conditional callbacks.
        """
        if type_ is None:
            type_ = self.scheduler_type

        callback_map: deque[tuple[AnyCallable, deque[Any]]] = deque()
        for name in condition_names:
            callback = self.conditional_callbacks_async[name]
            task_name = f"{name}_conditional_caller"
            if (tasks := self.tasks.get(task_name, None)) is None:
                self.tasks[task_name] = tasks = deque()
            callback_map.append((callback, tasks))

        return type_(callback_map, *args, **kwargs)

    # Callback Registration
    def register_callback(self, name: str, callback: AnyCallable, is_async: bool = False) -> None:
        """Registers a callback function with the manager.

        This method adds a callback function to either the synchronous or asynchronous callback registry, depending on
        the is_async parameter.

        Args:
            name: The name to register the callback under.
            callback: The callback function to register.
            is_async: Whether the callback is asynchronous. If True, the callback will be
                registered in the callbacks_async dictionary; otherwise, it will be registered
                in the callbacks dictionary.
        """
        if is_async:
            self.callbacks_async[name] = callback
        else:
            self.callbacks[name] = callback

    def register_callbacks(
        self,
        callbacks: dict[str, AnyCallable] | Iterable[tuple[str, AnyCallable]] | None = None,
        callbacks_async: dict[str, AnyCallable] | Iterable[tuple[str, AnyCallable]] | None = None,
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
        callback: AnyCallable,
        condition: AnyCallable | str | None = None,
        caller: AnyCallable | str | None = None,
        *args: Any,
        callback_kwargs: dict[str, Any] | None = None,
        condition_kwargs: dict[str, Any] | None = None,
        caller_kwargs: dict[str, Any] | None = None,
        is_async: bool = False,
        **kwargs: Any,
    ) -> None:
        """Registers a conditional callback function with the manager.

        This method formats and registers a callback function that will be executed only when a specified condition is
        met. It supports both synchronous and asynchronous callbacks.

        Args:
            name: The name to register the callback under.
            callback: The callback function to register.
            condition: The condition function or name that determines when the callback should be executed.
                If None, the default condition will be used.
            caller: The caller function or name that will execute the callback when the condition is met.
                If None, the default caller will be used.
            *args: Additional positional arguments to pass to format_conditional_callback.
            callback_kwargs: Keyword arguments to pass to the callback function when it's called.
            condition_kwargs: Keyword arguments to pass to the condition function when it's called.
            caller_kwargs: Keyword arguments to pass to the caller function when it's called.
            is_async: Whether the callback is asynchronous. If True, the callback will be registered
                in the conditional_callbacks_async dictionary and a task queue will be created for it.
            **kwargs: Additional keyword arguments to pass to format_conditional_callback.
        """
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
        """Registers a scheduler with the callback manager.

        This method either registers an existing scheduler or creates and registers a new one. If a scheduler is
        provided, it is registered directly. Otherwise, a new scheduler is created using the specified type and
        arguments.

        Args:
            name: The name to register the scheduler under.
            scheduler: An existing scheduler to register. If None, a new one will be created.
            type_: The type of scheduler to create if scheduler is None.
            *args: Positional arguments to pass to the scheduler constructor if creating a new one.
            **kwargs: Keyword arguments to pass to the scheduler constructor if creating a new one.
        """
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
        """Registers a conditional scheduler with the callback manager.

        This method either registers an existing scheduler or creates and registers a new one specifically for
        conditional callbacks. If a scheduler is provided, it is registered directly. Otherwise, a new conditional
        scheduler is created using the specified condition names, type, and arguments.

        Args:
            name: The name to register the scheduler under.
            scheduler: An existing scheduler to register. If None, a new one will be created.
            condition_names: Names of conditional callbacks to include in the scheduler if creating a new one.
                Required if scheduler is None.
            type_: The type of scheduler to create if scheduler is None.
            *args: Positional arguments to pass to the scheduler constructor if creating a new one.
            **kwargs: Keyword arguments to pass to the scheduler constructor if creating a new one.

        Raises:
            ValueError: If scheduler is None and condition_names is also None.
        """
        if scheduler is None:
            if condition_names is None:
                msg = "condition_names must be provided if scheduler is None."
                raise ValueError(msg)

            self.schedulers[name] = self.create_conditional_scheduler(condition_names, type_, *args, **kwargs)
        else:
            self.schedulers[name] = scheduler

    def register_scheduler_callback(self, name: str, scheduler: CallbackScheduler | str) -> None:
        """Registers a scheduler as both synchronous and asynchronous callbacks.

        This method creates callback functions that start the specified scheduler and registers them under the given
        name in both the synchronous and asynchronous callback registries. It also creates a task queue for the
        scheduler.

        Args:
            name: The name to register the callbacks under.
            scheduler: The scheduler to use, either as a CallbackScheduler instance or as a string
                name of a previously registered scheduler.
        """
        task_name = f"{name}_scheduler"
        if (tasks := self.tasks.get(task_name, None)) is None:
            if (tasks := self.tasks.get(name, None)) is None:
                self.tasks[name] = tasks = deque()

        if isinstance(scheduler, str):
            scheduler = self.schedulers[scheduler]

        self.callbacks[name] = partial(self.start_scheduler, scheduler, tasks)
        self.callbacks_async[name] = partial(self.start_scheduler_async, scheduler, tasks)

    # Callback Management
    def map_conditionals_to_scheduler(self, name: str, condition_names: Iterable[str]) -> None:
        """Maps conditional callbacks to an existing scheduler.

        This method adds the specified conditional callbacks to an existing scheduler's callback map. It creates task
        queues for each callback if they don't already exist.

        Args:
            name: The name of the scheduler to map the callbacks to.
            condition_names: An iterable of names of conditional callbacks to map to the scheduler.
        """
        callback_map: deque[tuple[AnyCallable, deque[Any]]] = deque()
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
    def call_callback(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: Keyword arguments to pass to the callback function.

        Returns:
            The result of the callback function.
        """
        return self.callbacks[name](*args, **kwargs)

    async def call_callback_async(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Asynchronously executes a given callback function.

        Args:
            name: The name of the callback to execute.
            *args: The positional arguments to pass to the callback function.
            **kwargs: Keyword arguments to pass to the callback function.

        Returns:
            The result of the callback function.
        """
        return await self.callbacks_async[name](*args, **kwargs)

    def call(self, callback: AnyCallable) -> Any:
        """Executes a callback function synchronously.

        This is a simple wrapper method that calls the provided callback function and returns its result.

        Args:
            callback: The callback function to execute.

        Returns:
            The result of the callback function.
        """
        return callback()

    async def call_async(self, callback: AnyCallable) -> Any:
        """Executes a callback function asynchronously.

        This is an async wrapper method that awaits the provided callback function and returns its result.

        Args:
            callback: The async callback function to execute.

        Returns:
            The result of the async callback function.
        """
        return await callback()

    # Conditional Callback Calling
    def call_conditional(
        self,
        condition: AnyCallable,
        callback: AnyCallable,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Evaluates the callback function if the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
            *args: Positional arguments forwarded to the callback when executed.
            **kwargs: Keyword arguments forwarded to the callback when executed.
        """
        if condition():
            callback(*args, **kwargs)

    async def call_conditional_async(
        self,
        condition_async: AnyCallable,
        callback_async: AnyCallable,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously evaluates the callback function if the callback condition is met.

        Args:
            condition_async: The condition to evaluate the callback function.
            callback_async: The callback function to evaluate.
            *args: Positional arguments forwarded to the async callback when executed.
            **kwargs: Keyword arguments forwarded to the async callback when executed.
        """
        if await condition_async():
            await callback_async(*args, **kwargs)

    def call_while_condition(
        self,
        condition: AnyCallable,
        callback: AnyCallable,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Evaluates the callback function while the callback condition is met.

        Args:
            condition: The condition to evaluate the callback function.
            callback: The callback function to evaluate.
            *args: Positional arguments forwarded to the callback each time it is executed.
            **kwargs: Keyword arguments forwarded to the callback each time it is executed.
        """
        while condition():
            callback(*args, **kwargs)

    async def call_while_condition_async(
        self,
        condition_async: AnyCallable,
        callback_async: AnyCallable,
        tasks: deque[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously evaluates the callback function while the callback condition is met.

        This method repeatedly checks the condition and executes the callback as long as the condition is true or there
        are pending tasks. It manages a queue of tasks to control concurrency and prevent overwhelming the system with
        too many simultaneous callback executions.

        Args:
            condition_async: The asynchronous condition function to evaluate.
            callback_async: The asynchronous callback function to execute when the condition is met.
            tasks: Optional deque to store and track callback tasks. If None, a new deque will be created.
            *args: Additional positional arguments (not used in this method but available for subclasses).
            **kwargs: Additional keyword arguments (not used in this method but available for subclasses).
        """
        if tasks is None:
            tasks = deque()

        checked = False
        while tasks or (checked := await condition_async()):
            # Add Callback Tasks and Await Them
            if tasks:
                await next(iter(tasks))
            elif len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = create_task(callback_async())
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)

    async def call_while_condition_task_async(
        self,
        condition_async: AnyCallable,
        callback_async: AnyCallable,
        tasks: deque[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously evaluates the callback function while the condition is met, with task awaiting.

        Similar to call_while_condition_async, but this method expects the callback_async function to return a task that
        will be added to the task queue. This allows for more complex task management where the callback itself creates
        and returns a task rather than being directly awaited.

        Args:
            condition_async: The asynchronous condition function to evaluate.
            callback_async: The asynchronous callback function that returns a task to be managed.
            tasks: A deque to store and track callback tasks.
            *args: Additional positional arguments (not used in this method but available for subclasses).
            **kwargs: Additional keyword arguments (not used in this method but available for subclasses).
        """
        if tasks is None:
            tasks = deque()

        checked = False
        while tasks or (checked := await condition_async()):
            # Add Callback Tasks and Await Them
            if tasks:
                await next(iter(tasks))
            elif len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = await callback_async()
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)

    async def enqueue_call_while_condition_async(
        self,
        condition_async: AnyCallable,
        callback_async: AnyCallable,
        tasks: deque[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously enqueues and executes callbacks while a condition is met.

        This method prioritizes creating new tasks when the condition is met, up to the maximum allowed number of
        concurrent tasks (max_callback_tasks). If the maximum is reached, it waits for existing tasks to complete before
        creating new ones. This approach ensures that new tasks are created as soon as possible when the condition is
        met.

        Args:
            condition_async: The asynchronous condition function to evaluate.
            callback_async: The asynchronous callback function to execute when the condition is met.
            tasks: Optional deque to store and track callback tasks. If None, a new deque will be created.
            *args: Additional positional arguments (not used in this method but available for subclasses).
            **kwargs: Additional keyword arguments (not used in this method but available for subclasses).
        """
        if tasks is None:
            tasks = deque()

        checked = False
        while tasks or (checked := await condition_async()):
            # Add Callback Tasks and Await Them
            if len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = create_task(callback_async())
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)
            else:
                await next(iter(tasks))

    async def enqueue_call_while_condition_task_async(
        self,
        condition_async: AnyCallable,
        callback_async: AnyCallable,
        tasks: deque[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously enqueues and executes task-returning callbacks while a condition is met.

        Similar to enqueue_call_while_condition_async, but this method expects the callback_async function to return a
        task that will be added to the task queue. This allows for more complex task management where the callback
        itself creates and returns a task rather than being directly awaited.

        This method prioritizes creating new tasks when the condition is met, up to the maximum allowed number of
        concurrent tasks (max_callback_tasks). If the maximum is reached, it waits for existing tasks to complete before
        creating new ones.

        Args:
            condition_async: The asynchronous condition function to evaluate.
            callback_async: The asynchronous callback function that returns a task to be managed.
            tasks: A deque to store and track callback tasks.
            *args: Additional positional arguments (not used in this method but available for subclasses).
            **kwargs: Additional keyword arguments (not used in this method but available for subclasses).
        """
        if tasks is None:
            tasks = deque()

        checked = False
        while tasks or (checked := await condition_async()):
            # Add Callback Tasks and Await Them
            if len(tasks) < self.max_callback_tasks and checked:
                # Create Callback Tasks
                callback_task = await callback_async()
                callback_task.add_done_callback(tasks.remove)
                tasks.append(callback_task)
            else:
                await next(iter(tasks))

    # Callback Scheduling
    def start_scheduler(self, scheduler: CallbackScheduler, tasks: deque[Any], *args: Any, **kwargs: Any) -> None:
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

    async def start_scheduler_async(
        self,
        scheduler: CallbackScheduler,
        tasks: deque[Any],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Asynchronously starts the scheduler for callback execution and management.

        This method initiates and starts a scheduler if it's not already running. Specifically, it ensures that the
        schedule of evaluations is managed asynchronously. It stores the reference to the created task in a dictionary
        for tracking and adds a callback that will handle cleanup after the task completion.
        """
        self.start_scheduler(scheduler, tasks, *args, **kwargs)

    # Task Management
    def join_tasks(self) -> None:
        """Joins all currently scheduled tasks.

        This method blocks until all tasks in the task registry are completed. It uses a busy-waiting approach, which
        may not be efficient for long-running tasks. For a more efficient approach, use join_tasks_async.
        """
        for tasks in self.tasks.values():
            for task in tasks:
                while not task.done():
                    pass

    async def join_tasks_async(self, timeout: float | None = None) -> None:
        """Asynchronously joins all currently scheduled tasks.

        This method awaits the completion of all tasks in the task registry. It uses asyncio.gather to efficiently wait
        for all tasks and can optionally timeout after a specified duration.

        Args:
            timeout: Optional timeout in seconds. If provided, the method will raise
                asyncio.TimeoutError if the tasks don't complete within this time.
        """
        all_tasks: deque[Any] = deque()
        for tasks in self.tasks.values():
            for task in tasks:
                all_tasks.append(shield(task))

        async with asyncio.timeout(timeout):
            await gather(*all_tasks)

    def cancel_tasks(self) -> None:
        """Cancels all currently scheduled tasks.

        This method cancels all tasks in the task registry. Cancelled tasks will raise asyncio.CancelledError when
        awaited, unless the cancellation is caught and handled.
        """
        for tasks in self.tasks.values():
            for task in tasks:
                task.cancel()
