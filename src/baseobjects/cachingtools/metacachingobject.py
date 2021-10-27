#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" metacachingobject.py
Creates a registry for the caching objects with a class.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Default Libraries #

# Downloaded Libraries #

# Local Libraries #
from ..basemeta import BaseMeta
from .basetimedcache import BaseTimedCache


# Definitions #
# Classes #
class MetaCachingObject(BaseMeta):
    """Automatically makes a set of all function that are Timed Caches in the class."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(cls, name, bases, attr):
        super().__init__(name, bases, attr)
        if hasattr(cls, "_caches_"):
            cls._caches_ = cls._caches_.copy()
        else:
            cls._caches_ = set()

        for name, cls_attribute in attr.items():
            if isinstance(cls_attribute, BaseTimedCache):
                cls._caches_.add(name)
