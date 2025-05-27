"""sentinelobject.py
An object which acts as a sentinel object.
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
from typing import Literal

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class SentinelObject:
    """An object which acts as a sentinel object.

    Attributes:
        id_number: The id of this sentinel.

    Args:
        id_: The id of this sentinel.
        encoding: The string encoding to use when given a string ID.
        errors: The string encoding errors to use when given a string ID.
    """

    # Attributes #
    id_number: int

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        id_: str | bytes | int,
        encoding: str = "utf-8",
        errors: str = "strict",
        byteorder: Literal["little", "big"] = "big",
        signed: bool = False
    ) -> None:
        match id_:
            case str():
                self.id_number = int.from_bytes(id_.encode(encoding, errors), byteorder, signed=signed)
            case bytes():
                self.id_number = int.from_bytes(id_, byteorder, signed=signed)
            case int():
                self.id_number = id_

    # Representation
    def __hash__(self) -> int:
        """Overrides hash to make the object hashable.

        Returns:
            The system ID of the object.
        """
        return self.id_number

    # Comparison
    def __eq__(self, other: "SentinelObject") -> bool:
        """Expands on equals comparison to include comparing the ID number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other sentinel is equivalent.
        """
        return isinstance(other, SentinelObject) and self.id_number == other.id_number


# Constants #
DEFAULTSENTINEL = SentinelObject("DEFAULTSENTINEL")
SEARCHSENTINEL = SentinelObject("SEARCHSENTINEL")
search_sentinel = SentinelObject("search_sentinel")
