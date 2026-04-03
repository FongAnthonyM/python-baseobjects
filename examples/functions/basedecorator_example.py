#!/usr/bin/env python
"""basedecorator_example.py
An example of how to create and use BaseDecorator.

This example demonstrates:
1. Using BaseDecorator directly as a simple decorator
2. Creating a decorator that accepts arguments
3. Creating custom decorators by subclassing BaseDecorator
4. Handling both regular functions and coroutine functions
5. Implementing decorators with state
6. Pickling and unpickling decorators
"""

# Imports #
# Standard Libraries #
import asyncio
import pickle
import time
from typing import Any

# Source Packages #
from baseobjects.functions import BaseDecorator
from baseobjects.typing import AnyCallable


# Definitions #
# Simple BaseDecorator Usage #
class TimerDecorator(BaseDecorator):
    """A decorator that measures the execution time of a function.

    This decorator demonstrates the basic usage of BaseDecorator by creating a simple timer that measures how long a
    function takes to execute.
    """

    def __init__(self, func: AnyCallable | None = None, decimal_places: int = 4) -> None:
        """Initializes the timer decorator.

        Args:
            func: The function to decorate.
            decimal_places: The number of decimal places to display in the time.
        """
        super().__init__(func)
        self.decimal_places = decimal_places

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the decorated function and measure its execution time.

        Args:
            *args: Positional arguments to pass to the decorated function.
            **kwargs: Keyword arguments to pass to the decorated function.

        Returns:
            The result of the decorated function.
        """
        wrapped = self.__wrapped__
        assert wrapped is not None
        start_time = time.time()
        result = wrapped(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        name = getattr(wrapped, "__name__", "wrapper")
        print(f"Function '{name}' executed in {execution_time:.{self.decimal_places}f} seconds")
        return result


# Decorator with Arguments #
class RepeatDecorator(BaseDecorator):
    """A decorator that repeats the execution of a function.

    This decorator demonstrates how to create a decorator that accepts arguments by using BaseDecorator's dual-mode
    behavior.
    """

    def __init__(self, func: AnyCallable | None = None, times: int = 1, show_iteration: bool = True) -> None:
        """Initializes the repeat decorator.

        Args:
            func: The function to decorate.
            times: The number of times to repeat the function execution.
            show_iteration: Whether to show the iteration number in the output.
        """
        super().__init__(func)
        self.times = times
        self.show_iteration = show_iteration

    def __call__(self, *args: Any, **kwargs: Any) -> list[Any]:
        """Executes the decorated function multiple times.

        Args:
            *args: Positional arguments to pass to the decorated function.
            **kwargs: Keyword arguments to pass to the decorated function.

        Returns:
            A list of results from each execution of the decorated function.
        """
        wrapped = self.__wrapped__
        assert wrapped is not None
        results = []
        for i in range(self.times):
            if self.show_iteration:
                print(f"Iteration {i + 1}/{self.times}:")
            result = wrapped(*args, **kwargs)
            results.append(result)
        return results


# Async Decorator #
class AsyncRetryDecorator(BaseDecorator):
    """A decorator that retries an async function on failure.

    This decorator demonstrates how BaseDecorator can handle coroutine functions.
    """

    def __init__(self, func: AnyCallable | None = None, max_retries: int = 3, delay: float = 1.0) -> None:
        """Initializes the async retry decorator.

        Args:
            func: The coroutine function to decorate.
            max_retries: The maximum number of retry attempts.
            delay: The delay between retries in seconds.
        """
        super().__init__(func)
        self.max_retries = max_retries
        self.delay = delay

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the decorated coroutine function with retry logic.

        Args:
            *args: Positional arguments to pass to the decorated function.
            **kwargs: Keyword arguments to pass to the decorated function.

        Returns:
            The result of the decorated coroutine function.
        """
        wrapped = self.__wrapped__
        assert wrapped is not None
        last_exception: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                if attempt > 0:
                    print(f"Retry attempt {attempt}/{self.max_retries}...")
                return await wrapped(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    print(f"Attempt {attempt + 1} failed: {e!s}")
                    print(f"Waiting {self.delay} seconds before next attempt...")
                    await asyncio.sleep(self.delay)
                else:
                    print(f"All {self.max_retries} retry attempts failed.")
                    if last_exception is not None:
                        raise last_exception from None
        return None


# Decorator with State #
class CounterDecorator(BaseDecorator):
    """A decorator that counts how many times a function is called.

    This decorator demonstrates how to create a decorator with state.
    """

    def __init__(self, func: AnyCallable | None = None) -> None:
        """Initializes the counter decorator.

        Args:
            func: The function to decorate.
        """
        super().__init__(func)
        self.call_count = 0

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the decorated function and increment the call counter.

        Args:
            *args: Positional arguments to pass to the decorated function.
            **kwargs: Keyword arguments to pass to the decorated function.

        Returns:
            The result of the decorated function.
        """
        wrapped = self.__wrapped__
        assert wrapped is not None
        self.call_count += 1
        name = getattr(wrapped, "__name__", "wrapper")
        print(f"Call #{self.call_count} to function '{name}'")
        return wrapped(*args, **kwargs)

    def reset_counter(self) -> None:
        """Reset the call counter to zero."""
        self.call_count = 0

    def __getstate__(self) -> dict[str, Any]:
        """Gets the state of the decorator for pickling.

        Returns:
            A dictionary containing the state of the decorator.
        """
        state = super().__getstate__()
        if isinstance(state, dict):
            state["call_count"] = self.call_count
            return state
        return {"call_count": self.call_count}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Sets the state of the decorator from unpickling.

        Args:
            state: A dictionary containing the state of the decorator.
        """
        super().__setstate__(state)
        self.call_count = state.get("call_count", 0)


# Example Functions #
def add(a: int, b: int) -> int:
    """Adds two numbers together.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the two numbers.
    """
    return a + b


def fibonacci(n: int) -> int:
    """Calculates the nth Fibonacci number recursively.

    Args:
        n: The position in the Fibonacci sequence.

    Returns:
        The nth Fibonacci number.
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


async def fetch_data(url: str, timeout: float = 1.0) -> dict[str, Any]:
    """Simulate fetching data from a URL.

    Args:
        url: The URL to fetch data from.
        timeout: The timeout in seconds.

    Returns:
        A dictionary containing the fetched data.

    Raises:
        Exception: If the URL is invalid.
        TimeoutError: If the timeout is exceeded.
    """
    # Simulate network delay
    await asyncio.sleep(0.1)

    # Simulate random failures
    if "error" in url:
        msg = f"Failed to fetch data from {url}"
        raise Exception(msg)

    # Simulate timeout
    if timeout < 0.2:
        msg = f"Request timed out after {timeout} seconds"
        raise TimeoutError(msg)

    # Returns simulated data
    return {"url": url, "timestamp": time.time(), "data": f"Data from {url}"}


# Example Sections #
def basic_decorator_example() -> None:
    """Demonstrates basic usage of BaseDecorator."""
    print("Basic Decorator Example:\n")

    # Creates a decorated function using TimerDecorator
    timed_fibonacci = TimerDecorator(fibonacci)

    # Calls the decorated function
    print("Calculating Fibonacci numbers with timing:")
    result = timed_fibonacci(10)
    print(f"fibonacci(10) = {result} == 55")

    result = timed_fibonacci(20)
    print(f"fibonacci(20) = {result} == 6765")

    # Use the decorator as a function decorator
    @TimerDecorator
    def calculate_sum(n: int) -> int:
        """Calculates the sum of numbers from 1 to n.

        Returns:
            The sum of numbers.
        """
        return sum(range(1, n + 1))

    # Calls the decorated function
    print("\nCalculating sums with timing:")
    result = calculate_sum(1000)
    print(f"sum(1-1000) = {result} == 500500")

    result = calculate_sum(10000)
    print(f"sum(1-10000) = {result} == 50005000")

    print()


def decorator_with_arguments_example() -> None:
    """Demonstrates creating decorators that accept arguments."""
    print("Decorator with Arguments Example:\n")

    # Creates a decorated function with arguments
    repeated_add = RepeatDecorator(add, times=3, show_iteration=True)

    # Calls the decorated function
    print("Repeating add function 3 times:")
    results = repeated_add(5, 7)
    print(f"Results: {results} == [12, 12, 12]")

    # Use the decorator with arguments
    @RepeatDecorator(times=2, show_iteration=False)
    def greet(name: str) -> str:
        """Greet a person.

        Returns:
            The greeting string.
        """
        greeting = f"Hello, {name}!"
        print(greeting)
        return greeting

    # Calls the decorated function
    print("\nRepeating greet function 2 times (without showing iterations):")
    results = greet("World")  # type: ignore[operator]
    print(f"Results: {results} == ['Hello, World!', 'Hello, World!']")

    # Use the decorator without arguments (default values)
    @RepeatDecorator
    def square(x: int) -> int:
        """Square a number.

        Returns:
            The squared number.
        """
        return x * x

    # Calls the decorated function
    print("\nRepeating square function once (default):")
    results = square(4)
    print(f"Results: {results} == [16]")

    print()


async def async_decorator_example() -> None:
    """Demonstrates using BaseDecorator with async functions."""
    print("Async Decorator Example:\n")

    # Creates a decorated async function
    retry_fetch = AsyncRetryDecorator(fetch_data, max_retries=3, delay=0.5)

    # Calls the decorated function with a valid URL
    print("Fetching data from a valid URL:")
    try:
        result = await retry_fetch("https://example.com/api/data")
        print(f"Success! Received: {result['data']}")
    except Exception as e:
        print(f"Failed: {e}")

    # Calls the decorated function with an error URL
    print("\nFetching data from an error URL (should retry and fail):")
    try:
        result = await retry_fetch("https://example.com/api/error")
        print(f"Success! Received: {result['data']}")
    except Exception as e:
        print(f"Failed after retries: {e}")

    # Use the decorator as a function decorator
    @AsyncRetryDecorator(max_retries=2, delay=0.3)
    async def fetch_with_timeout(url: str, timeout: float = 0.5) -> dict[str, Any]:
        """Fetch data with a specified timeout.

        Returns:
            The fetched data.
        """
        return await fetch_data(url, timeout)

    # Calls the decorated function with a timeout that's too short
    print("\nFetching data with a short timeout (should retry and succeed with default delay):")
    try:
        result = await fetch_with_timeout("https://example.com/api/data", timeout=0.1)  # type: ignore[operator]
        print(f"Success! Received: {result['data']}")
    except Exception as e:
        print(f"Failed after retries: {e}")

    print()


def decorator_with_state_example() -> None:
    """Demonstrates creating decorators with state."""
    print("Decorator with State Example:\n")

    # Creates a decorated function with state
    counted_add = CounterDecorator(add)

    # Calls the decorated function multiple times
    print("Calling the add function multiple times:")
    result = counted_add(1, 2)
    print(f"1 + 2 = {result} == 3")

    result = counted_add(3, 4)
    print(f"3 + 4 = {result} == 7")

    result = counted_add(5, 6)
    print(f"5 + 6 = {result} == 11")

    # Access the state
    print(f"\nTotal calls: {counted_add.call_count} == 3")

    # Reset the state
    counted_add.reset_counter()
    print(f"After reset, total calls: {counted_add.call_count} == 0")

    # Calls again after reset
    result = counted_add(7, 8)
    print(f"7 + 8 = {result} == 15")
    print(f"Total calls after reset: {counted_add.call_count} == 1")

    print()


def pickling_decorator_example() -> None:
    """Demonstrates pickling and unpickling decorators."""
    print("Pickling Decorator Example:\n")

    # Creates a decorated function with state
    counted_fibonacci = CounterDecorator(fibonacci)

    # Calls the decorated function a few times
    print("Calling the fibonacci function multiple times:")
    result = counted_fibonacci(5)
    print(f"fibonacci(5) = {result} == 5")

    result = counted_fibonacci(7)
    print(f"fibonacci(7) = {result} == 13")

    # Checks the state before pickling
    print(f"\nTotal calls before pickling: {counted_fibonacci.call_count} == 2")

    # Pickle the decorator
    print("\nPickling the decorator...")
    pickled_decorator = pickle.dumps(counted_fibonacci)

    # Unpickle the decorator
    print("Unpickling the decorator...")
    unpickled_decorator = pickle.loads(pickled_decorator)

    # Checks the state after unpickling
    print(f"Total calls after unpickling: {unpickled_decorator.call_count} == 2")

    # Calls the unpickled decorator
    result = unpickled_decorator(10)
    print(f"fibonacci(10) = {result} == 55")
    print(f"Total calls after additional call: {unpickled_decorator.call_count} == 3")

    print()


# Main #
if __name__ == "__main__":
    # Basic usage of BaseDecorator
    basic_decorator_example()

    # Decorator with arguments
    decorator_with_arguments_example()

    # Async decorator
    asyncio.run(async_decorator_example())

    # Decorator with state
    decorator_with_state_example()

    # Pickling decorator
    pickling_decorator_example()
