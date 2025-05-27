#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedsinglecache_performance.py
Performance tests for the timedsinglecache module in the baseobjects package.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools.caches.timedsinglecache import TimedSingleCache
from tests.cachingtools.performance.performance_basetimedcache import BaseCachePerformanceTest


# Definitions #
# Classes #
class TestTimedSingleCache(BaseCachePerformanceTest):
    """Performance tests for the TimedSingleCache class.

    This class tests the performance of the TimedSingleCache class.
    """
    class_ = TimedSingleCache


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
