"""basedict.py
An abstract class that is a mixin of UserDict and BaseObject.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from collections import UserDict
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class BaseDict(BaseObject, UserDict):
    """An abstract class that is a mixin of UserDict and BaseObject."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict: Any = None, /, *args: Any, **kwargs: Any) -> None:
        # Parent Initialization #
        super().__init__(*args, **kwargs)
        UserDict.__init__(self, dict, **kwargs)
