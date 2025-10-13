"""namespaceregisteredclass_test.py
Tests for the NamespaceRegisteredClass class in the baseobjects package.
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
from typing import Any, ClassVar, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.classregistration import NamespaceRegisteredClass
from src.baseobjects.testsuite.classregistration import NamespaceRegisteredClassTestSuite


# Definitions #
# Classes #
class ExampleNamespaceRegisteredClass(NamespaceRegisteredClass):
    """A base test subclass of NamespaceRegisteredClass for testing purposes."""

    # Class Attributes #
    class_registration: ClassVar[bool] = True
    class_namespace: ClassVar[str] = "test_namespace"


# Tests #
class TestNamespaceRegisteredClass(NamespaceRegisteredClassTestSuite):
    """Test the NamespaceRegisteredClass class.

    This class tests the functionality of the NamespaceRegisteredClass class, which is an abstract class that registers
    subclasses with namespaces, allowing subclass dispatching. It creates test subclasses of NamespaceRegisteredClass to
    test with.

    Attributes:
        TestClass: The test class to use for testing, an instance of BaseTestNamespaceRegisteredClass.
    """

    # Attributes #
    TestClass: Type[ExampleNamespaceRegisteredClass] = ExampleNamespaceRegisteredClass

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
