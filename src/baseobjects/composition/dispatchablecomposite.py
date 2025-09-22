"""dispatchablecomposite.py
A composite object that can dispatch component objects during instantiation and can dispatch itself to the correct subclass.

This module provides the DispatchableComposite class which combines the functionality of BaseDispatchingComposite and
DispatchableClass. It allows for dynamic class selection and component construction, serving as a foundation for creating
complex composite objects.
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

# Third-Party Packages #

# Local Packages #
from ..classregistration import DispatchableClass
from .basedispatchingcomposite import BaseDispatchingComposite


# Definitions #
# Classes #
class DispatchableComposite(BaseDispatchingComposite, DispatchableClass):
    """A composite object that combines component dispatching and class dispatching capabilities.

    This class combines the functionality of BaseDispatchingComposite and DispatchableClass, allowing it to dispatch
    component objects during instantiation and to dispatch itself to the correct subclass based on the given input. It
    serves as a foundation for creating complex composite objects that need dynamic class selection and component
    construction.

    When instantiated, it first determines the appropriate subclass to use based on the input arguments (via
    DispatchableClass.__new__), then constructs the components as needed (via BaseDispatchingComposite's component
    handling).

    Attributes:
        component_types_registry: A registry of component classes and their keyword arguments.
        components: The components of this object.

    Args:
        *args: Positional arguments used for class dispatching and component construction.
        **kwargs: Keyword arguments used for class dispatching and component construction.
    """
