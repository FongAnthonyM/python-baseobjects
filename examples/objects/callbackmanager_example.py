#!/usr/bin/env python
"""callbackmanager_example.py
An example of how to use CallbackManager class.

This example demonstrates:
1. Creating a CallbackManager instance
2. Registering and calling simple callbacks
3. Registering and calling conditional callbacks
4. Using callback schedulers
5. Working with asynchronous callbacks
   - Registering and calling async callbacks
   - Using async conditional callbacks
   - Managing async tasks with timeouts
6. Managing callback tasks
"""


# Imports #
# Standard Libraries #
import asyncio
import time
from asyncio import create_task
from collections import deque
from typing import Any, Callable, Dict, List

# Source Packages #
from baseobjects.objects import CallbackManager
from baseobjects.objects.callbackmanager import CallbackScheduler, ConditionalCallbackEntry


# Classes #
class DataRoutingProcessor:
    """A class that routes and processes data using CallbackManager as the routing engine.

    The simple case of checking resources can be done in many ways. However, CallbackManager offers conditional
    management in a separate object, which can reduce the logic and complexity of the main class. Additionally,
    CallbackManager is intended to manage the asynchronous execution of conditional callbacks, but this example
    highlights the basic usage in a synchronous context.
    """

    def __init__(self):
        """Initialize with data and a callback manager.

        Args:
            data: Initial data to process
        """
        self.point_a = None
        self.point_b = None
        self.callback_manager = CallbackManager()

        # Register some default callbacks
        self.callback_manager.register_conditional_callback(
            "all_strings",
            self.print_data_strings,
            self.all_strings,
        )
        self.callback_manager.register_conditional_callback(
            "all_numbers",
            self.print_data_numbers,
            self.all_numbers,
        )
        self.callback_manager.register_conditional_callback(
            "a_is_string",
            self.print_a_is_string,
            self.a_is_string,
        )
        self.callback_manager.register_conditional_callback(
            "b_is_string",
            self.print_b_is_string,
            self.b_is_string,
        )

    def all_strings(self) -> bool:
        """Check if all data points are strings."""
        return isinstance(self.point_a, str) and isinstance(self.point_b, str)

    def all_numbers(self) -> bool:
        """Check if all data points are numbers."""
        return isinstance(self.point_a, int) and isinstance(self.point_b, int)

    def a_is_string(self) -> bool:
        """Check if data point A is a string."""
        return isinstance(self.point_a, str) and isinstance(self.point_b, int)

    def b_is_string(self) -> bool:
        """Check if data point B is a string."""
        return isinstance(self.point_b, str) and isinstance(self.point_a, int)

    def print_data_strings(self) -> None:
        """Print the data points."""
        print(f"Both are strings: {self.point_a} {self.point_b}")

    def print_data_numbers(self) -> None:
        """Print the data points."""
        print(f"Both are numbers: {self.point_a} + {self.point_b} = {self.point_a + self.point_b}")

    def print_a_is_string(self) -> None:
        """Print the data point A."""
        print(f"A is a string: {self.point_a}")

    def print_b_is_string(self) -> None:
        """Print the data point B."""
        print(f"B is a string: {self.point_b}")

    def run_callbacks(self):
        """Run all callbacks."""
        self.callback_manager.conditional_callbacks["all_strings"]()
        self.callback_manager.conditional_callbacks["all_numbers"]()
        self.callback_manager.conditional_callbacks["a_is_string"]()
        self.callback_manager.conditional_callbacks["b_is_string"]()


# Example Sections #
def basic_callback_example():
    """Demonstrate basic usage of CallbackManager with simple callbacks."""
    print("\nBasic Callback Example:")

    # Create a callback manager
    callback_manager = CallbackManager()

    # Define some simple callback functions
    def on_event(message: str) -> None:
        print(f"Event received: {message}")

    def on_notification(sender: str, message: str) -> None:
        print(f"Notification from {sender}: {message}")

    # Register callbacks
    callback_manager.register_callback("event", on_event)
    callback_manager.register_callback("notification", on_notification)

    # Call callbacks
    print("Calling 'event' callback:")
    callback_manager.call_callback("event", "Something happened!")

    print("\nCalling 'notification' callback:")
    callback_manager.call_callback("notification", "System", "Server is running")

    # Register multiple callbacks at once
    def on_warning(message: str) -> None:
        print(f"Warning: {message}")

    def on_error(error_code: int, message: str) -> None:
        print(f"Error {error_code}: {message}")

    callback_manager.register_callbacks({"warning": on_warning, "error": on_error})

    print("\nCalling multiple registered callbacks:")
    callback_manager.call_callback("warning", "Disk space is low")
    callback_manager.call_callback("error", 404, "Resource not found")


