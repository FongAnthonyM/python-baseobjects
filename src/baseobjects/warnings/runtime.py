"""runtime.py
Adds additional runtime Warnings.
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
