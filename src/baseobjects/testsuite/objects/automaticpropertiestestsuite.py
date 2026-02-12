"""automaticpropertiestestsuite.py
Test suite for the AutomaticProperties class.

This module provides the AutomaticPropertiesTestSuite class which serves as a foundation for testing classes that
inherit from AutomaticProperties. It includes tests for property creation, access, modification, and deletion.
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

# Third-Party Packages #
import pytest

# Local Packages #
from ...objects import AutomaticProperties
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class AutomaticPropertiesTestSuite(BaseObjectTestSuite):
    """Base test suite for children of AutomaticProperties.

    This class provides common test functionality for child classes of AutomaticProperties, including tests for property
    creation, access, modification, and deletion. Subclasses should set the UnitTestClass attribute and may override or
    extend the test methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    UnitTestClass: type[AutomaticProperties]

    # Tests #
    # Instantiation #
    def test_instance_creation(self) -> None:
        """Tests that instances of the class can be created."""
        # Create Object
        obj = self.UnitTestClass()

        # Validate
        assert isinstance(obj, self.UnitTestClass)
        assert isinstance(obj, AutomaticProperties)

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: AutomaticProperties, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for copying ("copy" or "method").
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)

    @pytest.mark.parametrize("method", ["deepcopy", "method"])
    def test_deepcopy_operations(self, test_object: AutomaticProperties, method: str) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
            method: The method to use for deep copying ("deepcopy" or "method").
        """
        # Deep Copy Object
        if method == "deepcopy":
            obj_deepcopy = copy.deepcopy(test_object)
        else:
            obj_deepcopy = test_object.deepcopy()

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)

    # Pickling #
    def test_pickling(self, test_object: AutomaticProperties) -> None:
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
        assert isinstance(unpickled, self.UnitTestClass)

    # Functionality #
    @pytest.mark.parametrize("factory_method", ["property_method_factory", "property_class_method_factory"])
    def test_property_factory_methods(self, factory_method: str) -> None:
        """Tests the property factory methods.

        This test verifies that the property factory methods create the expected property callbacks.

        Args:
            factory_method: The name of the factory method to test.
        """
        # Get Property Callbacks
        factory = getattr(self.UnitTestClass, factory_method)
        get_cb, set_cb, del_cb = factory("_test_prop")

        # Create Test Object
        obj = self.UnitTestClass()
        obj._test_prop = "test value"  # type: ignore[attr-defined]

        # Validate
        assert callable(get_cb)
        assert callable(set_cb)
        assert callable(del_cb)
        assert get_cb(obj) == "test value"
        set_cb(obj, "new test value")
        assert obj._test_prop == "new test value"  # type: ignore[attr-defined]
        del_cb(obj)
        assert not hasattr(obj, "_test_prop")
