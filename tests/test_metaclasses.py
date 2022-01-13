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

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseObject
from src.baseobjects.metaclasses import *
from .test_bases import ClassTest


# Definitions #
# Classes #
class TestInitMeta(ClassTest):
    class InitMetaTest(BaseObject, metaclass=InitMeta):
        one = 1

        @classmethod
        def _init_class_(cls, *args, **kwargs):
            cls.one = 2

    def test_init_class(self):
        assert self.InitMetaTest.one == 2

    def test_meta(self):
        obj = self.InitMetaTest()
        obj.copy()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
