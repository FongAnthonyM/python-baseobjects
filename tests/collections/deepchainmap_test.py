"""deepchainmap_test.py
Tests for the DeepChainMap class in the baseobjects package.

This module provides tests for the DeepChainMap class, which is a ChainMap that updates and deletes items from the first
mapping that contains the key.
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
from typing import ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.collections import DeepChainMap
from baseobjects.testsuite.collections import DeepChainMapTestSuite


# Definitions #
# Tests #
class TestDeepChainMap(DeepChainMapTestSuite):
    """Test the DeepChainMap class.

    This class tests the functionality of the DeepChainMap class, which is a ChainMap that updates and deletes items
    from the first mapping that contains the key.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[DeepChainMap]] = DeepChainMap


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
