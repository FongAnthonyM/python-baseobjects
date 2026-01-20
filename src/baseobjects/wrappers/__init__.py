"""__init__.py
Abstract classes for objects that can wrap any objects and make their attributes/functions accessible from the wrapper.

StaticWrapper and DynamicWrapper are solutions for two different case. StaticWrapper should be used when
if the application is within the limitations StaticWrapper. DynamicWrapper would be used if the application involves
wrapping various indeterminate object types and/or if the objects change available attributes/functions frequently.

Here are some tested relative performance metrics to highlight those differences: let normal attribute access be 1, when
StaticWrapper accesses a wrapped attribute it takes about 1.7 while DynamicWrapper takes about 4.4. StaticWrapper's
performance loss is debatable depending on the application, but DynamicWrapper takes about x4 longer a normal attribute
access which is not great for most applications.

Todo: add magic method support for StaticWrapper and DynamicWrapper (requires thorough method resolution handling)
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Local Packages #
from .dynamicwrapper import DynamicWrapper

# Imports
from .staticwrapper import StaticWrapper

__all__ = ["DynamicWrapper", "StaticWrapper"]
