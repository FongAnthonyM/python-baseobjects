"""__init__.py
Provides test suite classes for composition.
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
from .basecomponenttestsuite import BaseComponentTestSuite
from .basecompositetestsuite import BaseCompositeTestSuite
from .basedispatchingcompositetestsuite import BaseDispatchingCompositeTestSuite
from .dispatchablecompositetestsuite import DispatchableCompositeTestSuite

__all__ = [
    "BaseComponentTestSuite",
    "BaseCompositeTestSuite",
    "BaseDispatchingCompositeTestSuite",
    "DispatchableCompositeTestSuite",
]
