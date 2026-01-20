"""__init__.py
Caching tools.

This module serves as an initialization file for the cachingtools package, which provides tools for implementing
caching functionality in Python objects. It imports and exposes classes like CachingObject and various cache
implementations from the caches subpackage, making them available for direct import from the cachingtools package.
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
from .caches import *
from .cachingobject import CachingObject

__all__ = [
    "BaseTimedCache",
    "BaseTimedCacheCallable",
    "BaseTimedCacheMethod",
    "CachingObject",
    "TimedCache",
    "TimedKeylessCache",
    "TimedLRUCache",
    "TimedSingleCache",
    "timed_cache",
    "timed_keyless_cache",
    "timed_lru_cache",
    "timed_single_cache",
]
