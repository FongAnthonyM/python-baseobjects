"""baseclassregistrytestsuite.py
Base test suite for BaseClassRegistry and its subclasses.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import BaseClassRegistry
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseClassRegistryTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseClassRegistry.

    This class provides common test functionality for child classes of BaseClassRegistry, including tests_old_ for
    class registration and retrieval. Subclasses should set the TestClass attribute and may override or extend the test
    methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Class Definitions #
    class ExampleClass1:
        """A test class for testing the registry."""

    class ExampleClass2:
        """Another test class for testing the registry."""

    # Attributes #
    TestClass: Type[BaseClassRegistry]

    # Instance Methods #
    def create_test_registry(self, *args: Any, **kwargs) -> BaseClassRegistry:
        """Create a test registry instance.

        Args:
            *args: Positional arguments to pass to the registry constructor.
            **kwargs: Keyword arguments to pass to the registry constructor.
        """
        return self.TestClass(*args, **kwargs)

    # Fixtures
    @pytest.fixture
    def populated_registry(self, *args: Any, **kwargs: Any) -> BaseClassRegistry:
        """Create a populated test registry for use in tests_old_.

        Returns:
            BaseClassRegistry: A populated instance of the test class.
        """
        registry = self.create_test_registry(*args, **kwargs)
        registry.register_class(self.ExampleClass1)
        registry.register_class(self.ExampleClass2)
        return registry

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
        assert obj_copy.head_class is test_object.head_class
        assert obj_copy.data is test_object.data

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
        assert obj_copy.head_class is test_object.head_class
        assert obj_copy.data is test_object.data

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
        assert obj_deepcopy.head_class is test_object.head_class
        assert obj_deepcopy.data == test_object.data

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
        assert obj_deepcopy.head_class is test_object.head_class
        assert obj_deepcopy.data == test_object.data

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
        assert unpickled.head_class is test_object.head_class
        assert unpickled.data == test_object.data

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Test the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to use in testing the register_class method.
            **kwargs: Keyword arguments to pass to use in testing the register_class method.
        """
        class_registry = self.create_test_registry(*args, **kwargs)
        class_registry.register_class(self.ExampleClass1)

        # Validate
        assert self.ExampleClass1.__name__ in class_registry
        assert class_registry[self.ExampleClass1.__name__] is self.ExampleClass1

    def test_get_class(self, populated_registry: BaseClassRegistry, *args: Any, **kwargs: Any) -> None:
        """Test the get_class method.

        This test verifies that the get_class method correctly retrieves a registered class.

        Args:
            *args: Positional arguments to pass to use in testing the get_class method.
            **kwargs: Keyword arguments to pass to use in testing the get_class method.
        """
        got_class = populated_registry.get_class(self.ExampleClass1.__name__)

        # Validate
        assert got_class is self.ExampleClass1
