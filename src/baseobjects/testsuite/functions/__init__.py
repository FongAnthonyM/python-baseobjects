"""__init__.py
Functions test suite package.
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
from .basedecoratortestsuite import BaseDecoratorTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite
from .dynamicdecoratortestsuite import DynamicDecoratorTestSuite
from .dynamicfunctiontestsuite import DynamicFunctionTestSuite
from .dynamicmethodtestsuite import DynamicMethodTestSuite
