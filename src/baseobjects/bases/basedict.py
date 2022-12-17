""" basedict.py
An abstract class that is a mixin of UserDict and BaseObject.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseDict(BaseObject, UserDict):
    """An abstract class that is a mixin of UserDict and BaseObject."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Parent Attributes #
        super().__init__(*args, **kwargs)
        UserDict.__init__(self)