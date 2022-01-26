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
import timeit

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects import StaticWrapper, DynamicWrapper
from .bases_performance import ClassPerformanceTest


# Definitions #
# Classes #
class BaseWrapperTest(ClassPerformanceTest):
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

    @pytest.fixture(params=[new_object])
    def test_object(self, request):
        return request.param(self)

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
    class StaticWrapperTestObject1(StaticWrapper):
        _wrapped_types = [BaseWrapperTest.ExampleOne(), BaseWrapperTest.ExampleTwo()]
        _wrap_attributes = ["_first", "_second"]

        def __init__(self, first=None, second=None):
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self):
            return "wrapper"

    class StaticWrapperTestObject2(StaticWrapper):
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
    class DynamicWrapperTestObject(DynamicWrapper):
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
