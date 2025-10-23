#!/usr/bin/env python
"""deepchainmap_example.py
An example of how to use DeepChainMap class.

This example demonstrates:
1. Creating and using a DeepChainMap
2. Comparing DeepChainMap with standard ChainMap
3. Updating and deleting items in a DeepChainMap
4. Practical use cases for DeepChainMap
"""

# Imports #
# Standard Libraries #
from collections import ChainMap
from typing import Any

# Source Packages #
from baseobjects.collections import DeepChainMap


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of DeepChainMap."""
    print("\nBasic DeepChainMap Usage:")

    # Create dictionaries for the chain
    defaults = {"theme": "default", "language": "en", "timeout": 30, "debug": False}
    user_settings = {"language": "fr", "timeout": 60}
    session_settings = {"theme": "dark"}

    # Create a DeepChainMap with these dictionaries
    settings = DeepChainMap(session_settings, user_settings, defaults)

    # Access values (looks through the chain)
    print("Accessing values:")
    print(f"  Theme: {settings['theme']} == 'dark'")
    print(f"  Language: {settings['language']} == 'fr'")
    print(f"  Timeout: {settings['timeout']} == 60")
    print(f"  Debug: {settings['debug']} == False")

    # Check the original dictionaries
    print("\nOriginal dictionaries:")
    print(f"  Session settings: {session_settings} == {{'theme': 'dark'}}")
    print(f"  User settings: {user_settings} == {{'language': 'fr', 'timeout': 60}}")
    print("  Defaults:")
    print(f"    {defaults} == {{'theme': 'default', 'language': 'en', 'timeout': 30, 'debug': False}}")

    # Add a new key
    print("\nAdding a new key 'notifications':")
    settings["notifications"] = True
    print(f"  Settings['notifications']: {settings['notifications']} == True")
    print(f"  First mapping (session_settings): {session_settings} == {{'theme': 'dark', 'notifications': True}}")

    # Update an existing key
    print("\nUpdating existing key 'language':")
    settings["language"] = "es"
    print(f"  Settings['language']: {settings['language']} == 'es'")
    print(f"  User settings: {user_settings} == {{'language': 'es', 'timeout': 60}}")
    print("  Defaults (unchanged):")
    print(f"    {defaults} == {{'theme': 'default', 'language': 'en', 'timeout': 30, 'debug': False}}")

    # Delete a key
    print("\nDeleting key 'timeout':")
    del settings["timeout"]
    print(f"  'timeout' in settings: {'timeout' in settings} == False")
    print(f"  User settings: {user_settings} == {{'language': 'es'}}")

    # Try to access a deleted key that exists in defaults
    print("\nAccessing 'timeout' after deletion from user_settings:")
    print(f"  Settings['timeout']: {settings['timeout']} == 30")


def compare_with_chainmap() -> None:
    """Compare DeepChainMap with standard ChainMap."""
    print("\nComparing DeepChainMap with standard ChainMap:")

    # Create dictionaries for the chains
    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 20, "c": 30}
    dict3 = {"c": 300, "d": 400}

    # Create a standard ChainMap
    standard_chain = ChainMap(dict1, dict2, dict3)

    # Create a DeepChainMap with the same dictionaries
    deep_chain = DeepChainMap(dict1, dict2, dict3)

    print("Initial dictionaries:")
    print(f"  dict1: {dict1} == {{'a': 1, 'b': 2}}")
    print(f"  dict2: {dict2} == {{'b': 20, 'c': 30}}")
    print(f"  dict3: {dict3} == {{'c': 300, 'd': 400}}")

    print("\nAccessing values (both work the same):")
    print(f"  standard_chain['a']: {standard_chain['a']} == 1")
    print(f"  deep_chain['a']: {deep_chain['a']} == 1")
    print(f"  standard_chain['b']: {standard_chain['b']} == 2")
    print(f"  deep_chain['b']: {deep_chain['b']} == 2")
    print(f"  standard_chain['c']: {standard_chain['c']} == 30")
    print(f"  deep_chain['c']: {deep_chain['c']} == 30")

    print("\nUpdating existing key 'b':")
    standard_chain["b"] = 200
    deep_chain["b"] = 200

    print("After update:")
    print(f"  standard_chain['b']: {standard_chain['b']} == 200")
    print(f"  deep_chain['b']: {deep_chain['b']} == 200")

    print("\nDifference in behavior - which dictionary was updated:")
    print(f"  dict1 with standard_chain: {dict1} == {{'a': 1, 'b': 2}}")
    print(f"  dict1 with deep_chain: {dict1} == {{'a': 1, 'b': 200}}")
    print(f"  standard_chain.maps[0]: {standard_chain.maps[0]} == {{'a': 1, 'b': 200}}")

    # Reset dict1 for the next test
    dict1["b"] = 2

    print("\nUpdating key 'c' (exists in dict2 and dict3):")
    standard_chain["c"] = 3000
    deep_chain["c"] = 3000

    print("After update:")
    print(f"  dict1 with standard_chain: {dict1} == {{'a': 1, 'b': 2}}")
    print(f"  dict2 with standard_chain: {dict2} == {{'b': 20, 'c': 30}}")
    print(f"  dict1 with deep_chain: {dict1} == {{'a': 1, 'b': 2}}")
    print(f"  dict2 with deep_chain: {dict2} == {{'b': 20, 'c': 3000}}")

    # Reset for deletion test
    dict2["c"] = 30

    print("\nDeleting key 'c':")
    try:
        del standard_chain["c"]
        print("  Deleted 'c' from standard_chain")
    except KeyError:
        print("  KeyError: Cannot delete 'c' from standard_chain")

    del deep_chain["c"]
    print("  Deleted 'c' from deep_chain")

    print("After deletion:")
    print(f"  dict2 with standard_chain: {dict2} == {{'b': 20, 'c': 30}}")
    print(f"  dict2 with deep_chain: {dict2} == {{'b': 20}}")
    print(f"  'c' in standard_chain: {'c' in standard_chain} == True")
    print(f"  'c' in deep_chain: {'c' in deep_chain} == True")
    print(f"  deep_chain['c']: {deep_chain['c']} == 300")


def configuration_example() -> None:
    """Demonstrate using DeepChainMap for configuration management."""
    print("\nConfiguration Management Example:")

    # System defaults
    system_defaults = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "app_db",
            "user": "app_user",
            "password": "default_password",
        },
        "api": {"url": "https://api.example.com", "timeout": 30, "retry_attempts": 3},
        "logging": {"level": "INFO", "file": "app.log"},
    }

    # User configuration (overrides some defaults)
    user_config = {"database": {"host": "db.example.com", "password": "user_password"}, "logging": {"level": "DEBUG"}}

    # Environment-specific overrides
    env_overrides = {"api": {"url": "https://staging-api.example.com"}}

    # Create configuration using DeepChainMap
    config = DeepChainMap(env_overrides, user_config, system_defaults)

    print("Effective configuration:")
    print("Database settings:")
    print(f"  Host: {config['database']['host']} == 'db.example.com'")
    print(f"  Port: {config['database']['port']} == 5432")
    print(f"  Name: {config['database']['name']} == 'app_db'")
    print(f"  User: {config['database']['user']} == 'app_user'")
    print(f"  Password: {config['database']['password']} == 'user_password'")

    print("\nAPI settings:")
    print(f"  URL: {config['api']['url']} == 'https://staging-api.example.com'")
    print(f"  Timeout: {config['api']['timeout']} == 30")
    print(f"  Retry attempts: {config['api']['retry_attempts']} == 3")

    print("\nLogging settings:")
    print(f"  Level: {config['logging']['level']} == 'DEBUG'")
    print(f"  File: {config['logging']['file']} == 'app.log'")

    # Update a nested setting
    print("\nUpdating API timeout:")
    config["api"]["timeout"] = 60

    print("After update:")
    print(f"  API timeout: {config['api']['timeout']} == 60")
    print(f"  env_overrides: {env_overrides} == {{'api': {{'url': 'https://staging-api.example.com', 'timeout': 60}}}}")


def error_handling_example() -> None:
    """Demonstrate error handling with DeepChainMap."""
    print("\nError Handling Example:")

    # Create a DeepChainMap
    map1 = {"a": 1, "b": 2}
    map2 = {"c": 3}
    deep_chain = DeepChainMap(map1, map2)

    # Accessing a non-existent key
    print("Trying to access a non-existent key:")
    try:
        value = deep_chain["d"]
        print(f"  Value: {value}")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Using get() method to provide a default
    print("\nUsing get() method with default:")
    value = deep_chain.get("d", "default")
    print(f"  Value: {value} == 'default'")

    # Deleting a non-existent key
    print("\nTrying to delete a non-existent key:")
    try:
        del deep_chain["d"]
        print("  Deleted 'd'")
    except KeyError as e:
        print(f"  KeyError: {e}")

    # Check if key exists before deleting
    print("\nChecking if key exists before deleting:")
    key = "d"
    if key in deep_chain:
        del deep_chain[key]
        print(f"  Deleted '{key}'")
    else:
        print(f"  Key '{key}' not found")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    compare_with_chainmap()
    configuration_example()
    error_handling_example()
