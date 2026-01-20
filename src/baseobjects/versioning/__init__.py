"""__init__.py
A package for version management and comparison.

This package provides classes for handling version numbers in various formats. It includes an abstract base class for
versions and implementations for specific version formats like three-number versioning (major.minor.patch).
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
from .trinumberversion import TriNumberVersion
from .version import Version

__all__ = ["TriNumberVersion", "Version"]
