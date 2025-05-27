"""baselist.py
An abstract class that is a mixin of UserList and BaseObject.
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
from collections import UserList
from collections.abc import Iterable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class BaseList(BaseObject, UserList):
    """An abstract class that is a mixin of UserList and BaseObject."""

    __slots__: str | Iterable[str] = {"data"}

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Parent Initialization #
        super().__init__(*args, **kwargs)
        UserList.__init__(self)
