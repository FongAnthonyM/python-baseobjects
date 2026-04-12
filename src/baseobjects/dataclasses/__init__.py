"""__init__.py
Base and/or common dataclasses.

This module contains the base and/or common dataclasses.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .parameters import Parameters

__all__ = [
    "Parameters",
]
