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
# Default Libraries #
import abc
import copy
import cProfile
import datetime
import functools
import io
import pathlib
import pickle
import pstats
from pstats import Stats, f8, func_std_string
import time
import timeit

# Downloaded Libraries #
import pytest

# Local Libraries #
import src.baseobjects as baseobjects
from src.baseobjects.cachingtools import timed_lru_cache, timed_keyless_cache_method


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class StatsMicro(Stats):
    def print_stats(self, *amount):
        for filename in self.files:
            print(filename, file=self.stream)
        if self.files:
            print(file=self.stream)
        indent = ' ' * 8
        for func in self.top_level:
            print(indent, func_get_function_name(func), file=self.stream)

        print(indent, self.total_calls, "function calls", end=' ', file=self.stream)
        if self.total_calls != self.prim_calls:
            print("(%d primitive calls)" % self.prim_calls, end=' ', file=self.stream)
        print("in %.3f microseconds" % (self.total_tt*1000000), file=self.stream)
        print(file=self.stream)
        width, list = self.get_print_list(amount)
        if list:
            self.print_title()
            for func in list:
                self.print_line(func)
            print(file=self.stream)
            print(file=self.stream)
        return self

    def print_line(self, func):  # hack: should print percentages
        cc, nc, tt, ct, callers = self.stats[func]
        c = str(nc)
        if nc != cc:
            c = c + '/' + str(cc)
        print(c.rjust(9), end=' ', file=self.stream)
        print(f8(tt*1000000), end=' ', file=self.stream)
        if nc == 0:
            print(' '*8, end=' ', file=self.stream)
        else:
            print(f8(tt/nc*1000000), end=' ', file=self.stream)
        print(f8(ct*1000000), end=' ', file=self.stream)
        if cc == 0:
            print(' '*8, end=' ', file=self.stream)
        else:
            print(f8(ct/cc*1000000), end=' ', file=self.stream)
        print(func_std_string(func), file=self.stream)


class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""
    class_ = None
    timeit_runs = 100000
    speed_tolerance = 200

    def test_instance_creation(self):
        pass


class TestInitMeta(ClassTest):
    class InitMetaTest(baseobjects.BaseObject, metaclass=baseobjects.InitMeta):
        one = 1

        @classmethod
        def _init_class_(cls):
             cls.one = 2

    def test_init_class(self):
        assert self.InitMetaTest.one == 2

    def test_meta(self):
        obj = self.InitMetaTest()
        obj.copy()


class BaseBaseObjectTest(ClassTest):
    """All BaseObject subclasses need to pass these tests to considered functional."""
    pass


