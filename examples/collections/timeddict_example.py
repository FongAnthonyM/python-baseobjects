#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""timeddict_example.py
An example of how to use TimedDict class.

This example demonstrates:
1. Creating and using a TimedDict
2. Setting and manipulating the lifetime and expiration
3. Using context managers to pause the timer
4. Practical use cases for TimedDict
"""
# Imports #
# Standard Libraries #
import time
from typing import Any, Dict

# Third-Party Packages #
from baseobjects.collections import TimedDict

# Local Packages #


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of TimedDict."""
    print("\nBasic TimedDict Usage:")

    # Create a TimedDict with a 2-second lifetime
    cache = TimedDict()
    cache.lifetime = 2  # 2 seconds

    print(f"Created TimedDict with lifetime: {cache.lifetime} seconds")

    # Add items to the cache
    cache["key1"] = "value1"
    cache["key2"] = "value2"
    cache["key3"] = "value3"

    print("Initial cache contents:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Access items (like a regular dictionary)
    print("\nAccessing items:")
    print(f"cache['key1']: {cache['key1']} == 'value1'")
    print(f"'key2' in cache: {'key2' in cache} == True")

    # Wait for less than the lifetime
    print("\nWaiting for 1 second (less than lifetime)...")
    time.sleep(1)

    # Check if items are still in the cache
    print("Cache contents after 1 second:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Wait for the cache to expire
    print("\nWaiting for 1.5 more seconds (total > lifetime)...")
    time.sleep(1.5)

    # Check if items are still in the cache (they should be cleared)
    print("Cache contents after expiration:")
    print(f"Cache is empty: {len(cache) == 0} == True")

    # Add new items after expiration
    print("\nAdding new items after expiration:")
    cache["new_key"] = "new_value"

    print("New cache contents:")
    for key, value in cache.items():
        print(f"  {key}: {value}")


def timer_manipulation_example():
    """Demonstrate manipulating the timer in TimedDict."""
    print("\nTimer Manipulation Example:")

    # Create a TimedDict with a 3-second lifetime
    cache = TimedDict()
    cache.lifetime = 3  # 3 seconds

    print(f"Created TimedDict with lifetime: {cache.lifetime} seconds")

    # Add items to the cache
    cache["key1"] = "value1"
    cache["key2"] = "value2"

    print("Initial cache contents:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Wait for some time
    print("\nWaiting for 2 seconds...")
    time.sleep(2)

    # Reset the expiration timer
    print("Resetting expiration timer...")
    cache.reset_expiration()

    # Add another item
    cache["key3"] = "value3"

    print("Cache contents after reset:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Wait for 2 more seconds (less than the new lifetime)
    print("\nWaiting for 2 more seconds...")
    time.sleep(2)

    # Check if items are still in the cache
    print("Cache contents after 2 more seconds:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Disable timing
    print("\nDisabling timing...")
    cache.is_timed = False

    # Wait for more than the lifetime
    print("Waiting for 4 seconds (> lifetime)...")
    time.sleep(4)

    # Check if items are still in the cache (they should still be there)
    print("Cache contents with timing disabled:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Re-enable timing
    print("\nRe-enabling timing...")
    cache.is_timed = True
    cache.reset_expiration()

    # Wait for more than the lifetime
    print("Waiting for 4 seconds (> lifetime)...")
    time.sleep(4)

    # Check if items are still in the cache (they should be cleared)
    print("Cache contents after re-enabling timing and waiting:")
    print(f"Cache is empty: {len(cache) == 0} == True")


def context_manager_example():
    """Demonstrate using context managers with TimedDict."""
    print("\nContext Manager Example:")

    # Create a TimedDict with a 2-second lifetime
    cache = TimedDict()
    cache.lifetime = 2  # 2 seconds

    print(f"Created TimedDict with lifetime: {cache.lifetime} seconds")

    # Add items to the cache
    cache["key1"] = "value1"
    cache["key2"] = "value2"

    print("Initial cache contents:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Wait for 1 second
    print("\nWaiting for 1 second...")
    time.sleep(1)

    # Use pause_timer context manager
    print("Using pause_timer context manager...")
    with cache.pause_timer():
        print("Timer paused")

        # Wait for more than the lifetime
        print("Waiting for 3 seconds (> lifetime) while timer is paused...")
        time.sleep(3)

        # Check if items are still in the cache (they should be)
        print("Cache contents while timer is paused:")
        for key, value in cache.items():
            print(f"  {key}: {value}")

    print("\nExited context manager (timer resumed)")

    # The timer should have about 1 second left
    print("Timer should have about 1 second left")
    print("Waiting for 1.5 seconds...")
    time.sleep(1.5)

    # Check if items are still in the cache (they should be cleared)
    print("Cache contents after waiting:")
    print(f"Cache is empty: {len(cache) == 0} == True")

    # Add new items
    cache["key3"] = "value3"
    cache["key4"] = "value4"

    # Use pause_reset_timer context manager
    print("\nUsing pause_reset_timer context manager...")
    with cache.pause_reset_timer():
        print("Timer paused and will be reset on exit")

        # Wait for more than the lifetime
        print("Waiting for 3 seconds (> lifetime) while timer is paused...")
        time.sleep(3)

        # Check if items are still in the cache (they should be)
        print("Cache contents while timer is paused:")
        for key, value in cache.items():
            print(f"  {key}: {value}")

    print("\nExited context manager (timer resumed and reset)")

    # The timer should be reset to the full lifetime
    print("Timer should be reset to the full lifetime (2 seconds)")
    print("Waiting for 1 second...")
    time.sleep(1)

    # Check if items are still in the cache (they should be)
    print("Cache contents after waiting 1 second:")
    for key, value in cache.items():
        print(f"  {key}: {value}")

    # Wait for the remaining lifetime
    print("\nWaiting for 1.5 more seconds...")
    time.sleep(1.5)

    # Check if items are still in the cache (they should be cleared)
    print("Cache contents after waiting for full lifetime:")
    print(f"Cache is empty: {len(cache) == 0} == True")


def practical_example():
    """Demonstrate a practical use case for TimedDict."""
    print("\nPractical Example - Session Cache:")

    # Create a simulated session cache with a short lifetime
    session_cache = TimedDict()
    session_cache.lifetime = 5  # 5 seconds

    print(f"Created session cache with lifetime: {session_cache.lifetime} seconds")

    # Simulate user login
    print("\nUser logs in:")
    session_cache["user_id"] = "12345"
    session_cache["username"] = "john_doe"
    session_cache["login_time"] = time.time()
    session_cache["permissions"] = ["read", "write"]

    print("Session cache after login:")
    for key, value in session_cache.items():
        print(f"  {key}: {value}")

    # Simulate user activity (which would reset the session timeout)
    print("\nUser performs an action after 2 seconds:")
    time.sleep(2)

    # Reset the expiration when user is active
    session_cache.reset_expiration()
    print("Session timeout reset")

    # Check session data
    print("Session data is still available:")
    print(f"  User ID: {session_cache.get('user_id')} == '12345'")
    print(f"  Username: {session_cache.get('username')} == 'john_doe'")

    # Simulate user inactivity
    print("\nUser is inactive for 6 seconds (> lifetime):")
    time.sleep(6)

    # Check if session has expired
    print("Checking if session has expired:")
    if len(session_cache) == 0:
        print("  Session has expired, user needs to log in again")
    else:
        print("  Session is still active")

    # Simulate user login again
    print("\nUser logs in again:")
    session_cache["user_id"] = "12345"
    session_cache["username"] = "john_doe"
    session_cache["login_time"] = time.time()

    # Simulate long operation that shouldn't reset the session
    print("\nPerforming a long operation (pausing the timer):")
    with session_cache.pause_timer():
        print("  Timer paused during operation")
        time.sleep(3)
        print("  Operation completed")

    print("Session is still active after long operation:")
    print(f"  User ID: {session_cache.get('user_id')} == '12345'")


def compare_dict_timeddict_example():
    """Compare regular dict with TimedDict."""
    print("\nComparing dict with TimedDict:")

    # Create a regular dict and a TimedDict
    regular_dict = {}
    timed_dict = TimedDict()
    timed_dict.lifetime = 2  # 2 seconds

    # Add the same items to both
    regular_dict["key1"] = "value1"
    regular_dict["key2"] = "value2"

    timed_dict["key1"] = "value1"
    timed_dict["key2"] = "value2"

    print("Initial contents:")
    print(f"  Regular dict: {regular_dict}")
    print(f"  TimedDict: {dict(timed_dict.items())}")

    # Wait for the TimedDict to expire
    print("\nWaiting for 3 seconds (> TimedDict lifetime)...")
    time.sleep(3)

    print("Contents after waiting:")
    print(f"  Regular dict: {regular_dict}")
    print(f"  TimedDict: {dict(timed_dict.items())}")

    print("\nKey differences:")
    print("  Regular dict - items remain until explicitly removed")
    print("  TimedDict - items are automatically cleared after the lifetime expires")


def error_handling_example():
    """Demonstrate error handling with TimedDict."""
    print("\nError Handling Example:")

    # Create a TimedDict
    cache = TimedDict()
    cache.lifetime = 1  # 1 second

    # Add an item
    cache["key"] = "value"

    # Try to access a non-existent key
    print("Trying to access a non-existent key:")
    try:
        value = cache["nonexistent"]
        print(f"  Value: {value}")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Using get() method with a default value
    print("\nUsing get() method with a default value:")
    value = cache.get("nonexistent", "default")
    print(f"  Value: {value} == 'default'")

    # Wait for the cache to expire
    print("\nWaiting for the cache to expire (1.5 seconds)...")
    time.sleep(1.5)

    # Try to access the expired key
    print("Trying to access an expired key:")
    try:
        value = cache["key"]
        print(f"  Value: {value}")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Using get() method after expiration
    print("\nUsing get() method after expiration:")
    value = cache.get("key", "expired")
    print(f"  Value: {value} == 'expired'")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    timer_manipulation_example()
    context_manager_example()
    practical_example()
    compare_dict_timeddict_example()
    error_handling_example()
