"""__init__.py
Caching tools.
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
from .basetimedcache import BaseTimedCache
from .timedsinglecache import TimedSingleCache, timed_single_cache
from .timedkeylesscache import TimedKeylessCache, timed_keyless_cache
from .timedcache import TimedCache, timed_cache
from .timedlrucache import TimedLRUCache, timed_lru_cache
