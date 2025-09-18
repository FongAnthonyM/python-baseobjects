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
import copy
import pickle
from typing import Any, ClassVar, Optional, Type, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from baseobjects.classregistration import DispatchableClass, BaseClassRegistry
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
    """Test the DispatchableClass class.

    This class tests the functionality of the DispatchableClass class, which is an abstract class
    that dispatches to subclasses based on arguments. It creates test subclasses of
    DispatchableClass to test with since DispatchableClass is abstract.
    """

    # Class Definitions #
    class BaseTestDispatchableClass(DispatchableClass):
        """A base test subclass of DispatchableClass for testing purposes."""

        # Class Attributes #
        class_registry_type: ClassVar[Type[BaseClassRegistry]] = ConcreteClassRegistry
        class_registration: ClassVar[bool] = True

        @classmethod
        def get_class_information(cls, *args: Any, **kwargs: Any) -> Tuple[str]:
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
        def get_registered_class(cls, name: str, default: Any = None) -> Optional["DispatchableClass"]:
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

    class TypeADispatchable(BaseTestDispatchableClass):
        """A subclass of BaseTestDispatchableClass for testing dispatching to type A."""
        class_registration = True

    class TypeBDispatchable(BaseTestDispatchableClass):
        """A subclass of BaseTestDispatchableClass for testing dispatching to type B."""
        class_registration = True

    # Attributes #
    TestClass: Type[BaseTestDispatchableClass] = BaseTestDispatchableClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestDispatchableClass.BaseTestDispatchableClass":
        """Create a test object for use in tests.

        Returns:
            BaseTestDispatchableClass: An instance of the test class.
        """
        return self.TestClass()

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

    def test_get_class_information(self, *args: Any, **kwargs: Any) -> None:
        """Test the get_class_information method.

        This test verifies that the get_class_information method correctly extracts class information from arguments.

        Args:
            *args: Positional arguments to test the get_class_information method.
            **kwargs: Keyword arguments to test the get_class_information method.
        """
        # Test with positional argument
        info = self.TestClass.get_class_information("TypeADispatchable")
        assert info == ("TypeADispatchable",)

        # Test with keyword argument
        info = self.TestClass.get_class_information(type="TypeBDispatchable")
        assert info == ("TypeBDispatchable",)

        # Test with no relevant arguments
        info = self.TestClass.get_class_information(123, irrelevant="value")
        assert info == (self.TestClass.__name__,)

    def test_class_dispatch(self, *args: Any, **kwargs: Any) -> None:
        """Test class dispatching.
        
        Args:
            *args: Positional arguments to test the class dispatching.
            **kwargs: Keyword arguments to test the class dispatching.
        """
        # Test dispatching with positional argument
        instance = self.TestClass("TypeADispatchable")
        assert isinstance(instance, self.TypeADispatchable)

        # Test dispatching with keyword argument
        instance = self.TestClass(type="TypeBDispatchable")
        assert isinstance(instance, self.TypeBDispatchable)

        # Test dispatching with unknown type
        instance = self.TestClass("UnknownType")
        assert isinstance(instance, self.TestClass)
        assert type(instance) is self.TestClass

        # Test that dispatching doesn't happen when called from a subclass
        instance = self.TypeADispatchable("TypeBDispatchable")
        assert isinstance(instance, self.TypeADispatchable)
        assert not isinstance(instance, self.TypeBDispatchable)

        # Test that dispatching doesn't happen when no arguments are provided
        instance = self.TestClass()
        assert isinstance(instance, self.TestClass)
        assert type(instance) is self.TestClass


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])