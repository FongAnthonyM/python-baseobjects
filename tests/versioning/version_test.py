#!/usr/bin/env python
"""version_test.py
Tests for the Version class in the baseobjects package.

This module contains tests for the Version abstract class, which provides the base functionality for version objects.
Since Version is an abstract class, a concrete test implementation is created for testing purposes.
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
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.testsuite.versioning import VersionTestSuite
from baseobjects.versioning.version import Version


# Definitions #
# Base Class Tests #
class MinimalVersion(Version):
    """A minimal implementation of Version to test base class methods for coverage."""

    def __init__(self, version: Any = None, init: bool = True, *args: Any, **kwargs: Any) -> None:
        """Initialize a MinimalVersion instance.

        Args:
            version: An object to derive a version from.
            init: Determines if this object will construct.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.value: int = 0
        super().__init__(version, init, *args, **kwargs)

    def construct(self, version: Any = None, **kwargs: Any) -> None:
        """Construct the version object based on inputs.

        Args:
            version: An object to derive a version from.
            **kwargs: More keyword arguments for constructing this object.

        Raises:
            TypeError: If version is not a compatible type.
        """
        if version is not None:
            if isinstance(version, int):
                self.value = version
            else:
                msg = "Invalid type"
                raise TypeError(msg)
        else:
            self.value = 0

    def list(self) -> list[Any]:
        """Return the list representation of the version.

        Returns:
            list[Any]: The list representation.
        """
        return [self.value]

    def tuple(self) -> tuple[Any, ...]:
        """Return the tuple representation of the version.

        Returns:
            tuple[Any, ...]: The tuple representation.
        """
        return (self.value,)

    def str(self) -> str:
        """Return the string representation of the version.

        Returns:
            str: The string representation.
        """
        # Call super().str() to test Version.str which calls super().__str__
        return super().str()

    def __hash__(self) -> int:
        """Return the hash of the object.

        Returns:
            int: The hash.
        """
        return super().__hash__()

    def __eq__(self, other: Any) -> bool:
        """Implement equality comparison.

        Returns:
            bool: True if equal.
        """
        return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Implement inequality comparison.

        Returns:
            bool: True if not equal.
        """
        return super().__ne__(other)

    def __lt__(self, other: Any) -> bool:
        """Implement less than comparison.

        Returns:
            bool: True if less than.
        """
        return super().__lt__(other)

    def __gt__(self, other: Any) -> bool:
        """Implement greater than comparison.

        Returns:
            bool: True if greater than.
        """
        return super().__gt__(other)

    def __le__(self, other: Any) -> bool:
        """Implement less than or equal comparison.

        Returns:
            bool: True if less than or equal.
        """
        return super().__le__(other)

    def __ge__(self, other: Any) -> bool:
        """Implement greater than or equal comparison.

        Returns:
            bool: True if greater than or equal.
        """
        return super().__ge__(other)


class TestMinimalVersion:
    """Test the base methods of Version class using MinimalVersion."""

    def test_init_no_init(self) -> None:
        """Test __init__ with init=False."""
        v_no_init = MinimalVersion(init=False)
        assert v_no_init.value == 0

    def test_hash(self) -> None:
        """Test __hash__."""
        v1 = MinimalVersion(1)
        assert hash(v1) == id(v1)

    @pytest.mark.parametrize(
        ("val1", "val2", "expected_eq"),
        [
            (1, 1, False),
            (1, 2, False),
        ],
    )
    def test_equality(self, val1: int, val2: int, expected_eq: bool) -> None:
        """Test equality and inequality (Identity based)."""
        v1 = MinimalVersion(val1)
        v2 = MinimalVersion(val2)
        assert (v1 == v2) is expected_eq
        assert (v1 != v2) is not expected_eq

        # Identity check
        assert (v1 == v1) is True
        assert (v1 != v1) is False

    @pytest.mark.parametrize(
        ("val1", "val2", "expected_lt", "expected_gt", "expected_le", "expected_ge"),
        [
            (5, 10, True, False, True, False),
            (5, 5, False, False, True, True),
            (10, 5, False, True, False, True),
        ],
    )
    def test_ordering(
        self, val1: int, val2: int, expected_lt: bool, expected_gt: bool, expected_le: bool, expected_ge: bool,
    ) -> None:
        """Test ordering."""
        v3 = MinimalVersion(val1)
        v4 = MinimalVersion(val2)

        assert (v3 < v4) is expected_lt
        assert (v3 > v4) is expected_gt
        assert (v3 <= v4) is expected_le
        assert (v3 >= v4) is expected_ge

    @pytest.mark.parametrize("op", ["__lt__", "__gt__", "__le__", "__ge__"])
    def test_comparison_invalid_types(self, op: str) -> None:
        """Test comparison with invalid types."""
        v3 = MinimalVersion(5)
        with pytest.raises(TypeError):
            getattr(v3, op)("string")

    def test_str(self) -> None:
        """Test str()."""
        v3 = MinimalVersion(5)
        s = v3.str()
        assert "MinimalVersion" in s


# Concrete Tests #
class ConcreteVersion(Version):
    """A concrete implementation of Version for testing purposes.

    This class implements the abstract methods of Version to allow testing of the base functionality.
    """

    def __init__(self, version: Any = None, init: bool = True, *args: Any, **kwargs: Any) -> None:
        """Initialize a ConcreteVersion instance.

        Args:
            version: An object to derive a version from.
            init: Determines if this object will construct.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.value: int | float = 0
        super().__init__(version, init, *args, **kwargs)

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
            return self.value == cast(ConcreteVersion, other).value
        else:
            return bool(self.value == other)

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
            return self.value < cast(ConcreteVersion, other).value
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
            return self.value > cast(ConcreteVersion, other).value
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
            return self.value <= cast(ConcreteVersion, other).value
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
            return self.value >= cast(ConcreteVersion, other).value
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
                self.value = cast(ConcreteVersion, version).value
            elif isinstance(version, str):
                try:
                    self.value = int(version)
                except ValueError:
                    msg = f"Cannot convert string '{version}' to ConcreteVersion"
                    raise TypeError(msg) from None
            else:
                msg = f"Cannot convert {type(version).__name__} to ConcreteVersion"
                raise TypeError(msg)
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


