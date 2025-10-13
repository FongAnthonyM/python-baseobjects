"""__init__.py
Specialized containers
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
from .circulardoublylinkedcontainer import CircularDoublyLinkedContainer, LinkedNode
from .deepchainmap import DeepChainMap
from .groupedlist import GroupedList
from .orderabledict import OrderableDict
from .timeddict import TimedDict
