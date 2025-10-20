"""basecomponenttestsuite.py
Base test suite for BaseComponent and its subclasses.
"""

# Header #
__package_name__ = "Anys"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import copy
import pickle
import weakref
from abc import abstractmethod
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...composition import BaseComponent
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseComponentTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseComponent.

    This class provides common test functionality for child classes of BaseComponent, including tests for composite
    relationships. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestComposite: type[Any]
    TestClass: type[BaseComponent]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_composite(self, *args: Any, **kwargs: Any) -> Any:
        """Create a test composite object.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            A test composite object instance.
        """
        return self.TestComposite()

    @pytest.fixture
    def test_object(self, test_composite: Any, *args: Any, **kwargs: Any) -> BaseComponent:
        """Create a test object.

        Args:
            test_composite: A fixture providing a test composite object.
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            Any: A test object instance.
        """
        return self.TestClass(test_composite, *args, **kwargs)

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

    def test_composite_property(self, test_composite: Any) -> None:
        """Test the composite property of the component.

        This test verifies that the composite property correctly gets and sets the composite object.

        Args:
            test_composite: A fixture providing a composite object.
        """
        # Test initial composite value
        test_object = self.TestClass(test_composite)
        assert test_object.composite is test_composite

        # Test setting new composite
        new_composite = self.TestComposite()
        test_object.composite = new_composite
        assert test_object.composite is new_composite

        # Test setting None
        test_object.composite = None
        assert test_object.composite is None

    def test_composite_weakref(self, test_composite: Any) -> None:
        """Test that the composite reference is a weak reference.

        This test verifies that the component holds a weak reference to its composite, which means
        the composite can be garbage collected even if the component still exists.

        Args:
            test_composite: A fixture providing a composite object.
        """
        # Verify the composite reference is a weak reference
        test_object = self.TestClass(test_composite)
        assert isinstance(test_object._composite, weakref.ReferenceType)

        # Verify we can still access the composite through the property
        assert test_object.composite is test_composite

        # Create a new scope to test garbage collection
        def temp_scope() -> None:
            temp_composite = self.TestComposite()
            test_object.composite = temp_composite

        # Get weak reference to temporary composite
        temp_scope()

        # Verify the temporary composite was garbage collected
        assert test_object.composite is None
