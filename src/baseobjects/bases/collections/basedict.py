"""basedict.py
BaseDict is an abstract class that combines UserDict and BaseObject functionality.

This module provides the BaseDict class, which is an abstract base class that inherits from both BaseObject and
UserDict. It combines the dictionary-like behavior of UserDict with the enhanced functionality of BaseObject, such as
proper copying and deep copying support.
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
    """An abstract class that combines UserDict and BaseObject functionality.

    Attributes:
        data: The underlying dictionary that stores the key-value pairs. This is inherited from UserDict and is used to
              implement all dictionary operations.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict: Any = None, /, *args: Any, **kwargs: Any) -> None:
        """Initialize a new BaseDict instance.

        This constructor initializes both the BaseObject and UserDict parent classes. It accepts an optional
        dictionary-like object to initialize the contents, as well as arbitrary positional and keyword arguments that
        are passed to the BaseObject constructor.

        Args:
            dict: An optional dictionary-like object to initialize the contents of this dictionary.
                If provided, all key-value pairs from this object will be added to the new BaseDict.
            *args: Positional arguments passed to the BaseObject constructor.
            **kwargs: Keyword arguments that can be used both by the UserDict constructor and the BaseObject
                constructor. If there are naming conflicts, the arguments will be used by UserDict.
        """
        # Parent Initialization #
        super().__init__(*args, **kwargs)
        UserDict.__init__(self, dict, **kwargs)
