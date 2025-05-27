"""methodnames.py
Functions for getting method names from objects.
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
from collections.abc import Generator
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def iter_method_names(obj: Any) -> Generator[str, None, None]:
    """Creates an iterator which iterates over the method names of an object.

    Args:
        obj: The object to iterate the method names from.

    Returns:
        The iterator as a generator which iterates over the method names of an object.
    """
    return (name for name in dir(obj) if callable(getattr(obj, name, None)))


def iter_public_method_names(obj: Any) -> Generator[str, None, None]:
    """Creates an iterator which iterates over the public method names of an object.

    Args:
        obj: The object to iterate the public method names from.

    Returns:
        The iterator as a generator which iterates over the public method names of an object.
    """
    return (name for name in iter_method_names(obj) if name[0] != '_')


def get_method_names(obj: Any) -> tuple[str, ...]:
    """Gets the method names of an object.

    Args:
        obj: The object to get the method names from.

    Returns:
        The method names of an object.
    """
    return tuple(iter_method_names(obj))


def get_public_method_names(obj: Any) -> tuple[str, ...]:
    """Gets the public method names of an object.

    Args:
        obj: The object to get the public method names from.

    Returns:
        The public method names of an object.
    """
    return tuple(iter_public_method_names(obj))


