#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from typing import Any, Dict

# Third-Party Packages #
from baseobjects.bases import SentinelObject, DEFAULTSENTINEL, SEARCHSENTINEL

# Local Packages #


# Classes #
class CacheManager:
    """A simple cache manager that uses sentinel objects to mark special values."""
    
    def __init__(self):
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
    
    def __init__(self):
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
def basic_sentinel_example():
    """Demonstrate basic usage of SentinelObject."""
    print("\nBasic SentinelObject Example:")
    
    # Create sentinel objects
    NULL = SentinelObject("NULL")
    MISSING = SentinelObject("MISSING")
    
    print(f"Created NULL sentinel: {NULL}")
    print(f"Created MISSING sentinel: {MISSING}")
    
    # Demonstrate that sentinel objects are singletons
    NULL2 = SentinelObject("NULL")
    print(f"Created another NULL sentinel: {NULL2}")
    print(f"Are they the same object? {NULL is NULL2} == True")
    
    # Demonstrate that different sentinel objects are different
    print(f"NULL is MISSING? {NULL is MISSING} == False")
    
    # Use sentinel objects as markers
    value = NULL
    
    if value is NULL:
        print("Value is NULL")
    elif value is MISSING:
        print("Value is MISSING")
    else:
        print("Value is something else")


def sentinel_as_markers_example():
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


def sentinel_in_collections_example():
    """Demonstrate using sentinel objects in dictionaries and sets."""
    print("\nSentinel Objects in Collections Example:")
    
    # Create sentinel objects
    RED = SentinelObject("RED")
    GREEN = SentinelObject("GREEN")
    BLUE = SentinelObject("BLUE")
    
    # Use sentinel objects as dictionary keys
    color_values = {
        RED: "#FF0000",
        GREEN: "#00FF00",
        BLUE: "#0000FF"
    }
    
    print(f"RED value: {color_values[RED]} == '#FF0000'")
    print(f"GREEN value: {color_values[GREEN]} == '#00FF00'")
    print(f"BLUE value: {color_values[BLUE]} == '#0000FF'")
    
    # Use sentinel objects in sets
    selected_colors = {RED, BLUE}
    
    print(f"Is RED selected? {RED in selected_colors} == True")
    print(f"Is GREEN selected? {GREEN in selected_colors} == False")
    print(f"Is BLUE selected? {BLUE in selected_colors} == True")


def pickling_sentinel_example():
    """Demonstrate pickling and unpickling sentinel objects."""
    print("\nPickling Sentinel Objects Example:")
    
    # Create sentinel objects
    PENDING = SentinelObject("PENDING")
    COMPLETED = SentinelObject("COMPLETED")
    
    # Create a dictionary with sentinel objects
    status = {
        "task1": PENDING,
        "task2": COMPLETED,
        "task3": PENDING
    }
    
    print("Original status:")
    print(f"task1: {status['task1'] is PENDING} == True")
    print(f"task2: {status['task2'] is COMPLETED} == True")
    
    # Pickle the dictionary
    print("\nPickling the status dictionary...")
    pickled_data = pickle.dumps(status)
    
    # Unpickle the dictionary
    print("Unpickling the status dictionary...")
    unpickled_status = pickle.loads(pickled_data)
    
    # Verify that the sentinel objects maintain their identity
    print("\nVerifying unpickled status:")
    print(f"task1 is PENDING? {unpickled_status['task1'] is PENDING} == True")
    print(f"task2 is COMPLETED? {unpickled_status['task2'] is COMPLETED} == True")
    
    # Demonstrate that sentinel objects maintain their identity across pickling
    original_pending = status["task1"]
    unpickled_pending = unpickled_status["task1"]
    print(f"Original PENDING is unpickled PENDING? {original_pending is unpickled_pending} == True")


def predefined_sentinels_example():
    """Demonstrate using the predefined sentinel constants."""
    print("\nPredefined Sentinel Constants Example:")
    
    # Use the predefined sentinel constants
    print(f"DEFAULTSENTINEL: {DEFAULTSENTINEL}")
    print(f"SEARCHSENTINEL: {SEARCHSENTINEL}")
    
    # Create a function that uses DEFAULTSENTINEL
    def get_value(data: Dict[str, Any], key: str, default: Any = DEFAULTSENTINEL) -> Any:
        """Get a value from a dictionary with a special default sentinel.
        
        Args:
            data: The dictionary to get the value from
            key: The key to look up
            default: The default value to return if the key is not found
            
        Returns:
            The value from the dictionary, or the default if the key is not found
        """
        value = data.get(key, DEFAULTSENTINEL)
        
        if value is DEFAULTSENTINEL:
            if default is DEFAULTSENTINEL:
                raise KeyError(f"Key '{key}' not found and no default provided")
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
        value = get_value(data, 'c')
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