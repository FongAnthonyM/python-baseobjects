"""compositefactoryclass_test.py
Tests for the CompositeFactoryClass in the baseobjects package.
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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.composition import BaseComponent, CompositeFactoryClass
from baseobjects.testsuite.composition import CompositeFactoryClassTestSuite
from baseobjects.testsuite.composition.compositefactoryclasstestsuite import MockFactory, MockFactoryPreset


# Definitions #
# Classes #
class TestCompositeFactoryClass(CompositeFactoryClassTestSuite):
    """Tests for the CompositeFactoryClass."""

    # Attributes #
    UnitTestClass: type[CompositeFactoryClass] = MockFactory
    MockFactoryPreset: type[CompositeFactoryClass] = MockFactoryPreset

    # Tests #
    def test_composite_factory_class_is_not_head_class(self) -> None:
        """Tests that CompositeFactoryClass itself is not a head class."""
        assert CompositeFactoryClass.class_registration is False
        assert CompositeFactoryClass.class_registry is None

    def test_new_with_no_registry(self) -> None:
        """Tests __new__ when class_registry is None."""
        class NoRegistryFactory(CompositeFactoryClass):
            class_registration = False

        # Should fall through to super().__new__(cls)
        instance = NoRegistryFactory()
        assert isinstance(instance, NoRegistryFactory)

    def test_new_with_no_head_class(self) -> None:
        """Tests __new__ when head_class is None (edge case)."""
        class TempFactory(CompositeFactoryClass):
            class_registration = True

        # Manually mess with the registry to make head_class None
        # Note: This is an edge case as head_class is usually set during registration
        registry = TempFactory.class_registry
        original_head = registry.head_class
        registry.head_class = None
        try:
            # Should fall through to super().__new__(cls)
            instance = TempFactory()
            assert isinstance(instance, TempFactory)
        finally:
            registry.head_class = original_head
