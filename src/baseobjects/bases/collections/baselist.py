"""baselist.py
BaseList is an abstract class that combines UserList and BaseObject functionality.

This module provides the BaseList class, which is an abstract base class that inherits from both BaseObject and
UserList. It combines the list-like behavior of UserList with the enhanced functionality of BaseObject, such as proper
copying and deep copying support.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class BaseList(BaseObject, UserList):
    """An abstract class that combines UserList and BaseObject functionality.

    Attributes:
        data: The underlying list that stores the elements. This is inherited from UserList and is used to implement all
            list operations.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, initlist: Any = None, *args: Any, **kwargs: Any) -> None:
        """Initialize a new BaseList instance.

        This constructor initializes both the BaseObject and UserList parent classes. It accepts an optional iterable
        object to initialize the contents, as well as arbitrary positional and keyword arguments that are passed to the
        BaseObject constructor.

        Args:
            initlist: An optional iterable object to initialize the contents of this list. If provided, all elements
                from this iterable will be added to the new BaseList.
            *args: Positional arguments passed to the BaseObject constructor.
            **kwargs: Keyword arguments passed to the BaseObject constructor.
        """
        # Parent Initialization #
        super().__init__(*args, **kwargs)
        UserList.__init__(self, initlist)
