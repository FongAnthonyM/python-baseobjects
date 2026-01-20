"""__init__.py
Metaclass utilities for class construction and initialization.

This package contains metaclass helpers used by baseobjects to customize class creation and provide class-level
initialization hooks.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports
# Local Packages #
from .initmeta import InitMeta

# Main #
__all__ = ["InitMeta"]