class TestBaseObject(BaseBaseObjectTest):
    """Test the BaseObject class which a subclass is created to test with."""
    class BaseTestObject(baseobjects.BaseObject):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class NormalObject(object):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class_ = BaseTestObject

    @pytest.fixture
    def test_object(self):
        return self.class_()

    def test_copy(self, test_object):
        new = test_object.copy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) == id(test_object.mutable)

    def test_deepcopy(self, test_object):
        new = test_object.deepcopy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) != id(test_object.mutable)

    def test_copy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_copy():
            copy.copy(normal)

        mean_new = timeit.timeit(test_object.copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_copy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_deepcopy_speed(self, test_object):
        normal = self.NormalObject()

        def normal_deepcopy():
            copy.deepcopy(normal)

        mean_new = timeit.timeit(test_object.deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(normal_deepcopy, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance


class BaseWrapperTest(BaseBaseObjectTest):
    class ExampleOne:
        def __init__(self):
            self.one = "one"
            self.two = "one"

        def __eq__(self, other):
            return True

        def method(self):
            return "one"

    class ExampleTwo:
        def __init__(self):
            self.one = "two"
            self.three = "two"

        def function(self):
            return "two"

    class NormalWrapper:
        def __init__(self, first):
            self._first = first
            self.four = "wrapper"

        @property
        def one(self):
            return self._first.one

    class_ = None

    def new_object(self):
        pass

    def pickle_object(self):
        obj = self.new_object()
        pickle_jar = pickle.dumps(obj)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(obj))

    @pytest.fixture(params=[new_object])
    def test_object(self, request):
        return request.param(self)

    def test_instance_creation(self):
        pass

    def test_pickling(self, test_object):
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(test_object))

    def test_copy(self, test_object):
        new = test_object.copy()
        assert id(new._first) == id(test_object._first)

    def test_deepcopy(self, test_object):
        new = test_object.deepcopy()
        assert id(new._first) != id(test_object._first)

    def test_wrapper_overrides(self, test_object):
        assert test_object.two == "wrapper"
        assert test_object.four == "wrapper"
        assert test_object.wrap() == "wrapper"

    def test_example_one_overrides(self, test_object):
        assert test_object.one == "one"
        assert test_object.method() == "one"

    def test_example_two_overrides(self, test_object):
        assert test_object.three == "two"
        assert test_object.function() == "two"

    def test_setting_wrapped(self, test_object):
        test_object.one = "set"
        assert test_object._first.one == "set"

    def test_deleting_wrapped(self, test_object):
        del test_object.one
        assert "one" not in dir(test_object._first)

    @pytest.mark.xfail
    def test_magic_inheritance(self, test_object):
        assert test_object == 1

    @pytest.mark.xfail
    def test_local_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "four")

        def old_access():
            getattr(normal, "four")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "one")

        def old_access():
            getattr(getattr(normal, "_first"), "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_property_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(normal, "one")

        def old_access():
            getattr(getattr(normal, "_first"), "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    @pytest.mark.xfail
    def test_vs_property_access_speed(self, test_object):
        normal = self.NormalWrapper(self.ExampleOne())

        def new_access():
            getattr(test_object, "one")

        def old_access():
            getattr(normal, "one")

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance


class TestStaticWrapper(BaseWrapperTest):
    class StaticWrapperTestObject1(baseobjects.StaticWrapper):
        _wrapped_types = [BaseWrapperTest.ExampleOne(), BaseWrapperTest.ExampleTwo()]
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self):
            return "wrapper"

    class StaticWrapperTestObject2(baseobjects.StaticWrapper):
        _set_next_wrapped = True
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self.two = "wrapper"
            self.four = "wrapper"
            self._first = first
            self._second = second
            self._wrap()

        def wrap(self):
            return "wrapper"

    class_ = StaticWrapperTestObject1

    def new_object_1(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject1(first, second)

    def new_object_2(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject2(first, second)

    @pytest.fixture(params=[new_object_1, new_object_2])
    def test_object(self, request):
        return request.param(self)


class TestDynamicWrapper(BaseWrapperTest):
    class DynamicWrapperTestObject(baseobjects.DynamicWrapper):
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self):
            return "wrapper"

    class_ = DynamicWrapperTestObject

    def new_object(self):
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.DynamicWrapperTestObject(first, second)

    @pytest.fixture(params=[new_object])
    def test_object(self, request):
        return request.param(self)


class TestCachingObject(ClassTest):
    class_ = baseobjects.CachingObject
    zero_time = datetime.timedelta(0)

    class CachingTestObject(baseobjects.CachingObject):
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

        n = add_one.func(number=1)

        assert n == 2

    def test_lru_cache_switch(self):
        @timed_lru_cache(lifetime=1)
        def add_one(number=0):
            return number + 1

        add_one.set_call(caching=False)

        n = add_one.func(number=1)

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

    def test_cache_bypass_speed(self):
        cacher = TestCachingObject.CachingTestObject()

        def new_access():
            cacher.get_proxy()

        def old_access():
            cacher.normal()

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_cached_speed(self):
        cacher = TestCachingObject.CachingTestObject()

        cacher.proxy

        def new_access():
            cacher.proxy

        def old_access():
            cacher.a

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_cached_profile(self):
        cacher = TestCachingObject.CachingTestObject()
        cacher.proxy

        pr = cProfile.Profile()
        pr.enable()

        cacher.proxy

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

    def test_functool_speed(self):
        x = 1

        @functools.lru_cache
        def proxy(a=None):
            return datetime.datetime.now()

        proxy()

        def new_access():
            proxy()

        def old_access():
            x

        mean_new = timeit.timeit(new_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        mean_old = timeit.timeit(old_access, number=self.timeit_runs) / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        print(f"\nNew speed {mean_new:.3f} μs took {percent:.3f}% of the time of the old function.")
        assert percent < self.speed_tolerance

    def test_functool_profile(self):
        @functools.lru_cache
        def proxy(a=None):
            return datetime.datetime.now()

        proxy()

        pr = cProfile.Profile()
        pr.enable()

        proxy()

        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.TIME
        ps = StatsMicro(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


# Main #
if __name__ == '__main__':
    pytest.main(["-v", "-s"])
