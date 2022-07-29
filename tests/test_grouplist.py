#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" test_groupedlist.py
Tests for the GroupedList.
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
from src.baseobjects.collections import GroupedList
from .test_bases import ClassTest


# Definitions #
# Classes #
class TestGroupedList(ClassTest):
    class_ = GroupedList
    zero_time = datetime.timedelta(0)

    @pytest.mark.parametrize("items", ([1, 2, 3], (1, 2, 3)))
    def test_instance_creation(self, items):
        assert GroupedList(items=items)

    def test_create_group(self):
        gl = GroupedList()
        gl.create_group("name", [1])
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_require_group_create(self):
        gl = GroupedList()
        gl.require_group("name")
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_require_group_retrieve(self):
        gl = GroupedList()
        group_1 = gl.create_group("name")
        group_2 = gl.require_group("name")
        assert group_1 is group_2

    def test_add_group(self):
        gl = GroupedList()
        gl.add_group(GroupedList([1]), "name")
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_remove_group(self):
        gl = GroupedList()
        group_1 = gl.create_group("name", [1])
        gl.remove_group("name")
        assert len(gl) == 0

    def test_remove_group_object(self):
        gl = GroupedList()
        group_1 = gl.create_group("name", [1])
        gl.remove_group(group_1)
        assert len(gl) == 0

    def test_check_if_child(self):
        gl = GroupedList([0, 1, 2, 3])
        child = gl.create_group("name", [4, 5, 6])
        assert gl.check_if_child(child)

    def test_check_if_parent(self):
        gl = GroupedList([0, 1, 2, 3])
        child = gl.create_group("name", [4, 5, 6])
        assert child.check_if_parent(gl)

    def test_add_parent_to_children(self,):
        gl = GroupedList([0, 1, 2, 3])
        first = gl.create_group("first", [4, 5, 6])
        second = gl.create_group("second", [7, 8, 9, 10])
        new = GroupedList([-1])
        gl.add_parent_to_children(new)
        assert first.check_if_parent(new) and second.check_if_parent(new)

    def test_remove_parent_from_children(self,):
        gl = GroupedList([0, 1, 2, 3])
        first = gl.create_group("first", [4, 5, 6])
        second = gl.create_group("second", [7, 8, 9, 10])
        new = GroupedList([-1])
        gl.add_parent_to_children(new)
        gl.remove_parent_from_children(new)
        assert not first.check_if_parent(new) and not second.check_if_parent(new)

    def test_lengths(self):
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.get_group_lengths() == (4, (3, 7))

    def test_lengths_recurse(self):
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.get_group_lengths(recurse=True) == (4, ((3, ()), (4, ((3, ()),))))

    def test_len(self):
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("name", [4, 5, 6])
        assert len(gl) == 7

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_get_item(self, index: int):
        answer = tuple(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        assert gl[index] == answer[index]

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_set_item(self, index):
        answer = list(range(15))
        answer[index] = 0
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        gl[index] = 0
        assert gl == answer

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_set_item(self, index):
        answer = list(range(15))
        del answer[index]
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        del gl[index]
        assert gl == answer

    def test_append(self):
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        assert gl == answer

    def test_append_group_name(self):
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14, "second")
        assert gl == answer

    def test_as_flat_list(self):
        answer = list(range(14))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.as_flat_list() == answer

    def test_as_flat_tuple(self):
        answer = tuple(range(14))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.as_flat_tuple() == answer

    def test_copy(self):
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        gl_2 = gl.copy()
        assert gl_2 == answer


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
