"""orderabledict.py
A dictionary with an adjustable order and additional supporting methods.
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
from collections import ChainMap
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from ..typing import KeyType, ValueType


# Definitions #
# Classes #
class DeepChainMap(BaseObject, ChainMap):

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Parent Attributes #
        super().__init__(*args, **kwargs)
        ChainMap.__init__(self, *args)

    # Container Methods
    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Sets an item in this object."""
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key: KeyType) -> None:
        """Deletes an item from this object."""
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

