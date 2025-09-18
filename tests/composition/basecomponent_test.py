"""basecomponent_test.py
Tests for the BaseComponent class in the baseobjects package.
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
from src.baseobjects.composition import BaseComponent, BaseComposite
from src.baseobjects.testsuite.composition import BaseComponentTestSuite


# Definitions #
# Classes #
class ExampleCompositeClass(BaseComposite):
    """A test composite class for testing BaseComponent."""


class ExampleComponentClass(BaseComponent):
    """A test component class for testing BaseComponent."""


# Tests #
class TestBaseComponent(BaseComponentTestSuite):
    """Test the BaseComponent class.

    This class tests the functionality of the BaseComponent class, which is a basic component object.
    It creates test subclasses of BaseComponent and BaseComposite to test with.
    """

    # Attributes #
    TestClass: Type[BaseComponent] = ExampleComponentClass
    TestComposite: Type[BaseComposite] = ExampleCompositeClass

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_composite(self) -> BaseComposite:
        """Create a test composite object.

        Returns:
            A test composite object instance.
        """
        return self.TestComposite()

    @pytest.fixture
    def test_object(self, test_composite: BaseComposite) -> BaseComponent:
        """Create a test object.

        Args:
            test_composite: A fixture providing a test composite object.

        Returns:
            A test component object instance.
        """
        return self.TestClass(composite=test_composite)

    # Tests
    def test_copy(self, test_object: BaseComponent) -> None:
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
        assert obj_copy.composite is test_object.composite

    def test_copy_method(self, test_object: BaseComponent) -> None:
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
        assert obj_copy.composite is test_object.composite

    def test_deepcopy(self, test_object: BaseComponent, memo: dict | None = None) -> None:
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
        assert obj_deepcopy.composite is not test_object.composite

    def test_deepcopy_method(self, test_object: BaseComponent, memo: dict | None = None) -> None:
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
        assert obj_deepcopy.composite is not test_object.composite

    def test_pickling(self, test_object: BaseComponent) -> None:
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
        assert unpickled.composite is not test_object.composite

    def test_composite_none(self) -> None:
        """Test that a component can be created with no composite.

        This test verifies that a component can be created with no composite and that the composite property
        returns None in this case.
        """
        # Create component with no composite
        component = self.TestClass()

        # Validate
        assert component.composite is None

    def test_composite_set_none(self, test_object: BaseComponent) -> None:
        """Test setting the composite to None.

        This test verifies that the composite property can be set to None and that the composite property
        returns None in this case.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Set composite to None
        test_object.composite = None

        # Validate
        assert test_object.composite is None

    def test_construct_with_composite(self, test_composite: BaseComposite) -> None:
        """Test constructing a component with a composite.

        This test verifies that a component can be constructed with a composite and that the composite property
        returns the correct composite.

        Args:
            test_composite: A fixture providing a test composite object.
        """
        # Create component with composite
        component = self.TestClass(composite=test_composite)

        # Validate
        assert component.composite is test_composite


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])