class TestVersion(VersionTestSuite):
    """Test suite for the Version class.

    This class tests the functionality of the Version class using a concrete implementation.
    """

    # Class Attributes #
    UnitTestClass: ClassVar[type[ConcreteVersion]] = ConcreteVersion

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> Version:
        """Create a test version instance for use in tests.

        Returns:
            Version: An instance of the test class.
        """
        return self.UnitTestClass(5)

    # Tests
    def test_creation_with_value(self) -> None:
        """Test that instances of the class can be created with a specific value.

        This test verifies that instances of the ConcreteVersion class can be created with a specific value.
        """
        instance = self.UnitTestClass(10)
        assert instance.value == 10

    @pytest.mark.parametrize(
        ("val", "other", "expected"),
        [
            (5, 5, True),
            (5, 10, False),
        ],
    )
    def test_equality(self, val: int, other: int, expected: bool) -> None:  # type: ignore[override]
        """Test the __eq__ and __ne__ methods of the version class.

        This test verifies that the __eq__ and __ne__ methods correctly compares version instances.
        """
        version = self.UnitTestClass(val)
        other_version = self.UnitTestClass(other)

        # Test Identity/Value Equality
        assert (version == other_version) is expected
        assert (version != other_version) is not expected

        # Test Equality with Value
        assert (version == other) is expected
        assert (version != other) is not expected

    def test_inequality(self) -> None:
        """Test the __ne__ method of the version class.

        This test is covered by test_equality via parametrization.
        """

    @pytest.mark.parametrize(
        ("val", "other", "expected_lt", "expected_gt", "expected_le", "expected_ge"),
        [
            (5, 10, True, False, True, False),
            (5, 5, False, False, True, True),
            (10, 5, False, True, False, True),
        ],
    )
    def test_ordering(
        self, val: int, other: int, expected_lt: bool, expected_gt: bool, expected_le: bool, expected_ge: bool,
    ) -> None:
        """Test the ordering methods (__lt__, __gt__, __le__, __ge__) of the version class.

        This test verifies that the ordering methods correctly compares version instances.
        """
        version = self.UnitTestClass(val)
        other_version = self.UnitTestClass(other)

        for o in [other_version, other]:
            assert (version < o) is expected_lt
            assert (version > o) is expected_gt
            assert (version <= o) is expected_le
            assert (version >= o) is expected_ge

    def test_less_than(self) -> None:
        """Test the __lt__ method of the version class. Covered by test_ordering."""

    def test_greater_than(self) -> None:
        """Test the __gt__ method of the version class. Covered by test_ordering."""

    def test_less_than_or_equal(self) -> None:
        """Test the __le__ method of the version class. Covered by test_ordering."""

    def test_greater_than_or_equal(self) -> None:
        """Test the __ge__ method of the version class. Covered by test_ordering."""

    @pytest.mark.parametrize(
        ("input_raw", "expected_val", "pass_arg", "expect_success", "expected_exception"),
        [
            (5, 5, None, True, None),
            (ConcreteVersion(10), 10, None, True, None),
            (object(), None, True, False, None),
            (object(), None, False, False, TypeError),
        ],
    )
    def test_cast_method(
        self, input_raw: Any, expected_val: Any, pass_arg: bool | None, expect_success: bool, expected_exception: Any,
    ) -> None:
        """Test the cast class method of the version class with various inputs.

        This test verifies that the cast method correctly converts objects to version instances.
        """
        # Determine kwargs
        kwargs = {}
        if pass_arg is not None:
            kwargs["pass_"] = pass_arg

        if expected_exception:
            with pytest.raises(expected_exception):
                self.UnitTestClass.cast(input_raw, **kwargs)
        else:
            result = self.UnitTestClass.cast(input_raw, **kwargs)

            if expect_success:
                assert isinstance(result, self.UnitTestClass)
                assert result.value == expected_val
            else:
                # pass_=True case with invalid input returns the input itself
                assert isinstance(result, object)
                assert not isinstance(result, self.UnitTestClass)
                assert result is input_raw

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
