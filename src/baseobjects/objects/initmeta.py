#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" initmeta.py
InitMeta is an abstract metaclass that implements an init class method which allows some setup after a class is created.
"""
# Package Header #
from .. import __header__ as package_header

# Header #
__package__ = package_header.__package__

__author__ = package_header.__author__
__credits__ = package_header.__credits__
__maintainer__ = package_header.__maintainer__
__email__ = package_header.__email__

__copyright__ = package_header.__copyright__
__license__ = package_header.__license__

__version__ = package_header.__version__
__status__ = package_header.__status__

# Default Libraries #

# Downloaded Libraries #

# Local Libraries #
from ..basemeta import BaseMeta


# Definitions #
# Meta Classes #
class InitMeta(BaseMeta):
    """An abstract metaclass that implements an init class method which allows some setup after a class is created."""

    # Magic Methods
    # Construction/Destruction
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        cls._init_class_()
        return cls
