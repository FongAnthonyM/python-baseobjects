"""__init__.py
Functions test suite package.

This module contains the functions test suite package.
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
from .callablemultiplexertestsuite import (
    CallableMultiplexerTestObject,
    CallableMultiplexerTestSuite,
    add_function,
    multiply_function,
)
from .dynamiccallabletestsuite import DynamicCallableTestSuite
from .dynamicdecoratortestsuite import DynamicDecoratorTestSuite
from .dynamicfunctiontestsuite import DynamicFunctionTestSuite
from .dynamicmethodtestsuite import DynamicMethodTestSuite
from .functionmultiplexertestsuite import FunctionMultiplexerTestSuite
from .functionregistrytestsuite import FunctionRegistryTestSuite
from .methodmultiplexertestsuite import MethodMultiplexerTestSuite
from .methodregistrytestsuite import (
    BaseMethodRegistryTestSuite,
    BoundMethodRegistryTestSuite,
    MethodRegistryTestSuite,
)
from .singlekwargdispatchtestsuite import SingleKwargDispatchTestSuite

__all__ = [
    "BaseDecoratorTestSuite",
    "BaseMethodRegistryTestSuite",
    "BoundMethodRegistryTestSuite",
    "CallableMultiplexerTestObject",
    "CallableMultiplexerTestSuite",
    "DynamicCallableTestSuite",
    "DynamicDecoratorTestSuite",
    "DynamicFunctionTestSuite",
    "DynamicMethodTestSuite",
    "FunctionMultiplexerTestSuite",
    "FunctionRegistryTestSuite",
    "MethodMultiplexerTestSuite",
    "MethodRegistryTestSuite",
    "SingleKwargDispatchTestSuite",
    "add_function",
    "multiply_function",
]
