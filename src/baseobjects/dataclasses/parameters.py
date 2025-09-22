"""parameters.py
A dataclass (NamedTuple) that holds parameters for any function.
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
from collections.abc import Iterable, Mapping
from typing import Any, NamedTuple

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class Parameters(NamedTuple):
    """A named tuple for holding the parameters of a function."""

    # Attributes #
    args: Iterable[Any] = tuple()
    kwargs: Mapping[str, Any] = dict()
