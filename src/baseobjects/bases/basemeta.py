"""basemeta.py
BaseMeta is an abstract metaclass that implements fundamental functions for metaclass objects.

This module provides the BaseMeta class, which is an abstract metaclass that inherits from ABCMeta. It serves as a
foundation for other metaclasses in the baseobjects package.
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
from abc import ABCMeta


# Definitions #
# Classes #
class BaseMeta(ABCMeta):
    """An abstract metaclass that implements fundamental functions for metaclass objects.

    BaseMeta extends Python's ABCMeta (Abstract Base Class Metaclass) and is designed to be used as a metaclass for
    other classes, typically by specifying it in the class definition: `class MyClass(metaclass=BaseMeta): ...`
    """
