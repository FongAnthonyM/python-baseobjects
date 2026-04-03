"""__init__.py
Test suites for the baseobjects package.

Contains test suites for the baseobjects package. It provides a structured testing framework to ensure the functionality
and reliability of the baseobjects components and is a basis for creating tests for hierarchies of components.
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
from .bases import *
from .cachingtools import *
from .classregistration import *
from .collections import *
from .composition import *
from .functions import *
from .objects import *
from .state import *
from .versioning import *
from .wrappers import *

__all__ = [
    "AutomaticPropertiesTestSuite",
    "BaseCallableTestSuite",
    "BaseClassRegistryTestSuite",
    "BaseClassTestSuite",
    "BaseComponentTestSuite",
    "BaseCompositeTestSuite",
    "BaseDecoratorTestSuite",
    "BaseDictTestSuite",
    "BaseDispatchingCompositeTestSuite",
    "BaseFunctionTestSuite",
    "BaseIOModeObjectTestSuite",
    "BaseListTestSuite",
    "BaseMethodRegistryTestSuite",
    "BaseMethodTestSuite",
    "BaseObjectTestSuite",
    "BasePerformanceTestSuite",
    "BaseReducibleTestSuite",
    "BaseRegisteredClassTestSuite",
    "BaseTestSuite",
    "BaseTimedCacheCallableTestSuite",
    "BoundMethodRegistryTestSuite",
    "CachingObjectTestSuite",
    "CallableMultiplexerTestObject",
    "CallableMultiplexerTestSuite",
    "CallbackManagerTestSuite",
    "CallbackSchedulerTestSuite",
    "CircularDoublyLinkedContainerTestSuite",
    "ConcreteBindTarget",
    "DeepChainMapTestSuite",
    "DispatchableClassTestSuite",
    "DispatchableCompositeTestSuite",
    "DynamicCallableTestSuite",
    "DynamicDecoratorTestSuite",
    "DynamicFunctionTestSuite",
    "DynamicMethodTestSuite",
    "DynamicWrapperTestSuite",
    "FunctionMultiplexerTestSuite",
    "FunctionRegistryTestSuite",
    "GroupedListTestSuite",
    "LinkedNodeTestSuite",
    "MethodMultiplexerTestSuite",
    "MethodRegistryTestSuite",
    "NamespaceClassRegistryTestSuite",
    "NamespaceRegisteredClassTestSuite",
    "OrderableDictTestSuite",
    "SentinelObjectTestSuite",
    "SingleKwargDispatchTestSuite",
    "StateRestrictionTestSuite",
    "StaticWrapperTestSuite",
    "StatsMicro",
    "TimedCacheTestSuite",
    "TimedDictTestSuite",
    "TimedKeylessCacheTestSuite",
    "TimedLRUCacheTestSuite",
    "TimedSingleCacheTestSuite",
    "TriNumberVersionTestSuite",
    "VersionTestSuite",
    "WrapperPerformanceTestSuite",
    "WrapperTestSuite",
]
