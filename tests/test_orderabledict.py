#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_orderabledict.py
Tests for the OrderableDict.
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

import time


# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import OrderableDict
from .test_bases import ClassTest


# Definitions #
# Classes #
class TestGroupedList(ClassTest):
    class_ = OrderableDict
    zero_time = datetime.timedelta(0)

    @pytest.mark.parametrize("items", ({"a": 1, "b": 2, "c": 3}, {"c": 3, "b": 2, "a": 1}))
    def test_instance_creation(self, items):
        assert OrderableDict(items)

    def test_list(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od) == ["c", "b", "a"]

    def test_keys(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.keys()) == ["c", "b", "a"]

    def test_values(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.values()) == [3, 2, 1]

    def test_items(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.items()) == [("c", 3), ("b", 2), ("a", 1)]

    def test_clear(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.clear()
        assert not od.data
        assert not od.order

    def test_pop(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        value = od.pop("b")
        assert value == 2
        assert list(od.data.keys()) == ["a", "c"]
        assert od.order == ["a", "c"]

    def test_popitem(self):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        item = od.popitem()
        assert item == ("c", 3)
        assert list(od.data.keys()) == ["a", "b"]
        assert od.order == ["a", "b"]

    @pytest.mark.parametrize("param", ({"d": 4, "e": 5}, (("d", 4), ("e", 5))))
    def test_update(self, param):
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.update(param)
        assert list(od.data.keys()) == ["a", "b", "c", "d", "e"]
        assert od.order == ["a", "b", "c", "d", "e"]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
