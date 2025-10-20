#!/usr/bin/env python
"""sentinelobject_example.py
An example of how to use SentinelObject class.

This example demonstrates:
1. Creating custom sentinel objects
2. Using sentinel objects as markers
3. Verifying the singleton nature of sentinel objects
4. Using sentinel objects in dictionaries and sets
5. Pickling and unpickling sentinel objects
6. Using the predefined sentinel constants
"""
# Imports #
# Standard Libraries #
import pickle
from typing import Any

# Source Packages #
from baseobjects.bases import DEFAULTSENTINEL, SEARCHSENTINEL, SentinelObject


# Classes #
class CacheManager:
    """A simple cache manager that uses sentinel objects to mark special values."""

    def __init__(self) -> None:
        """Initialize the cache manager with an empty cache."""
        self.cache = {}
        self.NOT_FOUND = SentinelObject("NOT_FOUND")
        self.EXPIRED = SentinelObject("EXPIRED")
        self.COMPUTING = SentinelObject("COMPUTING")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the cache.

        Args:
            key: The key to look up
            default: The default value to return if the key is not found

        Returns:
            The cached value, or the default if the key is not found
        """
        value = self.cache.get(key, self.NOT_FOUND)

        if value is self.NOT_FOUND:
            return default
        elif value is self.EXPIRED:
            # Handle expired value
            return default
        elif value is self.COMPUTING:
            # Value is being computed, return a temporary result
            return "Computing..."
        else:
            return value

    def set(self, key: str, value: Any) -> None:
        """Set a value in the cache.

        Args:
            key: The key to store the value under
            value: The value to store
        """
        self.cache[key] = value

    def mark_computing(self, key: str) -> None:
        """Mark a key as currently being computed.

        Args:
            key: The key to mark
        """
        self.cache[key] = self.COMPUTING

    def mark_expired(self, key: str) -> None:
        """Mark a key as expired.

        Args:
            key: The key to mark
        """
        self.cache[key] = self.EXPIRED


class ConfigManager:
    """A configuration manager that uses sentinel objects for default values."""

    def __init__(self) -> None:
        """Initialize the configuration manager with default settings."""
        self.settings = {}
        self.UNSET = SentinelObject("UNSET")

    def get_setting(self, name: str, default: Any = None) -> Any:
        """Get a setting value.

        Args:
            name: The name of the setting
            default: The default value to return if the setting is not found

        Returns:
            The setting value, or the default if the setting is not found
        """
        value = self.settings.get(name, self.UNSET)

        if value is self.UNSET:
            return default
        else:
            return value

    def set_setting(self, name: str, value: Any) -> None:
        """Set a setting value.

        Args:
            name: The name of the setting
            value: The value to set
        """
        self.settings[name] = value


# Example Sections #
def basic_sentinel_example() -> None:
    """Demonstrate basic usage of SentinelObject."""
    print("\nBasic SentinelObject Example:")

    # Create sentinel objects
    null = SentinelObject("NULL")
    missing = SentinelObject("MISSING")

    print(f"Created NULL sentinel: {null}")
    print(f"Created MISSING sentinel: {missing}")

    # Demonstrate that sentinel objects are singletons
    null2 = SentinelObject("NULL")
    print(f"Created another NULL sentinel: {null2}")
    print(f"Are they the same object? {null is null2} == True")

    # Demonstrate that different sentinel objects are different
    print(f"NULL is MISSING? {null is missing} == False")

    # Use sentinel objects as markers
    value = null

    if value is null:
        print("Value is NULL")
    elif value is missing:
        print("Value is MISSING")
    else:
        print("Value is something else")


def sentinel_as_markers_example() -> None:
    """Demonstrate using sentinel objects as markers in a cache."""
    print("\nSentinel Objects as Markers Example:")

    # Create a cache manager
    cache = CacheManager()

    # Set some values
    cache.set("key1", "value1")
    cache.mark_computing("key2")
    cache.mark_expired("key3")

    # Get values
    print(f"key1: {cache.get('key1')} == 'value1'")
    print(f"key2: {cache.get('key2')} == 'Computing...'")
    print(f"key3: {cache.get('key3')} == None")
    print(f"key4: {cache.get('key4')} == None")

    # Demonstrate using sentinel objects for comparison
    value = cache.cache.get("key2")
    if value is cache.COMPUTING:
        print("key2 is currently being computed")

    value = cache.cache.get("key3")
    if value is cache.EXPIRED:
        print("key3 has expired")


def sentinel_in_collections_example() -> None:
    """Demonstrate using sentinel objects in dictionaries and sets."""
    print("\nSentinel Objects in Collections Example:")

    # Create sentinel objects
    red = SentinelObject("RED")
    green = SentinelObject("GREEN")
    blue = SentinelObject("BLUE")

    # Use sentinel objects as dictionary keys
    color_values = {red: "#FF0000", green: "#00FF00", blue: "#0000FF"}

    print(f"RED value: {color_values[red]} == '#FF0000'")
    print(f"GREEN value: {color_values[green]} == '#00FF00'")
    print(f"BLUE value: {color_values[blue]} == '#0000FF'")

    # Use sentinel objects in sets
    selected_colors = {red, blue}

    print(f"Is RED selected? {red in selected_colors} == True")
    print(f"Is GREEN selected? {green in selected_colors} == False")
    print(f"Is BLUE selected? {blue in selected_colors} == True")


def pickling_sentinel_example() -> None:
    """Demonstrate pickling and unpickling sentinel objects."""
    print("\nPickling Sentinel Objects Example:")

    # Create sentinel objects
    pending = SentinelObject("PENDING")
    completed = SentinelObject("COMPLETED")

    # Create a dictionary with sentinel objects
    status = {"task1": pending, "task2": completed, "task3": pending}

    print("Original status:")
    print(f"task1: {status['task1'] is pending} == True")
    print(f"task2: {status['task2'] is completed} == True")

    # Pickle the dictionary
    print("\nPickling the status dictionary...")
    pickled_data = pickle.dumps(status)

    # Unpickle the dictionary
    print("Unpickling the status dictionary...")
    unpickled_status = pickle.loads(pickled_data)

    # Verify that the sentinel objects maintain their identity
    print("\nVerifying unpickled status:")
    print(f"task1 is PENDING? {unpickled_status['task1'] is pending} == True")
    print(f"task2 is COMPLETED? {unpickled_status['task2'] is completed} == True")

    # Demonstrate that sentinel objects maintain their identity across pickling
    original_pending = status["task1"]
    unpickled_pending = unpickled_status["task1"]
    print(f"Original PENDING is unpickled PENDING? {original_pending is unpickled_pending} == True")


def predefined_sentinels_example() -> None:
    """Demonstrate using the predefined sentinel constants."""
    print("\nPredefined Sentinel Constants Example:")

    # Use the predefined sentinel constants
    print(f"DEFAULTSENTINEL: {DEFAULTSENTINEL}")
    print(f"SEARCHSENTINEL: {SEARCHSENTINEL}")

    # Create a function that uses DEFAULTSENTINEL
    def get_value(data: dict[str, Any], key: str, default: Any = DEFAULTSENTINEL) -> Any:
        """Get a value from a dictionary with a special default sentinel.

        Args:
            data: The dictionary to get the value from
            key: The key to look up
            default: The default value to return if the key is not found

        Returns:
            The value from the dictionary, or the default if the key is not found

        Raises:
            KeyError: If the key is not found and no default is provided
        """
        value = data.get(key, DEFAULTSENTINEL)

        if value is DEFAULTSENTINEL:
            if default is DEFAULTSENTINEL:
                msg = f"Key '{key}' not found and no default provided"
                raise KeyError(msg)
            return default
        return value

    # Use the function
    data = {"a": 1, "b": 2}

    # With existing key
    print(f"get_value(data, 'a'): {get_value(data, 'a')} == 1")

    # With non-existing key and default
    print(f"get_value(data, 'c', 'default'): {get_value(data, 'c', 'default')} == 'default'")

    # With non-existing key and no default
    try:
        value = get_value(data, "c")
        print(f"get_value(data, 'c'): {value}")
    except KeyError as e:
        print(f"KeyError as expected: {e}")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_sentinel_example()
    sentinel_as_markers_example()
    sentinel_in_collections_example()
    pickling_sentinel_example()
    predefined_sentinels_example()
