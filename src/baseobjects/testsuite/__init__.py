"""__init__.py
testsuite provides test suite classes.

This module serves as an initialization file for the testsuite package, which provides various test suite classes
for testing baseobjects functionality. It imports and exposes classes from subpackages, making them available for
direct import from the testsuite package.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Source Packages #
# Imports #
from baseobjects.testsuite.cachingtools.cachingtoolstestsuite import TimedCacheTestSuite

# Local Packages #
from .bases import *
from .cachingtools import *
from .classregistration import *
from .functions import *
from .objects import *
from .versiontestsuite import VersionTestSuite
from .wrappers import *
