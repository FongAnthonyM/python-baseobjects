#!/usr/bin/env python
"""updaterecursive_example.py
An example of how to use the update_recursive function.

This example demonstrates:
1. Basic usage of update_recursive
2. Updating nested dictionaries
3. Comparing update_recursive with standard dict.update()
4. Handling different types of mapping objects
5. Practical use cases for update_recursive
"""


# Imports #
# Standard Libraries #
from collections import defaultdict

# Source Packages #
from baseobjects.operations import update_recursive


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of update_recursive."""
    print("\nBasic update_recursive Usage:")

    # Create a simple dictionary
    original = {"a": 1, "b": 2, "c": 3}

    # Create an update dictionary
    updates = {"b": 22, "d": 4}

    # Update the original dictionary
    result = update_recursive(original, updates)

    print(f"Original dictionary: {original}")
    print(f"Updates: {updates}")
    print(f"Result: {result}")
    print("Expected: {'a': 1, 'b': 22, 'c': 3, 'd': 4}")

    # Verify that result is the same object as original (modified in-place)
    print(f"Result is original: {result is original} == True")


def nested_dictionary_example() -> None:
    """Demonstrate updating nested dictionaries with update_recursive."""
    print("\nNested Dictionary Example:")

    # Create a nested dictionary
    original = {
        "user": {"name": "John", "age": 30, "address": {"city": "New York", "zip": "10001"}},
        "settings": {"theme": "dark", "notifications": True},
    }

    # Create an update with nested changes
    updates = {
        "user": {"age": 31, "address": {"state": "NY"}},  # Update existing value  # Add new nested value
        "settings": {"language": "en"},  # Add new value to existing nested dict
    }

    # Update the original dictionary
    result = update_recursive(original, updates)

    print("Original nested dictionary:")
    print(f"  {original}")

    print("\nUpdates:")
    print(f"  {updates}")

    print("\nResult:")
    print(f"  {result}")

    # Expected result
    expected = {
        "user": {
            "name": "John",
            "age": 31,  # Updated
            "address": {"city": "New York", "zip": "10001", "state": "NY"},  # Added
        },
        "settings": {"theme": "dark", "notifications": True, "language": "en"},  # Added
    }

    print("\nExpected:")
    print(f"  {expected}")

    # Verify that nested structures are preserved
    print("\nVerifying nested structures:")
    print(f"  User name: {result['user']['name']} == 'John'")
    print(f"  User age: {result['user']['age']} == 31")
    print(f"  User city: {result['user']['address']['city']} == 'New York'")
    print(f"  User state: {result['user']['address']['state']} == 'NY'")
    print(f"  Settings language: {result['settings']['language']} == 'en'")


def compare_with_dict_update_example() -> None:
    """Compare update_recursive with standard dict.update()."""
    print("\nComparing update_recursive with dict.update():")

    # Create nested dictionaries
    dict1 = {"a": 1, "b": {"x": 10, "y": 20}}

    dict2 = {"a": 1, "b": {"x": 10, "y": 20}}

    # Updates with nested structure
    updates = {"b": {"z": 30}}

    # Update using standard dict.update()
    dict1.update(updates)
    print("Using dict.update():")
    print(f"  Result: {dict1}")
    print("  Expected: {'a': 1, 'b': {'z': 30}}")
    print("  Note: The nested dictionary was completely replaced")

    # Update using update_recursive
    update_recursive(dict2, updates)
    print("\nUsing update_recursive():")
    print(f"  Result: {dict2}")
    print("  Expected: {'a': 1, 'b': {'x': 10, 'y': 20, 'z': 30}}")
    print("  Note: The nested dictionary was preserved and updated")


def different_mapping_types_example() -> None:
    """Demonstrate update_recursive with different mapping types."""
    print("\nDifferent Mapping Types Example:")

    # Create a defaultdict
    original = defaultdict(dict)
    original["user"]["name"] = "John"
    original["user"]["age"] = 30
    original["settings"]["theme"] = "dark"

    # Create updates
    updates = {"user": {"email": "john@example.com"}, "settings": {"language": "en"}}

    # Update using update_recursive
    result = update_recursive(original, updates)

    print(f"Original (defaultdict): {dict(original)}")
    print(f"Updates: {updates}")
    print(f"Result: {dict(result)}")
    expected = {
        "user": {"name": "John", "age": 30, "email": "john@example.com"},
        "settings": {"theme": "dark", "language": "en"},
    }
    print(f"Expected: {expected}")

    # Verify the result is still a defaultdict
    print(f"Result is defaultdict: {isinstance(result, defaultdict)} == True")

    # Try adding a new nested key (should work with defaultdict)
    result["new_section"]["key"] = "value"
    print("\nAfter adding new nested key:")
    print(f"  {dict(result)}")
    print("  Note: defaultdict behavior is preserved")


def practical_example() -> None:
    """Demonstrate a practical use case for update_recursive."""
    print("\nPractical Example - Configuration Management:")

    # Default configuration
    default_config = {
        "app": {"name": "MyApp", "version": "1.0.0"},
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {"username": "admin", "password": "default_password"},
        },
        "logging": {"level": "INFO", "file": "app.log"},
    }

    # User configuration (partial override)
    user_config = {
        "database": {"host": "db.example.com", "credentials": {"password": "user_password"}},
        "logging": {"level": "DEBUG"},
    }

    # Environment-specific configuration
    env_config = {"database": {"port": 6432, "credentials": {"username": "prod_user"}}}

    # Create working configuration by applying updates
    config = default_config.copy()
    print("Starting with default configuration:")
    print(f"  {config}")

    # Apply user configuration
    update_recursive(config, user_config)
    print("\nAfter applying user configuration:")
    print(f"  {config}")

    # Apply environment configuration
    update_recursive(config, env_config)
    print("\nAfter applying environment configuration:")
    print(f"  {config}")

    # Final configuration should have merged all settings
    print("\nVerifying final configuration:")
    print(f"  App name: {config['app']['name']} == 'MyApp'")
    print(f"  Database host: {config['database']['host']} == 'db.example.com'")
    print(f"  Database port: {config['database']['port']} == 6432")
    print(f"  Database username: {config['database']['credentials']['username']} == 'prod_user'")
    print(f"  Database password: {config['database']['credentials']['password']} == 'user_password'")
    print(f"  Logging level: {config['logging']['level']} == 'DEBUG'")
    print(f"  Logging file: {config['logging']['file']} == 'app.log'")


def iterable_input_example() -> None:
    """Demonstrate using update_recursive with different types of iterables."""
    print("\nIterable Input Example:")

    # Create a base dictionary
    original = {"a": 1, "b": {"x": 10, "y": 20}}

    # Example 1: Using a list of tuples
    original_copy1 = original.copy()
    updates_list = [("c", 3), ("b", {"z": 30})]
    result1 = update_recursive(original_copy1, updates_list)

    print("Using a list of tuples:")
    print(f"  Original: {original}")
    print(f"  Updates: {updates_list}")
    print(f"  Result: {result1}")
    print("  Expected: {'a': 1, 'b': {'x': 10, 'y': 20, 'z': 30}, 'c': 3}")

    # Example 2: Using a generator expression
    original_copy2 = original.copy()
    updates_gen = ((k, v) for k, v in [("c", 3), ("b", {"z": 30})])
    result2 = update_recursive(original_copy2, updates_gen)

    print("\nUsing a generator expression:")
    print(f"  Original: {original}")
    print("  Updates: generator of [('c', 3), ('b', {'z': 30})]")
    print(f"  Result: {result2}")
    print("  Expected: {'a': 1, 'b': {'x': 10, 'y': 20, 'z': 30}, 'c': 3}")

    # Example 3: Using zip to create an iterable of pairs
    original_copy3 = original.copy()
    keys = ["c", "b"]
    values = [3, {"z": 30}]
    updates_zip = zip(keys, values, strict=False)
    result3 = update_recursive(original_copy3, updates_zip)

    print("\nUsing zip to create an iterable of pairs:")
    print(f"  Original: {original}")
    print(f"  Keys: {keys}")
    print(f"  Values: {values}")
    print(f"  Result: {result3}")
    print("  Expected: {'a': 1, 'b': {'x': 10, 'y': 20, 'z': 30}, 'c': 3}")

    # Example 4: Converting a dictionary to an iterable with items()
    original_copy4 = original.copy()
    updates_dict = {"c": 3, "b": {"z": 30}}
    updates_items = updates_dict.items()
    result4 = update_recursive(original_copy4, updates_items)

    print("\nUsing dictionary.items():")
    print(f"  Original: {original}")
    print(f"  Updates dict: {updates_dict}")
    print(f"  Result: {result4}")
    print("  Expected: {'a': 1, 'b': {'x': 10, 'y': 20, 'z': 30}, 'c': 3}")

    # Verify all results are equivalent
    print("\nVerifying all results are equivalent:")
    print(f"  All results equal: {result1 == result2 == result3 == result4} == True")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    nested_dictionary_example()
    compare_with_dict_update_example()
    different_mapping_types_example()
    iterable_input_example()
    practical_example()
