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


# Base Function
class TestBaseFunction(BaseBaseObjectTest):
    class_ = BaseFunction

    @pytest.fixture
    def generic_function(self):
        def generic(*args, **kwargs):
            return True

        return generic()

    @pytest.fixture
    def generate_function(self, request=None):
        def generic(*args, **kwargs):
            return args[0]

        if request is None:
            return self.class_(func=generic)
        else:
            return self.class_(func=generic, get_function=request.param)

    def test_function_call(self, generate_function):
        assert generate_function(5) == 5

    def test_binding(self, generate_function):
        obj = BaseObject()
        method = generate_function.bind(instance=obj)
        assert method() == obj

    def test_binding_to_attribute(self, generate_function):
        obj = BaseObject()
        generate_function.bind_to_attribute(instance=obj)
        assert isinstance(obj.generic, BaseMethod)


# Base Method
class TestBaseMethod(BaseBaseObjectTest):
    class_ = BaseMethod

    @pytest.fixture
    def generic_function(self):
        def generic(*args, **kwargs):
            return True

        return generic()

    @pytest.fixture
    def generate_method(self, request=None):
        def generic(*args, **kwargs):
            return args[0]

        if request is None:
            return self.class_(func=generic, instance=self)
        else:
            return self.class_(func=generic, instance=self, get_method=request.param)

    def test_method_call(self, generate_method):
        assert self == generate_method()

    def test_binding(self, generate_method):
        obj = BaseObject()
        generate_method.bind(instance=obj)
        assert obj == generate_method()

    def test_binding_to_attribute(self, generate_method):
        obj = BaseObject()
        generate_method.bind_to_attribute(instance=obj)
        assert obj.generic == generate_method


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
