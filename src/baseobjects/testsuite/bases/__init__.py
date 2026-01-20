"""__init__.py
Provides base classes for creating test suite classes.

This module serves as an initialization file for the testsuite.bases package, which provides base classes for
creating test suites. It imports and exposes classes like BaseTestSuite, BaseClassTestSuite, and
BasePerformanceTestSuite, making them available for direct import from the testsuite.bases package. These base
classes provide common functionality and structure for testing different components of the baseobjects package.
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
from .basecallabletestsuite import (
    BaseCallableTestSuite,
    ConcreteBindTarget,
    concrete_coroutine,
    concrete_coroutine_method,
    concrete_function,
    concrete_method,
)
from .baseclasstestsuite import BaseClassTestSuite
from .basedicttestsuite import BaseDictTestSuite
from .basefunctiontestsuite import BaseFunctionTestSuite
from .baselisttestsuite import BaseListTestSuite
from .basemethodtestsuite import BaseMethodTestSuite
from .baseobjecttestsuite import BaseObjectTestSuite
from .baseperformancetestsuite import BasePerformanceTestSuite, StatsMicro
from .basereducibletestsuite import BaseReducibleTestSuite
from .basetestsuite import BaseTestSuite
from .sentinelobjecttestsuite import SentinelObjectTestSuite

__all__ = [
    "BaseCallableTestSuite",
    "BaseClassTestSuite",
    "BaseDictTestSuite",
    "BaseFunctionTestSuite",
    "BaseListTestSuite",
    "BaseMethodTestSuite",
    "BaseObjectTestSuite",
    "BasePerformanceTestSuite",
    "BaseReducibleTestSuite",
    "BaseTestSuite",
    "ConcreteBindTarget",
    "SentinelObjectTestSuite",
    "StatsMicro",
    "concrete_coroutine",
    "concrete_coroutine_method",
    "concrete_function",
    "concrete_method",
]
