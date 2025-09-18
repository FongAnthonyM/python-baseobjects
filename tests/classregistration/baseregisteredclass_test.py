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
import copy
import pickle
from typing import Any, ClassVar, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.classregistration import BaseRegisteredClass, BaseClassRegistry
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


class ExampleRegisteredClass(BaseRegisteredClass):
    """A base test subclass of BaseRegisteredClass for testing purposes."""

    # Class Attributes #
    class_registry_type: ClassVar[Type[BaseClassRegistry]] = ConcreteClassRegistry
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
    def get_registered_class(cls, name: str, default: Any = None) -> Optional["BaseRegisteredClass"]:
        """Gets a subclass from the registry.

        Args:
            name: The name of the class to get.
            default: The default value to return if the class is not found.

        Returns:
            The requested subclass or the default value.
        """
        if cls.class_registry is None:
            return default
        return cls.class_registry.get_class(name, default)


# Tests #
class TestBaseRegisteredClass(BaseRegisteredClassTestSuite):
    """Test the BaseRegisteredClass class.

    This class tests the functionality of the BaseRegisteredClass class, which is an abstract class that registers
    subclasses, allowing subclass dispatching. It creates test subclasses of BaseRegisteredClass to test with since BaseRegisteredClass is abstract.
    """

    # Attributes #
    TestClass: Type[ExampleRegisteredClass] = ExampleRegisteredClass

    # Instance Methods #
    # Tests
    def test_copy(self, test_object: Any) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)

    def test_copy_method(self, test_object: Any) -> None:
        """Test the copy method behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)

    def test_deepcopy(self, test_object: Any, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

    def test_deepcopy_method(self, test_object: Any, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])