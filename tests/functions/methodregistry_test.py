#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" methodregistry_test.py
Tests for the methodregistry.py module in the baseobjects package.
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
from typing import Callable, Dict, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions.methodregistry import BaseMethodRegistry, BoundMethodRegistry, MethodRegistry
from src.baseobjects.functions.functionregistry import FunctionRegistry
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestObject:
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


class TestClassWithMethodRegistry:
    """A test class with a MethodRegistry attribute."""

    methods = MethodRegistry()

    def __init__(self, name: str = "test") -> None:
        self.name = name

    def method1(self) -> str:
        """A test method."""
        return f"{self.name}_method1"

    def method2(self, arg: str) -> str:
        """Another test method."""
        return f"{self.name}_method2_{arg}"


class TestBaseMethodRegistry(ClassTest):
    """Test the BaseMethodRegistry class.

    This class tests the functionality of the BaseMethodRegistry class, which is an abstract
    registry that holds methods.
    """

    # Class Attributes #
    class_: Type[BaseMethodRegistry] = BaseMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_methods(self) -> Dict[str, Callable]:
        """Create a dictionary of test methods.

        Returns:
            A dictionary mapping method names to methods.
        """
        def func1() -> str:
            return "func1"

        def func2(arg: str) -> str:
            return f"func2_{arg}"

        return {
            "func1": func1,
            "func2": func2,
        }

    @pytest.fixture
    def test_object(self) -> TestObject:
        """Create a test object with methods.

        Returns:
            A TestObject instance.
        """
        return TestObject()

    @pytest.fixture
    def method_register(self) -> BaseMethodRegistry:
        """Create an empty BaseMethodRegistry instance.

        Returns:
            An empty BaseMethodRegistry instance.
        """
        return BaseMethodRegistry()

    # Tests
    def test_init_empty(self) -> None:
        """Test initialization of an empty BaseMethodRegistry.

        This test verifies that BaseMethodRegistry can be initialized without arguments.
        """
        register = BaseMethodRegistry()
        assert len(register) == 0
        assert isinstance(register.data, FunctionRegistry)

    def test_init_with_methods(self, test_methods: Dict[str, Callable]) -> None:
        """Test initialization with methods.

        This test verifies that BaseMethodRegistry can be initialized with a dictionary of methods.

        Args:
            test_methods: A fixture providing a dictionary of test methods.
        """
        register = BaseMethodRegistry(methods=test_methods)

        # Verify the methods were added to the registry
        assert len(register) == len(test_methods)
        for name, func in test_methods.items():
            assert name in register
            assert register[name] == func
            if name == "func2":
                assert register[name]("test") == func("test")
            else:
                assert register[name]() == func()

    def test_init_with_object(self, test_object: TestObject) -> None:
        """Test initialization with an object.

        This test verifies that BaseMethodRegistry can be initialized with an object whose
        methods will be added to the registry.

        Args:
            test_object: A fixture providing a TestObject instance.
        """
        register = BaseMethodRegistry(object_=test_object)

        # Verify the methods were added to the registry
        assert "method1" in register
        assert "method2" in register
        assert "static_method" in register
        assert "class_method" in register

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert register["method1"](test_object) == test_object.method1()
        assert register["method2"](test_object, "arg") == test_object.method2("arg")
        assert register["static_method"]() == TestObject.static_method()
        assert register["class_method"](TestObject) == TestObject.class_method()

    def test_func_property(self, method_register: BaseMethodRegistry) -> None:
        """Test the __func__ property.

        This test verifies that the __func__ property correctly gets and sets the FunctionRegistry.

        Args:
            method_register: A fixture providing an empty BaseMethodRegistry instance.
        """
        # Verify the default FunctionRegistry
        assert isinstance(method_register.__func__, FunctionRegistry)

        # Create a new FunctionRegistry
        new_register = FunctionRegistry()
        new_register["test"] = lambda: "test"

        # Set the FunctionRegistry
        method_register.__func__ = new_register

        # Verify the FunctionRegistry was set correctly
        assert method_register.__func__ is new_register
        assert "test" in method_register
        assert method_register["test"]() == "test"

    def test_construct(self, test_methods: Dict[str, Callable], test_object: TestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the registry.

        Args:
            test_methods: A fixture providing a dictionary of test methods.
            test_object: A fixture providing a TestObject instance.
        """
        # Create a registry without initialization
        register = BaseMethodRegistry(init=False)

        # Construct the registry
        register.construct(methods=test_methods, object_=test_object)

        # Verify the methods were added to the registry
        for name, func in test_methods.items():
            assert name in register
            assert register[name] == func
            if name == "func2":
                assert register[name]("test") == func("test")
            else:
                assert register[name]() == func()

        # Verify the methods were added to the registry
        assert "method1" in register
        assert "method2" in register
        assert "static_method" in register
        assert "class_method" in register

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert register["method1"](test_object) == test_object.method1()
        assert register["method2"](test_object, "arg") == test_object.method2("arg")
        assert register["static_method"]() == TestObject.static_method()
        assert register["class_method"](TestObject) == TestObject.class_method()


class TestBoundMethodRegistry(ClassTest):
    """Test the BoundMethodRegistry class.

    This class tests the functionality of the BoundMethodRegistry class, which is a
    BaseMethodRegistry that is bound to another object.
    """

    # Class Attributes #
    class_: Type[BoundMethodRegistry] = BoundMethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> TestObject:
        """Create a test object with methods.

        Returns:
            A TestObject instance.
        """
        return TestObject()

    @pytest.fixture
    def method_register(self, test_object: TestObject) -> BaseMethodRegistry:
        """Create a BaseMethodRegistry instance with methods from a test object.

        Args:
            test_object: A fixture providing a TestObject instance.

        Returns:
            A BaseMethodRegistry instance with methods from the test object.
        """
        return BaseMethodRegistry(object_=test_object)

    @pytest.fixture
    def bound_register(self, method_register: BaseMethodRegistry, test_object: TestObject) -> BoundMethodRegistry:
        """Create a BoundMethodRegistry instance.

        Args:
            method_register: A fixture providing a BaseMethodRegistry instance.
            test_object: A fixture providing a TestObject instance.

        Returns:
            A BoundMethodRegistry instance bound to the test object.
        """
        return BoundMethodRegistry(registry=method_register, instance=test_object, owner=TestObject)

    # Tests
    def test_init_empty(self) -> None:
        """Test initialization of an empty BoundMethodRegistry.

        This test verifies that BoundMethodRegistry can be initialized without arguments.
        """
        register = BoundMethodRegistry()
        assert len(register) == 0
        assert register.__self__ is None
        assert register.__owner__ is None

    def test_init_with_register_and_instance(self, method_register: BaseMethodRegistry, test_object: TestObject) -> None:
        """Test initialization with a registry and instance.

        This test verifies that BoundMethodRegistry can be initialized with a registry and instance.

        Args:
            method_register: A fixture providing a BaseMethodRegistry instance.
            test_object: A fixture providing a TestObject instance.
        """
        bound_register = BoundMethodRegistry(registry=method_register, instance=test_object, owner=TestObject)

        # Verify the registry was set correctly
        assert bound_register.data is method_register.data

        # Verify the instance and owner were set correctly
        assert bound_register.__self__ is test_object
        assert bound_register.__owner__ is TestObject

    def test_self_property(self, bound_register: BoundMethodRegistry, test_object: TestObject) -> None:
        """Test the __self__ property.

        This test verifies that the __self__ property correctly gets and sets the bound instance.

        Args:
            bound_register: A fixture providing a BoundMethodRegistry instance.
            test_object: A fixture providing a TestObject instance.
        """
        # Verify the default bound instance
        assert bound_register.__self__ is test_object

        # Create a new test object
        new_object = TestObject(name="new")

        # Set the bound instance
        bound_register.__self__ = new_object

        # Verify the bound instance was set correctly
        assert bound_register.__self__ is new_object

    def test_construct(self, method_register: BaseMethodRegistry, test_object: TestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the bound registry.

        Args:
            method_register: A fixture providing a BaseMethodRegistry instance.
            test_object: A fixture providing a TestObject instance.
        """
        # Create a bound registry without initialization
        bound_register = BoundMethodRegistry(init=False)

        # Construct the bound registry
        bound_register.construct(registry=method_register, instance=test_object, owner=TestObject)

        # Verify the registry was set correctly
        assert bound_register.data is method_register.data

        # Verify the instance and owner were set correctly
        assert bound_register.__self__ is test_object
        assert bound_register.__owner__ is TestObject


class TestMethodRegistry(ClassTest):
    """Test the MethodRegistry class.

    This class tests the functionality of the MethodRegistry class, which is a registry
    that holds functions and binds appropriately.
    """

    # Class Attributes #
    class_: Type[MethodRegistry] = MethodRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_class_instance(self) -> TestClassWithMethodRegistry:
        """Create an instance of a class with a MethodRegistry attribute.

        Returns:
            An instance of TestClassWithMethodRegistry.
        """
        return TestClassWithMethodRegistry()

    # Tests
    def test_init_empty(self) -> None:
        """Test initialization of an empty MethodRegistry.

        This test verifies that MethodRegistry can be initialized without arguments.
        """
        register = MethodRegistry()
        assert len(register) == 0
        assert isinstance(register.data, FunctionRegistry)

    def test_get(self, test_class_instance: TestClassWithMethodRegistry) -> None:
        """Test the __get__ method.

        This test verifies that the __get__ method returns a BoundMethodRegistry bound to the instance.

        Args:
            test_class_instance: A fixture providing an instance of TestClassWithMethodRegistry.
        """
        # Access the methods attribute through the descriptor protocol
        bound_methods = test_class_instance.methods

        # Verify the bound methods is a BoundMethodRegistry
        assert isinstance(bound_methods, BoundMethodRegistry)

        # Verify the bound methods is bound to the instance
        assert bound_methods.__self__ is test_class_instance
        assert bound_methods.__owner__ is TestClassWithMethodRegistry

    def test_descriptor_usage(self) -> None:
        """Test using MethodRegistry as a descriptor.

        This test verifies that MethodRegistry can be used as a descriptor to create
        bound method registers.
        """
        # Create a class with a MethodRegistry attribute
        class TestClass:
            methods = MethodRegistry(methods={"test": lambda self: f"{self.name}_test"})

            def __init__(self, name: str) -> None:
                self.name = name

        # Create instances of the class
        instance1 = TestClass("instance1")
        instance2 = TestClass("instance2")

        # Access the methods attribute through the descriptor protocol
        bound_methods1 = instance1.methods
        bound_methods2 = instance2.methods

        # Verify the bound methods are different objects
        assert bound_methods1 is not bound_methods2

        # Verify the bound methods are bound to the correct instances
        assert bound_methods1.__self__ is instance1
        assert bound_methods2.__self__ is instance2

        # Verify the methods work correctly
        assert "test" in bound_methods1
        assert "test" in bound_methods2
        assert bound_methods1["test"](instance1) == "instance1_test"
        assert bound_methods2["test"](instance2) == "instance2_test"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
