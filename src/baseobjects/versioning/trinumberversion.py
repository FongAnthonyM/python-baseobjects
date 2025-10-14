"""trinumberversion.py
Implementation of a three-number versioning system.

This module provides the TriNumberVersion class which implements a version system defined by three numbers: major,
minor, and patch. The class does not enforce any special meaning of these numbers, but follows the convention that the
major number is more significant than the minor number, which is more significant than the patch number. This follows
similar patterns like Semantic Versioning (https://semver.org/).

Typical usage example:

  version = TriNumberVersion("1.2.3")
  print(f"Version: {version}")  # Outputs: Version: 1.2.3

  # Compare versions
  if version > TriNumberVersion("1.0.0"):
      print("Newer version")

  # Create from components
  new_version = TriNumberVersion(major=2, minor=0, patch=0)
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
from collections.abc import Iterable
from typing import Any

# Local Packages #
from ..functions import singlekwargdispatch
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

    Args:
        version: An object to derive a version from.
        minor: The minor change number of the version.
        patch: The patch change number of the version.
        major: The major change number of the version.
        ver_name : The name of the version type being used.
        init: Determines if this object will construct.
    """

    # Attributes #
    major: int = 0
    minor: int = 0
    patch: int = 0

    # Magic Methods
    # Construction/Destruction
    def __init__(
        self,
        version: Iterable[int] | str | int | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: str | None = None,
        init: bool = True,
    ) -> None:
        """Initialize a TriNumberVersion instance.

        Optionally constructs the version values from the provided inputs.

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
        if isinstance(other, TriNumberVersion):
            return self.tuple() == other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() == other.VERSION.tuple()  # Todo: Maybe change the order to be cast friendly
        else:
            try:
                return self.tuple() == self.cast(other).tuple()
            except TypeError:
                return super().__eq__(other)

    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is not equivalent.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() != other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() != other.VERSION.tuple()
        else:
            try:
                return self.tuple() != self.cast(other).tuple()
            except TypeError:
                return super().__ne__(other)

    def __lt__(self, other: Any) -> bool:
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() < other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() < other.VERSION.tuple()
        else:
            try:
                return self.tuple() < self.cast(other).tuple()
            except TypeError:
                msg = f"'<' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

    def __gt__(self, other: Any) -> bool:
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() > other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() > other.VERSION.tuple()
        else:
            try:
                return self.tuple() > self.cast(other).tuple()
            except TypeError:
                msg = f"'>' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

    def __le__(self, other: Any) -> bool:
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() <= other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() <= other.VERSION.tuple()
        else:
            try:
                return self.tuple() <= self.cast(other).tuple()
            except TypeError:
                msg = f"'<=' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

    def __ge__(self, other: Any) -> bool:
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        if isinstance(other, TriNumberVersion):
            return self.tuple() >= other.tuple()
        elif hasattr(other, "VERSION"):
            return self.tuple() >= other.VERSION.tuple()
        else:
            try:
                return self.tuple() >= self.cast(other).tuple()
            except TypeError:
                msg = f"'>=' not supported between instances of '{self!s}' and '{other!s}'"
                raise TypeError(msg) from None

    # Instance Methods
    # Constructors/Destructors
    def construct(
        self,
        version: Iterable[int] | str | int | None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
        ver_name: str | None = None,
    ) -> None:
        """Constructs the version object based on inputs.

        Args:
            version: An object to derive a version from.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.
            ver_name: The name of the version type being used.
        """
        self.set_version(version=version, minor=minor, patch=patch, major=major)

        super().construct(ver_name)

    @singlekwargdispatch(kwarg="version")
    def set_version(
        self,
        version: Iterable[int] | str | int | None = None,
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
        """
        msg = f"{type(self)} cannot set the version with {type(version)}"
        raise TypeError(msg)

    @set_version.register(Iterable)
    def _set_version_iterable(self, version: Iterable[int], **kwargs: Any) -> None:
        """Sets the version when given an iterable.

        Args:
            version: The version as an iterable.
            **kwargs: Keyword arguments for setting the version.
        """
        self.major, self.minor, self.patch = version

    @set_version.register
    def _set_version_str(self, version: str, **kwargs: Any) -> None:
        """Sets the version when given a string.

        Args:
            version: The version as a string.
            **kwargs: Keyword arguments for setting the version.
        """
        ranks = version.split(".")
        for i, r in enumerate(ranks):
            ranks[i] = int(r)
        self.major, self.minor, self.patch = ranks

    @set_version.register
    def _set_version_int(
        self,
        version: int,
        minor: int | None = None,
        patch: int | None = None,
        **kwargs: Any,
    ) -> None:
        """Sets the version when given int.

        Args:
            version: The major change number of the version.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            **kwargs: Keyword arguments for setting the version.
        """
        self.major = version
        if minor is not None:
            self.minor = minor
        if patch is not None:
            self.patch = patch

    @set_version.register
    def _set_version_none(
        self,
        version: None = None,
        minor: int | None = None,
        patch: int | None = None,
        major: int | None = None,
    ) -> None:
        """Sets the version when given None.

        Args:
            version: The major change number of the version.
            minor: The minor change number of the version.
            patch: The patch change number of the version.
            major: The major change number of the version.
        """
        if major is not None:
            self.major = major
        if minor is not None:
            self.minor = minor
        if patch is not None:
            self.patch = patch

    # Type Conversion
    def list(self) -> list[int]:
        """Returns the list representation of the version.

        Returns:
            A list with the version numbers in order.
        """
        return [self.major, self.minor, self.patch]

    def tuple(self) -> tuple[int, int, int]:
        """Returns the tuple representation of the version.

        Returns:
            A tuple with the version numbers in order.
        """
        return self.major, self.minor, self.patch

    def str(self) -> str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return f"{self.major}.{self.minor}.{self.patch}"
