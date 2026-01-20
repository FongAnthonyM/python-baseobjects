"""dispatchablecomposite_test.py
Tests for the DispatchableComposite class in the baseobjects package.
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
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import BaseClassRegistry
from baseobjects.composition import BaseComponent, DispatchableComposite
from baseobjects.testsuite.composition import DispatchableCompositeTestSuite


# Definitions #
# Classes #
class ConcreteClassRegistry(BaseClassRegistry):
    """A concrete subclass of BaseClassRegistry for testing purposes."""

    def register_class(self, cls: type, *args: Any, **kwargs: Any) -> None:
        """Registers a class with the registry.

        Args:
            cls: The class to register.
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        self[cls.__name__] = cls

    def get_class(self, name: str, default: Any = None) -> Any:
        """Gets a class from the registry.

        Args:
            name: The name of the class to get.
            default: The default value to return if the class is not found.

        Returns:
            The requested class or the default value.
        """
        return self.get(name, default)


class ConcreteComponentClass(BaseComponent):
    """A test component class for testing DispatchableComposite."""


class ConcreteTypeAComponent(BaseComponent):
    """A test component class for type A."""


class ConcreteTypeBComponent(BaseComponent):
    """A test component class for type B."""


class ConcreteDispatchableComposite(DispatchableComposite):
    """A base test subclass of DispatchableComposite for testing purposes."""

    # Class Attributes #
    class_registry_type: ClassVar[type[BaseClassRegistry]] = ConcreteClassRegistry
    class_registration: ClassVar[bool] = True
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {
        "default_component": (ConcreteComponentClass, {}),
    }

    @classmethod
    def get_class_information(cls, *args: Any, **kwargs: Any) -> tuple[str]:
        """Gets a class's lookup information from a given set of arguments.

        Args:
            *args: Positional arguments to get the name from.
            **kwargs: Keyword arguments to get the name from.

        Returns:
            A tuple containing the class name to look up.
        """
        if args and isinstance(args[0], str):
            return (args[0],)
        if "type_" in kwargs and isinstance(kwargs["type_"], str):
            return (kwargs["type_"],)
        return (cls.__name__,)

    @classmethod
    def register_class(cls, *args: Any, **kwargs: Any) -> None:
        """Registers this class with the registry.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        if cls.class_registry is not None:
            cls.class_registry.register_class(cls)

    @classmethod
    def get_registered_class(
        cls,
        name: str,
        default: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> type["DispatchableComposite"] | None:
        """Gets a subclass from the registry.

        Args:
            name: The name of the class to get.
            default: The default value to return if the class is not found.
            *args: Positional arguments (unused).
            **kwargs: Keyword arguments (unused).

        Returns:
            The requested subclass or the default value.
        """
        if cls.class_registry is None:
            return cast(type["DispatchableComposite"] | None, default)
        return cast(
            type["DispatchableComposite"] | None,
            cls.class_registry.get_class(name, default),
        )

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        type_: str | None = None,
        component_type: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
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
                type_=type_,
                component_type=component_type,
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
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
        component_type: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            component_kwargs: Keyword arguments for components.
            component_types: Types and arguments for components.
            components: The components of the BIDS directory.
            type_: A string to dispatch classes based on.
            component_type: A string to dispatch components based on.
            **kwargs: Additional keyword arguments.
        """
        component_types = self.dispatch_component_types(component_type) | (component_types or {})

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
            A dictionary mapping component names to tuples containing the component type and a dictionary
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


class TypeADispatchable(ConcreteDispatchableComposite):
    """A subclass of ConcreteDispatchableComposite for testing dispatching to type A."""

    class_registration = True


class TypeBDispatchable(ConcreteDispatchableComposite):
    """A subclass of ConcreteDispatchableComposite for testing dispatching to type B."""

    class_registration = True


