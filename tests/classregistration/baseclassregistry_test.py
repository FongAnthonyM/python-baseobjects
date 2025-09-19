"""baseclassregistry_test.py
Tests for the BaseClassRegistry class in the baseobjects package.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.classregistration import BaseClassRegistry
from src.baseobjects.testsuite.classregistration import BaseClassRegistryTestSuite


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

# Tests #
class TestBaseClassRegistry(BaseClassRegistryTestSuite):
    """Test the BaseClassRegistry class.

    This class tests the functionality of the BaseClassRegistry class, which is a registry for classes that allows for
    class registration and retrieval.
    """

    # Attributes #
    TestClass: Type[BaseClassRegistry] = ConcreteClassRegistry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])