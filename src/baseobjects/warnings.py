#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" warnings.py
Adds additional Warnings.
"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.2.0"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Prototype"

# Default Libraries #

# Downloaded Libraries #

# Local Libraries #


# Definitions #
# Classes #
class TimeoutWarning(Warning):
    """A general warning for timeouts."""
    def __init__(self, name="A function"):
        message = f"{name} timed out"
        super().__init__(message)