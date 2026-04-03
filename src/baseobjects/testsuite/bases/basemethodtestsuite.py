"""basemethodtestsuite.py
Base class for test suites which test BaseMethod and its subclasses.

This module provides a base test suite for testing the BaseMethod class and its subclasses. It defines abstract methods
for testing the core functionality of method objects, including binding to instances, weak references, binding to
attributes, and non-binding methods. It inherits from BaseMethodTestSuite to include tests for the callable behavior of
methods.
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
import asyncio
import copy
import inspect
import pickle
from abc import abstractmethod
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseMethod
from .basecallabletestsuite import BaseCallableTestSuite


# Definitions #
# Classes #
class BaseMethodTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test BaseMethod and its subclasses.

    This class provides common functionality for test suites that test method objects, including fixtures and
    test methods for verifying the behavior of BaseMethod objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseMethod or a subclass.
    """

    # Attributes #
    UnitTestClass: type[BaseMethod]
    BindTargetClass: type[Any]

    # Fixtures #
    @pytest.fixture
    def test_object(self, test_method_object: BaseMethod, *args: Any, **kwargs: Any) -> BaseMethod:
        """Creates a test object.

        Args:
            test_method_object: A fixture providing a BaseMethod instance.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            BaseMethod: A test object instance.
        """
        return test_method_object

    # Tests #
    # Magic Methods #
    def test_call(self, test_method_object: BaseMethod) -> None:  # type: ignore[override]
        """Tests that the method object can be called and correctly delegates to the wrapped method.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Creates a bind target
        bind_target = self.create_bind_target()

        # Binds the method to the target
        test_method_object.__self__ = bind_target

        # Calls the method
        result = test_method_object(3)

        # Verifies it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Calls with different arguments
        result = test_method_object(3, 4)

        # Verifies it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    def test_call_wrapped(self, test_method_object: BaseMethod) -> None:  # type: ignore[override]
        """Tests that the wrapped method can be called directly.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Creates a bind target
        bind_target = self.create_bind_target()

        # Calls the wrapped method directly
        result = test_method_object.call_wrapped(bind_target, 3)

        # Verifies it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Calls with different arguments
        result = test_method_object.call_wrapped(bind_target, 3, 4)

        # Verifies it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    def test_call_binding(self, test_method_object: BaseMethod) -> None:
        """Tests that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Creates a bind target
        bind_target = self.create_bind_target()

        # Binds the method to the target
        test_method_object.__self__ = bind_target
        test_method_object.__owner__ = self.BindTargetClass

        # Calls the method using call_binding
        result = test_method_object.call_binding(3)

        # Verifies it returns the expected result
        assert result == (5, bind_target)  # (3 + 2, instance)

        # Calls with different arguments
        result = test_method_object.call_binding(3, 4)

        # Verifies it returns the expected result
        assert result == (7, bind_target)  # (3 + 4, instance)

    # Instantiation #
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, test_object: BaseMethod, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of the method object.

        This test verifies that copy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            obj_copy = copy.copy(test_object)
        else:
            obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, type(test_object))
        assert obj_copy.__func__ is test_object.__func__
        assert obj_copy.__self__ is test_object.__self__

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        test_object: BaseMethod,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deep copy behavior of the method object.

        This test verifies that deepcopy creates a new object with the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)
        else:
            obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, type(test_object))
        assert obj_deepcopy.__func__ is test_object.__func__
        assert obj_deepcopy.__self__ is test_object.__self__

    # Pickling #
    def test_pickling(self, test_object: BaseMethod) -> None:  # type: ignore[override]
        """Tests pickling and unpickling of the method object.

        This test verifies that the object can be pickled and unpickled correctly, and that the unpickled object
        has the same wrapped function.

        Args:
            test_object: A fixture providing a BaseMethod instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, type(test_object))
        assert unpickled.__func__ is test_object.__func__
        assert unpickled.__self__ is test_object.__self__

    def test_init_false_pickling(self) -> None:
        """Tests pickling of a method initialized with init=False."""
        obj = self.UnitTestClass(init=False)
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.__wrapped__ is None
        assert loaded.__self__ is None

    def test_pickling_with_instance(self) -> None:
        """Tests pickling and unpickling of the method object with a bound instance."""
        # Creates a method and a bind target
        method = self.create_method_object()
        bind_target = self.create_bind_target()

        # Binds the method to the target
        method.__self__ = bind_target  # type: ignore[attr-defined]
        method.__owner__ = self.BindTargetClass  # type: ignore[attr-defined]

        # Pickle and unpickle the method and bind target (need a strong reference to the bind target)
        items = (method, bind_target)
        pickled = pickle.dumps(items)
        unpickled_method, unpickled_bind_target = pickle.loads(pickled)

        # Verifies the unpickled method is a new instance
        assert unpickled_method is not method

        # Verifies it has the correct wrapped function
        assert unpickled_method.__func__ is method.__func__

        # Verifies it's bound to the correct instance
        assert unpickled_method.__self__ is not bind_target
        assert unpickled_method.__self__ is unpickled_bind_target
        assert unpickled_method.__owner__ is self.BindTargetClass

        # Verifies it returns the expected result when called
        result = unpickled_method(3)
        assert result == (5, unpickled_bind_target)  # (3 + 2, instance)

    # Functionality #
    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False)
        assert obj._self_ is None
        assert "is_binding" not in obj.__dict__

    @pytest.mark.parametrize("name", [None, "named_method"])
    @pytest.mark.parametrize("use_owner_kwarg", [False, True])
    def test_bind_to_attribute(self, name: str | None, use_owner_kwarg: bool) -> None:
        """Tests that the method can be bound to an instance and set as an attribute.

        This test only varifies that a bound method is returned and bound to the target instance's attribute. This
        method may be overwritten to include validation that the method functions as intended.

        Args:
            name: The name of the attribute to set.
            use_owner_kwarg: Whether to pass the owner as a keyword argument.
        """
        method_object = self.create_method_object()
        new_bind_target = self.create_bind_target()

        args: tuple[Any, ...]
        kwargs: dict[str, Any] = {}
        if use_owner_kwarg:
            args = (new_bind_target,)
            kwargs["owner"] = self.BindTargetClass
        else:
            args = (new_bind_target, self.BindTargetClass)

        if name is not None:
            kwargs["name"] = name
            expected_name = name
        else:
            expected_name = method_object.__wrapped__.__name__  # type: ignore[union-attr]

        bound_method = method_object.bind_to_attribute(*args, **kwargs)  # type: ignore[attr-defined]

        assert method_object is bound_method
        assert bound_method.__self__ is new_bind_target
        assert bound_method.__owner__ is self.BindTargetClass
        assert hasattr(new_bind_target, expected_name)

    def test_self_typeerror(self) -> None:
        """Tests accessing __self__ when it is None."""
        method = self.UnitTestClass(lambda: None)
        assert method.__self__ is None

    @pytest.mark.parametrize(
        ("kwargs", "is_binding", "expected_self", "expected_owner"),
        [
            ({"instance": True, "owner": True}, True, "target", "class"),
            ({"instance": True}, True, "target", None),
            ({"owner": True}, True, None, "class"),
            ({"instance": True, "owner": True}, False, None, None),
        ],
    )
    def test_bind_self_branches(
        self,
        test_bind_target: Any,
        kwargs: dict[str, bool],
        is_binding: bool,
        expected_self: str | None,
        expected_owner: str | None,
    ) -> None:
        """Tests different binding branches of bind_self.

        Args:
            test_bind_target: Fixture for bind target.
            kwargs: Arguments flags for bind_self.
            is_binding: Whether the method is binding.
            expected_self: Expected value for __self__ ('target' or None).
            expected_owner: Expected value for __owner__ ('class' or None).
        """
        method = self.UnitTestClass(lambda: None, is_binding=is_binding)

        # Prepare kwargs
        call_kwargs = {}
        if kwargs.get("instance"):
            call_kwargs["instance"] = test_bind_target
        if kwargs.get("owner"):
            call_kwargs["owner"] = self.BindTargetClass

        method.bind_self(**call_kwargs)

        if expected_self == "target":
            assert method.__self__ is test_bind_target
        else:
            assert method.__self__ is None

        if expected_owner == "class":
            assert method.__owner__ is self.BindTargetClass
        else:
            assert method.__owner__ is None

    def test_bind_to_attribute_none_instance(self) -> None:
        """Tests bind_to_attribute with None instance."""
        method = self.UnitTestClass(lambda: None)
        with pytest.raises(AttributeError):
            method.bind_to_attribute(None)

    def test_as_function(self, test_method_object: BaseMethod) -> None:  # type: ignore[override]
        """Tests that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a BaseMethod instance that wraps a method.
        """
        # Creates a bind target
        bind_target = self.create_bind_target()

        # Binds the method to the target
        test_method_object.__self__ = bind_target

        # Converts to a standard Python function
        func = test_method_object.as_function()

        # Verifies it's a function
        assert callable(func)

        # Verifies it returns the expected result
        assert func(3) == (5, bind_target)  # (3 + 2, instance)
        assert func(3, 4) == (7, bind_target)  # (3 + 4, instance)

        # Verifies it has the correct attributes
        assert func.__name__ == test_method_object.__name__  # type: ignore[attr-defined]
        assert func.__doc__ == test_method_object.__doc__
        assert func.__wrapped__ is test_method_object  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_as_function_coroutine(self, test_method_object: BaseMethod) -> None:  # type: ignore[override]
        """Tests as_function with a coroutine."""

        async def example_coro(x: int, y: int) -> int:
            await asyncio.sleep(0)
            return x + y

        method = self.UnitTestClass(example_coro)
        func = method.as_function()

        assert inspect.iscoroutinefunction(func)
        result = await func(1, 2)
        assert result == 3

    def test_as_function_missing_attrs(self) -> None:
        """Tests as_function with a callable missing standard attributes."""

        class CallableNoAttrs:
            def __call__(self, x: int, y: int) -> int:
                return x + y

        c = CallableNoAttrs()
        # verify it misses attributes
        assert not hasattr(c, "__name__")

        method = self.UnitTestClass(c)
        func = method.as_function()

        assert func(1, 2) == 3
