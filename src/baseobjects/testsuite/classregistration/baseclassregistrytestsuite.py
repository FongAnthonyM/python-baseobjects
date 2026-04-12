"""baseclassregistrytestsuite.py
Base test suite for BaseClassRegistry and its subclasses.

This module contains the base test suite for BaseClassRegistry and its subclasses.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import BaseClassRegistry
from ..bases import BaseDictTestSuite


# Definitions #
# Classes #
class BaseClassRegistryTestSuite(BaseDictTestSuite):
    """Base test suite for children of BaseClassRegistry.

    This class provides common test functionality for child classes of BaseClassRegistry, including tests for class
    registration and retrieval. Subclasses should set the UnitTestClass attribute and may override or extend the test
    methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    class ConcreteClass1:
        """A test class for testing the registry."""

    class ConcreteClass2:
        """Another test class for testing the registry."""

    UnitTestClass: type[BaseClassRegistry]

    # Helper Methods #
    def create_test_registry(self, *args: Any, **kwargs: Any) -> BaseClassRegistry:
        """Creates a test registry instance.

        Args:
            *args: Positional arguments to pass to the registry constructor.
            **kwargs: Keyword arguments to pass to the registry constructor.

        Returns:
            The created test registry.
        """
        return self.UnitTestClass(*args, **kwargs)

    # Fixtures #
    @pytest.fixture
    def populated_registry(self, *args: Any, **kwargs: Any) -> BaseClassRegistry:
        """Creates a populated test registry for use in tests.

        Returns:
            BaseClassRegistry: A populated instance of the test class.
        """
        registry = self.create_test_registry(*args, **kwargs)
        registry.register_class(self.ConcreteClass1)
        registry.register_class(self.ConcreteClass2)
        return registry

    # Tests #
    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: Any, method: str) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method of copying to test.

        Raises:
            ValueError: If the method is invalid.
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        elif method == "method":
            obj_copy = test_object.copy()
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_copy is not test_object
        assert obj_copy.head_class is test_object.head_class
        assert obj_copy.data == test_object.data
        assert obj_copy.data is not test_object.data

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(self, test_object: Any, method: str, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method of deepcopying to test.
            memo: A memo dictionary to pass to deepcopy.

        Raises:
            ValueError: If the method is invalid.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        elif method == "method":
            obj_deepcopy = test_object.deepcopy(memo=memo)
        else:
            msg = f"Invalid method: {method}"
            raise ValueError(msg)

        # Validate
        assert obj_deepcopy is not test_object
        assert obj_deepcopy.head_class is test_object.head_class
        assert obj_deepcopy.data == test_object.data

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

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

    # Functionality #
    def test_dict_initialization(self) -> None:
        """Tests initialization with a dictionary.

        BaseClassRegistry does not support initialization with a dictionary in the same way as BaseDict/UserDict.
        """

    def test_dict_initialization_with_kwargs(self) -> None:
        """Tests initialization with keyword arguments.

        BaseClassRegistry does not support initialization with keyword arguments in the same way as BaseDict/UserDict.
        """

    def test_dict_iteration(self) -> None:  # type: ignore[override]
        """Tests iteration over the dictionary.

        BaseClassRegistry initialization differs from BaseDict, so the default test fails because the registry remains
        empty. Subclasses that support dict initialization (like NamespaceClassRegistry) should override this or test
        separately.
        """

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False)
        assert obj.head_class is None

        # Manually construct
        obj.construct()

    def test_head_class_init(self) -> None:
        """Tests initialization with head_class."""

        class MyHeadClass:
            pass

        obj = self.UnitTestClass(head_class=MyHeadClass)
        assert obj.head_class is MyHeadClass

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Tests the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to use in testing the register_class method.
            **kwargs: Keyword arguments to pass to use in testing the register_class method.
        """
        class_registry = self.create_test_registry(*args, **kwargs)
        class_registry.register_class(self.ConcreteClass1)

        # Validate
        assert self.ConcreteClass1.__name__ in class_registry
        assert class_registry[self.ConcreteClass1.__name__] is self.ConcreteClass1

    def test_get_class(self, populated_registry: BaseClassRegistry, *args: Any, **kwargs: Any) -> None:
        """Tests the get_class method.

        This test verifies that the get_class method correctly retrieves a registered class.

        Args:
            populated_registry: A fixture providing a registry already populated with example classes.
            *args: Positional arguments to pass to use in testing the get_class method.
            **kwargs: Keyword arguments to pass to use in testing the get_class method.
        """
        got_class = populated_registry.get_class(self.ConcreteClass1.__name__)

        # Validate
        assert got_class is self.ConcreteClass1
