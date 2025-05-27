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
from .basecomposite import BaseComposite
from .basecomponent import BaseComponent
from .basedispatchingcomposite import BaseDispatchingComposite
from .dispatchablecomposite import DispatchableComposite
