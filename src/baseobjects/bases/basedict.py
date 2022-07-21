""" basedict.py

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
from collections import UserDict

# Third-Party Packages #

# Local Packages #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseDict(UserDict, BaseObject):
    """An abstract class that is a mixin of UserDict and BaseObject.

    Args:
        dict_: The dictionary to copy into this dictionary.
        **kwargs: The keywords to add to this dictionary.
    """
