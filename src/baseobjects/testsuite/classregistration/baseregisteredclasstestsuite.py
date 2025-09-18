"""baseregisteredclasstestsuite.py
Base test suite for BaseRegisteredClass and its subclasses.
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
from abc import abstractmethod
import copy
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...classregistration import BaseRegisteredClass, BaseClassRegistry
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseRegisteredClassTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseRegisteredClass.

    This class provides common test functionality for child classes of BaseRegisteredClass, including tests_old_ for
    class registration and retrieval. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[BaseRegisteredClass]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def example_subclass(self) -> Type[BaseRegisteredClass]:
        """Create a test subclass of the TestClass.

        Returns:
            A test subclass of the TestClass.
        """
        class TestSubclass(self.TestClass):
            class_registration = True

        return TestSubclass

    # Tests
    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    def test_register_class(self, *args: Any, **kwargs: Any) -> None:
        """Test the register_class method.

        This test verifies that the register_class method correctly registers a class.

        Args:
            *args: Positional arguments to pass to the register_class method.
            **kwargs: Keyword arguments to pass to the register_class method.
        """
        class NewTestSubclass(self.TestClass):
            class_registration = False

        # Register class
        NewTestSubclass.register_class(*args, **kwargs)

        # Verify class was registered
        assert NewTestSubclass.__name__ in self.TestClass.class_registry
        assert self.TestClass.class_registry[NewTestSubclass.__name__] is NewTestSubclass

    def test_get_registered_class(self, example_subclass: Type[BaseRegisteredClass], *args: Any, **kwargs: Any) -> None:
        """Test the get_registered_class method.

        This test verifies that the get_registered_class method correctly retrieves a registered class.

        Args:
            example_subclass: A fixture providing a test subclass.
            *args: Positional arguments to test the get_register_class method.
            **kwargs: Keyword arguments to test the get_register_class method.
        """
        # Register class
        got_class = self.TestClass.get_registered_class(example_subclass.__name__)

        # Verify class was registered
        assert example_subclass.__name__ in self.TestClass.class_registry
        assert got_class is example_subclass
