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
import abc
import pathlib

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import *


# Definitions #
# Functions #
@pytest.fixture
def tmp_dir(tmpdir):
    """A pytest fixture that turn the tmpdir into a Path object."""
    return pathlib.Path(tmpdir)


# Classes #
class ClassTest(abc.ABC):
    """Default class tests that all classes should pass."""

    class_ = None

    def test_instance_creation(self, *args, **kwargs):
        pass


# Base Meta
class BaseBaseMetaTest(ClassTest):
    """All BaseMeta subclasses need to pass these tests to considered functional."""

    pass


class TestBaseMeta(BaseBaseMetaTest):
    """Test the BaseObject class which a subclass is created to test with."""

    pass


# Base Object
class BaseBaseObjectTest(ClassTest):
    """All BaseObject subclasses need to pass these tests to considered functional."""

    pass


class TestBaseObject(BaseBaseObjectTest):
    """Test the BaseObject class which a subclass is created to test with."""

    # Create a test subclass
    class BaseTestObject(BaseObject):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    # Create a normal object to test against
    class NormalObject(object):
        def __init__(self):
            self.immutable = 0
            self.mutable = {}

    class_ = BaseTestObject

    @pytest.fixture
    def test_object(self):
        return self.class_()

    def test_instance_creation(self, test_object):
        assert test_object is not None

    def test_copy(self, test_object):
        new = test_object.copy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) == id(test_object.mutable)

    def test_deepcopy(self, test_object):
        new = test_object.deepcopy()
        assert id(new.immutable) == id(test_object.immutable)
        assert id(new.mutable) != id(test_object.mutable)


# Base Method
class TestBaseMethod(BaseBaseObjectTest):
    class_ = BaseMethod
    get_names = ["get_self", "get_self_bind", "get_new_bind", "get_subinstance"]

    @pytest.fixture
    def generic_function(self):
        def generic(*args, **kwargs):
            return True

        return generic()

    @pytest.fixture
    def test_method(self, request=None):
        def generic(*args, **kwargs):
            return args[0]

        if request is None:
            return self.class_(func=generic)
        else:
            return self.class_(func=generic, get_method=request.param)

    def test_method_function_call(self, test_method):
        assert test_method(True)

    @pytest.mark.parametrize("test_method", get_names, indirect=True)
    def test_binding(self, test_method):
        obj = BaseObject()
        test_method.bind(instance=obj)
        assert obj.generic == test_method

    @pytest.mark.parametrize("get_method", get_names)
    def test_set_get_method(self, test_method, get_method):
        test_method.set_get_method(get_method)
        assert getattr(test_method, get_method) == test_method._get_method

    @pytest.mark.parametrize("test_method", get_names, indirect=True)
    def test_(self, test_method):
        pass


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
