"""baseobject.py
BaseObject is an abstract class which implements some basic functions that all objects should have.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Names #
search_sentinel = object()


# Classes #
class SentinelObject:
    """An abstract class that implements some basic functions that all objects should have."""

    # Attributes #
    name: str

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, name: str) -> None:
        self.name = name

    # Comparison
    def __eq__(self, other: Any) -> bool:
        """Expands on equals comparison to include comparing the version number.

        Args:
            other: The object to compare to this object.

        Returns:
            True if the other object or version number is equivalent.
        """
        return super().__eq__(other)
