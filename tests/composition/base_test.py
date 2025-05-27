"""base_test.py
Base test classes for testing the composition package in the baseobjects package.
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
from src.baseobjects.composition import BaseComponent, BaseComposite, BaseDispatchingComposite, DispatchableComposite
from tests.bases.base_test import BaseBaseObjectTest


# Definitions #
# Classes #
class BaseComponentTest(BaseBaseObjectTest):
    """Base test class for testing BaseComponent and its subclasses.

    This class provides common test methods and fixtures for testing BaseComponent and its subclasses.
    """

    # Class Attributes #
    class_: Type[BaseComponent] = BaseComponent

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_component(self) -> BaseComponent:
        """Create a test component instance for use in tests.

        Returns:
            BaseComponent: An instance of the test class.
        """
        return self.class_()


class BaseCompositeTest(BaseBaseObjectTest):
    """Base test class for testing BaseComposite and its subclasses.

    This class provides common test methods and fixtures for testing BaseComposite and its subclasses.
    """

    # Class Attributes #
    class_: Type[BaseComposite] = BaseComposite

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_composite(self) -> BaseComposite:
        """Create a test composite instance for use in tests.

        Returns:
            BaseComposite: An instance of the test class.
        """
        return self.class_()


class BaseDispatchingCompositeTest(BaseCompositeTest):
    """Base test class for testing BaseDispatchingComposite and its subclasses.

    This class provides common test methods and fixtures for testing BaseDispatchingComposite and its subclasses.
    """

    # Class Attributes #
    class_: Type[BaseDispatchingComposite] = BaseDispatchingComposite

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dispatching_composite(self) -> BaseDispatchingComposite:
        """Create a test dispatching composite instance for use in tests.

        Returns:
            BaseDispatchingComposite: An instance of the test class.
        """
        return self.class_()


class DispatchableCompositeTest(BaseDispatchingCompositeTest):
    """Base test class for testing DispatchableComposite and its subclasses.

    This class provides common test methods and fixtures for testing DispatchableComposite and its subclasses.
    """

    # Class Attributes #
    class_: Type[DispatchableComposite] = DispatchableComposite

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dispatchable_composite(self) -> DispatchableComposite:
        """Create a test dispatchable composite instance for use in tests.

        Returns:
            DispatchableComposite: An instance of the test class.
        """
        return self.class_()