def conditional_callback_example():
    """Demonstrate conditional callbacks with CallbackManager."""
    print("\nConditional Callback Example:")

    # Create a callback manager
    callback_manager = CallbackManager()

    # Define condition and callback function
    def is_important(priority: int) -> bool:
        return priority >= 5

    def process_message(message: str, priority: int) -> None:
        print(f"Processing message with priority {priority}: {message}")

    # Demonstrate using call_conditional directly
    print("Using call_conditional directly with static methods:")
    print("Calling with priority 3 (should not execute):")
    callback_manager.call_conditional(lambda: is_important(3), lambda: process_message("Low priority message", 3))
    print("(Did not print)")

    print("Calling with priority 7 (should execute):")
    callback_manager.call_conditional(lambda: is_important(7), lambda: process_message("High priority message", 7))

    # Define condition and callback function
    mutable_state = {}

    def check_for_code() -> bool:
        return "code" in mutable_state

    def process_message_with_code(message: str) -> None:
        print(f"Code {mutable_state['code']}: {message}")

    # Demonstrate registering
    print("Using call_conditional to check state:")
    callback_manager.register_conditional_callback(
        name="code_printer",
        callback=process_message_with_code,
        condition=check_for_code,
        callback_kwargs={"message": "extra message"},
    )

    print("Calling without a code:")
    callback_manager.conditional_callbacks["code_printer"]()
    print("(Did not print)")

    print("Calling with code set to 1234:")
    mutable_state["code"] = 1234
    callback_manager.conditional_callbacks["code_printer"]()


def data_processor_example():
    """Demonstrate using CallbackManager in a class."""
    print("\nData Processor Example:")

    # Create a data processor with callbacks
    processor = DataRoutingProcessor()

    print("Call conditional callbacks:")
    processor.run_callbacks()
    print("(Did not print)")

    print("Set to strings:")
    processor.point_a = "a"
    processor.point_b = "b"
    processor.run_callbacks()

    print("Set to numbers:")
    processor.point_a = 1
    processor.point_b = 2
    processor.run_callbacks()

    print("Set to string and number:")
    processor.point_a = "a"
    processor.point_b = 2
    processor.run_callbacks()

    print("Set to number and string:")
    processor.point_a = 1
    processor.point_b = "b"
    processor.run_callbacks()

    print("Set only point A to string:")
    processor.point_a = "a"
    processor.point_b = None
    processor.run_callbacks()
    print("(Did not print)")


# Asynchronous Example Sections #
async def basic_callback_example_async():
    """Demonstrate basic usage of CallbackManager with asynchronous callbacks."""
    print("\nBasic Async Callback Example:")

    # Create a callback manager
    callback_manager = CallbackManager()

    # Define some simple async callback functions
    async def on_event_async(message: str) -> None:
        await asyncio.sleep(0.1)  # Simulate async operation
        print(f"Async event received: {message}")

    async def on_notification_async(sender: str, message: str) -> None:
        await asyncio.sleep(0.1)  # Simulate async operation
        print(f"Async notification from {sender}: {message}")

    # Register async callbacks
    callback_manager.register_callback("event_async", on_event_async, is_async=True)
    callback_manager.register_callback("notification_async", on_notification_async, is_async=True)

    # Call async callbacks
    print("Calling 'event_async' callback:")
    await callback_manager.call_callback_async("event_async", "Something happened asynchronously!")

    print("\nCalling 'notification_async' callback:")
    await callback_manager.call_callback_async("notification_async", "System", "Server is running asynchronously")

    # Register multiple async callbacks at once
    async def on_warning_async(message: str) -> None:
        await asyncio.sleep(0.1)  # Simulate async operation
        print(f"Async warning: {message}")

    async def on_error_async(error_code: int, message: str) -> None:
        await asyncio.sleep(0.1)  # Simulate async operation
        print(f"Async error {error_code}: {message}")

    callback_manager.register_callbacks(
        callbacks_async={"warning_async": on_warning_async, "error_async": on_error_async}
    )

    print("\nCalling multiple registered async callbacks:")
    await callback_manager.call_callback_async("warning_async", "Disk space is low")
    await callback_manager.call_callback_async("error_async", 404, "Resource not found")


