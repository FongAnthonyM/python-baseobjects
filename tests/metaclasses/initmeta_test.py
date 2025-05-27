#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta_test.py
Tests for the InitMeta class in the baseobjects package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.metaclasses import InitMeta
from tests.bases.base_test import BaseBaseMetaTest


# Definitions #
# Classes #
class TestInitMeta(BaseBaseMetaTest):
    """Test the InitMeta class.

    This class tests the functionality of the InitMeta metaclass, which implements an init class method
    that allows some setup after a class is created.
    """
    # Class Definitions #
    class TestClass(metaclass=InitMeta):
        """A test class that uses the InitMeta metaclass."""
        init_called = False
        init_args = None
        init_kwargs = None

        @classmethod
        def _init_class_(cls, name=None, bases=None, namespace=None, **kwargs):
            """Record that _init_class_ was called and store the arguments."""
            cls.init_called = True
            cls.init_args = (name, bases, namespace)
            cls.init_kwargs = kwargs

    # Attributes #
    class_: Type[InitMeta] = InitMeta

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the InitMeta class can be created."""
        assert self.class_ is not None
        assert issubclass(self.class_, type)

    def test_init_class_method_called(self) -> None:
        """Test that the _init_class_ method is called when a class is created with InitMeta."""
        # The TestClass should have had _init_class_ called during its creation
        assert self.TestClass.init_called is True
        
        # Check that the arguments were passed correctly
        name, bases, namespace = self.TestClass.init_args
        assert name == "TestClass"
        assert isinstance(bases, tuple)
        assert isinstance(namespace, dict)

    def test_init_class_method_with_custom_args(self) -> None:
        """Test that the _init_class_ method can be called with custom arguments."""
        # Create a new class with custom arguments
        class CustomArgsClass(metaclass=InitMeta):
            init_called = False
            init_args = None
            init_kwargs = None

            @classmethod
            def _init_class_(cls, name=None, bases=None, namespace=None, **kwargs):
                cls.init_called = True
                cls.init_args = (name, bases, namespace)
                cls.init_kwargs = kwargs

        # Call _init_class_ with custom arguments
        CustomArgsClass._init_class_(custom_arg="test")
        
        # Check that the method was called and the custom argument was passed
        assert CustomArgsClass.init_called is True
        assert CustomArgsClass.init_kwargs.get("custom_arg") == "test"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])