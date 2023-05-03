#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_baseobjects.py
Test for the baseobjects package.
"""
# Package Header #
from src.baseobjects.header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import datetime
import pickle
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

        @timed_keyless_cache(lifetime=2, call_method="clearing_call", local=True)
        def get_proxy(self):
            return datetime.datetime.now()

        def normal(self):
            return datetime.datetime.now()

        def printer(self):
            print(self.a)

    def test_pickling(self):
        cacher = TestCachingObject.CachingTestObject()

        pickle_jar = pickle.dumps(cacher)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(cacher))

    def test_lru_cache(self):
        @timed_lru_cache(lifetime=2)
        def add_one(number=0):
            time.sleep(1)
            return number + 1

        first = add_one(number=1)

        s_time = time.perf_counter()
        second = add_one(number=1)
        t_time = time.perf_counter() - s_time

        assert first == second == 2
        assert t_time < 1

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

        assert second == first
        assert third > first

    def test_object_cache_reset(self):
        cacher = TestCachingObject.CachingTestObject()

        first = cacher.proxy
        time.sleep(1)
        second = cacher.get_proxy()
        time.sleep(1)
        third = cacher.proxy

        assert second > first
        assert third == second

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
