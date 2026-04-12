"""functionmultiplexertestsuite.py
Base test suite for ~baseobjects.functions.FunctionMultiplexer and its subclasses.

This module contains the base test suite for ~baseobjects.functions.FunctionMultiplexer and its subclasses.
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
# from typing import

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import CallableMultiplexer, FunctionMultiplexer
from .callablemultiplexertestsuite import CallableMultiplexerTestObject, CallableMultiplexerTestSuite


# Classes #
class FunctionMultiplexerTestSuite(CallableMultiplexerTestSuite):
    """Base test suite for children of ~baseobjects.functions.FunctionMultiplexer.

    This class provides common test functionality for child classes of ~baseobjects.functions.FunctionMultiplexer.
    """

    UnitTestClass: type[FunctionMultiplexer]

    # Tests #
    # Magic Methods #
    def test_add_method(
        self,
        test_multiplexer: CallableMultiplexer,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> None:
        """Tests adding a method to the registry.

        For FunctionMultiplexer, methods are added as unbound functions and NOT bound upon call.
        """
        # Adds method
        test_multiplexer.add_method("method1", test_object_instance.method1)

        # Select
        test_multiplexer.select("method1")

        # Binds to instance (should have NO effect on call for FunctionMultiplexer)
        test_multiplexer.bind_self(test_object_instance)

        # Calls with instance as argument (manual binding)
        assert test_multiplexer(test_object_instance, 3) == 13

        # Calls without instance should fail (missing argument)
        with pytest.raises(TypeError):
            test_multiplexer(3)

    def test_add_select_method(
        self,
        test_multiplexer: CallableMultiplexer,
        test_object_instance: CallableMultiplexerTestObject,
    ) -> None:
        """Tests adding and selecting a method in one step.

        For FunctionMultiplexer, methods are added as unbound functions and NOT bound upon call.
        """
        # Adds and select method
        test_multiplexer.add_select_method("method1", test_object_instance.method1)

        # Verifies it's selected
        assert test_multiplexer.selected == "method1"

        # Calls with instance as argument
        assert test_multiplexer(test_object_instance, 3) == 13

    # Functionality #
    def test_descriptor_protocol(self, test_method_object: FunctionMultiplexer) -> None:  # type: ignore[override]
        """Tests the descriptor protocol for FunctionMultiplexer.

        FunctionMultiplexer can be bound, but it does NOT use the bound instance in __call__.
        So we must pass the instance explicitly if the underlying function requires it.
        """

        class BindTarget:
            new_method = test_method_object

            def __init__(self, value: int = 10) -> None:
                self.value = value

            def method1(self, x: int) -> int:
                return self.value + x

        instance = BindTarget()
        bound_multiplexer = instance.new_method

        # Verifies it returns the multiplexer (bound to instance)
        assert bound_multiplexer is test_method_object
        assert bound_multiplexer.__self__ is instance

        # Select method from the bound instance
        bound_multiplexer.select("method1")

        # Calls with instance as argument (manual binding required for FunctionMultiplexer)
        assert bound_multiplexer(instance, 3) == 13

    def test_object_method_selection(self, test_multiplexer_with_object: FunctionMultiplexer) -> None:  # type: ignore[override]
        """Tests selecting methods from the bound object.

        For FunctionMultiplexer, we must pass the instance explicitly.
        """
        # Select method1
        test_multiplexer_with_object.select("method1")
        instance = test_multiplexer_with_object.__self__
        assert test_multiplexer_with_object(instance, 3) == 13

        # Select method2
        test_multiplexer_with_object.select("method2")
        assert test_multiplexer_with_object(instance, 3) == 30
