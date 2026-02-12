"""linkednode_test.py
Tests for the LinkedNode class in the baseobjects package.

This module provides tests for the LinkedNode class, which is a node in a circular doubly linked container. It tests the
functionality of LinkedNode including its properties, construction, and methods.
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
from baseobjects.collections.circulardoublylinkedcontainer import LinkedNode
from baseobjects.testsuite.collections import LinkedNodeTestSuite


# Definitions #
# Tests #
class TestLinkedNode(LinkedNodeTestSuite):
    """Test the LinkedNode class.

    This class tests the functionality of the LinkedNode class, which is a node in a circular doubly linked container.
    """

    # Attributes #
    UnitTestClass: type[LinkedNode] = LinkedNode


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
