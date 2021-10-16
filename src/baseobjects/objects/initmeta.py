#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
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


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created."""

    # Magic Methods #
    # Construction/Destruction
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls._init_class_()
        return cls
