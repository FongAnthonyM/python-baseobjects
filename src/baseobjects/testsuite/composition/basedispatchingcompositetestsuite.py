"""basedispatchingcompositetestsuite.py
Base test suite for BaseDispatchingComposite and its subclasses.
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

# Local Packages #
from ...composition.basedispatchingcomposite import BaseDispatchingComposite
from .basecompositetestsuite import BaseCompositeTestSuite


# Definitions #
# Classes #
class BaseDispatchingCompositeTestSuite(BaseCompositeTestSuite):
    """Base test suite for children of BaseDispatchingComposite.

    This class provides common test functionality for child classes of BaseDispatchingComposite, including tests for
    component type dispatching. Subclasses should set the UnitTestClass attribute and may override or extend the test
    methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: type[BaseDispatchingComposite]

    # Fixtures #
    @pytest.fixture
    def dispatch_args(self) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """Returns args/kwargs that trigger a specific dispatch.

        Override this fixture in subclasses to provide arguments that cause a known dispatch.
        """
        return (), {}

    @pytest.fixture
    def expected_dispatch(self) -> tuple[str, type]:
        """Returns (component_name, component_type) expected from dispatch_args.

        Override this fixture in subclasses to provide the expected result of the dispatch.
        """
        return "", type(None)

    # Tests #
    def test_dispatch_component_types(
        self,
        dispatch_args: tuple[tuple[Any, ...], dict[str, Any]],
        expected_dispatch: tuple[str, type],
    ) -> None:
        """Tests the dispatch_component_types method via construction.

        This test verifies that the object correctly dispatches component types based on the given arguments.
        """
        args, kwargs = dispatch_args
        name, expected_type = expected_dispatch

        if expected_type is type(None):
            pytest.skip("Dispatch args/expectation not implemented.")

        # Creates Composite
        composite = self.UnitTestClass(*args, **kwargs)

        # Validate
        assert name in composite.components
        assert isinstance(composite.components[name], expected_type)

    def test_dispatch_override_types(
        self,
        dispatch_args: tuple[tuple[Any, ...], dict[str, Any]],
        expected_dispatch: tuple[str, type],
    ) -> None:
        """Tests that explicit component_types override dispatched types."""
        args, kwargs = dispatch_args
        name, _ = expected_dispatch

        if name == "":
            pytest.skip("Dispatch expectation not implemented.")

        # Override with UnitTestComponent (defined in BaseCompositeTestSuite)
        override_type = self.UnitTestComponent
        component_types: dict[str, tuple[type, dict[str, Any]]] = {name: (override_type, {})}

        # Creates Composite with override
        composite = self.UnitTestClass(*args, component_types=component_types, **kwargs)  # type: ignore[misc]

        # Validate
        assert isinstance(composite.components[name], override_type)

    def test_dispatch_override_instances(
        self,
        dispatch_args: tuple[tuple[Any, ...], dict[str, Any]],
        expected_dispatch: tuple[str, type],
    ) -> None:
        """Tests that explicit components override dispatched types."""
        args, kwargs = dispatch_args
        name, _ = expected_dispatch

        if name == "":
            pytest.skip("Dispatch expectation not implemented.")

        # Override with UnitTestComponent instance
        override_instance = self.UnitTestComponent()
        components = {name: override_instance}

        # Creates Composite with override
        composite = self.UnitTestClass(*args, components=components, **kwargs)  # type: ignore[misc]

        # Validate
        assert composite.components[name] is override_instance