async def conditional_callback_example_async():
    """Demonstrate conditional callbacks with CallbackManager using async methods."""
    print("\nConditional Async Callback Example:")

    # Create a callback manager
    callback_manager = CallbackManager()

    # Define async condition and callback function
    async def is_important_async(priority: int) -> bool:
        await asyncio.sleep(0.1)  # Simulate async condition check
        return priority >= 5

    async def process_message_async(message: str, priority: int) -> None:
        await asyncio.sleep(0.1)  # Simulate async processing
        print(f"Async processing message with priority {priority}: {message}")

    # Demonstrate using call_conditional_async directly
    print("Using call_conditional_async directly:")
    print("Calling with priority 3 (should not execute):")
    await callback_manager.call_conditional_async(
        lambda: is_important_async(3), lambda: process_message_async("Low priority message", 3)
    )
    print("(Did not print)")

    print("Calling with priority 7 (should execute):")
    await callback_manager.call_conditional_async(
        lambda: is_important_async(7), lambda: process_message_async("High priority message", 7)
    )

    # Define async condition and callback function with mutable state
    mutable_state = {}

    async def check_for_code_async() -> bool:
        await asyncio.sleep(0.1)  # Simulate async condition check
        return "code" in mutable_state

    async def process_message_with_code_async(message: str) -> None:
        await asyncio.sleep(0.1)  # Simulate async processing
        print(f"Async code {mutable_state['code']}: {message}")

    # Demonstrate registering async conditional callback
    print("Using async conditional callbacks with state:")
    callback_manager.register_conditional_callback(
        name="code_printer_async",
        callback=process_message_with_code_async,
        condition=check_for_code_async,
        caller="call_conditional_async",
        callback_kwargs={"message": "extra async message"},
        is_async=True,
    )

    print("Calling without a code:")
    await callback_manager.conditional_callbacks_async["code_printer_async"]()
    print("(Did not print)")

    print("Calling with code set to 5678:")
    mutable_state["code"] = 5678
    await callback_manager.conditional_callbacks_async["code_printer_async"]()


async def task_management_example_async():
    """Demonstrate task management with CallbackManager."""
    print("\nTask Management Example:")

    # Create a callback manager
    callback_manager = CallbackManager()
    tasks = deque()

    # Define async condition and callback functions
    async def always_true_async() -> bool:
        return True

    async def limited_true_async() -> bool:
        # Only return true for a limited number of calls
        limited_true_async.count += 1
        if limited_true_async.count <= 5:
            return True
        return False

    limited_true_async.count = 0

    async def task_callback_async() -> None:
        task_id = task_callback_async.counter
        task_callback_async.counter += 1
        print(f"Starting task {task_id}")
        await asyncio.sleep(0.2)  # Simulate work
        print(f"Completed task {task_id}")

    task_callback_async.counter = 1

    # Demonstrate call_while_condition_async
    print("Using call_while_condition_async to run 5 tasks:")
    await callback_manager.call_while_condition_async(limited_true_async, task_callback_async, tasks)
    print("All tasks completed")

    # Reset counter
    limited_true_async.count = 0
    task_callback_async.counter = 1

    # Demonstrate enqueue_call_while_condition_async
    print("\nUsing enqueue_call_while_condition_async to run 5 tasks concurrently:")
    await callback_manager.enqueue_call_while_condition_async(limited_true_async, task_callback_async, tasks)
    print("All tasks completed")

    # Demonstrate join_tasks_async with timeout
    print("\nDemonstrating join_tasks_async with timeout:")

    # Create a long-running task
    async def long_running_task() -> None:
        print("Starting long-running task")
        try:
            await asyncio.sleep(2)  # This will be interrupted by the timeout
            print("Long-running task completed")  # This won't be printed
        except asyncio.CancelledError:
            print("Long-running task was cancelled")
            raise

    # Register and start the task
    task = create_task(long_running_task())
    task.add_done_callback(lambda t: tasks.remove(t) if t in tasks else None)
    tasks.append(task)

    try:
        print("Waiting for tasks with a 0.5 second timeout...")
        await callback_manager.join_tasks_async(timeout=0.5)
    except asyncio.TimeoutError:
        print("Timeout occurred while waiting for tasks")
        callback_manager.cancel_tasks()

    # Wait a moment for the cancellation to complete
    await asyncio.sleep(0.1)
    print("Task management example completed")


