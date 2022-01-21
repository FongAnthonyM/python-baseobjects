#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" types_.py
Several custom types used in this package.
"""
# Package Header #
from .__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Default Libraries #
from collections.abc import Callable
from typing import Any

# Downloaded Libraries #

# Local Libraries #


# Definitions #
# Types #
# Callables
AnyCallable = Callable[..., Any]

# Objects
GetObjectMethod = Callable[[Any, Any, type[Any] | None, ...], "BaseMethod"]

# Getters, Setters, and Deletes
GetterMethod = Callable[Any, Any]
SetterMethod = Callable[[Any, str], None]
DeleteMethod = Callable[Any, None]
PropertyCallbacks = tuple[GetterMethod, SetterMethod, DeleteMethod]
