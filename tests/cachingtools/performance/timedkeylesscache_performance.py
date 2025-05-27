#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedkeylesscache_performance.py
Performance tests for the timedkeylesscache module in the baseobjects package.
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
from src.baseobjects.cachingtools.caches.timedkeylesscache import TimedKeylessCache
from tests.cachingtools.performance.performance_basetimedcache import BaseCachePerformanceTest


# Definitions #
# Classes #
class TestTimedKeylessCache(BaseCachePerformanceTest):
    """Performance tests for the TimedKeylessCache class.

    This class tests the performance of the TimedKeylessCache class.
    """
    speed_tolerance = 2000
    class_ = TimedKeylessCache


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