async def scheduler_example_async():
    """Demonstrate using schedulers with CallbackManager asynchronously."""
    print("\nAsync Scheduler Example:")

    # Create a callback manager
    callback_manager = CallbackManager()

    # Define some async callback functions
    async def async_task1() -> None:
        await asyncio.sleep(0.1)  # Simulate async work
        print("Executing async task 1")

    async def async_task2() -> None:
        await asyncio.sleep(0.1)  # Simulate async work
        print("Executing async task 2")

    # Create task queues
    task1_queue = deque()
    task2_queue = deque()

    # Create a basic scheduler for async tasks
    print("Creating a scheduler for async tasks:")
    async_scheduler = callback_manager.create_scheduler()

    # Add async callbacks to the scheduler
    async_scheduler.callback_map.extend([(async_task1, task1_queue), (async_task2, task2_queue)])

    # Execute the async scheduler
    print("Executing schedule_async_callbacks:")
    async_scheduler.schedule_async_callbacks()

    # Wait for tasks to complete
    await asyncio.sleep(0.2)

    # Create and register a conditional scheduler
    print("\nCreating a conditional scheduler:")

    # Define condition functions
    async def condition1() -> bool:
        await asyncio.sleep(0.1)
        return True

    async def condition2() -> bool:
        await asyncio.sleep(0.1)
        return False

    # Register conditional callbacks
    callback_manager.register_conditional_callback(
        "async_condition1", async_task1, condition1, "call_conditional_async", is_async=True
    )

    callback_manager.register_conditional_callback(
        "async_condition2", async_task2, condition2, "call_conditional_async", is_async=True
    )

    # Create a conditional scheduler
    print("Creating and registering a conditional scheduler:")
    callback_manager.register_conditional_scheduler(
        "conditional_scheduler", condition_names=["async_condition1", "async_condition2"]
    )

    # Start the conditional scheduler
    print("Starting the conditional scheduler:")
    tasks = deque()
    await callback_manager.start_scheduler_async(callback_manager.schedulers["conditional_scheduler"], tasks)

    # Wait for tasks to complete
    await asyncio.sleep(0.3)

    # Map additional conditionals to an existing scheduler
    print("\nMapping additional conditionals to existing scheduler:")

    # Register another conditional callback
    async def async_task3() -> None:
        await asyncio.sleep(0.1)
        print("Executing async task 3")

    callback_manager.register_conditional_callback(
        "async_condition3",
        async_task3,
        condition1,  # Reuse the first condition
        "call_conditional_async",
        is_async=True,
    )

    # Map the new conditional to the existing scheduler
    callback_manager.map_conditionals_to_scheduler("conditional_scheduler", ["async_condition3"])

    # Start the scheduler again
    print("Starting the updated scheduler:")
    await callback_manager.start_scheduler_async(callback_manager.schedulers["conditional_scheduler"], tasks)

    # Wait for tasks to complete
    await asyncio.sleep(0.3)

    print("Async scheduler example completed")


# Main #
if __name__ == "__main__":
    # Run synchronous examples
    basic_callback_example()
    conditional_callback_example()
    data_processor_example()

    # Run asynchronous examples
    asyncio.run(basic_callback_example_async())
    asyncio.run(conditional_callback_example_async())
    asyncio.run(task_management_example_async())
    asyncio.run(scheduler_example_async())
