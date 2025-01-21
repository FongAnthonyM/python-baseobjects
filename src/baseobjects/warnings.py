"""warnings.py
Adds additional Warnings.
"""
# Package Header #
from .header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class NotImplementedWarning(RuntimeWarning):
    """A warning for when a method or function hasn't been implemented yet."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, name: str = "A method or function") -> None:
        message = f"{name} has not been implemented yet."
        super().__init__(message)


class TimeoutWarning(Warning):
    """A warning for timeouts."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, name: str = "A function") -> None:
        message = f"{name} timed out"
        super().__init__(message)
