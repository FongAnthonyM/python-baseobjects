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
import pickle

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.objects import StaticWrapper, DynamicWrapper
from .test_bases import BaseBaseObjectTest


# Definitions #
# Classes #
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
