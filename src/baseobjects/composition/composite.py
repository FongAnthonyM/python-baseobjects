""" composite.py

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

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class Conposite(BaseObject):
    """

    Class Attributes:

    Attributes:

    Args:

    """

    __original_dir_set: set[str] | None = None
    _exclude_attributes: set[str] = {"__slotnames__"}
    _component_attributes: dict[str, set[str]] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, init=True):
        if init:
            self.construct()

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, ):
        pass

