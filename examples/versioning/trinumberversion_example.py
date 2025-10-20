#!/usr/bin/env python
"""trinumberversion_example.py
An example of how to use the TriNumberVersion class.

This example demonstrates:
1. Creating and initializing TriNumberVersion objects
2. Different ways to specify version numbers
3. Comparing versions
4. Converting versions to different formats
5. Practical use cases for version management
"""


# Imports #
# Standard Libraries #
from typing import Any

# Source Packages #
from baseobjects.versioning import TriNumberVersion


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of TriNumberVersion."""
    print("\nBasic TriNumberVersion Usage:")

    # Create a TriNumberVersion with default values (0.0.0)
    version1 = TriNumberVersion()
    print(f"Default version: {version1} == '0.0.0'")

    # Create a TriNumberVersion with specific values
    version2 = TriNumberVersion(1, 2, 3)
    print(f"Specific version: {version2} == '1.2.3'")

    # Create a TriNumberVersion from a string
    version3 = TriNumberVersion("2.3.4")
    print(f"From string: {version3} == '2.3.4'")

    # Create a TriNumberVersion from a tuple
    version4 = TriNumberVersion((3, 4, 5))
    print(f"From tuple: {version4} == '3.4.5'")

    # Create a TriNumberVersion from a list
    version5 = TriNumberVersion([4, 5, 6])
    print(f"From list: {version5} == '4.5.6'")

    # Create a TriNumberVersion with named parameters
    version6 = TriNumberVersion(major=5, minor=6, patch=7)
    print(f"With named parameters: {version6} == '5.6.7'")


def version_components_example() -> None:
    """Demonstrate accessing and modifying version components."""
    print("\nVersion Components:")

    # Create a version
    version = TriNumberVersion(1, 2, 3)
    print(f"Initial version: {version} == '1.2.3'")

    # Access components
    print(f"Major: {version.major} == 1")
    print(f"Minor: {version.minor} == 2")
    print(f"Patch: {version.patch} == 3")

    # Modify components
    version.major = 2
    print(f"After changing major: {version} == '2.2.3'")

    version.minor = 3
    print(f"After changing minor: {version} == '2.3.3'")

    version.patch = 4
    print(f"After changing patch: {version} == '2.3.4'")

    # Set a new version
    version.set_version("3.4.5")
    print(f"After set_version: {version} == '3.4.5'")


def version_comparison_example() -> None:
    """Demonstrate version comparison operations."""
    print("\nVersion Comparison:")

    # Create versions for comparison
    v1 = TriNumberVersion(1, 0, 0)
    v2 = TriNumberVersion(1, 1, 0)
    v3 = TriNumberVersion(1, 0, 0)
    v4 = TriNumberVersion(2, 0, 0)

    # Equality comparison
    print(f"v1 == v3: {v1 == v3} == True")
    print(f"v1 == v2: {v1 == v2} == False")

    # Inequality comparison
    print(f"v1 != v2: {v1 != v2} == True")
    print(f"v1 != v3: {v1 != v3} == False")

    # Less than comparison
    print(f"v1 < v2: {v1 < v2} == True")
    print(f"v1 < v4: {v1 < v4} == True")
    print(f"v4 < v1: {v4 < v1} == False")

    # Greater than comparison
    print(f"v2 > v1: {v2 > v1} == True")
    print(f"v4 > v1: {v4 > v1} == True")
    print(f"v1 > v4: {v1 > v4} == False")

    # Less than or equal comparison
    print(f"v1 <= v3: {v1 <= v3} == True")
    print(f"v1 <= v2: {v1 <= v2} == True")
    print(f"v2 <= v1: {v2 <= v1} == False")

    # Greater than or equal comparison
    print(f"v1 >= v3: {v1 >= v3} == True")
    print(f"v2 >= v1: {v2 >= v1} == True")
    print(f"v1 >= v2: {v1 >= v2} == False")

    # Compare with string
    print(f"v1 == '1.0.0': {v1 == '1.0.0'} == True")
    print(f"v1 < '1.1.0': {v1 < '1.1.0'} == True")
    print(f"v2 > '1.0.0': {v2 > '1.0.0'} == True")

    # Compare with tuple
    print(f"v1 == (1, 0, 0): {v1 == (1, 0, 0)} == True")
    print(f"v1 < (1, 1, 0): {v1 < (1, 1, 0)} == True")
    print(f"v2 > (1, 0, 0): {v2 > (1, 0, 0)} == True")


def version_conversion_example() -> None:
    """Demonstrate version conversion operations."""
    print("\nVersion Conversion:")

    # Create a version
    version = TriNumberVersion(2, 3, 4)

    # Convert to different formats
    print(f"Version: {version} == '2.3.4'")
    print(f"As string: {version.str()} == '2.3.4'")
    print(f"As list: {version.list()} == [2, 3, 4]")
    print(f"As tuple: {version.tuple()} == (2, 3, 4)")

    # String representation is automatically used in string contexts
    message = f"Current version is {version}"
    print(f"In string context: {message} == 'Current version is 2.3.4'")


def semantic_versioning_example() -> None:
    """Demonstrate using TriNumberVersion for semantic versioning."""
    print("\nSemantic Versioning Example:")

    # Initial version
    version = TriNumberVersion(1, 0, 0)
    print(f"Initial version: {version} == '1.0.0'")

    # Patch update (bug fixes)
    version.patch += 1
    print(f"After bug fix: {version} == '1.0.1'")

    # Minor update (new features, backwards compatible)
    version.minor += 1
    version.patch = 0
    print(f"After adding new feature: {version} == '1.1.0'")

    # Major update (breaking changes)
    version.major += 1
    version.minor = 0
    version.patch = 0
    print(f"After breaking change: {version} == '2.0.0'")


def version_management_example() -> None:
    """Demonstrate practical version management."""
    print("\nVersion Management Example:")

    # Define a dictionary of software components and their versions
    components: dict[str, TriNumberVersion] = {
        "api": TriNumberVersion(1, 2, 3),
        "database": TriNumberVersion(2, 0, 1),
        "ui": TriNumberVersion(1, 1, 0),
        "core": TriNumberVersion(2, 3, 4),
    }

    # Display current versions
    print("Current component versions:")
    for name, version in components.items():
        print(f"  {name}: {version}")

    # Check compatibility (example: api must be at least 1.2.0)
    min_api_version = TriNumberVersion(1, 2, 0)
    is_api_compatible = components["api"] >= min_api_version
    print(f"\nAPI compatibility check: {is_api_compatible} == True")

    # Find components that need updates (example: all components should be at least 2.0.0)
    min_version = TriNumberVersion(2, 0, 0)
    needs_update = [name for name, version in components.items() if version < min_version]
    print(f"Components needing updates: {needs_update} == ['api', 'ui']")

    # Sort components by version
    sorted_components = sorted(components.items(), key=lambda x: x[1])
    print("\nComponents sorted by version:")
    for name, version in sorted_components:
        print(f"  {name}: {version}")


def error_handling_example() -> None:
    """Demonstrate error handling with TriNumberVersion."""
    print("\nError Handling Example:")

    # Try to create a version with invalid string
    print("Trying to create a version with invalid string:")
    try:
        version = TriNumberVersion("not.a.version")
        print(f"Version: {version}")
    except ValueError as e:
        print(f"ValueError raised as expected: {e}")

    # Try to create a version with too few components
    print("\nTrying to create a version with too few components:")
    try:
        version = TriNumberVersion([1, 2])
        print(f"Version: {version}")
    except ValueError as e:
        print(f"ValueError raised as expected: {e}")

    # Proper error handling
    print("\nProper error handling:")
    try:
        version_str = "invalid.version"
        version = TriNumberVersion(version_str)
    except ValueError:
        print(f"Invalid version string '{version_str}', using default version instead")
        version = TriNumberVersion(1, 0, 0)

    print(f"Final version: {version} == '1.0.0'")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    version_components_example()
    version_comparison_example()
    version_conversion_example()
    semantic_versioning_example()
    version_management_example()
    error_handling_example()
