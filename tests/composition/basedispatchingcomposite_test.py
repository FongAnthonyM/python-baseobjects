"""basedispatchingcomposite_test.py
Tests for the BaseDispatchingComposite class in the baseobjects package.
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
from typing import Any, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.composition import BaseComponent, BaseDispatchingComposite
from baseobjects.testsuite.composition import BaseDispatchingCompositeTestSuite


# Definitions #
# Classes #
class ConcreteComponentClass(BaseComponent):
    """A test component class for testing BaseDispatchingComposite."""

    __test__ = False


class ConcreteTypeAComponent(BaseComponent):
    """A test component class for type A."""


class ConcreteTypeBComponent(BaseComponent):
    """A test component class for type B."""


class ConcreteDispatchingCompositeClass(BaseDispatchingComposite):
    """A test dispatching composite class for testing BaseDispatchingComposite."""

    # Class Attributes #
    default_component_types: dict[str, tuple[type, dict[str, Any]]] = {
        "default_component": (ConcreteComponentClass, {}),
    }

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        type_: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the object."""
        # Attributes #
        self.components: dict[str, Any] = self.components.copy()

        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                type_=type_,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors #
    def construct(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        type_: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            component_kwargs: Keyword arguments for components.
            component_types: Types and arguments for components.
            components: The components of the BIDS directory.
            type_: A string to dispatch components based on.
            **kwargs: Additional keyword arguments.
        """
        component_types = self.dispatch_component_types(type_) | (component_types or {})

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def dispatch_component_types(self, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """Dispatches component types using the given arguments.

        Args:
            *args: Positional arguments to use in dispatching.
            **kwargs: Keyword arguments to use in dispatching.

        Returns:
            dict[str, tuple[type, dict[str, Any]]: A dictionary mapping component names to tuples containing the
                component type and a dictionary
            of keyword arguments.
        """
        if args and isinstance(args[0], str):
            if args[0] == "type_a":
                return {"type_a_component": (ConcreteTypeAComponent, {})}
            elif args[0] == "type_b":
                return {"type_b_component": (ConcreteTypeBComponent, {})}

        if "type_" in kwargs and isinstance(kwargs["type_"], str):
            if kwargs["type_"] == "type_a":
                return {"type_a_component": (ConcreteTypeAComponent, {})}
            elif kwargs["type_"] == "type_b":
                return {"type_b_component": (ConcreteTypeBComponent, {})}

        return {}


# Tests #
class TestBaseDispatchingComposite(BaseDispatchingCompositeTestSuite):
    """Tests the BaseDispatchingComposite class.

    This class tests the functionality of the BaseDispatchingComposite class, which is a composite object that includes
    methods for dispatching component objects during instantiation. It creates test subclasses of BaseComponent and
    BaseDispatchingComposite to test with.
    """

    # Attributes #
    UnitTestComponent: type[BaseComponent] = ConcreteComponentClass
    UnitTestClass: type[BaseDispatchingComposite] = ConcreteDispatchingCompositeClass

    # Fixtures
    @pytest.fixture(
        params=[
            ((), {"type_": "type_a"}, "type_a_component", ConcreteTypeAComponent),
            ((), {"type_": "type_b"}, "type_b_component", ConcreteTypeBComponent),
            ((), {}, "default_component", ConcreteComponentClass),
        ],
    )
    def dispatch_scenario(self, request: Any) -> tuple[tuple[Any, ...], dict[str, Any], str, type]:
        """A fixture providing dispatch scenarios.

        Returns:
            The dispatch scenario.
        """
        return cast(tuple[tuple[Any, ...], dict[str, Any], str, type], request.param)

    @pytest.fixture
    def dispatch_args(
        self,
        dispatch_scenario: tuple[tuple[Any, ...], dict[str, Any], str, type],
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """A fixture providing arguments for dispatching.

        Returns:
            The arguments for dispatching.
        """
        return dispatch_scenario[0], dispatch_scenario[1]

    @pytest.fixture
    def expected_dispatch(
        self,
        dispatch_scenario: tuple[tuple[Any, ...], dict[str, Any], str, type],
    ) -> tuple[str, type]:
        """A fixture providing expected dispatch results.

        Returns:
            The expected dispatch results.
        """
        return dispatch_scenario[2], dispatch_scenario[3]

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("args", "kwargs", "expected_key", "expected_type"),
        [
            (("type_a",), {}, "type_a_component", ConcreteTypeAComponent),
            ((), {"type_": "type_b"}, "type_b_component", ConcreteTypeBComponent),
            ((), {"irrelevant": "value"}, None, None),
        ],
    )
    def test_dispatch_component_types_direct(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected_key: str | None,
        expected_type: type | None,
    ) -> None:
        """Tests calling the dispatch_component_types method directly.

        This test verifies that the dispatch_component_types method returns the correct component types when called
        directly.
        """
        composite = self.UnitTestClass()

        dispatched = composite.dispatch_component_types(*args, **kwargs)

        if expected_key:
            assert expected_key in dispatched
            assert expected_type is not None
            assert dispatched[expected_key][0] is expected_type
            assert isinstance(dispatched[expected_key][1], dict)
        else:
            assert len(dispatched) == 0

    def test_base_dispatch_not_implemented(self) -> None:
        """Tests that the base class raises NotImplementedError."""
        obj = BaseDispatchingComposite()
        with pytest.raises(NotImplementedError):
            obj.dispatch_component_types()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
