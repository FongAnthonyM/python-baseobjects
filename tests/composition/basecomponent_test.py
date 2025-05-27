"""test_basecomponent.py
Tests for the BaseComponent class in the baseobjects.composition package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.composition import BaseComponent
from tests.composition.base_test import BaseComponentTest


# Definitions #
# Classes #
class TestBaseComponent(BaseComponentTest):
    """Test the BaseComponent class.

    This class tests the functionality of the BaseComponent class, which is the base class for all components in the
    composition pattern.
    """

    # Class Attributes #
    class_: Type[BaseComponent] = BaseComponent

    # Instance Methods #
    # Tests
    def test_initialization(self, test_component: BaseComponent) -> None:
        """Test that the BaseComponent initializes correctly.

        Args:
            test_component: A fixture providing a BaseComponent instance.
        """
        assert isinstance(test_component, BaseComponent)
        assert hasattr(test_component, "composite")
        assert test_component.composite is None

    def test_set_composite(self, test_component: BaseComponent) -> None:
        """Test setting the composite attribute.

        Args:
            test_component: A fixture providing a BaseComponent instance.
        """
        # Create a mock composite
        class MockComposite:
            pass

        mock_composite = MockComposite()
        
        # Set the composite
        test_component.composite = mock_composite
        
        # Verify the composite was set
        assert test_component.composite is mock_composite


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])