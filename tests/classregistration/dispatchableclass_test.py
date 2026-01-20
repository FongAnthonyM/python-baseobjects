"""dispatchableclass_test.py
Tests for the DispatchableClass class in the baseobjects package.
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
from typing import Any, ClassVar, Optional, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import BaseClassRegistry, DispatchableClass
from baseobjects.testsuite.classregistration import DispatchableClassTestSuite


# Definitions #
# Classes #
# Class Definitions #
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


class TestDispatchableClass(DispatchableClassTestSuite):
    """Tests the DispatchableClass class.

    This class tests the functionality of the DispatchableClass class, which is an abstract class that dispatches to
    subclasses based on arguments. It creates test subclasses of DispatchableClass to test with since DispatchableClass
    is abstract.
    """

    # Class Definitions #
    class ConcreteDispatchableClass(DispatchableClass):
        """A base test subclass of DispatchableClass for testing purposes."""

        # Class Attributes #
        class_registry_type: ClassVar[type[BaseClassRegistry]] = ConcreteClassRegistry
        class_registration: ClassVar[bool] = True

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
            if "type" in kwargs and isinstance(kwargs["type"], str):
                return (kwargs["type"],)
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
        def get_registered_class(cls, name: str, default: Any = None) -> Optional["DispatchableClass"]:  # type: ignore[override]
            """Gets a subclass from the registry.

            Args:
                name: The name of the class to get.
                default: The default value to return if the class is not found.

            Returns:
                The requested subclass or the default value.
            """
            if cls.class_registry is None:
                return cast("DispatchableClass | None", default)
            return cast("DispatchableClass | None", cls.class_registry.get_class(name, default))

    class TypeADispatchable(ConcreteDispatchableClass):
        """A subclass of ConcreteDispatchableClass for testing dispatching to type A."""

        class_registration = True

    class TypeBDispatchable(ConcreteDispatchableClass):
        """A subclass of ConcreteDispatchableClass for testing dispatching to type B."""

        class_registration = True

    # Attributes #
    UnitTestClass: ClassVar[type[ConcreteDispatchableClass]] = ConcreteDispatchableClass

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("args", "kwargs", "expected"),
        [
            (("TypeADispatchable",), {}, ("TypeADispatchable",)),
            ((), {"type": "TypeBDispatchable"}, ("TypeBDispatchable",)),
            ((123,), {"irrelevant": "value"}, ("ConcreteDispatchableClass",)),
        ],
    )
    def test_get_class_information(self, args: tuple[Any, ...], kwargs: dict[str, Any], expected: tuple[str]) -> None:
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
        ("args", "kwargs", "expected_class_name", "strict_type"),
        [
            (("TypeADispatchable",), {}, "TypeADispatchable", False),
            ((), {"type": "TypeBDispatchable"}, "TypeBDispatchable", False),
            (("UnknownType",), {}, "ConcreteDispatchableClass", True),
            ((), {}, "ConcreteDispatchableClass", True),
        ],
    )
    def test_class_dispatch_variations(
        self,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        expected_class_name: str,
        strict_type: bool,
    ) -> None:
        """Tests class dispatching variations.

        Args:
            args: Positional arguments to test the class dispatching.
            kwargs: Keyword arguments to test the class dispatching.
            expected_class_name: The name of the expected class of the instance.
            strict_type: Whether to check strict type equality.
        """
        if expected_class_name == "ConcreteDispatchableClass":
            expected_class = self.UnitTestClass
        else:
            expected_class = getattr(self, expected_class_name)

        instance = self.UnitTestClass(*args, **kwargs)
        assert isinstance(instance, expected_class)
        if strict_type:
            assert type(instance) is expected_class

    def test_class_dispatch_subclass(self) -> None:
        """Tests that dispatching doesn't happen when called from a subclass."""
        instance = self.TypeADispatchable("TypeBDispatchable")
        assert isinstance(instance, self.TypeADispatchable)
        assert not isinstance(instance, self.TypeBDispatchable)


class DispatchMockRegistry(BaseClassRegistry):
    """A mock registry for testing."""

    def __init__(self, head_class: type | None = None, init: bool = True, **kwargs: Any) -> None:
        """Initializes the mock registry."""
        self.registered: list[type] = []
        super().__init__(head_class=head_class, init=init, **kwargs)

    def register_class(self, cls: type, *args: Any, **kwargs: Any) -> None:
        """Registers a class."""
        self.registered.append(cls)

    def get_class(self, *args: Any, **kwargs: Any) -> Any:
        """Gets a class.

        Returns:
            None.
        """
        return None


class TestDispatchableClassCoverage:
    """Tests coverage for DispatchableClass."""

    def test_get_class_information_not_implemented(self) -> None:
        """Tests that get_class_information raises NotImplementedError when not overridden."""

        class Dispatcher(DispatchableClass):
            class_registry_type = DispatchMockRegistry
            class_registration = True

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> None:
                """Gets registered class."""
                return

        # Dispatcher is head_class (created by class_registration=True)
        # Instantiate with args to trigger dispatch logic
        with pytest.raises(NotImplementedError, match=r"This method needs to be implemented to dispatch classes\."):
            Dispatcher("arg")


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
