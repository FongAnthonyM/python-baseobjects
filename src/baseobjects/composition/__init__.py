"""__init__.py
The composition package provides classes for implementing the Composite design pattern.

This package includes classes for creating composite objects (BaseComposite, BaseDispatchingComposite,
DispatchableComposite) and component objects (BaseComponent) that can be used together to build complex object
hierarchies. The Composite pattern allows clients to treat individual objects and compositions of objects uniformly.
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
from .basecomponent import BaseComponent
from .basecomposite import BaseComposite
from .basedispatchingcomposite import BaseDispatchingComposite
from .compositefactoryclass import CompositeFactoryClass
from .dispatchablecomposite import DispatchableComposite

__all__ = [
    "BaseComponent",
    "BaseComposite",
    "BaseDispatchingComposite",
    "CompositeFactoryClass",
    "DispatchableComposite",
]
