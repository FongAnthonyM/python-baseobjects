#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" functionregistry_test.py
Tests for the functionregistry.py module in the baseobjects package.
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
from src.baseobjects.functions.functionregistry import FunctionRegistry
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestObject:
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


class TestFunctionRegistry(ClassTest):
    """Test the FunctionRegistry class.

    This class tests the functionality of the FunctionRegistry class, which is a registry
    that holds functions.
    """

    # Class Attributes #
    class_: Type[FunctionRegistry] = FunctionRegistry

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_functions(self) -> Dict[str, Callable]:
        """Create a dictionary of test functions.

        Returns:
            A dictionary mapping function names to functions.
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
    def function_register(self) -> FunctionRegistry:
        """Create an empty FunctionRegistry instance.

        Returns:
            An empty FunctionRegistry instance.
        """
        return FunctionRegistry()

    # Tests
    def test_init_empty(self) -> None:
        """Test initialization of an empty FunctionRegistry.

        This test verifies that FunctionRegistry can be initialized without arguments.
        """
        register = FunctionRegistry()
        assert len(register) == 0

    def test_init_with_functions(self, test_functions: Dict[str, Callable]) -> None:
        """Test initialization with functions.

        This test verifies that FunctionRegistry can be initialized with a dictionary of functions.

        Args:
            test_functions: A fixture providing a dictionary of test functions.
        """
        register = FunctionRegistry(functions=test_functions)

        # Verify the functions were added to the registry
        assert len(register) == len(test_functions)
        for name, func in test_functions.items():
            assert name in register
            assert register[name] == func
            if name == "func2":
                assert register[name]("test") == func("test")
            else:
                assert register[name]() == func()

    def test_init_with_object(self, test_object: TestObject) -> None:
        """Test initialization with an object.

        This test verifies that FunctionRegistry can be initialized with an object whose
        methods will be added to the registry.

        Args:
            test_object: A fixture providing a TestObject instance.
        """
        register = FunctionRegistry(object_=test_object)

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

    def test_init_with_objects(self, test_object: TestObject) -> None:
        """Test initialization with multiple objects.

        This test verifies that FunctionRegistry can be initialized with multiple objects
        whose methods will be added to the registry.

        Args:
            test_object: A fixture providing a TestObject instance.
        """
        # Create another test object
        another_object = TestObject(name="another")

        register = FunctionRegistry(objects=[test_object, another_object])

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

    def test_update_from_object(self, function_register: FunctionRegistry, test_object: TestObject) -> None:
        """Test updating the registry from an object.

        This test verifies that the registry can be updated with methods from an object.

        Args:
            function_register: A fixture providing an empty FunctionRegistry instance.
            test_object: A fixture providing a TestObject instance.
        """
        # Update the registry from the test object
        function_register.update_from_object(test_object)

        # Verify the methods were added to the registry
        assert "method1" in function_register
        assert "method2" in function_register
        assert "static_method" in function_register
        assert "class_method" in function_register

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert function_register["method1"](test_object) == test_object.method1()
        assert function_register["method2"](test_object, "arg") == test_object.method2("arg")
        assert function_register["static_method"]() == TestObject.static_method()
        assert function_register["class_method"](TestObject) == TestObject.class_method()

    def test_update_from_objects(self, function_register: FunctionRegistry, test_object: TestObject) -> None:
        """Test updating the registry from multiple objects.

        This test verifies that the registry can be updated with methods from multiple objects.

        Args:
            function_register: A fixture providing an empty FunctionRegistry instance.
            test_object: A fixture providing a TestObject instance.
        """
        # Create another test object
        another_object = TestObject(name="another")

        # Update the registry from the test objects
        function_register.update_from_objects(test_object, another_object)

        # Verify the methods were added to the registry
        assert "method1" in function_register
        assert "method2" in function_register
        assert "static_method" in function_register
        assert "class_method" in function_register

        # Verify the methods work correctly
        # Note: These are unbound methods, so we need to pass self for instance methods
        assert function_register["method1"](test_object) == test_object.method1()
        assert function_register["method2"](test_object, "arg") == test_object.method2("arg")
        assert function_register["static_method"]() == TestObject.static_method()
        assert function_register["class_method"](TestObject) == TestObject.class_method()

    def test_construct(self, test_functions: Dict[str, Callable], test_object: TestObject) -> None:
        """Test the construct method.

        This test verifies that the construct method correctly sets up the registry.

        Args:
            test_functions: A fixture providing a dictionary of test functions.
            test_object: A fixture providing a TestObject instance.
        """
        # Create a registry without initialization
        register = FunctionRegistry(init=False)

        # Construct the registry
        register.construct(functions=test_functions, object_=test_object)

        # Verify the functions were added to the registry
        for name, func in test_functions.items():
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
