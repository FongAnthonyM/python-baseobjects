#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""version_example.py
An example of how to use the Version abstract class.

This example demonstrates:
1. Creating a concrete subclass of Version
2. Implementing the required abstract methods
3. Using the Version class for version comparison
4. Converting versions to different formats
"""


# Imports #
# Standard Libraries #
from typing import Any, List, Tuple

# Third-Party Packages #
from baseobjects.versioning import Version

# Local Packages #


# Classes #
class SimpleVersion(Version):
    """A simple implementation of the Version abstract class.

    This class represents a version with a single number.

    Attributes:
        number: The version number.
    """

    # Attributes #
    number: int = 0

    # Magic Methods #
    # Construction/Destruction #
    def __init__(
        self,
        version: Any = None,
        init: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize a SimpleVersion object.

        Args:
            version: An object to derive a version from.
            init: Determines if this object will construct.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(version=version, init=False, *args, **kwargs)

        if init:
            self.construct(version=version, **kwargs)

    # Comparison #
    def __eq__(self, other: Any) -> bool:
        """Compare this version with another for equality.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the versions are equal, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number == other.number
        elif isinstance(other, int):
            return self.number == other
        else:
            try:
                return self.number == self.cast(other).number
            except TypeError:
                return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Compare this version with another for inequality.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the versions are not equal, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number != other.number
        elif isinstance(other, int):
            return self.number != other
        else:
            try:
                return self.number != self.cast(other).number
            except TypeError:
                return super().__ne__(other)

    def __lt__(self, other: Any) -> bool:
        """Compare if this version is less than another.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this version is less than the other, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number < other.number
        elif isinstance(other, int):
            return self.number < other
        else:
            try:
                return self.number < self.cast(other).number
            except TypeError:
                return super().__lt__(other)

    def __gt__(self, other: Any) -> bool:
        """Compare if this version is greater than another.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this version is greater than the other, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number > other.number
        elif isinstance(other, int):
            return self.number > other
        else:
            try:
                return self.number > self.cast(other).number
            except TypeError:
                return super().__gt__(other)

    def __le__(self, other: Any) -> bool:
        """Compare if this version is less than or equal to another.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this version is less than or equal to the other, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number <= other.number
        elif isinstance(other, int):
            return self.number <= other
        else:
            try:
                return self.number <= self.cast(other).number
            except TypeError:
                return super().__le__(other)

    def __ge__(self, other: Any) -> bool:
        """Compare if this version is greater than or equal to another.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this version is greater than or equal to the other, False otherwise.
        """
        if isinstance(other, SimpleVersion):
            return self.number >= other.number
        elif isinstance(other, int):
            return self.number >= other
        else:
            try:
                return self.number >= self.cast(other).number
            except TypeError:
                return super().__ge__(other)

    # Instance Methods #
    # Constructors/Destructors #
    def construct(self, version: Any = None, **kwargs: Any) -> None:
        """Construct the version object based on inputs.

        Args:
            version: An object to derive a version from.
            **kwargs: Additional keyword arguments.
        """
        if version is not None:
            if isinstance(version, int):
                self.number = version
            elif isinstance(version, str):
                self.number = int(version)
            elif isinstance(version, SimpleVersion):
                self.number = version.number
            else:
                try:
                    self.number = int(version)
                except (ValueError, TypeError):
                    raise TypeError(f"Cannot convert {type(version)} to SimpleVersion")

    # Type Conversion #
    def list(self) -> List[int]:
        """Convert the version to a list.

        Returns:
            A list containing the version number.
        """
        return [self.number]

    def tuple(self) -> Tuple[int]:
        """Convert the version to a tuple.

        Returns:
            A tuple containing the version number.
        """
        return (self.number,)

    def str(self) -> str:
        """Convert the version to a string.

        Returns:
            A string representation of the version number.
        """
        return str(self.number)


# Example Sections #
def creating_version_subclass_example():
    """Demonstrate how to create a concrete subclass of Version."""
    print("\nCreating a Version Subclass:")

    # Create a SimpleVersion instance
    version = SimpleVersion(1)

    print(f"Created SimpleVersion with number: {version.number} == 1")
    print(f"String representation: {str(version)} == '1'")
    print(f"List representation: {version.list()} == [1]")
    print(f"Tuple representation: {version.tuple()} == (1,)")


def version_comparison_example():
    """Demonstrate version comparison operations."""
    print("\nVersion Comparison:")

    # Create versions for comparison
    v1 = SimpleVersion(1)
    v2 = SimpleVersion(2)
    v3 = SimpleVersion(1)

    # Equality comparison
    print(f"v1 == v3: {v1 == v3} == True")
    print(f"v1 == v2: {v1 == v2} == False")

    # Inequality comparison
    print(f"v1 != v2: {v1 != v2} == True")
    print(f"v1 != v3: {v1 != v3} == False")

    # Less than comparison
    print(f"v1 < v2: {v1 < v2} == True")
    print(f"v2 < v1: {v2 < v1} == False")

    # Greater than comparison
    print(f"v2 > v1: {v2 > v1} == True")
    print(f"v1 > v2: {v1 > v2} == False")

    # Less than or equal comparison
    print(f"v1 <= v3: {v1 <= v3} == True")
    print(f"v1 <= v2: {v1 <= v2} == True")
    print(f"v2 <= v1: {v2 <= v1} == False")

    # Greater than or equal comparison
    print(f"v1 >= v3: {v1 >= v3} == True")
    print(f"v2 >= v1: {v2 >= v1} == True")
    print(f"v1 >= v2: {v1 >= v2} == False")


def version_conversion_example():
    """Demonstrate version conversion operations."""
    print("\nVersion Conversion:")

    # Create a version
    version = SimpleVersion(5)

    # Convert to different formats
    print(f"Version number: {version.number} == 5")
    print(f"String representation: {str(version)} == '5'")
    print(f"List representation: {version.list()} == [5]")
    print(f"Tuple representation: {version.tuple()} == (5,)")


def version_casting_example():
    """Demonstrate version casting operations."""
    print("\nVersion Casting:")

    # Cast from different types
    v1 = SimpleVersion(10)
    v2 = SimpleVersion("20")
    v3 = SimpleVersion.cast(30)

    print(f"Cast from int: {v1.number} == 10")
    print(f"Cast from string: {v2.number} == 20")
    print(f"Using cast method: {v3.number} == 30")

    # Try casting an incompatible type
    print("\nCasting incompatible types:")
    try:
        SimpleVersion.cast([1, 2, 3])
        print("This should not be printed")
    except TypeError as e:
        print(f"TypeError raised as expected: {e}")

    # Using pass_ parameter to handle errors
    result = SimpleVersion.cast([1, 2, 3], pass_=True)
    print(f"Result with pass_=True: {type(result).__name__} == 'list'")


# Main #
if __name__ == "__main__":
    # Run examples
    creating_version_subclass_example()
    version_comparison_example()
    version_conversion_example()
    version_casting_example()
