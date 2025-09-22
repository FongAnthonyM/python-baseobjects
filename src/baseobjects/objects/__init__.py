"""__init__.py
More specific objects for the package.

This module serves as an initialization file for the objects package, which provides specialized object classes
with specific functionality. It imports and exposes classes like AutomaticProperties and CallbackManager,
making them available for direct import from the objects package.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports
# Local Packages #
from .automaticproperties import AutomaticProperties
from .callbackmanager import ConditionalCallbackEntry, CallbackScheduler, CallbackManager
