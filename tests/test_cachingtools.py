#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package.
"""
# Package Header #
from src.baseobjects.__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import datetime

import time


# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.cachingtools import *
from .test_bases import ClassTest


# Definitions #
# Classes #
class TestCachingObject(ClassTest):
    class_ = CachingObject
    zero_time = datetime.timedelta(0)

    class CachingTestObject(CachingObject):
        def __init__(self, a=1, init=True):
            super().__init__()
            self.a = a

        @property
        def proxy(self):
            return self.get_proxy.caching_call()

        @timed_keyless_cache_method(lifetime=2, call_method="clearing_call", collective=False)
        def get_proxy(self):
            return datetime.datetime.now()

        def normal(self):
            return datetime.datetime.now()

        def printer(self):
            print(self.a)

    def test_lru_cache(self):
        @timed_lru_cache(lifetime=1)
        def add_one(number=0):
            return number + 1

        n = add_one(number=1)

        assert n == 2

    def test_lru_cache_original_func(self):
        @timed_lru_cache(lifetime=1)
        def add_one(number=0):
            return number + 1

        n = add_one.__func__(number=1)

        assert n == 2

    def test_object_timed_cache(self):
        cacher = TestCachingObject.CachingTestObject()

        first = cacher.proxy
        time.sleep(1)
        second = cacher.proxy
        time.sleep(2)
        third = cacher.proxy

        assert (second - first == self.zero_time) and (third - first != self.zero_time)

    def test_object_cache_reset(self):
        cacher = TestCachingObject.CachingTestObject()

        first = cacher.proxy
        second = cacher.get_proxy()
        third = cacher.proxy

        assert (second - first != self.zero_time) and (third - second == self.zero_time)

    def test_object_cache_instances(self):
        cacher = TestCachingObject.CachingTestObject()
        cacher2 = TestCachingObject.CachingTestObject()

        first = cacher.proxy
        _ = cacher.proxy
        time.sleep(1)
        second = cacher2.proxy

        assert second - first != self.zero_time


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
