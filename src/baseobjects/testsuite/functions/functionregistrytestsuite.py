"""functionregistrytestsuite.py
Base test suite for ~baseobjects.functions.FunctionRegistry and its subclasses.

This module contains the base test suite for ~baseobjects.functions.FunctionRegistry and its subclasses.
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
from collections.abc import Callable
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import FunctionRegistry
from ..bases import BaseDictTestSuite


# Definitions #
# Helper Functions #
def func1() -> str:
    """A test function.

    Returns:
        The string 'func1'.
    """
    return "func1"


def func2(arg: str) -> str:
    """Another test function.

    Returns:
        The string 'func2' followed by the argument.
    """
    return f"func2 {arg}"


# Helper Classes #
class RegistryTestObject:
    """A test class with methods to register."""

    def __init__(self, name: str = "test") -> None:
        """Initializes the RegistryTestObject."""
        self.name = name

    def method1(self) -> str:
        """A test method.

        Returns:
            The string 'method1'.
        """
        return "method1"

    def method2(self, arg: str) -> str:
        """Another test method.

        Returns:
            The string 'method2' followed by the argument.
        """
        return f"method2 {arg}"

    @staticmethod
    def static_method() -> str:
        """A static method.

        Returns:
            The string 'static_method'.
        """
        return "static_method"

    @classmethod
    def class_method(cls) -> str:
        """A class method.

        Returns:
            The string 'class_method'.
        """
        return "class_method"


# Classes #
class FunctionRegistryTestSuite(BaseDictTestSuite):
    """Base test suite for children of ~baseobjects.functions.FunctionRegistry.

    This class provides common test functionality for child classes of ~baseobjects.functions.FunctionRegistry.
    """

    UnitTestClass: type[FunctionRegistry]

    # Fixtures #
    @pytest.fixture
    def test_functions(self) -> dict[str, Callable[..., Any]]:
        """Creates a dictionary of test functions.

        Returns:
            dict: A dictionary of test functions.
        """
        return {"func1": func1, "func2": func2}

    @pytest.fixture
    def test_instance(self) -> RegistryTestObject:
        """Creates a test object instance.

        Returns:
            RegistryTestObject: An instance of the test object.
        """
        return RegistryTestObject()

    @pytest.fixture
    def test_object(self) -> FunctionRegistry:
        """Creates a test object (empty).

        Returns:
            FunctionRegistry: A test object instance.
        """
        return self.UnitTestClass()

    # Tests #
    def test_init_with_functions(self, test_functions: dict[str, Callable[..., Any]]) -> None:
        """Tests initialization with functions.

        Args:
            test_functions: A fixture providing test functions.
        """
        registry = self.UnitTestClass(test_functions)
        assert len(registry) == len(test_functions)
        for name, func in test_functions.items():
            assert name in registry
            assert registry[name] is func

    def test_init_with_object(self, test_instance: RegistryTestObject) -> None:
        """Tests initialization with an object.

        Args:
            test_instance: A fixture providing a test object instance.
        """
        registry = self.UnitTestClass(object_=test_instance)

        # Should contain methods of the object
        assert "method1" in registry
        assert "method2" in registry
        # method1 is bound method? No, FunctionRegistry stores UNBOUND functions by default?
        # FunctionRegistry.update_from_object implementation uses getattr.
        # If accessing obj.method1, it returns bound method.
        # It then checks if it has __func__ and uses that if available?
        # Code: func = ... attr.__func__ if hasattr(attr, "__func__") else attr
        # Bound methods have __func__. So it stores the UNBOUND function.
        # So registry["method1"] should be UNBOUND function.
        # RegistryTestObject.method1 is unbound (function).
        assert registry["method1"] == RegistryTestObject.method1
        assert registry["method2"] == RegistryTestObject.method2

    def test_update_from_object(self, test_object: FunctionRegistry, test_instance: RegistryTestObject) -> None:
        """Tests updating from an object.

        Args:
            test_object: A fixture providing a FunctionRegistry.
            test_instance: A fixture providing a test object instance.
        """
        test_object.update_from_object(test_instance)

        assert "method1" in test_object
        assert test_object["method1"] == RegistryTestObject.method1

    def test_non_callable_attributes(self) -> None:
        """Tests that non-callable attributes are ignored."""

        class ObjectWithAttributes:
            def __init__(self) -> None:
                """Initializes ObjectWithAttributes."""
                self.attr = "value"

            def custom_method(self) -> None:
                pass

        obj = ObjectWithAttributes()
        registry = self.UnitTestClass(object_=obj)

        assert "custom_method" in registry
        assert "attr" not in registry

    # Overrides #
    @pytest.fixture
    def populated_test_dict(self, test_functions: dict[str, Callable[..., Any]]) -> FunctionRegistry:
        """Creates a populated test dictionary for use in tests.

        Returns:
            FunctionRegistry: A populated instance of the test class.
        """
        return self.UnitTestClass(test_functions)

    def test_dict_initialization(self) -> None:
        """Tests initialization of BaseDict with a dictionary."""
        # Initializes with a dictionary
        init_dict = {"func1": func1, "func2": func2}
        test_dict = self.UnitTestClass(init_dict)  # type: ignore[arg-type]

        # Validate
        assert len(test_dict) == 2
        assert test_dict["func1"] is func1
        assert test_dict["func2"] is func2

    def test_dict_initialization_with_kwargs(self) -> None:
        """Tests initialization of BaseDict with keyword arguments."""
        # Initializes with keyword arguments
        test_dict = self.UnitTestClass(func1=func1, func2=func2)

        # Validate
        assert len(test_dict) == 2
        assert test_dict["func1"] is func1
        assert test_dict["func2"] is func2

    def test_dict_set_item(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests setting items in BaseDict."""
        test_object["func1"] = func1
        assert len(test_object) == 1
        assert test_object["func1"] is func1

    def test_dict_update(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests updating BaseDict with multiple items."""
        test_object.update({"func1": func1, "func2": func2})
        assert len(test_object) == 2
        assert test_object["func1"] is func1
        assert test_object["func2"] is func2

    def test_dict_get(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests getting items from BaseDict."""
        test_object["func1"] = func1
        assert test_object.get("func1") is func1
        assert test_object.get("nonexistent", func2) is func2

    def test_dict_pop(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict."""
        test_object["func1"] = func1
        test_object["func2"] = func2

        popped = test_object.pop("func2")
        assert popped is func2
        assert len(test_object) == 1
        assert "func2" not in test_object

    def test_dict_popitem(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests popping an arbitrary item from BaseDict."""
        test_object["func1"] = func1
        test_object["func3"] = func2

        key, value = test_object.popitem()
        assert len(test_object) == 1
        assert key in ["func1", "func3"]
        assert value in [func1, func2]

    def test_dict_clear(self, test_object: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests clearing BaseDict."""
        test_object["func1"] = func1
        test_object["func2"] = func2

        test_object.clear()
        assert len(test_object) == 0

    def test_dict_iteration(self, populated_test_dict: FunctionRegistry) -> None:  # type: ignore[override]
        """Tests iteration over BaseDict."""
        # Test keys
        keys = list(populated_test_dict.keys())
        assert len(keys) == 2
        assert "func1" in keys
        assert "func2" in keys
