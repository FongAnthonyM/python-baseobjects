#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" __init__.py
baseobjects provides several base classes.
"""
# Header #
from . import __header__ as package_header

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
from .baseobject import BaseObject
from .basemeta import BaseMeta
from .objects import *
from .warnings import TimeoutWarning
