"""trinumberversion.py
Implementation of a three-number versioning system.

This module provides the TriNumberVersion class which implements a version system defined by three numbers: major,
minor, and patch. The class does not enforce any special meaning of these numbers, but follows the convention that the
major number is more significant than the minor number, which is more significant than the patch number. This follows
similar patterns like Semantic Versioning (https://semver.org/).
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
import builtins
from collections.abc import Iterable
from typing import Any

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:  # pragma: no cover
    TypeCheckError = TypeError  # type: ignore

# Local Packages #
from .version import Version


# Definitions #
# Classes #
class TriNumberVersion(Version):
    """A dataclass like class that stores and handles a version number.

    Class Attributes:
        default_version_name: The default name of this version object.

    Attributes:
        major: The major change number of the version.
        minor: The minor change number of the version.
        patch: The patch change number of the version.
    """

    # Attributes #
    major: int = 0
    minor: int = 0
    patch: int = 0

    # Magic Methods
    # Construction/Destruction
    def __init__(
        self,
        version: Iterable[int] | builtins.str | int | TriNumberVersion | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: builtins.str | None = None,
        init: bool = True,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            version: A 3-part iterable, dotted string (e.g., "1.2.3"), integer for major, or None.
            minor: Optional minor component when constructing from an int or explicit parts.
            patch: Optional patch component when constructing from an int or explicit parts.
            major: Optional major component when constructing from explicit parts.
            ver_name: Optional name for the version type.
            init: If True, call construct to set fields from the provided arguments.
        """
        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(version=version, minor=minor, patch=patch, major=major, ver_name=ver_name)

    # Representation #
    def __hash__(self) -> int:
        """Overrides hash to make the object hashable.

        Returns:
            The system ID of the object.
        """
        return id(self)

    # Comparison
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            return False
        elif not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                return False

        return bool(self.tuple() == other.tuple())

    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is not equivalent.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            return True
        elif not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                return True

        return bool(self.tuple() != other.tuple())

    def __lt__(self, other: Any) -> bool:
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            msg = f"'<' not supported between instances of '{self!s}' and 'NoneType'"
            raise TypeError(msg) from None
        if not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                msg = f"'<' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

        return bool(self.tuple() < other.tuple())

    def __gt__(self, other: Any) -> bool:
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            msg = f"'>' not supported between instances of '{self!s}' and 'NoneType'"
            raise TypeError(msg) from None
        if not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                msg = f"'>' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

        return bool(self.tuple() > other.tuple())

    def __le__(self, other: Any) -> bool:
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            msg = f"'<=' not supported between instances of '{self!s}' and 'NoneType'"
            raise TypeError(msg) from None
        if not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                msg = f"'<=' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

        return bool(self.tuple() <= other.tuple())

    def __ge__(self, other: Any) -> bool:
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if hasattr(other, "VERSION"):
            other = other.VERSION

        if other is None:
            msg = f"'>=' not supported between instances of '{self!s}' and 'NoneType'"
            raise TypeError(msg) from None
        if not isinstance(other, TriNumberVersion):
            try:
                other = self.cast(other)
            except (TypeError, TypeCheckError):
                msg = f"'>=' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

        return bool(self.tuple() >= other.tuple())

    # Instance Methods
    # Constructors/Destructors
    def construct(
        self,
        version: Iterable[int] | builtins.str | int | TriNumberVersion | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: builtins.str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            version: An object to derive a version from.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.
            ver_name: The name of the version type being used.
            **kwargs: Additional keyword arguments.
        """
        self.set_version(version=version, minor=minor, patch=patch, major=major)

    def set_version(
        self,
        version: Iterable[int] | builtins.str | int | TriNumberVersion | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
    ) -> None:
        """Sets the version based on the first input type.

        Args:
            version: An object to derive a version from.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.

        Raises:
            TypeError: If the supplied input cannot be used to construct this object.
            ValueError: If the version string or iterable is invalid.
        """
        try:
            match version:
                case str():
                    ranks = [int(r) for r in version.split(".")]
                    self.major, self.minor, self.patch = ranks
                case int():
                    self.major = version
                    if minor is not None:
                        self.minor = minor
                    if patch is not None:
                        self.patch = patch
                case None:
                    if major is not None:
                        self.major = major
                    if minor is not None:
                        self.minor = minor
                    if patch is not None:
                        self.patch = patch
                case TriNumberVersion():
                    self.major = version.major
                    self.minor = version.minor
                    self.patch = version.patch
                case Iterable():
                    self.major, self.minor, self.patch = version
                case _:
                    msg = f"Cannot construct version from '{version!s}' of type '{type(version)!s}'"  # type: ignore[unreachable]
                    raise TypeError(msg)
        except ValueError as e:
            msg = f"Invalid version format: {version}"
            raise ValueError(msg) from e

    # Type Conversion
    def list(self) -> builtins.list[int]:
        """Returns the list representation of the version.

        Returns:
            A list with the version numbers in order.
        """
        return [self.major, self.minor, self.patch]

    def tuple(self) -> builtins.tuple[int, int, int]:
        """Returns the tuple representation of the version.

        Returns:
            A tuple with the version numbers in order.
        """
        return self.major, self.minor, self.patch

    def str(self) -> builtins.str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return f"{self.major}.{self.minor}.{self.patch}"
