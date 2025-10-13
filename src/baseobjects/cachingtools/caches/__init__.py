"""__init__.py
Caching tools.

This module serves as an initialization file for the caches subpackage, which provides various implementations of
time-based caches. It imports and exposes classes like BaseTimedCache, TimedSingleCache, TimedKeylessCache,
TimedCache, and TimedLRUCache, making them available for direct import from the caches subpackage. These caches
offer different strategies for storing and managing cached data with automatic expiration.
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
from .basetimedcache import BaseTimedCache, BaseTimedCacheCallable, BaseTimedCacheMethod
from .timedcache import TimedCache, timed_cache
from .timedkeylesscache import TimedKeylessCache, timed_keyless_cache
from .timedlrucache import TimedLRUCache, timed_lru_cache
from .timedsinglecache import TimedSingleCache, timed_single_cache
