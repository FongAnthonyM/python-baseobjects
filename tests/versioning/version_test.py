#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""version_test.py
Tests for the Version class in the baseobjects package.

This module contains tests for the Version abstract class, which provides the base functionality
for version objects. Since Version is an abstract class, a concrete test implementation is created
for testing purposes.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import copy
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.versioning.version import Version
from src.baseobjects.testsuite.versiontestsuite import VersionTestSuite


# Definitions #
# Classes #
class TestVersion(Version):
    """A concrete implementation of Version for testing purposes.

    This class implements the abstract methods of Version to allow testing of the base functionality.
    """

    def __init__(self, version: Any = None, init: bool = True, *args: Any, **kwargs: Any) -> None:
        """Initialize a TestVersion instance.

        Args:
            version: An object to derive a version from.
            init: Determines if this object will construct.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.value = 0
        super().__init__(version=version, init=init, *args, **kwargs)

    def __hash__(self) -> int:
        """Return the hash of the object.

        Returns:
            The id of the object.
        """
        return id(self)

    def __eq__(self, other: Any) -> bool:
        """Implement equality comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other: Any) -> bool:
        """Implement inequality comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is not equivalent.
        """
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        """Implement less than comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than the other object.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.value < other.value
        elif isinstance(other, (int, float)):
            return self.value < other
        else:
            return super().__lt__(other)

    def __gt__(self, other: Any) -> bool:
        """Implement greater than comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than the other object.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.value > other.value
        elif isinstance(other, (int, float)):
            return self.value > other
        else:
            return super().__gt__(other)

    def __le__(self, other: Any) -> bool:
        """Implement less than or equal comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to the other object.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.value <= other.value
        elif isinstance(other, (int, float)):
            return self.value <= other
        else:
            return super().__le__(other)

    def __ge__(self, other: Any) -> bool:
        """Implement greater than or equal comparison.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to the other object.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.value >= other.value
        elif isinstance(other, (int, float)):
            return self.value >= other
        else:
            return super().__ge__(other)

    def construct(self, version: Any = None, **kwargs: Any) -> None:
        """Construct the version object based on inputs.

        Args:
            version: An object to derive a version from.
            **kwargs: More keyword arguments for constructing this object.

        Raises:
            TypeError: If version is not a compatible type.
        """
        if version is not None:
            if isinstance(version, (int, float)):
                self.value = version
            elif isinstance(version, Version):
                self.value = version.value
            elif isinstance(version, str):
                try:
                    self.value = int(version)
                except ValueError:
                    raise TypeError(f"Cannot convert string '{version}' to TestVersion")
            else:
                raise TypeError(f"Cannot convert {type(version).__name__} to TestVersion")
        else:
            self.value = 0

    def list(self) -> list[Any]:
        """Return the list representation of the version.

        Returns:
            The list representation of the version.
        """
        return [self.value]

    def tuple(self) -> tuple[Any, ...]:
        """Return the tuple representation of the version.

        Returns:
            The tuple representation of the version.
        """
        return (self.value,)

    def str(self) -> str:
        """Return the string representation of the version.

        Returns:
            A string with the version number.
        """
        return str(self.value)


