"""__init__.py
bases provides several base classes.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .sentinelobject import SentinelObject, DEFAULTSENTINEL, SEARCHSENTINEL, search_sentinel
from .baseobject import BaseObject
from .basereducible import BaseReducible
from .basemeta import BaseMeta
from .basecallable import BaseCallable, BaseMethod, BaseFunction
from .collections import *
