#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemeta_test.py
Tests for the BaseMeta class in the baseobjects package.
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

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseMeta
from .base_test import BaseBaseMetaTest


# Classes #
class TestBaseMeta(BaseBaseMetaTest):
    """Test the BaseMeta class.

    This class tests the functionality of the BaseMeta metaclass, which is the base metaclass for all classes in the
    baseobjects package.
    """


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])