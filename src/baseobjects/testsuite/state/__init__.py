"""__init__.py
Test suites for the baseobjects state tools.

This module contains the test suites for the baseobjects state tools.
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
from .baseiomodeobjecttestsuite import *

__all__ = ["BaseIOModeObjectTestSuite", "StateRestrictionTestSuite"]
