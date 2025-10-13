"""methodregistry_test.py
Unit tests for the MethodRegistry classes.

This module provides tests for the BaseMethodRegistry, BoundMethodRegistry, and MethodRegistry classes,
which are registries that hold methods. They inherit from FunctionRegistry and provide functionality
to store and retrieve methods by name, with proper binding behavior.
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
from typing import Any, Callable, Dict, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions.functionregistry import FunctionRegistry
from src.baseobjects.functions.methodregistry import BaseMethodRegistry, BoundMethodRegistry, MethodRegistry
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Functions #
def picklable_func() -> str:
    """A picklable function."""
    return "picklable_func"


def picklable_method(self) -> str:
    """A picklable method."""
    return "picklable_method"


def func1() -> str:
    return "func1"


def func2(arg: str) -> str:
    return f"func2_{arg}"


# Classes #
class RegistryTestObject:
    """A test object with methods for testing MethodRegistry."""

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
class TestBaseMethodRegistry(BaseObjectTestSuite):
    """Test suite for the BaseMethodRegistry class.

    This class tests the functionality of the BaseMethodRegistry class, which is a registry that holds methods.
    """

    # Attributes #
    TestClass: Type[BaseMethodRegistry] = BaseMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_methods(self) -> Dict[str, Callable]:
        """Create a dictionary of test methods.

        Returns:
            A dictionary mapping method names to methods.
        """
        return {
            "func1": func1,
            "func2": func2,
        }

    @pytest.fixture
    def test_object(self) -> BaseMethodRegistry:
        """Create an empty BaseMethodRegistry instance.

        Returns:
            An empty BaseMethodRegistry instance.
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
    def populated_registry(self, test_methods: Dict[str, Callable]) -> BaseMethodRegistry:
        """Create a BaseMethodRegistry populated with test methods.

        Args:
            test_methods: A fixture providing a dictionary of test methods.

        Returns:
            A BaseMethodRegistry populated with test methods.
        """
        return self.TestClass(methods=test_methods)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of BaseMethodRegistry can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, BaseMethodRegistry)
        assert isinstance(obj.data, FunctionRegistry)

    def test_copy(self, populated_registry: BaseMethodRegistry) -> None:
        """Test the copy behavior of BaseMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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

    def test_copy_method(self, populated_registry: BaseMethodRegistry) -> None:
        """Test the copy method behavior of BaseMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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

    def test_deepcopy(self, populated_registry: BaseMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy behavior of BaseMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_deepcopy_method(self, populated_registry: BaseMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of BaseMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_pickling(self, test_object: BaseMethodRegistry) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing an empty BaseMethodRegistry instance.
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
        """Test initialization of an empty BaseMethodRegistry.

        This test verifies that BaseMethodRegistry can be initialized without arguments.
        """
        registry = self.TestClass()
        assert len(registry) == 0
        assert isinstance(registry.data, FunctionRegistry)

    def test_init_with_methods(self, test_methods: Dict[str, Callable]) -> None:
        """Test initialization with methods.

        This test verifies that BaseMethodRegistry can be initialized with a dictionary of methods.

        Args:
            test_methods: A fixture providing a dictionary of test methods.
        """
        registry = self.TestClass(methods=test_methods)

        # Verify the methods were added to the registry
        assert len(registry) == len(test_methods)
        for name, func in test_methods.items():
            assert name in registry
            assert registry[name] == func
            if name == "func2":
                assert registry[name]("test") == func("test")
            else:
                assert registry[name]() == func()

    def test_init_with_object(self, test_instance: RegistryTestObject) -> None:
        """Test initialization with an object.

        This test verifies that BaseMethodRegistry can be initialized with an object whose
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

        This test verifies that BaseMethodRegistry can be initialized with multiple objects
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

    def test_construct(self, test_methods: Dict[str, Callable], test_instance: RegistryTestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the registry.

        Args:
            test_methods: A fixture providing a dictionary of test methods.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create a registry without initialization
        registry = self.TestClass(init=False)

        # Construct the registry
        registry.construct(methods=test_methods, object_=test_instance)

        # Verify the methods were added to the registry
        for name, func in test_methods.items():
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

    def test_func_property(self, populated_registry: BaseMethodRegistry) -> None:
        """Test the __func__ property.

        This test verifies that the __func__ property returns the underlying FunctionRegistry.

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
        """
        # Verify the __func__ property returns the data attribute
        assert populated_registry.__func__ is populated_registry.data
        assert isinstance(populated_registry.__func__, FunctionRegistry)

        # Test setting the __func__ property
        new_registry = FunctionRegistry()
        new_registry["new_func"] = lambda: "new_func"

        populated_registry.__func__ = new_registry

        # Verify the data attribute was updated
        assert populated_registry.data is new_registry
        assert "new_func" in populated_registry
        assert populated_registry["new_func"]() == "new_func"

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
            def __init__(self):
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

    def test_overriding_methods(self) -> None:
        """Test edge case where methods with the same name are provided."""

        # Create two methods with the same name
        def method1() -> str:
            return "method1_version1"

        def method1_override() -> str:
            return "method1_version2"

        # Create a registry with the first method
        registry = self.TestClass(methods={"method1": method1})

        # Verify the method was added to the registry
        assert len(registry) == 1
        assert "method1" in registry
        assert registry["method1"]() == "method1_version1"

        # Update the registry with the second method
        registry.update({"method1": method1_override})

        # Verify the method was overridden
        assert len(registry) == 1
        assert "method1" in registry
        assert registry["method1"]() == "method1_version2"

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

    def test_bound_registry_with_garbage_collected_instance(self) -> None:
        """Test edge case where the instance bound to a BoundMethodRegistry is garbage collected."""
        # Create a registry
        registry = BaseMethodRegistry()

        # Create a bound registry with a temporary instance
        bound_registry = BoundMethodRegistry(registry=registry, instance=RegistryTestObject())

        # The instance should be garbage collected after this point
        # Accessing __self__ should return None
        assert bound_registry.__self__ is None


class TestBoundMethodRegistry(BaseObjectTestSuite):
    """Test suite for the BoundMethodRegistry class.

    This class tests the functionality of the BoundMethodRegistry class, which is a registry that holds methods bound to
    an instance.
    """

    # Attributes #
    TestClass: Type[BoundMethodRegistry] = BoundMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_methods(self) -> Dict[str, Callable]:
        """Create a dictionary of test methods.

        Returns:
            A dictionary mapping method names to methods.
        """
        return {
            "func1": func1,
            "func2": func2,
        }

    @pytest.fixture
    def test_object(self) -> BoundMethodRegistry:
        """Create an empty BoundMethodRegistry instance.

        Returns:
            An empty BoundMethodRegistry instance.
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
    def base_registry(self, test_methods: Dict[str, Callable]) -> BaseMethodRegistry:
        """Create a BaseMethodRegistry populated with test methods.

        Args:
            test_methods: A fixture providing a dictionary of test methods.

        Returns:
            A BaseMethodRegistry populated with test methods.
        """
        return BaseMethodRegistry(methods=test_methods)

    @pytest.fixture
    def bound_registry(
        self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject
    ) -> BoundMethodRegistry:
        """Create a BoundMethodRegistry bound to a test instance.

        Args:
            base_registry: A fixture providing a BaseMethodRegistry.
            test_instance: A fixture providing a RegistryTestObject instance.

        Returns:
            A BoundMethodRegistry bound to the test instance.
        """
        return self.TestClass(registry=base_registry, instance=test_instance, owner=RegistryTestObject)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of BoundMethodRegistry can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, BoundMethodRegistry)
        assert isinstance(obj, BaseMethodRegistry)
        assert isinstance(obj.data, FunctionRegistry)

    def test_copy(self, bound_registry: BoundMethodRegistry) -> None:
        """Test the copy behavior of BoundMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy) and preserves the binding to the instance.

        Args:
            bound_registry: A fixture providing a BoundMethodRegistry bound to a test instance.
        """
        # Copy Object
        new = copy.copy(bound_registry)

        # Validate
        assert id(new) != id(bound_registry)
        assert isinstance(new, type(bound_registry))
        assert len(new) == len(bound_registry)
        for key in new:
            assert key in bound_registry
            assert new[key] == bound_registry[key]
            assert id(new[key]) == id(bound_registry[key])

        # Verify the instance binding was preserved
        assert new.__self__ is bound_registry.__self__
        assert new.__owner__ is bound_registry.__owner__

    def test_copy_method(self, bound_registry: BoundMethodRegistry) -> None:
        """Test the copy method behavior of BoundMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy) and preserves the binding to the instance.

        Args:
            bound_registry: A fixture providing a BoundMethodRegistry bound to a test instance.
        """
        # Copy Object
        new = bound_registry.copy()

        # Validate
        assert id(new) != id(bound_registry)
        assert isinstance(new, type(bound_registry))
        assert len(new) == len(bound_registry)
        for key in new:
            assert key in bound_registry
            assert new[key] == bound_registry[key]
            assert id(new[key]) == id(bound_registry[key])

        # Verify the instance binding was preserved
        assert new.__self__ is bound_registry.__self__
        assert new.__owner__ is bound_registry.__owner__

    def test_deepcopy(self, bound_registry: BoundMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy behavior of BoundMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied) and preserves the binding to the instance.

        Args:
            bound_registry: A fixture providing a BoundMethodRegistry bound to a test instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = copy.deepcopy(bound_registry, memo=memo)

        # Validate
        assert id(new) != id(bound_registry)
        assert isinstance(new, type(bound_registry))
        assert len(new) == len(bound_registry)
        for key in new:
            assert key in bound_registry
            assert new[key] == bound_registry[key]
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(bound_registry[key])

        # Verify the instance binding was preserved
        assert new.__self__ is not bound_registry.__self__
        assert new.__owner__ is bound_registry.__owner__

    def test_deepcopy_method(self, bound_registry: BoundMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of BoundMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied) and preserves the binding to the instance.

        Args:
            bound_registry: A fixture providing a BoundMethodRegistry bound to a test instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = bound_registry.deepcopy(memo=memo)

        # Validate
        assert id(new) != id(bound_registry)
        assert isinstance(new, type(bound_registry))
        assert len(new) == len(bound_registry)
        for key in new:
            assert key in bound_registry
            assert new[key] == bound_registry[key]
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(bound_registry[key])

        # Verify the instance binding was preserved
        assert new.__self__ is not bound_registry.__self__
        assert new.__owner__ is bound_registry.__owner__

    def test_pickling(self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly, preserving the binding to the
        instance.

        Args:
            base_registry: A fixture providing a BaseMethodRegistry.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Add the picklable function to the registry
        base_registry["picklable_method"] = picklable_method

        # Create a bound registry
        bound_registry = self.TestClass(registry=base_registry, instance=test_instance, owner=RegistryTestObject)

        # Pickle and Unpickle Object
        items = (bound_registry, test_instance)
        pickled = pickle.dumps(items)
        unpickled_registry, unpickled_instance = pickle.loads(pickled)

        # Validate
        assert unpickled_registry is not bound_registry
        assert isinstance(unpickled_registry, type(bound_registry))
        assert len(unpickled_registry) == len(bound_registry)
        assert "picklable_method" in unpickled_registry
        assert unpickled_registry["picklable_method"]() == "picklable_method"

        # Verify the instance binding was preserved
        assert unpickled_registry.__self__ is not bound_registry.__self__
        assert unpickled_registry.__owner__ is bound_registry.__owner__

    def test_init_with_registry_and_instance(
        self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject
    ) -> None:
        """Test initialization with a registry and instance.

        This test verifies that BoundMethodRegistry can be initialized with a registry and instance.

        Args:
            base_registry: A fixture providing a BaseMethodRegistry.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        bound_registry = self.TestClass(registry=base_registry, instance=test_instance, owner=RegistryTestObject)

        # Verify the registry was set correctly
        assert bound_registry.data is base_registry.data

        # Verify the instance was set correctly
        assert bound_registry.__self__ is test_instance

        # Verify the owner was set correctly
        assert bound_registry.__owner__ is RegistryTestObject

    def test_self_property(self, test_instance: RegistryTestObject) -> None:
        """Test the __self__ property.

        This test verifies that the __self__ property returns the bound instance.

        Args:
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create a bound registry
        bound_registry = self.TestClass(instance=test_instance)

        # Verify the __self__ property returns the bound instance
        assert bound_registry.__self__ is test_instance

        # Test setting the __self__ property
        new_instance = RegistryTestObject(name="new")
        bound_registry.__self__ = new_instance

        # Verify the bound instance was updated
        assert bound_registry.__self__ is new_instance

    def test_self_property_with_none(self) -> None:
        """Test the __self__ property with None.

        This test verifies that the __self__ property returns None when no instance is bound.
        """
        # Create a bound registry with no instance
        bound_registry = self.TestClass()

        # Verify the __self__ property returns None
        assert bound_registry.__self__ is None

        # Test setting the __self__ property to None
        bound_registry.__self__ = None

        # Verify the bound instance is still None
        assert bound_registry.__self__ is None

    def test_construct(self, base_registry: BaseMethodRegistry, test_instance: RegistryTestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the registry.

        Args:
            base_registry: A fixture providing a BaseMethodRegistry.
            test_instance: A fixture providing a RegistryTestObject instance.
        """
        # Create a registry without initialization
        bound_registry = self.TestClass(init=False)

        # Construct the registry
        bound_registry.construct(registry=base_registry, instance=test_instance, owner=RegistryTestObject)

        # Verify the registry was set correctly
        assert bound_registry.data is base_registry.data

        # Verify the instance was set correctly
        assert bound_registry.__self__ is test_instance

        # Verify the owner was set correctly
        assert bound_registry.__owner__ is RegistryTestObject


class TestMethodRegistry(BaseObjectTestSuite):
    """Test suite for the MethodRegistry class.

    This class tests the functionality of the MethodRegistry class, which is a registry
    that holds methods and implements the descriptor protocol.
    """

    # Attributes #
    TestClass: Type[MethodRegistry] = MethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_methods(self) -> Dict[str, Callable]:
        """Create a dictionary of test methods.

        Returns:
            A dictionary mapping method names to methods.
        """
        return {
            "func1": func1,
            "func2": func2,
        }

    @pytest.fixture
    def test_object(self) -> MethodRegistry:
        """Create an empty MethodRegistry instance.

        Returns:
            An empty MethodRegistry instance.
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
    def populated_registry(self, test_methods: Dict[str, Callable]) -> MethodRegistry:
        """Create a MethodRegistry populated with test methods.

        Args:
            test_methods: A fixture providing a dictionary of test methods.

        Returns:
            A MethodRegistry populated with test methods.
        """
        return self.TestClass(methods=test_methods)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of MethodRegistry can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, MethodRegistry)
        assert isinstance(obj, BaseMethodRegistry)
        assert isinstance(obj.data, FunctionRegistry)

    def test_copy(self, populated_registry: BaseMethodRegistry) -> None:
        """Test the copy behavior of BaseMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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

    def test_copy_method(self, populated_registry: BaseMethodRegistry) -> None:
        """Test the copy method behavior of BaseMethodRegistry.

        This test verifies that the copy method creates a new registry with references to the same methods
        (shallow copy).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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

    def test_deepcopy(self, populated_registry: BaseMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy behavior of BaseMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_deepcopy_method(self, populated_registry: BaseMethodRegistry, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of BaseMethodRegistry.

        This test verifies that the deepcopy method creates a new registry with references to the same methods
        (since methods are not deep-copied).

        Args:
            populated_registry: A fixture providing a populated BaseMethodRegistry instance.
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
            # Methods are not deep-copied, so the ids should be the same
            assert id(new[key]) == id(populated_registry[key])

    def test_pickling(self, test_object: BaseMethodRegistry) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing an empty BaseMethodRegistry instance.
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

    def test_descriptor_protocol(self, populated_registry: MethodRegistry, test_instance: RegistryTestObject) -> None:
        """Test the descriptor protocol.

        This test verifies that the __get__ method returns a BoundMethodRegistry when accessed through an instance.

        Args:
            populated_registry: A fixture providing a populated MethodRegistry instance.
            test_instance: A fixture providing a RegistryTestObject instance.
        """

        # Create a class with a MethodRegistry descriptor
        class DescriptorTest:
            registry = populated_registry

        # Create an instance of the class
        instance = DescriptorTest()

        # Access the descriptor through the instance
        bound_registry = instance.registry

        # Verify the result is a BoundMethodRegistry
        assert isinstance(bound_registry, BoundMethodRegistry)

        # Verify the registry is bound to the instance
        assert bound_registry.__self__ is instance

        # Verify the registry is bound to the correct owner
        assert bound_registry.__owner__ is DescriptorTest

        # Verify the registry has the same data as the original
        assert bound_registry.data is populated_registry.data


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
