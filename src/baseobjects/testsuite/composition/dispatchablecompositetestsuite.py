"""dispatchablecompositetestsuite.py
Base test suite for DispatchableComposite and its subclasses.
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
from abc import abstractmethod
from typing import Any, Type

# Local Packages #
from ...composition import DispatchableComposite
from ..classregistration import DispatchableClassTestSuite
from .basedispatchingcompositetestsuite import BaseDispatchingCompositeTestSuite


# Definitions #
# Classes #
class DispatchableCompositeTestSuite(BaseDispatchingCompositeTestSuite, DispatchableClassTestSuite):
    """Base test suite for children of DispatchableComposite.

    This class provides common test functionality for child classes of DispatchableComposite, including tests for
    dispatchable class functionality. Subclasses should set the TestClass attribute and may override or extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: type[DispatchableComposite]

    # Instance Methods #
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

    @abstractmethod
    def test_construct_components_defaults(self, component_kwargs: dict[str, dict[str, Any]] | None = None) -> None:
        """Test the construct_components successfully builds components with default values.

        This test verifies that the defualt components were built correctly.

        Args:
            component_kwargs: A dictionary mapping component names to a dictionary of keyword arguments to pass to
                component constructor.
        """
        composite = self.TestClass(component_kwargs=component_kwargs)

        # Validate
        # assert isinstance(test_object.components["component_name"], ComponentType)
        # assert isinstance(test_object.components["other_component_name", ComponentType2]

    @abstractmethod
    def test_dispatch_component_types(self, *args: Any, **kwargs: Any) -> None:
        """Test the dispatch_component_types method.

        This test verifies that the dispatch_component_types method correctly dispatches component types based on the
        given arguments.

        Args:
            *args: Positional arguments to pass to the dispatch_component_types method.
            **kwargs: Keyword arguments to pass to the dispatch_component_types method.
        """
        composite = self.TestClass()

        dispatched_component_types = composite.dispatch_component_types(*args, **kwargs)

        # Validate
        # assert dispatched_component_types["name"][0] is ComponentType

    @abstractmethod
    def test_get_class_information(self, *args: Any, **kwargs: Any) -> None:
        """Test the get_class_information method.

        This test verifies that the get_class_information method correctly extracts class information from arguments.

        Args:
            *args: Positional arguments to test the get_class_information method.
            **kwargs: Keyword arguments to test the get_class_information method.
        """

    @abstractmethod
    def test_class_dispatch(self, *args: Any, **kwargs: Any) -> None:
        """Test class dispatching.

        Args:
            *args: Positional arguments to test the class dispatching.
            **kwargs: Keyword arguments to test the class dispatching.
        """
