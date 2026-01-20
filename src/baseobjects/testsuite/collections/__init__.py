"""__init__.py
Test suites for collections.
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
from .circulardoublylinkedcontainertestsuite import CircularDoublyLinkedContainerTestSuite
from .deepchainmaptestsuite import DeepChainMapTestSuite
from .groupedlisttestsuite import GroupedListTestSuite
from .linkednodetestsuite import LinkedNodeTestSuite
from .orderabledicttestsuite import OrderableDictTestSuite
from .timeddicttestsuite import TimedDictTestSuite

__all__ = [
    "CircularDoublyLinkedContainerTestSuite",
    "DeepChainMapTestSuite",
    "GroupedListTestSuite",
    "LinkedNodeTestSuite",
    "OrderableDictTestSuite",
    "TimedDictTestSuite",
]
