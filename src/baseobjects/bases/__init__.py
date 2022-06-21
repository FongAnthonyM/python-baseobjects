""" __init__.py
bases provides several base classes.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Local Packages #
from .baseobject import BaseObject, search_sentinel
from .basemeta import BaseMeta
from .basemethod import BaseMethod
from .basedecorator import BaseDecorator
from .singlekwargdispatchmethod import singlekwargdispatchmethod
