#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" version_test.py
Tests for the Version class in the baseobjects package.
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
from src.baseobjects.versioning.version import Version
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
class TestVersionSubclass(Version):
    """A concrete subclass of Version for testing purposes.

    This class implements all the abstract methods required by Version.
    """
    def __eq__(self, other: Any) -> bool:
        """Implements the abstract __eq__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object is equivalent.
        """
        return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Implements the abstract __ne__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object is not equivalent.
        """
        return super().__ne__(other)

    def __lt__(self, other: Any) -> bool:
        """Implements the abstract __lt__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than the other object.
        """
        return super().__lt__(other)

    def __gt__(self, other: Any) -> bool:
        """Implements the abstract __gt__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than the other object.
        """
        return super().__gt__(other)

    def __le__(self, other: Any) -> bool:
        """Implements the abstract __le__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to the other object.
        """
        return super().__le__(other)

    def __ge__(self, other: Any) -> bool:
        """Implements the abstract __ge__ method.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to the other object.
        """
        return super().__ge__(other)

    def __hash__(self) -> int:
        """Implements the __hash__ method to make the object hashable.

        Returns:
            The id of the object.
        """
        return id(self)

    def construct(self, version: Any = None, **kwargs: Any) -> None:
        """Implements the abstract construct method.

        Args:
            version: An object to derive a version from.
            **kwargs: More keyword arguments for constructing this object
        """
        super().construct()

    def list(self) -> list[Any]:
        """Implements the abstract list method.

        Returns:
            The list representation of the version.
        """
        return []

    def tuple(self) -> tuple[Any]:
        """Implements the abstract tuple method.

        Returns:
            The tuple representation of the version.
        """
        return ()

    def str(self) -> str:
        """Implements the abstract str method.

        Returns:
            A str with the version numbers in order.
        """
        return "0.0.0"


class TestVersion(BaseBaseObjectTest):
    """Test the Version class.

    This class tests the functionality of the Version class, which is an abstract base class for version objects.
    It creates a concrete subclass of Version to test with.
    """

    # Class Definitions #
    class TestVersion(TestVersionSubclass):
        """A concrete subclass of Version for testing purposes."""
        pass

    # Attributes #
    class_: Type[TestVersion] = TestVersion

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_version(self) -> TestVersion:
        """Create a test version instance for use in tests.

        Returns:
            TestVersion: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created.

        This test verifies that instances of the TestVersion class can be created.
        """
        instance = self.class_()
        assert instance is not None
        assert isinstance(instance, self.class_)
        assert isinstance(instance, Version)

    def test_hash(self, test_version: TestVersion) -> None:
        """Test the __hash__ method of Version.

        This test verifies that the __hash__ method returns the id of the object.

        Args:
            test_version: A fixture providing a TestVersion instance.
        """
        assert hash(test_version) == id(test_version)

    def test_str(self, test_version: TestVersion) -> None:
        """Test the __str__ method of Version.

        This test verifies that the __str__ method returns the result of the str method.

        Args:
            test_version: A fixture providing a TestVersion instance.
        """
        assert str(test_version) == test_version.str()

    def test_pickle(self, test_version: TestVersion) -> None:
        """Test that Version objects can be pickled and unpickled.

        This test verifies that Version objects can be serialized and deserialized using pickle.

        Args:
            test_version: A fixture providing a TestVersion instance.
        """
        pickled = pickle.dumps(test_version)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_version
        assert isinstance(unpickled, Version)
        assert isinstance(unpickled, self.class_)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
