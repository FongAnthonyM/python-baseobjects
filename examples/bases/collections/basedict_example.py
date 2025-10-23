#!/usr/bin/env python
"""basedict_example.py
An example of how to use BaseDict class.

This example demonstrates:
1. Creating dictionaries using BaseDict
2. Basic dictionary operations with BaseDict
3. Inheriting from BaseDict to create custom dictionary classes
4. Using BaseObject features with dictionary-like objects
"""

# Imports #
# Standard Libraries #
import copy
from typing import Any

# Source Packages #
from baseobjects.bases.collections import BaseDict


# Classes #
class ConfigDict(BaseDict):
    """A custom dictionary for configuration settings that inherits from BaseDict."""

    def __init__(self, data: dict[str, Any] | None = None, /, *args: Any, **kwargs: Any) -> None:
        """Initialize a ConfigDict object.

        Args:
            data: Initial dictionary data
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(data, *args, **kwargs)
        self.construct()

    def construct(self, *args: Any, **kwargs: Any) -> None:
        """Construct the ConfigDict object with default values if empty.

        Args:
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        # Set default values if the dictionary is empty
        if not self.data:
            self.data = {"debug": False, "log_level": "INFO", "max_connections": 10, "timeout": 30}

    def get_with_default(self, key: str, default: Any = None) -> Any:
        """Get a value with a default if the key doesn't exist.

        Args:
            key: The key to look up
            default: The default value to return if key doesn't exist

        Returns:
            The value for the key or the default
        """
        return self.data.get(key, default)

    def update_if_exists(self, key: str, value: Any) -> bool:
        """Update a value only if the key already exists.

        Args:
            key: The key to update
            value: The new value

        Returns:
            True if the key existed and was updated, False otherwise
        """
        if key in self.data:
            self.data[key] = value
            return True
        return False


# Example Sections #
def basic_basedict_example() -> None:
    """Demonstrate basic usage of BaseDict."""
    print("\nBasic BaseDict Example:")

    # Create a BaseDict instance
    base_dict = BaseDict({"name": "John", "age": 30, "city": "New York"})
    print(f"BaseDict: {base_dict}")

    # Access items
    print(f"Name: {base_dict['name']} == 'John'")
    print(f"Age: {base_dict['age']} == 30")

    # Modify items
    base_dict["age"] = 31
    print(f"Updated age: {base_dict['age']} == 31")

    # Add new items
    base_dict["email"] = "john@example.com"
    print(f"Added email: {base_dict['email']} == 'john@example.com'")

    # Delete items
    del base_dict["city"]
    print(f"After deleting city: {base_dict} == {{'name': 'John', 'age': 31, 'email': 'john@example.com'}}")

    # Dictionary methods
    print(f"Keys: {list(base_dict.keys())} == ['name', 'age', 'email']")
    print(f"Values: {list(base_dict.values())} == ['John', 31, 'john@example.com']")
    print(f"Items: {list(base_dict.items())} == [('name', 'John'), ('age', 31), ('email', 'john@example.com')]")


def custom_basedict_example() -> None:
    """Demonstrate creating a custom dictionary class that inherits from BaseDict."""
    print("\nCustom BaseDict Example:")

    # Create an empty ConfigDict (will be populated with defaults)
    config = ConfigDict()
    print(f"Default config: {config}")

    # Access configuration values
    print(f"Debug mode: {config['debug']} == False")
    print(f"Log level: {config['log_level']} == 'INFO'")

    # Modify configuration
    config["debug"] = True
    config["log_level"] = "DEBUG"
    print(f"Updated config: {config}")

    # Use custom method
    value = config.get_with_default("cache_size", 1024)
    print(f"Cache size (with default): {value} == 1024")

    # Update existing key
    updated = config.update_if_exists("max_connections", 20)
    print(f"Updated max_connections: {updated} == True")
    print(f"New max_connections value: {config['max_connections']} == 20")

    # Try to update non-existing key
    updated = config.update_if_exists("database", "mysql")
    print(f"Updated database: {updated} == False")
    print(f"Database key exists: {'database' in config} == False")


def baseobject_features_example() -> None:
    """Demonstrate BaseObject features with BaseDict."""
    print("\nBaseObject Features Example:")

    # Create a ConfigDict
    config = ConfigDict(
        {
            "debug": True,
            "log_level": "DEBUG",
            "max_connections": 20,
            "timeout": 60,
            "database": {"host": "localhost", "port": 5432, "name": "mydb"},
        },
    )

    # Shallow copy
    shallow_copy = config.copy()
    print(f"Original config: {config}")
    print(f"Shallow copy: {shallow_copy}")
    print(f"Are they the same object? {config is shallow_copy} == False")

    # Modify nested dictionary in shallow copy
    shallow_copy["database"]["port"] = 3306
    print(f"Original database port after modifying shallow copy: {config['database']['port']} == 3306")
    print(f"Shallow copy database port: {shallow_copy['database']['port']} == 3306")

    # Deep copy
    deep_copy = config.deepcopy()
    print(f"\nDeep copy: {deep_copy}")
    print(f"Are they the same object? {config is deep_copy} == False")

    # Modify nested dictionary in deep copy
    deep_copy["database"]["name"] = "newdb"
    print(f"Original database name after modifying deep copy: {config['database']['name']} == 'mydb'")
    print(f"Deep copy database name: {deep_copy['database']['name']} == 'newdb'")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_basedict_example()
    custom_basedict_example()
    baseobject_features_example()
