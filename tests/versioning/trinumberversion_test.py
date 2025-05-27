#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" trinumberversion_test.py
Tests for the TriNumberVersion class in the baseobjects package.
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
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.versioning.trinumberversion import TriNumberVersion
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
class TestTriNumberVersion(BaseBaseObjectTest):
    """Test the TriNumberVersion class.

    This class tests the functionality of the TriNumberVersion class, which is a concrete implementation of the Version
    abstract class that represents a version with three numbers (major.minor.patch).
    """

    # Attributes #
    class_: Type[TriNumberVersion] = TriNumberVersion

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_version(self) -> TriNumberVersion:
        """Create a test version instance for use in tests.

        Returns:
            TriNumberVersion: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def test_version_with_values(self) -> TriNumberVersion:
        """Create a test version instance with specific values for use in tests.

        Returns:
            TriNumberVersion: An instance of the test class with major=1, minor=2, patch=3.
        """
        return self.class_(1, 2, 3)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the TriNumberVersion class can be created.
        """
        instance = self.class_()
        assert instance is not None
        assert isinstance(instance, self.class_)
        assert instance.major == 0
        assert instance.minor == 0
        assert instance.patch == 0

    def test_creation_with_values(self) -> None:
        """Test that instances of the class can be created with specific values.

        This test verifies that instances of the TriNumberVersion class can be created with specific values.
        """
        instance = self.class_(1, 2, 3)
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_from_string(self) -> None:
        """Test that instances of the class can be created from a string.

        This test verifies that instances of the TriNumberVersion class can be created from a string.
        """
        instance = self.class_("1.2.3")
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_from_iterable(self) -> None:
        """Test that instances of the class can be created from an iterable.

        This test verifies that instances of the TriNumberVersion class can be created from an iterable.
        """
        instance = self.class_([1, 2, 3])
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

        instance = self.class_((1, 2, 3))
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_creation_with_keyword_args(self) -> None:
        """Test that instances of the class can be created with keyword arguments.

        This test verifies that instances of the TriNumberVersion class can be created with keyword arguments.
        """
        instance = self.class_(major=1, minor=2, patch=3)
        assert instance.major == 1
        assert instance.minor == 2
        assert instance.patch == 3

    def test_str(self, test_version_with_values: TriNumberVersion) -> None:
        """Test the __str__ method of TriNumberVersion.

        This test verifies that the __str__ method returns the correct string representation.

        Args:
            test_version_with_values: A fixture providing a TriNumberVersion instance with values.
        """
        assert str(test_version_with_values) == "1.2.3"

    def test_list(self, test_version_with_values: TriNumberVersion) -> None:
        """Test the list method of TriNumberVersion.

        This test verifies that the list method returns the correct list representation.

        Args:
            test_version_with_values: A fixture providing a TriNumberVersion instance with values.
        """
        assert test_version_with_values.list() == [1, 2, 3]

    def test_tuple(self, test_version_with_values: TriNumberVersion) -> None:
        """Test the tuple method of TriNumberVersion.

        This test verifies that the tuple method returns the correct tuple representation.

        Args:
            test_version_with_values: A fixture providing a TriNumberVersion instance with values.
        """
        assert test_version_with_values.tuple() == (1, 2, 3)

    def test_equality(self) -> None:
        """Test the __eq__ method of TriNumberVersion.

        This test verifies that the __eq__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 3)
        version3 = self.class_(1, 2, 4)
        
        assert version1 == version2
        assert not (version1 == version3)
        assert version1 == "1.2.3"
        assert version1 == [1, 2, 3]
        assert version1 == (1, 2, 3)

    def test_inequality(self) -> None:
        """Test the __ne__ method of TriNumberVersion.

        This test verifies that the __ne__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 3)
        version3 = self.class_(1, 2, 4)
        
        assert not (version1 != version2)
        assert version1 != version3
        assert not (version1 != "1.2.3")
        assert not (version1 != [1, 2, 3])
        assert not (version1 != (1, 2, 3))

    def test_less_than(self) -> None:
        """Test the __lt__ method of TriNumberVersion.

        This test verifies that the __lt__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 4)
        version3 = self.class_(1, 3, 0)
        version4 = self.class_(2, 0, 0)
        
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
        """Test the __gt__ method of TriNumberVersion.

        This test verifies that the __gt__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 2)
        version3 = self.class_(1, 1, 0)
        version4 = self.class_(0, 9, 9)
        
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
        """Test the __le__ method of TriNumberVersion.

        This test verifies that the __le__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 3)
        version3 = self.class_(1, 2, 4)
        
        assert version1 <= version2
        assert version1 <= version3
        assert not (version3 <= version1)
        
        assert version1 <= "1.2.3"
        assert version1 <= [1, 2, 4]
        assert not (version1 <= (1, 2, 2))

    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of TriNumberVersion.

        This test verifies that the __ge__ method correctly compares TriNumberVersion instances.
        """
        version1 = self.class_(1, 2, 3)
        version2 = self.class_(1, 2, 3)
        version3 = self.class_(1, 2, 2)
        
        assert version1 >= version2
        assert version1 >= version3
        assert not (version3 >= version1)
        
        assert version1 >= "1.2.3"
        assert version1 >= [1, 2, 2]
        assert not (version1 >= (1, 2, 4))

    def test_set_version_from_string(self) -> None:
        """Test setting the version from a string.

        This test verifies that the set_version method correctly sets the version from a string.
        """
        version = self.class_()
        version.set_version("1.2.3")
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

    def test_set_version_from_iterable(self) -> None:
        """Test setting the version from an iterable.

        This test verifies that the set_version method correctly sets the version from an iterable.
        """
        version = self.class_()
        version.set_version([1, 2, 3])
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

        version = self.class_()
        version.set_version((4, 5, 6))
        assert version.major == 4
        assert version.minor == 5
        assert version.patch == 6

    def test_set_version_from_int(self) -> None:
        """Test setting the version from integers.

        This test verifies that the set_version method correctly sets the version from integers.
        """
        version = self.class_()
        version.set_version(1, 2, 3)
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3

        version = self.class_()
        version.set_version(4)
        assert version.major == 4
        assert version.minor == 0
        assert version.patch == 0

    def test_pickle(self, test_version_with_values: TriNumberVersion) -> None:
        """Test that TriNumberVersion objects can be pickled and unpickled.

        This test verifies that TriNumberVersion objects can be serialized and deserialized using pickle.

        Args:
            test_version_with_values: A fixture providing a TriNumberVersion instance with values.
        """
        pickled = pickle.dumps(test_version_with_values)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_version_with_values
        assert isinstance(unpickled, TriNumberVersion)
        assert unpickled.major == 1
        assert unpickled.minor == 2
        assert unpickled.patch == 3


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])