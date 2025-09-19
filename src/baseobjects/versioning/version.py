"""version.py
Abstract base class for version objects.

This module provides the Version abstract base class that defines the interface for all version implementations. It
includes abstract methods for comparison, construction, and type conversion that must be implemented by subclasses.

Typical usage example:

  class CustomVersion(Version):
      # Implement abstract methods
      ...

  version = CustomVersion("1.0")
  print(f"Version: {version}")
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
from abc import abstractmethod
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class Version(BaseObject):
    """An abstract class for creating versions which stores and handles a versioning.

    Args:
        version: An object to derive a version from.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for constructing this object
    """

    # Class Methods #
    @classmethod
    def cast(cls, other: Any, pass_: bool = False) -> Any:
        """A cast method that optionally returns the original object rather than raise an error

        Args:
            other: An object to convert to this type.
            pass_: True to return the original object rather than raise an error.

        Returns:
            obj: The converted object of this type or the original object.

        Raises:
            TypeError: If the object cannot be converted to this type.
        """
        try:
            other = cls(other)
        except Exception as e:
            if not pass_:
                raise e

        return other

    # Magic Methods #
    # Construction/Destruction #
    def __init__(
        self,
        version: Any | None = None,
        init: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(version=version, **kwargs)

    # Representation #
    @abstractmethod
    def __hash__(self) -> int:
        """Overrides hash to make the object hashable.

        Subclasses must override this method if they wish to be hashable.

        Returns:
            The system ID of the object.
        """
        return id(self)

    # Type Conversion #
    def __str__(self) -> str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return self.str()

    # Comparison #
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        return super().__eq__(other)

    @abstractmethod
    def __ne__(self, other: Any) -> bool:
        """Expands on not equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is not equivalent.
        """
        return super().__ne__(other)

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        """Creates the less than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() < other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        """Creates the greater than comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() > other.tuple()
        else:
            raise TypeError(f"'>' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        """Creates the less than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is less than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() <= other.tuple()
        else:
            raise TypeError(f"'<=' not supported between instances of '{str(self)}' and '{str(other)}'")

    @abstractmethod
    def __ge__(self, other: Any) -> bool:
        """Creates the greater than or equal to comparison for these objects which includes str, list, and tuple.

        Args:
            other: The object to compare to this object.

        Returns:
            True if this object is greater than or equal to to the other objects' version number.

        Raises:
            TypeError: If 'other' is a type that cannot be compared to.
        """
        other = self.cast(other, pass_=True)

        if isinstance(other, Version):
            return self.tuple() >= other.tuple()
        else:
            raise TypeError(f"'>=' not supported between instances of '{str(self)}' and '{str(other)}'")

    # Instance Methods #
    # Constructors/Destructors #
    @abstractmethod
    def construct(self, version: Any = None, **kwargs: Any) -> None:
        """Constructs the version object based on inputs

        Args:
            version: An object to derive a version from.
            **kwargs: More keyword arguments for constructing this object
        """

    # Type Conversion #
    @abstractmethod
    def list(self) -> list[Any]:
        """Returns the list representation of the version.

        Returns:
            The list representation of the version.
        """

    @abstractmethod
    def tuple(self) -> tuple[Any]:
        """Returns the tuple representation of the version.

        Returns:
            The tuple representation of the version.
        """

    @abstractmethod
    def str(self) -> str:
        """Returns the str representation of the version.

        Returns:
            A str with the version numbers in order.
        """
        return super().__str__()
