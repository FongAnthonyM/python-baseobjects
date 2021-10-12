#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachingobject.py
An abstract class which creates properties for this class automatically.
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
from ..baseobject import BaseObject
from .caches import TimedLRUCache


# Definitions #
# Classes #
class CachingObject(BaseObject):
    """An abstract class which is has functionality for methods that are caching.

    Attributes:
        is_cache: Determines if the caching methods of this object will cache.
    """

    # Magic Methods
    # Construction/Destruction
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        for name, attribute in cls.__dict__.items():
            if isinstance(attribute, TimedLRUCache):
                attribute.bind_to_deepcopy(instance, name)
        return instance

    def __init__(self):
        self.is_cache = True