class TestVersionTests(VersionTestSuite):
    """Test suite for the Version class.

    This class tests the functionality of the Version class using a concrete implementation.
    """

    # Class Attributes #
    TestClass: Type[Version] = TestVersion

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> Version:
        """Create a test version instance for use in tests.

        Returns:
            Version: An instance of the test class.
        """
        return self.TestClass(5)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the TestVersion class can be created.
        """
        instance = self.TestClass()
        assert instance is not None
        assert isinstance(instance, self.TestClass)
        assert instance.value == 0

    def test_creation_with_value(self) -> None:
        """Test that instances of the class can be created with a specific value.

        This test verifies that instances of the TestVersion class can be created with a specific value.
        """
        instance = self.TestClass(10)
        assert instance.value == 10

    def test_copy(self, test_object: Version) -> None:
        """Test the copy behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert obj_copy.value == test_object.value

    def test_copy_method(self, test_object: Version) -> None:
        """Test the copy method behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert obj_copy.value == test_object.value

    def test_deepcopy(self, test_object: Version, memo: dict | None = None) -> None:
        """Test the deep copy behavior of a version object.

        This test verifies that deepcopy creates a new version object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test version object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Version Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.value == test_object.value

    def test_deepcopy_method(self, test_object: Version, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of a version object.

        This test verifies that deepcopy creates a new version object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test version object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Version Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.value == test_object.value

    def test_pickling(self, test_object: Version) -> None:
        """Test pickling and unpickling of a version object.

        This test verifies that the version object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Pickle and Unpickle Version Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert unpickled.value == test_object.value

    def test_equality(self) -> None:
        """Test the __eq__ method of the version class.

        This test verifies that the __eq__ method correctly compares version instances.
        """
        version1 = self.TestClass(5)
        version2 = self.TestClass(5)
        version3 = self.TestClass(10)

        assert version1 == version2
        assert not (version1 == version3)
        assert version1 == 5
        assert not (version1 == 10)

    def test_inequality(self) -> None:
        """Test the __ne__ method of the version class.

        This test verifies that the __ne__ method correctly compares version instances.
        """
        version1 = self.TestClass(5)
        version2 = self.TestClass(5)
        version3 = self.TestClass(10)

        assert not (version1 != version2)
        assert version1 != version3
        assert not (version1 != 5)
        assert version1 != 10

    def test_less_than(self) -> None:
        """Test the __lt__ method of the version class.

        This test verifies that the __lt__ method correctly compares version instances.
        """
        version1 = self.TestClass(5)
        version2 = self.TestClass(10)

        assert version1 < version2
        assert version1 < 10
        assert not (version1 < 5)
        assert not (version1 < 3)

    def test_greater_than(self) -> None:
        """Test the __gt__ method of the version class.

        This test verifies that the __gt__ method correctly compares version instances.
        """
        version1 = self.TestClass(10)
        version2 = self.TestClass(5)

        assert version1 > version2
        assert version1 > 5
        assert not (version1 > 10)
        assert not (version1 > 15)

    def test_less_than_or_equal(self) -> None:
        """Test the __le__ method of the version class.

        This test verifies that the __le__ method correctly compares version instances.
        """
        version1 = self.TestClass(5)
        version2 = self.TestClass(5)
        version3 = self.TestClass(10)

        assert version1 <= version2
        assert version1 <= version3
        assert version1 <= 5
        assert version1 <= 10
        assert not (version1 <= 3)

    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of the version class.

        This test verifies that the __ge__ method correctly compares version instances.
        """
        version1 = self.TestClass(10)
        version2 = self.TestClass(10)
        version3 = self.TestClass(5)

        assert version1 >= version2
        assert version1 >= version3
        assert version1 >= 10
        assert version1 >= 5
        assert not (version1 >= 15)

    def test_cast_method(self) -> None:
        """Test the cast class method of the version class.

        This test verifies that the cast method correctly converts objects to version instances.
        """
        # Test casting an integer
        result = self.TestClass.cast(5)
        assert isinstance(result, self.TestClass)
        assert result.value == 5

        # Test casting a version instance
        version = self.TestClass(10)
        result = self.TestClass.cast(version)
        assert isinstance(result, self.TestClass)
        assert result.value == 10

        # Test casting an incompatible object with pass_=True
        result = self.TestClass.cast(object(), pass_=True)
        assert isinstance(result, object)
        assert not isinstance(result, self.TestClass)

        # Test casting an incompatible object with pass_=False
        with pytest.raises(TypeError):
            self.TestClass.cast(object(), pass_=False)

    def test_str_representation(self, test_object: Version) -> None:
        """Test the string representation of the version object.

        This test verifies that the __str__ method returns the correct string representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert str(test_object) == "5"
        assert test_object.str() == "5"

    def test_list_representation(self, test_object: Version) -> None:
        """Test the list representation of the version object.

        This test verifies that the list method returns the correct list representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert test_object.list() == [5]

    def test_tuple_representation(self, test_object: Version) -> None:
        """Test the tuple representation of the version object.

        This test verifies that the tuple method returns the correct tuple representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert test_object.tuple() == (5,)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
