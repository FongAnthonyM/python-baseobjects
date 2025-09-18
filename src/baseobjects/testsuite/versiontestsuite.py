""" versiontestsuite.py
Specialized test suite for version classes in the baseobjects package.
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
from abc import abstractmethod
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ..versioning.version import Version
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class VersionTestSuite(BaseObjectTestSuite):
    """Base test suite for version classes.

    This class provides common test functionality for version classes, including tests for comparison operations,
    type conversions, and serialization. Subclasses should set the TestClass attribute and may override or extend
    the test methods.

    Attributes:
        TestClass: The version class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[Version] | None = None

    # Instance Methods #
    # Fixtures
    @abstractmethod
    @pytest.fixture
    def test_version(self) -> Version:
        """Create a test version instance for use in tests.

        Returns:
            Version: An instance of the test class.
        """

    @abstractmethod
    @pytest.fixture
    def test_version_with_values(self) -> Version:
        """Create a test version instance with specific values for use in tests.

        Returns:
            Version: An instance of the test class with specific values.
        """

    # Tests
    @abstractmethod
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the version class can be created.
        """

    def test_pickling(self, test_version_with_values: Version) -> None:
        """Test pickling and unpickling of the version object.

        This test verifies that the version object can be pickled and unpickled correctly.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """
        pickled = pickle.dumps(test_version_with_values)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_version_with_values
        assert isinstance(unpickled, self.TestClass)
        assert unpickled == test_version_with_values

    def test_copy(self, test_version_with_values: Version) -> None:
        """Test copying a version object.

        This test verifies that version objects can be copied correctly.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """
        new = copy.copy(test_version_with_values)
        assert new is not test_version_with_values
        assert isinstance(new, self.TestClass)
        assert new == test_version_with_values

    def test_deepcopy(self, test_version_with_values: Version) -> None:
        """Test deep copying a version object.

        This test verifies that version objects can be deep copied correctly.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """
        new = copy.deepcopy(test_version_with_values)
        assert new is not test_version_with_values
        assert isinstance(new, self.TestClass)
        assert new == test_version_with_values

    @abstractmethod
    def test_creation_with_values(self) -> None:
        """Test that instances of the class can be created with specific values.

        This test verifies that instances of the version class can be created with specific values.
        """

    @abstractmethod
    def test_creation_from_string(self) -> None:
        """Test that instances of the class can be created from a string.

        This test verifies that instances of the version class can be created from a string.
        """

    @abstractmethod
    def test_creation_from_iterable(self) -> None:
        """Test that instances of the class can be created from an iterable.

        This test verifies that instances of the version class can be created from an iterable.
        """

    @abstractmethod
    def test_str(self, test_version_with_values: Version) -> None:
        """Test the __str__ method of the version class.

        This test verifies that the __str__ method returns the correct string representation.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """

    @abstractmethod
    def test_list(self, test_version_with_values: Version) -> None:
        """Test the list method of the version class.

        This test verifies that the list method returns the correct list representation.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """

    @abstractmethod
    def test_tuple(self, test_version_with_values: Version) -> None:
        """Test the tuple method of the version class.

        This test verifies that the tuple method returns the correct tuple representation.

        Args:
            test_version_with_values: A fixture providing a version instance with values.
        """

    @abstractmethod
    def test_equality(self) -> None:
        """Test the __eq__ method of the version class.

        This test verifies that the __eq__ method correctly compares version instances.
        """

    @abstractmethod
    def test_inequality(self) -> None:
        """Test the __ne__ method of the version class.

        This test verifies that the __ne__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than(self) -> None:
        """Test the __lt__ method of the version class.

        This test verifies that the __lt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than(self) -> None:
        """Test the __gt__ method of the version class.

        This test verifies that the __gt__ method correctly compares version instances.
        """

    @abstractmethod
    def test_less_than_or_equal(self) -> None:
        """Test the __le__ method of the version class.

        This test verifies that the __le__ method correctly compares version instances.
        """

    @abstractmethod
    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of the version class.

        This test verifies that the __ge__ method correctly compares version instances.
        """


