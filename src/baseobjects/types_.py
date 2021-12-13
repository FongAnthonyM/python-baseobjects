#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" types_.py
Types
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
from typing import Any, Callable, Tuple

# Downloaded Libraries #

# Local Libraries #


# Definitions #
# Types #
PropertyCallbacks = Tuple[Callable[[Any], Any], Callable[[Any, Any], None], Callable[[Any], None]]
