"""baseregisteredclass_test.py
Tests for the BaseRegisteredClass class in the baseobjects package.
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
from baseobjects.classregistration import BaseClassRegistry, BaseRegisteredClass
from baseobjects.testsuite.classregistration import BaseRegisteredClassTestSuite


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


class ConcreteRegisteredClass(BaseRegisteredClass):
    """A base test subclass of BaseRegisteredClass for testing purposes."""

    # Class Attributes #
    class_registry_type: ClassVar[type[BaseClassRegistry]] = ConcreteClassRegistry
    class_registration: ClassVar[bool] = True

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
    def get_registered_class(cls, name: str, default: Any = None) -> Optional["BaseRegisteredClass"]:  # type: ignore[override]
        """Gets a subclass from the registry.

        Args:
            name: The name of the class to get.
            default: The default value to return if the class is not found.

        Returns:
            The requested subclass or the default value.
        """
        if cls.class_registry is None:
            return cast("BaseRegisteredClass | None", default)
        return cast("BaseRegisteredClass | None", cls.class_registry.get_class(name, default))


class DefaultRegisteredClass(BaseRegisteredClass):
    """A test subclass of BaseRegisteredClass that uses the default register_class implementation."""

    class_registry_type: ClassVar[type[BaseClassRegistry]] = ConcreteClassRegistry
    class_registration: ClassVar[bool] = True

    @classmethod
    def get_registered_class(cls, *args: Any, **kwargs: Any) -> type[BaseRegisteredClass] | None:
        """Gets the registered class.

        Returns:
            None.
        """
        return None


# Tests #
class TestBaseRegisteredClass(BaseRegisteredClassTestSuite):
    """Tests the BaseRegisteredClass class.

    This class tests the functionality of the BaseRegisteredClass class, which is an abstract class that registers
    subclasses, allowing subclass dispatching. It creates test subclasses of BaseRegisteredClass to test with since
    BaseRegisteredClass is abstract.
    """

    # Attributes #
    UnitTestClass: type[ConcreteRegisteredClass] = ConcreteRegisteredClass

    def test_base_register_class_coverage(self) -> None:
        """Tests the base implementation of register_class."""
        assert DefaultRegisteredClass.class_registry is not None
        assert "DefaultRegisteredClass" in DefaultRegisteredClass.class_registry

    def test_base_register_class_no_registry_coverage(self) -> None:
        """Tests base register_class when no registry is present."""

        class NoRegistryClass(BaseRegisteredClass):
            class_registration = False

            @classmethod
            def get_registered_class(cls, *args: Any, **kwargs: Any) -> None:
                """Gets the registered class."""

        # Manually call register_class
        NoRegistryClass.register_class()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
