"""trinumberversiontestsuite.py
Test suite for the TriNumberVersion class.
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
from typing import Any

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Local Packages #
from ...versioning.trinumberversion import TriNumberVersion
from .versiontestsuite import VersionTestSuite


# Definitions #
# Classes #
class TriNumberVersionTestSuite(VersionTestSuite):
    """Tests suite for the TriNumberVersion class.

    This class provides common test functionality for TriNumberVersion classes.
    """

    UnitTestClass: type[TriNumberVersion] = TriNumberVersion

    # Fixtures #
    @pytest.fixture
    def test_object(self, *args: Any, **kwargs: Any) -> TriNumberVersion:
        """Creates a test version instance for use in tests.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            TriNumberVersion: An instance of the test class with major=1, minor=2, patch=3.
        """
        return self.UnitTestClass(1, 2, 3)

    # Tests #
    # Magic Methods #
    def test_str_representation(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests the string representation."""
        assert str(test_object) == "1.2.3"
        assert test_object.str() == "1.2.3"

    # Instantiation #
    def test_instance_creation(self) -> None:
        """Tests that instances of the class can be created."""
        instance = self.UnitTestClass()
        assert instance is not None
        assert isinstance(instance, self.UnitTestClass)
        assert instance.major == 0
        assert instance.minor == 0
        assert instance.patch == 0

    # Copying #
    def test_copy(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests the copy behavior of a version object."""
        obj_copy = copy.copy(test_object)
        assert obj_copy is not test_object
        assert obj_copy.major == test_object.major
        assert obj_copy.minor == test_object.minor
        assert obj_copy.patch == test_object.patch

    def test_copy_method(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests the copy method behavior of a version object."""
        obj_copy = test_object.copy()
        assert obj_copy is not test_object
        assert obj_copy.major == test_object.major
        assert obj_copy.minor == test_object.minor
        assert obj_copy.patch == test_object.patch

    def test_deepcopy(self, test_object: TriNumberVersion, memo: dict[Any, Any] | None = None) -> None:  # type: ignore[override]
        """Tests the deep copy behavior of a version object."""
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.major == test_object.major
        assert obj_deepcopy.minor == test_object.minor
        assert obj_deepcopy.patch == test_object.patch

    def test_deepcopy_method(self, test_object: TriNumberVersion, memo: dict[Any, Any] | None = None) -> None:  # type: ignore[override]
        """Tests the deepcopy method behavior of a version object."""
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.major == test_object.major
        assert obj_deepcopy.minor == test_object.minor
        assert obj_deepcopy.patch == test_object.patch

    # Pickling #
    def test_pickling(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests pickling and unpickling of a version object."""
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)
        assert unpickled is not test_object
        assert isinstance(unpickled, TriNumberVersion)
        assert unpickled.major == test_object.major
        assert unpickled.minor == test_object.minor
        assert unpickled.patch == test_object.patch

    # Functionality #
    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            ([1, 2, 3], {}, (1, 2, 3)),
            (["1.2.3"], {}, (1, 2, 3)),
            ([[1, 2, 3]], {}, (1, 2, 3)),
            ([(1, 2, 3)], {}, (1, 2, 3)),
            ([], {"major": 1, "minor": 2, "patch": 3}, (1, 2, 3)),
        ],
    )
    def test_creation(
        self,
        args: list[Any],
        kwargs: dict[str, Any],
        expected: tuple[int, int, int],
    ) -> None:
        """Tests that instances of the class can be created with various inputs.

        Args:
            args: Positional arguments for instantiation.
            kwargs: Keyword arguments for instantiation.
            expected: Expected (major, minor, patch) tuple.
        """
        instance = self.UnitTestClass(*args, **kwargs)
        assert instance.major == expected[0]
        assert instance.minor == expected[1]
        assert instance.patch == expected[2]

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 3), True),
            (lambda cls: cls(1, 2, 4), False),
            (lambda _: "1.2.3", True),
            (lambda _: [1, 2, 3], True),
            (lambda _: (1, 2, 3), True),
            (lambda _: "1.2.4", False),
            (lambda _: [1, 2, 4], False),
            (lambda _: (1, 2, 4), False),
            (lambda _: None, False),
            (lambda _: object(), False),
        ],
    )
    def test_equality(self, other_factory: Any, expected: bool) -> None:
        """Tests the __eq__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of equality.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version == other) is expected

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 3), False),
            (lambda cls: cls(1, 2, 4), True),
            (lambda _: "1.2.3", False),
            (lambda _: [1, 2, 3], False),
            (lambda _: (1, 2, 3), False),
            (lambda _: "1.2.4", True),
            (lambda _: [1, 2, 4], True),
            (lambda _: (1, 2, 4), True),
            (lambda _: None, True),
            (lambda _: object(), True),
        ],
    )
    def test_inequality(self, other_factory: Any, expected: bool) -> None:
        """Tests the __ne__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of inequality.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version != other) is expected

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 4), True),
            (lambda cls: cls(1, 3, 0), True),
            (lambda cls: cls(2, 0, 0), True),
            (lambda cls: cls(1, 2, 3), False),
            (lambda cls: cls(1, 1, 0), False),
            (lambda _: "1.2.4", True),
            (lambda _: [1, 3, 0], True),
            (lambda _: (2, 0, 0), True),
        ],
    )
    def test_less_than(self, other_factory: Any, expected: bool) -> None:
        """Tests the __lt__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of less than comparison.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version < other) is expected

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 2), True),
            (lambda cls: cls(1, 1, 0), True),
            (lambda cls: cls(0, 9, 9), True),
            (lambda cls: cls(1, 2, 3), False),
            (lambda cls: cls(1, 2, 4), False),
            (lambda _: "1.2.2", True),
            (lambda _: [1, 1, 0], True),
            (lambda _: (0, 9, 9), True),
        ],
    )
    def test_greater_than(self, other_factory: Any, expected: bool) -> None:
        """Tests the __gt__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of greater than comparison.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version > other) is expected

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 3), True),
            (lambda cls: cls(1, 2, 4), True),
            (lambda cls: cls(1, 2, 2), False),
            (lambda _: "1.2.3", True),
            (lambda _: [1, 2, 4], True),
            (lambda _: (1, 2, 2), False),
        ],
    )
    def test_less_than_or_equal(self, other_factory: Any, expected: bool) -> None:
        """Tests the __le__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of less than or equal comparison.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version <= other) is expected

    @pytest.mark.parametrize(
        ("other_factory", "expected"),
        [
            (lambda cls: cls(1, 2, 3), True),
            (lambda cls: cls(1, 2, 2), True),
            (lambda cls: cls(1, 2, 4), False),
            (lambda _: "1.2.3", True),
            (lambda _: [1, 2, 2], True),
            (lambda _: (1, 2, 4), False),
        ],
    )
    def test_greater_than_or_equal(self, other_factory: Any, expected: bool) -> None:
        """Tests the __ge__ method.

        Args:
            other_factory: A function that takes the class and returns the object to compare.
            expected: The expected result of greater than or equal comparison.
        """
        version = self.UnitTestClass(1, 2, 3)
        other = other_factory(self.UnitTestClass)
        assert (version >= other) is expected

    def test_list_representation(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests the list representation."""
        assert test_object.list() == [1, 2, 3]

    def test_tuple_representation(self, test_object: TriNumberVersion) -> None:  # type: ignore[override]
        """Tests the tuple representation."""
        assert test_object.tuple() == (1, 2, 3)

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            (("1.2.3",), (1, 2, 3)),
            (([1, 2, 3],), (1, 2, 3)),
            (((4, 5, 6),), (4, 5, 6)),
            ((1, 2, 3), (1, 2, 3)),
            ((4,), (4, 0, 0)),
        ],
    )
    def test_set_version(self, args: tuple[Any, ...], expected: tuple[int, int, int]) -> None:
        """Tests setting the version from various inputs.

        Args:
            args: Arguments for set_version.
            expected: Expected (major, minor, patch) tuple.
        """
        version = self.UnitTestClass()
        version.set_version(*args)
        assert version.major == expected[0]
        assert version.minor == expected[1]
        assert version.patch == expected[2]

    @pytest.mark.parametrize("arg", ["1.2", "1", [1, 2], [1], "invalid", "1.invalid.3", "1.2.3.4", []])
    def test_creation_invalid(self, arg: Any) -> None:
        """Tests handling invalid inputs for creation.

        Args:
            arg: The invalid argument to test.
        """
        with pytest.raises(ValueError, match="Invalid"):
            self.UnitTestClass(arg)

    @pytest.mark.parametrize("other", [object(), None])
    def test_comparison_with_invalid_types(self, other: Any) -> None:
        """Tests comparison with invalid types.

        Args:
            other: The invalid object to compare with.
        """
        version = self.UnitTestClass(1, 2, 3)

        with pytest.raises(TypeError, match="not supported"):
            _ = version < other

        with pytest.raises(TypeError, match="not supported"):
            _ = version > other

        with pytest.raises(TypeError, match="not supported"):
            _ = version <= other

        with pytest.raises(TypeError, match="not supported"):
            _ = version >= other

    def test_equality_with_version_attribute(self) -> None:
        """Tests equality with an object having a VERSION attribute."""

        class ObjWithVersion:  # noqa: B903
            def __init__(self, v: Any) -> None:
                self.VERSION = v

        version1 = self.UnitTestClass(1, 2, 3)
        obj = ObjWithVersion(self.UnitTestClass(1, 2, 3))
        assert version1 == obj

        obj_diff = ObjWithVersion(self.UnitTestClass(1, 2, 4))
        assert not (version1 == obj_diff)

    def test_init_without_init(self) -> None:
        """Tests initialization with init=False."""
        version = self.UnitTestClass(1, 2, 3, init=False)
        assert version.major == 0
        assert version.minor == 0
        assert version.patch == 0

    def test_set_version_invalid_type(self) -> None:
        """Tests setting the version from an invalid type."""
        version = self.UnitTestClass()
        with pytest.raises((TypeError, TypeCheckError)):
            version.set_version(object())  # type: ignore[arg-type]

    def test_creation_from_trinumberversion(self, test_object: TriNumberVersion) -> None:
        """Tests that instances of the class can be created from another TriNumberVersion instance."""
        instance = self.UnitTestClass(test_object)
        assert instance is not test_object
        assert instance.major == test_object.major
        assert instance.minor == test_object.minor
        assert instance.patch == test_object.patch

    def test_set_version_from_trinumberversion(self, test_object: TriNumberVersion) -> None:
        """Tests setting the version from another TriNumberVersion instance."""
        version = self.UnitTestClass()
        version.set_version(test_object)
        assert version.major == test_object.major
        assert version.minor == test_object.minor
        assert version.patch == test_object.patch

    def test_comparison_with_version_attribute(self) -> None:
        """Tests comparisons with an object having a VERSION attribute."""

        class ObjWithVersion:  # noqa: B903
            def __init__(self, v: Any) -> None:
                self.VERSION = v

        v1 = self.UnitTestClass(1, 2, 3)
        v2_obj = ObjWithVersion(self.UnitTestClass(1, 2, 4))
        v3 = self.UnitTestClass(1, 2, 4)
        v1_obj = ObjWithVersion(self.UnitTestClass(1, 2, 3))

        # Test __ne__
        assert v1 != v2_obj

        # Test __lt__
        assert v1 < v2_obj

        # Test __le__
        assert v1 <= v2_obj

        # Test __gt__
        assert v3 > v1_obj

        # Test __ge__
        assert v3 >= v1_obj
