""" baselist.py
An abstract class that is a mixin of UserList and BaseObject.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections import UserList

# Third-Party Packages #

# Local Packages #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseList(UserList, BaseObject):
    """An abstract class that is a mixin of UserList and BaseObject."""