# Tests #
class TestDispatchableComposite(DispatchableCompositeTestSuite):
    """Tests the DispatchableComposite class.

    This class tests the functionality of the DispatchableComposite class, which is a composite object that combines
    component dispatching and class dispatching capabilities. It creates test subclasses of BaseComponent and
    DispatchableComposite to test with.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[DispatchableComposite]] = ConcreteDispatchableComposite
    UnitTestComponent: ClassVar[type[BaseComponent]] = ConcreteComponentClass

    # Fixtures
    @pytest.fixture(
        params=[
            ((None, "type_a"), {}, "type_a_component", ConcreteTypeAComponent),
            ((), {"component_type": "type_b"}, "type_b_component", ConcreteTypeBComponent),
            ((), {"irrelevant": "value"}, "default_component", ConcreteComponentClass),
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
        ("args", "kwargs", "expected"),
        [
            (("TypeADispatchable",), {}, ("TypeADispatchable",)),
            ((), {"type_": "TypeBDispatchable"}, ("TypeBDispatchable",)),
            ((123,), {"irrelevant": "value"}, ("ConcreteDispatchableComposite",)),
        ],
    )
    def test_get_class_information(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected: tuple[str],
    ) -> None:
        """Tests the get_class_information method.

        This test verifies that the get_class_information method correctly extracts class information from arguments.

        Args:
            args: Positional arguments to test the get_class_information method.
            kwargs: Keyword arguments to test the get_class_information method.
            expected: The expected class information tuple.
        """
        info = self.UnitTestClass.get_class_information(*args, **kwargs)
        assert info == expected

    @pytest.mark.parametrize(
        ("cls", "args", "kwargs", "expected_class", "strict_type"),
        [
            (None, ("TypeADispatchable",), {}, TypeADispatchable, False),
            (None, (), {"type_": "TypeBDispatchable"}, TypeBDispatchable, False),
            (None, ("UnknownType",), {}, ConcreteDispatchableComposite, True),
            (None, (), {}, ConcreteDispatchableComposite, True),
            (TypeADispatchable, ("TypeBDispatchable",), {}, TypeADispatchable, True),
        ],
    )
    def test_class_dispatch_variations(
        self,
        cls: type | None,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected_class: type,
        strict_type: bool,
    ) -> None:
        """Tests class dispatching variations.

        Args:
            cls: The class to instantiate. If None, uses UnitTestClass.
            args: Positional arguments to test the class dispatching.
            kwargs: Keyword arguments to test the class dispatching.
            expected_class: The expected class of the instance.
            strict_type: Whether to check strict type equality.
        """
        if cls is None:
            cls = self.UnitTestClass
        instance = cls(*args, **kwargs)
        assert isinstance(instance, expected_class)
        if strict_type:
            assert type(instance) is expected_class

    @pytest.mark.parametrize(
        ("args", "kwargs", "expected_class", "expected_component_key", "expected_component_type"),
        [
            (
                ("TypeADispatchable",),
                {"component_type": "type_b"},
                TypeADispatchable,
                "type_b_component",
                ConcreteTypeBComponent,
            ),
            (
                (),
                {"component_type": "type_a", "type_": "TypeBDispatchable"},
                TypeBDispatchable,
                "type_a_component",
                ConcreteTypeAComponent,
            ),
        ],
    )
    def test_combined_dispatch(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected_class: type,
        expected_component_key: str,
        expected_component_type: type,
    ) -> None:
        """Tests combined class and component dispatching.

        Args:
            args: Positional arguments.
            kwargs: Keyword arguments.
            expected_class: The expected class of the instance.
            expected_component_key: The expected key of the component.
            expected_component_type: The expected type of the component.
        """
        instance = self.UnitTestClass(*args, **kwargs)
        assert isinstance(instance, expected_class)
        assert expected_component_key in instance.components
        assert isinstance(instance.components[expected_component_key], expected_component_type)
        assert instance.components[expected_component_key].composite is instance

    def test_dispatchable_dispatch_not_implemented(self) -> None:
        """Tests that the base class raises NotImplementedError."""
        with pytest.raises(NotImplementedError):
            DispatchableComposite.get_registered_class("any")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
