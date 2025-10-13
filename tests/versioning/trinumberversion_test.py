#!/usr/bin/env python
"""trinumberversion_test.py
Tests for the TriNumberVersion class in the baseobjects package.

This module contains tests for the TriNumberVersion class, which is a concrete implementation of the Version
abstract class that represents a version with three numbers (major.minor.patch).
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

# Source Packages #
from src.baseobjects.testsuite.versiontestsuite import VersionTestSuite
from src.baseobjects.versioning.trinumberversion import TriNumberVersion


# Definitions #
# Classes #
class TestTriNumberVersion(VersionTestSuite):
    """Test suite for the TriNumberVersion class.

    This class tests the functionality of the TriNumberVersion class, which is a concrete implementation of the Version
    abstract class that represents a version with three numbers (major.minor.patch).
    """

    # Class Attributes #
    TestClass: Type[TriNumberVersion] = TriNumberVersion

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> TriNumberVersion:
        """Create a test version instance for use in tests.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            TriNumberVersion: An instance of the test class with major=1, minor=2, patch=3.
        """
        return self.TestClass(1, 2, 3)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the TriNumberVersion class can be created.
        """
        instance = self.TestClass()
        assert instance is not None
        assert isinstance(instance, self.TestClass)
        assert instance.major == 0
        assert instance.minor == 0
        assert instance.patch == 0

    def test_creation_with_values(self) -> None:
        """Test that instances of the class can be created with specific values.

        This test verifies that instances of the TriNumberVersion class can be created with specific values.
        """
        instance = self.TestClass(1, 2, 3)
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_from_string(self) -> None:
        """Test that instances of the class can be created from a string.

        This test verifies that instances of the TriNumberVersion class can be created from a string.
        """
        instance = self.TestClass("1.2.3")
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_from_iterable(self) -> None:
        """Test that instances of the class can be created from an iterable.

        This test verifies that instances of the TriNumberVersion class can be created from an iterable.
        """
        instance = self.TestClass([1, 2, 3])
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

        instance = self.TestClass((1, 2, 3))
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_with_keyword_args(self) -> None:
        """Test that instances of the class can be created with keyword arguments.

        This test verifies that instances of the TriNumberVersion class can be created with keyword arguments.
        """
        instance = self.TestClass(major=1, minor=2, patch=3)
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_copy(self, test_object: TriNumberVersion) -> None:
        """Test the copy behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert obj_copy.major == test_object.major
        assert obj_copy.minor == test_object.minor
        assert obj_copy.patch == test_object.patch

    def test_copy_method(self, test_object: TriNumberVersion) -> None:
        """Test the copy method behavior of a version object.

        This test verifies that copy creates a new version object with the same attributes.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        # Copy Version Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert obj_copy.major == test_object.major
        assert obj_copy.minor == test_object.minor
        assert obj_copy.patch == test_object.patch

    def test_deepcopy(self, test_object: TriNumberVersion, memo: dict | None = None) -> None:
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
        assert obj_deepcopy.major == test_object.major
        assert obj_deepcopy.minor == test_object.minor
        assert obj_deepcopy.patch == test_object.patch

    def test_deepcopy_method(self, test_object: TriNumberVersion, memo: dict | None = None) -> None:
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
        assert obj_deepcopy.major == test_object.major
        assert obj_deepcopy.minor == test_object.minor
        assert obj_deepcopy.patch == test_object.patch

    def test_pickling(self, test_object: TriNumberVersion) -> None:
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
        assert isinstance(unpickled, TriNumberVersion)
        assert unpickled.major == test_object.major
        assert unpickled.minor == test_object.minor
        assert unpickled.patch == test_object.patch

    def test_equality(self) -> None:
        """Test the __eq__ method of the version class.

        This test verifies that the __eq__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 3)
        version3 = self.TestClass(1, 2, 4)

        assert version1 == version2
        assert not (version1 == version3)
        assert version1 == "1.2.3"
        assert version1 == [1, 2, 3]
        assert version1 == (1, 2, 3)

    def test_inequality(self) -> None:
        """Test the __ne__ method of the version class.

        This test verifies that the __ne__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 3)
        version3 = self.TestClass(1, 2, 4)

        assert not (version1 != version2)
        assert version1 != version3
        assert not (version1 != "1.2.3")
        assert not (version1 != [1, 2, 3])
        assert not (version1 != (1, 2, 3))

    def test_less_than(self) -> None:
        """Test the __lt__ method of the version class.

        This test verifies that the __lt__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 4)
        version3 = self.TestClass(1, 3, 0)
        version4 = self.TestClass(2, 0, 0)

        assert version1 < version2
        assert version1 < version3
        assert version1 < version4
        assert version2 < version3
        assert version2 < version4
        assert version3 < version4

        assert version1 < "1.2.4"
        assert version1 < [1, 3, 0]
        assert version1 < (2, 0, 0)

    def test_greater_than(self) -> None:
        """Test the __gt__ method of the version class.

        This test verifies that the __gt__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 2)
        version3 = self.TestClass(1, 1, 0)
        version4 = self.TestClass(0, 9, 9)

        assert version1 > version2
        assert version1 > version3
        assert version1 > version4
        assert version2 > version3
        assert version2 > version4
        assert version3 > version4

        assert version1 > "1.2.2"
        assert version1 > [1, 1, 0]
        assert version1 > (0, 9, 9)

    def test_less_than_or_equal(self) -> None:
        """Test the __le__ method of the version class.

        This test verifies that the __le__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 3)
        version3 = self.TestClass(1, 2, 4)

        assert version1 <= version2
        assert version1 <= version3
        assert not (version3 <= version1)

        assert version1 <= "1.2.3"
        assert version1 <= [1, 2, 4]
        assert not (version1 <= (1, 2, 2))

    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of the version class.

        This test verifies that the __ge__ method correctly compares version instances.
        """
        version1 = self.TestClass(1, 2, 3)
        version2 = self.TestClass(1, 2, 3)
        version3 = self.TestClass(1, 2, 2)

        assert version1 >= version2
        assert version1 >= version3
        assert not (version3 >= version1)

        assert version1 >= "1.2.3"
        assert version1 >= [1, 2, 2]
        assert not (version1 >= (1, 2, 4))

    def test_str_representation(self, test_object: TriNumberVersion) -> None:
        """Test the string representation of the version object.

        This test verifies that the __str__ method returns the correct string representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert str(test_object) == "1.2.3"
        assert test_object.str() == "1.2.3"

    def test_list_representation(self, test_object: TriNumberVersion) -> None:
        """Test the list representation of the version object.

        This test verifies that the list method returns the correct list representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert test_object.list() == [1, 2, 3]

    def test_tuple_representation(self, test_object: TriNumberVersion) -> None:
        """Test the tuple representation of the version object.

        This test verifies that the tuple method returns the correct tuple representation.

        Args:
            test_object: A fixture providing a test version object instance.
        """
        assert test_object.tuple() == (1, 2, 3)

    def test_set_version_from_string(self) -> None:
        """Test setting the version from a string.

        This test verifies that the set_version method correctly sets the version from a string.
        """
        version = self.TestClass()
        version.set_version("1.2.3")
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

    def test_set_version_from_iterable(self) -> None:
        """Test setting the version from an iterable.

        This test verifies that the set_version method correctly sets the version from an iterable.
        """
        version = self.TestClass()
        version.set_version([1, 2, 3])
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

        version = self.TestClass()
        version.set_version((4, 5, 6))
        assert version.major == 4
        assert version.minor == 5
        assert version.patch == 6

    def test_set_version_from_int(self) -> None:
        """Test setting the version from integers.

        This test verifies that the set_version method correctly sets the version from integers.
        """
        version = self.TestClass()
        version.set_version(1, 2, 3)
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

        version = self.TestClass()
        version.set_version(4)
        assert version.major == 4
        assert version.minor == 0
        assert version.patch == 0

    # Additional tests for edge cases
    def test_creation_from_partial_string(self) -> None:
        """Test that instances of the class handle partial strings appropriately.

        This test verifies that the TriNumberVersion class raises an appropriate exception when given a string with fewer than 3 numbers.
        """
        with pytest.raises(ValueError):
            self.TestClass("1.2")

        with pytest.raises(ValueError):
            self.TestClass("1")

    def test_creation_from_partial_iterable(self) -> None:
        """Test that instances of the class handle partial iterables appropriately.

        This test verifies that the TriNumberVersion class raises an appropriate exception when given an iterable with fewer than 3 numbers.
        """
        with pytest.raises(ValueError):
            self.TestClass([1, 2])

        with pytest.raises(ValueError):
            self.TestClass([1])

    def test_creation_from_invalid_string(self) -> None:
        """Test that instances of the class handle invalid strings appropriately.

        This test verifies that the TriNumberVersion class raises an appropriate exception when given an invalid string.
        """
        with pytest.raises(ValueError):
            self.TestClass("invalid")

        with pytest.raises(ValueError):
            self.TestClass("1.invalid.3")

    def test_creation_from_empty_iterable(self) -> None:
        """Test that instances of the class handle empty iterables appropriately.

        This test verifies that the TriNumberVersion class raises an appropriate exception when given an empty iterable.
        """
        with pytest.raises(ValueError):
            self.TestClass([])

    def test_comparison_with_different_types(self) -> None:
        """Test comparison with different types.

        This test verifies that the comparison methods handle different types gracefully.
        """
        version = self.TestClass(1, 2, 3)

        # Test comparison with incompatible types
        with pytest.raises(TypeError):
            version < object()

        with pytest.raises(TypeError):
            version > object()

        with pytest.raises(TypeError):
            version <= object()

        with pytest.raises(TypeError):
            version >= object()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
