"""__init__.py
Classes for objects that have states and decorators for restricting state-dependent methods.

This package provides classes for objects that need to track their state and decorators that can be used to restrict
access to methods based on the object's current state.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2026, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .baseiomodeobject import BaseIOModeObject, asopen, asopenasync, staterestriction

__all__ = ["BaseIOModeObject", "asopen", "asopenasync", "staterestriction"]
