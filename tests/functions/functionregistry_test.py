"""functionregistry_test.py
Unit tests for the FunctionRegistry class.

This module provides tests for the FunctionRegistry class, which is a registry that holds functions.
It inherits from BaseDict and provides functionality to store and retrieve functions by name.
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
from collections.abc import Callable
from typing import Any, Dict, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions.functionregistry import FunctionRegistry
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Functions #
def picklable_func() -> str:
    """A picklable function."""
    return "picklable_func"


def func1() -> str:
    return "func1"


def func2(arg: str) -> str:
    return f"func2_{arg}"


# Classes #
class RegistryTestObject:
    """A test object with functions for testing FunctionRegistry."""

    def __init__(self, name: str = "test") -> None:
        self.name = name

    def method1(self) -> str:
        """A test method."""
        return f"{self.name}_method1"

    def method2(self, arg: str) -> str:
        """Another test method."""
        return f"{self.name}_method2_{arg}"

    @staticmethod
    def static_method() -> str:
        """A static method."""
        return "static_method"

    @classmethod
    def class_method(cls) -> str:
        """A class method."""
        return f"{cls.__name__}_class_method"


# Tests #
class TestFunctionRegistry(BaseObjectTestSuite):
    """Test suite for the FunctionRegistry class.

    This class tests the functionality of the FunctionRegistry class, which is a registry
    that holds functions.
    """

    # Attributes #
    TestClass: type[FunctionRegistry] = FunctionRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_functions(self) -> dict[str, Callable]:
        """Create a dictionary of test functions.

        Returns:
            A dictionary mapping function names to functions.
        """
        return {
            "func1": func1,
            "func2": func2,
        }

    @pytest.fixture
    def test_object(self) -> FunctionRegistry:
        """Create an empty FunctionRegistry instance.

        Returns:
            An empty FunctionRegistry instance.
        """
        return self.TestClass()

    @pytest.fixture
    def test_instance(self) -> RegistryTestObject:
        """Create a test object with methods.

        Returns:
            A RegistryTestObject instance.
        """
        return RegistryTestObject()

    @pytest.fixture
    def populated_registry(self, test_functions: dict[str, Callable]) -> FunctionRegistry:
        """Create a FunctionRegistry populated with test functions.

        Args:
            test_functions: A fixture providing a dictionary of test functions.

        Returns:
            A FunctionRegistry populated with test functions.
        """
        return self.TestClass(functions=test_functions)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of FunctionRegistry can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, FunctionRegistry)
        assert isinstance(obj.data, dict)

    def test_copy(self, populated_registry: FunctionRegistry) -> None:
        """Test the copy behavior of FunctionRegistry.

        This test verifies that the copy method creates a new registry with references to the same functions
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated FunctionRegistry instance.
        """
        # Copy Object
        new = copy.copy(populated_registry)

        # Validate
        assert id(new) != id(populated_registry)
        assert isinstance(new, type(populated_registry))
        assert len(new) == len(populated_registry)
        for key in new:
            assert key in populated_registry
            assert new[key] == populated_registry[key]
            assert id(new[key]) == id(populated_registry[key])

    def test_copy_method(self, populated_registry: FunctionRegistry) -> None:
        """Test the copy method of FunctionRegistry.

        This test verifies that the copy method creates a new registry with references to the same functions
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated FunctionRegistry instance.
        """
        # Copy Object
        new = populated_registry.copy()

        # Validate
        assert id(new) != id(populated_registry)
        assert isinstance(new, type(populated_registry))
        assert len(new) == len(populated_registry)
        for key in new:
            assert key in populated_registry
            assert new[key] == populated_registry[key]
            assert id(new[key]) == id(populated_registry[key])

    def test_deepcopy(self, populated_registry: FunctionRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy behavior of FunctionRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same functions
        (since functions are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated FunctionRegistry instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = copy.deepcopy(populated_registry, memo=memo)

        # Validate
        assert id(new) != id(populated_registry)
        assert isinstance(new, type(populated_registry))
        assert len(new) == len(populated_registry)
        for key in new:
            assert key in populated_registry
            assert new[key] == populated_registry[key]
            # Functions are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_deepcopy_method(self, populated_registry: FunctionRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy method of FunctionRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same functions
        (since functions are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated FunctionRegistry instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = populated_registry.deepcopy(memo=memo)

        # Validate
        assert id(new) != id(populated_registry)
        assert isinstance(new, type(populated_registry))
        assert len(new) == len(populated_registry)
        for key in new:
            assert key in populated_registry
            assert new[key] == populated_registry[key]
            # Functions are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_pickling(self, test_object: FunctionRegistry) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing an empty FunctionRegistry instance.
        """
        # Add the picklable function to the registry
        test_object["picklable_func"] = picklable_func

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, type(test_object))
        assert len(unpickled) == len(test_object)
        assert "picklable_func" in unpickled
        assert unpickled["picklable_func"]() == "picklable_func"

    def test_init_empty(self) -> None:
        """Test initialization of an empty FunctionRegistry.

        This test verifies that FunctionRegistry can be initialized without arguments.
        """
        registry = self.TestClass()
        assert len(registry) == 0

    def test_init_with_functions(self, test_functions: dict[str, Callable]) -> None:
        """Test initialization with functions.

        This test verifies that FunctionRegistry can be initialized with a dictionary of functions.

        Args:
            test_functions: A fixture providing a dictionary of test functions.
        """
        registry = self.TestClass(functions=test_functions)

        # Verify the functions were added to the registry
        assert len(registry) == len(test_functions)
        for name, func in test_functions.items():
            assert name in registry
            assert registry[name] == func
            if name == "func2":
                assert registry[name]("test") == func("test")
            else:
                assert registry[name]() == func()

    def test_init_with_object(self, test_instance: RegistryTestObject) -> None:
        """Test initialization with an object.

        This test verifies that FunctionRegistry can be initialized with an object whose
        methods will be added to the registry.

        Args:
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        registry = self.TestClass(object_=test_instance)

        # Verify the methods were added to the registry
        assert "method1" in registry
        assert "method2" in registry
        assert "static_method" in registry
        assert "class_method" in registry

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert registry["method1"](test_instance) == test_instance.method1()
        assert registry["method2"](test_instance, "arg") == test_instance.method2("arg")
        assert registry["static_method"]() == RegistryTestObject.static_method()
        assert registry["class_method"](RegistryTestObject) == RegistryTestObject.class_method()

    def test_init_with_objects(self, test_instance: RegistryTestObject) -> None:
        """Test initialization with multiple objects.

        This test verifies that FunctionRegistry can be initialized with multiple objects
        whose methods will be added to the registry.

        Args:
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create another test object
        another_object = RegistryTestObject(name="another")

        registry = self.TestClass(objects=[test_instance, another_object])

        # Verify the methods were added to the registry
        assert "method1" in registry
        assert "method2" in registry
        assert "static_method" in registry
        assert "class_method" in registry

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert registry["method1"](test_instance) == test_instance.method1()
        assert registry["method2"](test_instance, "arg") == test_instance.method2("arg")
        assert registry["static_method"]() == RegistryTestObject.static_method()
        assert registry["class_method"](RegistryTestObject) == RegistryTestObject.class_method()

    def test_update_from_object(self, test_object: FunctionRegistry, test_instance: RegistryTestObject) -> None:
        """Test updating the registry from an object.

        This test verifies that the registry can be updated with methods from an object.

        Args:
            test_object: A fixture providing an empty FunctionRegistry instance.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Update the registry from the test object
        test_object.update_from_object(test_instance)

        # Verify the methods were added to the registry
        assert "method1" in test_object
        assert "method2" in test_object
        assert "static_method" in test_object
        assert "class_method" in test_object

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert test_object["method1"](test_instance) == test_instance.method1()
        assert test_object["method2"](test_instance, "arg") == test_instance.method2("arg")
        assert test_object["static_method"]() == RegistryTestObject.static_method()
        assert test_object["class_method"](RegistryTestObject) == RegistryTestObject.class_method()

    def test_update_from_objects(self, test_object: FunctionRegistry, test_instance: RegistryTestObject) -> None:
        """Test updating the registry from multiple objects.

        This test verifies that the registry can be updated with methods from multiple objects.

        Args:
            test_object: A fixture providing an empty FunctionRegistry instance.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create another test object
        another_object = RegistryTestObject(name="another")

        # Update the registry from the test objects
        test_object.update_from_objects(test_instance, another_object)

        # Verify the methods were added to the registry
        assert "method1" in test_object
        assert "method2" in test_object
        assert "static_method" in test_object
        assert "class_method" in test_object

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert test_object["method1"](test_instance) == test_instance.method1()
        assert test_object["method2"](test_instance, "arg") == test_instance.method2("arg")
        assert test_object["static_method"]() == RegistryTestObject.static_method()
        assert test_object["class_method"](RegistryTestObject) == RegistryTestObject.class_method()

    def test_construct(self, test_functions: dict[str, Callable], test_instance: RegistryTestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the registry.

        Args:
            test_functions: A fixture providing a dictionary of test functions.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create a registry without initialization
        registry = self.TestClass(init=False)

        # Construct the registry
        registry.construct(functions=test_functions, object_=test_instance)

        # Verify the functions were added to the registry
        for name, func in test_functions.items():
            assert name in registry
            assert registry[name] == func
            if name == "func2":
                assert registry[name]("test") == func("test")
            else:
                assert registry[name]() == func()

        # Verify the methods were added to the registry
        assert "method1" in registry
        assert "method2" in registry
        assert "static_method" in registry
        assert "class_method" in registry

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert registry["method1"](test_instance) == test_instance.method1()
        assert registry["method2"](test_instance, "arg") == test_instance.method2("arg")
        assert registry["static_method"]() == RegistryTestObject.static_method()
        assert registry["class_method"](RegistryTestObject) == RegistryTestObject.class_method()

    def test_empty_object(self) -> None:
        """Test edge case where an object with no methods is provided."""

        # Create an object with no methods
        class EmptyObject:
            pass

        empty_obj = EmptyObject()

        # Create a registry with the empty object
        registry = self.TestClass(object_=empty_obj)

        # Verify no custom methods were added to the registry
        # Note: The registry may contain built-in methods from object
        assert not any(name.startswith("custom_") for name in registry)

    def test_non_callable_attributes(self) -> None:
        """Test edge case where an object has non-callable attributes."""

        # Create an object with non-callable attributes
        class ObjectWithAttributes:
            def __init__(self) -> None:
                self.attr1 = "value1"
                self.attr2 = 42
                self.attr3 = [1, 2, 3]

            def custom_method(self) -> str:
                return "custom_method"

        obj = ObjectWithAttributes()

        # Create a registry with the object
        registry = self.TestClass(object_=obj)

        # Verify the custom method was added to the registry
        assert "custom_method" in registry
        assert registry["custom_method"](obj) == "custom_method"

        # Verify non-callable attributes were not added
        assert "attr1" not in registry
        assert "attr2" not in registry
        assert "attr3" not in registry

    def test_overriding_functions(self) -> None:
        """Test edge case where functions with the same name are provided."""

        # Create two functions with the same name
        def func1() -> str:
            return "func1_version1"

        def func1_override() -> str:
            return "func1_version2"

        # Create a registry with the first function
        registry = self.TestClass(functions={"func1": func1})

        # Verify the function was added to the registry
        assert len(registry) == 1
        assert "func1" in registry
        assert registry["func1"]() == "func1_version1"

        # Update the registry with the second function
        registry.update({"func1": func1_override})

        # Verify the function was overridden
        assert len(registry) == 1
        assert "func1" in registry
        assert registry["func1"]() == "func1_version2"

    def test_object_with_same_method_names(self) -> None:
        """Test edge case where multiple objects with the same method names are provided."""

        # Create two objects with the same method names
        class Object1:
            def custom_method(self) -> str:
                return "custom_method_from_object1"

        class Object2:
            def custom_method(self) -> str:
                return "custom_method_from_object2"

        obj1 = Object1()
        obj2 = Object2()

        # Create a registry with both objects
        registry = self.TestClass(objects=[obj1, obj2])

        # Verify the method was added to the registry (the last one should override)
        assert "custom_method" in registry
        # The method from obj2 should be used since it was added last
        assert registry["custom_method"](obj2) == "custom_method_from_object2"
        # The method from obj1 should be overridden
        assert registry["custom_method"](obj1) != "custom_method_from_object1"

    def test_object_with_property(self) -> None:
        """Test edge case where an object has a property."""

        # Create an object with a property
        class ObjectWithProperty:
            @property
            def prop(self) -> str:
                return "property_value"

            def custom_method(self) -> str:
                return "custom_method_value"

        obj = ObjectWithProperty()

        # Create a registry with the object
        registry = self.TestClass(object_=obj)

        # Verify the custom method was added to the registry
        assert "custom_method" in registry
        assert registry["custom_method"](obj) == "custom_method_value"

        # Verify the property was not added to the registry
        assert "prop" not in registry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
