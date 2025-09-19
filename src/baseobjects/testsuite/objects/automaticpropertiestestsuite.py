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
from typing import Type

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
    creation, access, modification, and deletion. Subclasses should set the TestClass attribute and may override or
    extend the test methods.

    Attributes:
        TestClass: The class that the test suite is testing.
    """

    # Attributes #
    TestClass: Type[AutomaticProperties]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_with_properties(self) -> Type[AutomaticProperties]:
        """Create a test class with properties.

        Returns:
            Type[AutomaticProperties]: A test class with properties.
        """
        class TestAutomaticProperties(self.TestClass):
            """Test class for AutomaticProperties."""
            properties = {
                "test_prop": "_test_prop",
                "another_prop": "_another_prop"
            }

        return TestAutomaticProperties

    @pytest.fixture
    def test_object_with_properties(self, test_class_with_properties: Type[AutomaticProperties]) -> AutomaticProperties:
        """Create a test object with properties.

        Args:
            test_class_with_properties: A test class with properties.

        Returns:
            AutomaticProperties: A test object with properties.
        """
        obj = test_class_with_properties()
        obj._test_prop = "test value"
        obj._another_prop = "another value"
        return obj

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the class can be created."""
        # Create Object
        obj = self.TestClass()

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, AutomaticProperties)

    def test_copy(self, test_object: AutomaticProperties) -> None:
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

    def test_copy_method(self, test_object: AutomaticProperties) -> None:
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

    def test_deepcopy(self, test_object: AutomaticProperties) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Deep Copy Object
        obj_deepcopy = copy.deepcopy(test_object)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

    def test_deepcopy_method(self, test_object: AutomaticProperties) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes but the same immutable
        attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Deep Copy Object
        obj_deepcopy = test_object.deepcopy()

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

    def test_pickling(self, test_object: AutomaticProperties) -> None:
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

    def test_property_creation(self, test_class_with_properties: Type[AutomaticProperties]) -> None:
        """Test that properties are created correctly.

        This test verifies that properties are created correctly based on the properties dictionary.

        Args:
            test_class_with_properties: A fixture providing a test class with properties.
        """
        # Create Object
        obj = test_class_with_properties()

        # Validate
        assert hasattr(test_class_with_properties, "test_prop")
        assert hasattr(test_class_with_properties, "another_prop")
        assert isinstance(getattr(test_class_with_properties, "test_prop"), property)
        assert isinstance(getattr(test_class_with_properties, "another_prop"), property)

    def test_property_access(self, test_object_with_properties: AutomaticProperties) -> None:
        """Test that properties can be accessed correctly.

        This test verifies that properties can be accessed correctly and return the expected values.

        Args:
            test_object_with_properties: A fixture providing a test object with properties.
        """
        # Access Properties
        test_prop_value = test_object_with_properties.test_prop
        another_prop_value = test_object_with_properties.another_prop

        # Validate
        assert test_prop_value == "test value"
        assert another_prop_value == "another value"

    def test_property_modification(self, test_object_with_properties: AutomaticProperties) -> None:
        """Test that properties can be modified correctly.

        This test verifies that properties can be modified correctly and the changes are reflected in the underlying
        attributes.

        Args:
            test_object_with_properties: A fixture providing a test object with properties.
        """
        # Modify Properties
        test_object_with_properties.test_prop = "new test value"
        test_object_with_properties.another_prop = "new another value"

        # Validate
        assert test_object_with_properties._test_prop == "new test value"
        assert test_object_with_properties._another_prop == "new another value"
        assert test_object_with_properties.test_prop == "new test value"
        assert test_object_with_properties.another_prop == "new another value"

    def test_property_deletion(self, test_object_with_properties: AutomaticProperties) -> None:
        """Test that properties can be deleted correctly.

        This test verifies that properties can be deleted correctly and the underlying attributes are removed.

        Args:
            test_object_with_properties: A fixture providing a test object with properties.
        """
        # Delete Properties
        del test_object_with_properties.test_prop
        del test_object_with_properties.another_prop

        # Validate
        assert not hasattr(test_object_with_properties, "_test_prop")
        assert not hasattr(test_object_with_properties, "_another_prop")
        with pytest.raises(AttributeError):
            _ = test_object_with_properties.test_prop
        with pytest.raises(AttributeError):
            _ = test_object_with_properties.another_prop

    def test_property_factory_methods(self) -> None:
        """Test the property factory methods.

        This test verifies that the property factory methods create the expected property callbacks.
        """
        # Get Property Callbacks
        get_cb, set_cb, del_cb = self.TestClass.property_method_factory("_test_prop")
        class_get_cb, class_set_cb, class_del_cb = self.TestClass.property_class_method_factory("_test_prop")

        # Create Test Object
        obj = self.TestClass()
        obj._test_prop = "test value"

        # Validate
        assert callable(get_cb)
        assert callable(set_cb)
        assert callable(del_cb)
        assert callable(class_get_cb)
        assert callable(class_set_cb)
        assert callable(class_del_cb)
        assert get_cb(obj) == "test value"
        set_cb(obj, "new test value")
        assert obj._test_prop == "new test value"
        del_cb(obj)
        assert not hasattr(obj, "_test_prop")

    def test_construct_properties(self) -> None:
        """Test the _construct_properties_ method.

        This test verifies that the _construct_properties_ method creates properties correctly based on a property map.
        """
        # Create Test Class
        class TestClass(self.TestClass):
            """Test class for _construct_properties_."""
            pass

        # Construct Properties
        property_map = {
            "dynamic_prop": "_dynamic_prop",
            "another_dynamic_prop": "_another_dynamic_prop"
        }
        TestClass._construct_properties_(property_map)

        # Create Test Object
        obj = TestClass()
        obj._dynamic_prop = "dynamic value"
        obj._another_dynamic_prop = "another dynamic value"

        # Validate
        assert hasattr(TestClass, "dynamic_prop")
        assert hasattr(TestClass, "another_dynamic_prop")
        assert isinstance(getattr(TestClass, "dynamic_prop"), property)
        assert isinstance(getattr(TestClass, "another_dynamic_prop"), property)
        assert obj.dynamic_prop == "dynamic value"
        assert obj.another_dynamic_prop == "another dynamic value"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])