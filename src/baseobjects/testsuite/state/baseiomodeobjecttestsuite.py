"""baseiomodeobjecttestsuite.py
Base test suite classes for BaseIOModeObject and its decorators.

This module provides the BaseIOModeObjectTestSuite, StateRestrictionTestSuite, AsOpenTestSuite, and
AsOpenAsyncTestSuite classes, which serve as foundations for testing classes that inherit from BaseIOModeObject and its
associated decorators.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2026, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
import asyncio
from enum import StrEnum
from io import UnsupportedOperation
from typing import Any, Self

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import BaseDecorator
from ...state.baseiomodeobject import BaseIOModeObject, asopen, asopenasync, staterestriction
from ..bases.basecallabletestsuite import ConcreteBindTarget, concrete_function
from ..bases.baseobjecttestsuite import BaseObjectTestSuite
from ..functions.basedecoratortestsuite import BaseDecoratorTestSuite


# Definitions #
# Classes #
class BaseIOModeObjectTestSuite(BaseObjectTestSuite):
    """Base test suite for children of BaseIOModeObject.

    This class provides common test functionality for child class of BaseIOModeObject, including tests for opening,
    closing, and mode handling. Subclasses should set the UnitTestClass attribute and may override or extend the test
    methods.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[BaseIOModeObject]

    # Tests #
    # Properties #
    def test_is_open(self, test_object: BaseIOModeObject) -> None:
        """Tests the is_open property.

        Args:
            test_object: A fixture providing a test object instance.
        """
        assert isinstance(test_object.is_open, bool)

    def test_mode(self, test_object: BaseIOModeObject) -> None:
        """Tests the mode property.

        Args:
            test_object: A fixture providing a test object instance.
        """
        assert isinstance(test_object.mode, (str, StrEnum))

    def test_set_mode(self, test_object: BaseIOModeObject) -> None:
        """Tests setting the mode property.

        Args:
            test_object: A fixture providing a test object instance.
        """
        valid_mode = next(iter(test_object._valid_modes))
        test_object.mode = valid_mode
        assert test_object.mode == valid_mode

    # Magic Methods #
    # Context Manager #
    def test_context_manager(self, test_object: BaseIOModeObject) -> None:
        """Tests the context manager methods.

        Args:
            test_object: A fixture providing a test object instance.
        """
        with test_object as entered_obj:
            assert entered_obj is test_object
            assert test_object.is_open

        assert not test_object.is_open

    @pytest.mark.asyncio
    async def test_async_context_manager(self, test_object: BaseIOModeObject) -> None:
        """Tests the asynchronous context manager methods.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            async with test_object as entered_obj:
                assert entered_obj is test_object
                assert test_object.is_open

            assert not test_object.is_open
        except NotImplementedError:
            pytest.skip("Async context manager not implemented.")

    # Instance Methods #
    def test_open(self, test_object: BaseIOModeObject) -> None:
        """Tests the open method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        result = test_object.open()
        assert result is test_object
        assert test_object.is_open

    @pytest.mark.asyncio
    async def test_open_async(self, test_object: BaseIOModeObject) -> None:
        """Tests the open_async method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            result = await test_object.open_async()
            assert result is test_object
            assert test_object.is_open
        except NotImplementedError:
            pytest.skip("Async open not implemented.")

    def test_close(self, test_object: BaseIOModeObject) -> None:
        """Tests the close method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.open()
        test_object.close()
        assert not test_object.is_open

    @pytest.mark.asyncio
    async def test_close_async(self, test_object: BaseIOModeObject) -> None:
        """Tests the close_async method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            await test_object.open_async()
            await test_object.close_async()
            assert not test_object.is_open
        except (NotImplementedError, AttributeError):
            pytest.skip("Async close not implemented.")

    def test_repr(self, test_object: BaseIOModeObject) -> None:
        """Tests the __repr__ method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        assert f"is_open={test_object.is_open}" in repr(test_object)
        assert f"mode={test_object.mode!r}" in repr(test_object)

    def test_validate_mode(self, test_object: BaseIOModeObject) -> None:
        """Tests the validate_mode method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        valid_mode = next(iter(test_object._valid_modes))
        assert test_object.validate_mode(valid_mode)
        assert not test_object.validate_mode("invalid_mode_that_does_not_exist")

    def test_require_open(self, test_object: BaseIOModeObject) -> None:
        """Tests the require_open method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.open()
        test_object.require_open()
        test_object.close()
        with pytest.raises(ValueError, match=r"Operation on a closed .* is not allowed."):
            test_object.require_open()

    def test_require_closed(self, test_object: BaseIOModeObject) -> None:
        """Tests the require_closed method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.close()
        test_object.require_closed()
        test_object.open()
        with pytest.raises(ValueError, match=r"Operation on an? open .* is not allowed."):
            test_object.require_closed()

    def test_require_mode(self, test_object: BaseIOModeObject) -> None:
        """Tests the require_mode method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        valid_mode = next(iter(test_object._valid_modes))
        invalid_mode = list(test_object._valid_modes)[-1]
        test_object.mode = valid_mode
        test_object.require_mode(valid_mode)
        test_object.require_mode({valid_mode, invalid_mode})
        test_object.require_mode([valid_mode, invalid_mode])
        test_object.require_mode(modes=None)
        if valid_mode != invalid_mode:
            test_object.mode = invalid_mode
            with pytest.raises(UnsupportedOperation):
                test_object.require_mode(valid_mode)

    def test_require_mode_group(self, test_object: BaseIOModeObject) -> None:
        """Tests the require_mode method with a mode group.

        Args:
            test_object: A fixture providing a test object instance.
        """
        if not test_object._mode_registry:
            # If no registry, just test it raises KeyError if group not found
            with pytest.raises(KeyError):
                test_object.require_mode(mode_group="non_existent")
            return

        group_name = next(iter(test_object._mode_registry))
        group = test_object._mode_registry[group_name]

        if not group:
            return

        valid_mode = next(iter(group))
        test_object.mode = valid_mode
        test_object.require_mode(mode_group=group_name)

        # Test failure
        # Find a mode NOT in the group
        invalid_mode = None
        for m in test_object._valid_modes:
            if m not in group:
                invalid_mode = m
                break

        if invalid_mode:
            test_object.mode = invalid_mode
            with pytest.raises(UnsupportedOperation):
                test_object.require_mode(mode_group=group_name)

        # Test invalid group
        with pytest.raises(KeyError):
            test_object.require_mode(mode_group="invalid_group")

    def test_ensure_open(self, test_object: BaseIOModeObject) -> None:
        """Tests the ensure_open method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.close()
        test_object.ensure_open()
        assert test_object.is_open

    @pytest.mark.asyncio
    async def test_ensure_open_async(self, test_object: BaseIOModeObject) -> None:
        """Tests the ensure_open_async method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            test_object.close()
            await test_object.ensure_open_async()
            assert test_object.is_open
        except (NotImplementedError, AttributeError):
            pytest.skip("Async open not implemented.")

    def test_reopen(self, test_object: BaseIOModeObject) -> None:
        """Tests the reopen method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        test_object.open()
        test_object.reopen()
        assert test_object.is_open

    @pytest.mark.asyncio
    async def test_reopen_async(self, test_object: BaseIOModeObject) -> None:
        """Tests the reopen_async method.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            test_object.open()
            await test_object.reopen_async()
            assert test_object.is_open
        except (NotImplementedError, AttributeError):
            pytest.skip("Async reopen not implemented.")

    def test_as_open(self, test_object: BaseIOModeObject) -> None:
        """Tests the asopen context manager.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Test when closed
        test_object.close()
        with test_object.as_open():
            assert test_object.is_open
        assert not test_object.is_open

        # Test when already open
        test_object.open()  # type: ignore[unreachable]
        with test_object.as_open():
            assert test_object.is_open
        assert test_object.is_open

    @pytest.mark.asyncio
    async def test_as_open_async(self, test_object: BaseIOModeObject) -> None:
        """Tests the asopenasync context manager.

        Args:
            test_object: A fixture providing a test object instance.
        """
        try:
            # Test when closed
            test_object.close()
            async with test_object.as_open_async():
                assert test_object.is_open
            assert not test_object.is_open

            # Test when already open
            await test_object.open_async()  # type: ignore[unreachable]
            async with test_object.as_open_async():
                assert test_object.is_open
            assert test_object.is_open
        except (NotImplementedError, AttributeError):
            pytest.skip("Async context manager not implemented.")


class MockModes(StrEnum):
    """Mock modes for testing."""

    READ = "r"
    WRITE = "w"


class ConcreteIOModeBindTarget(BaseIOModeObject, ConcreteBindTarget):
    """A test class for testing method binding with I/O mode objects."""

    _valid_modes: type[StrEnum] = MockModes
    _mode_registry: dict[str, set[str | StrEnum]] = {"read_only": {MockModes.READ}}

    def __init__(self, value: int = 42) -> None:
        """Initializes the instance.

        Args:
            value: The initial value to set.
        """
        self._mode = MockModes.READ
        self._is_open = False
        self.value = value

    def open(self, *args: Any, **kwargs: Any) -> Self:
        """Opens the object.

        Returns:
            The opened object.
        """
        self._is_open = True
        return self

    def close(self) -> None:
        """Closes the object."""
        self._is_open = False

    async def open_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously opens the object.

        Returns:
            The opened object.
        """
        self._is_open = True
        return self

    async def close_async(self, *args: Any, **kwargs: Any) -> None:
        """Asynchronously closes the object."""
        self._is_open = False


class BaseIOModeDecoratorTestSuite(BaseDecoratorTestSuite):
    """Base test suite for I/O mode decorators."""

    BindTargetClass: type[Any] = ConcreteIOModeBindTarget

    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created."""
        instance = self.UnitTestClass(concrete_function)
        assert isinstance(instance, self.UnitTestClass)
        assert instance.__func__ is concrete_function

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_call(
        self,
        test_function_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
        io_object: BaseIOModeObject,
    ) -> None:
        """Tests that the callable object can be called."""
        try:
            io_object.open()
        except (NotImplementedError, AttributeError):
            pass

        def wrapped(obj: BaseIOModeObject, x: int, y: int = 2) -> int:
            return x + y

        test_function_object.__func__ = wrapped
        assert test_function_object(io_object, *args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_call_wrapped(
        self,
        test_function_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
        io_object: BaseIOModeObject,
    ) -> None:
        """Tests that the wrapped function can be called directly."""

        def wrapped(obj: BaseIOModeObject, x: int, y: int = 2) -> int:
            return x + y

        test_function_object.__func__ = wrapped
        assert test_function_object.call_wrapped(io_object, *args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_as_function(
        self,
        test_function_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
        io_object: BaseIOModeObject,
    ) -> None:
        """Tests that the callable object can be converted to a standard Python function."""

        def wrapped(obj: BaseIOModeObject, x: int, y: int = 2) -> int:
            return x + y

        test_function_object.__func__ = wrapped
        func = test_function_object.as_function()
        assert func(io_object, *args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_coroutine(
        self,
        test_coroutine_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
        io_object: BaseIOModeObject,
    ) -> None:
        """Tests that the callable object correctly handles coroutine functions."""
        try:
            io_object.open()
        except (NotImplementedError, AttributeError):
            pass

        async def wrapped(obj: BaseIOModeObject, x: int, y: int = 2) -> int:  # noqa: RUF029
            return x + y

        test_coroutine_object.__func__ = wrapped
        coro = test_coroutine_object(io_object, *args)
        assert asyncio.iscoroutine(coro)
        result = asyncio.run(coro)
        assert result == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_as_function_coroutine(
        self,
        test_coroutine_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
        io_object: BaseIOModeObject,
    ) -> None:
        """Tests that the callable object wrapping a coroutine can be converted to a coroutine function."""

        async def wrapped(obj: BaseIOModeObject, x: int, y: int = 2) -> int:  # noqa: RUF029
            return x + y

        test_coroutine_object.__func__ = wrapped
        func = test_coroutine_object.as_function()
        coro = func(io_object, *args)
        result = asyncio.run(coro)
        assert result == expected

    def test_decorator_usage(self, io_object: BaseIOModeObject) -> None:  # type: ignore[override]
        """Tests the decorator usage."""
        try:
            io_object.open()
        except (NotImplementedError, AttributeError):
            pass

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(obj: BaseIOModeObject, x: int, y: int = 2) -> int:
            return x + y

        assert test_func(io_object, 3) == 5

    def test_decorator_with_args(self, io_object: BaseIOModeObject) -> None:
        """Tests the decorator with arguments."""
        try:
            io_object.open()
        except (NotImplementedError, AttributeError):
            pass

        @self.UnitTestClass(open_state=True)
        def test_func(obj: BaseIOModeObject, x: int, y: int = 2) -> int:
            return x + y

        assert test_func(io_object, 3) == 5

    def test_coroutine_decorator(self, io_object: BaseIOModeObject) -> None:  # type: ignore[override]
        """Tests the coroutine decorator."""
        try:
            io_object.open()
        except (NotImplementedError, AttributeError):
            pass

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        async def test_coro(obj: BaseIOModeObject, x: int, y: int = 2) -> int:  # noqa: RUF029
            return x + y

        result = asyncio.run(test_coro(io_object, 3))
        assert result == 5


class StateRestrictionTestSuite(BaseIOModeDecoratorTestSuite):
    """Base test suite for staterestriction.

    This class provides common test functionality for the staterestriction decorator.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[staterestriction]
    BindTargetClass: type[Any] = ConcreteIOModeBindTarget

    # Tests #
    def test_open_state_restriction(self, io_object: BaseIOModeObject) -> None:
        """Tests the open state restriction.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """

        @staterestriction(open_state=True)  # type: ignore[arg-type]
        def restricted_method(obj: BaseIOModeObject) -> str:
            return "success"

        # Test when closed
        io_object.close()
        with pytest.raises(ValueError, match=r"Operation on a closed .* is not allowed."):
            restricted_method(io_object)

        # Test when open
        io_object.open()
        assert restricted_method(io_object) == "success"

    def test_closed_state_restriction(self, io_object: BaseIOModeObject) -> None:
        """Tests the closed state restriction.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """

        @staterestriction(open_state=False)  # type: ignore[arg-type]
        def restricted_method(obj: BaseIOModeObject) -> str:
            return "success"

        # Test when open
        io_object.open()
        with pytest.raises(ValueError, match=r"Operation on an? open .* is not allowed."):
            restricted_method(io_object)

        # Test when closed
        io_object.close()
        assert restricted_method(io_object) == "success"

    def test_mode_restriction(self, io_object: BaseIOModeObject) -> None:
        """Tests the mode restriction.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """
        valid_mode = next(iter(io_object._valid_modes))
        invalid_mode = list(io_object._valid_modes)[-1]

        @staterestriction(valid_modes=valid_mode)  # type: ignore[arg-type]
        def restricted_method(obj: BaseIOModeObject) -> str:
            return "success"

        # Test with invalid mode
        io_object.mode = invalid_mode
        if valid_mode != invalid_mode:
            with pytest.raises(UnsupportedOperation, match=f"Mode {invalid_mode} is not valid for this operation."):
                restricted_method(io_object)

        # Test with valid mode
        io_object.mode = valid_mode
        assert restricted_method(io_object) == "success"

    def test_mode_group_restriction(self, io_object: BaseIOModeObject) -> None:
        """Tests the mode_group restriction.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """
        io_object._mode_registry["test_group"] = {MockModes.READ}

        @staterestriction(mode_group="test_group")
        def restricted_method(obj: BaseIOModeObject) -> str:
            return "success"

        # Test with valid mode in group
        io_object.mode = MockModes.READ
        assert restricted_method(io_object) == "success"

        # Test with invalid mode not in group
        io_object.mode = MockModes.WRITE
        with pytest.raises(UnsupportedOperation):
            restricted_method(io_object)

    def test_combined_restriction(self, io_object: BaseIOModeObject) -> None:
        """Tests combined open state and mode restriction.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """
        valid_mode = next(iter(io_object._valid_modes))

        @staterestriction(open_state=True, valid_modes=valid_mode)  # type: ignore[arg-type]
        def restricted_method(obj: BaseIOModeObject) -> str:
            return "success"

        # Test when closed
        io_object.close()
        io_object.mode = valid_mode
        with pytest.raises(ValueError, match=r"Operation on a closed .* is not allowed."):
            restricted_method(io_object)

        # Test when open with valid mode
        io_object.open()
        io_object.mode = valid_mode
        assert restricted_method(io_object) == "success"

    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method.

        This test is overridden because staterestriction requires an object as the first argument when called.
        """
        pytest.skip("staterestriction requires an object as the first argument when called.")

    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property.

        This test is overridden because staterestriction() returns a partial, which doesn't have the property.
        """
        pytest.skip("staterestriction() returns a partial when called without arguments.")


class AsOpenTestSuite(BaseIOModeDecoratorTestSuite):
    """Base test suite for asopen.

    This class provides common test functionality for the asopen decorator.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[asopen]
    BindTargetClass: type[Any] = ConcreteIOModeBindTarget

    # Tests #
    def test_as_open_decorator(self, io_object: BaseIOModeObject) -> None:
        """Tests the asopen decorator.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """

        @asopen
        def restricted_method(obj: BaseIOModeObject) -> bool:
            return obj.is_open

        assert io_object.is_open is False
        assert restricted_method(io_object) is True
        assert io_object.is_open is False

    def test_as_open_decorator_with_args(self, io_object: BaseIOModeObject) -> None:
        """Tests the asopen decorator with arguments.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """
        valid_mode = next(iter(io_object._valid_modes))

        @asopen(mode=valid_mode)  # type: ignore[arg-type]
        def restricted_method(obj: BaseIOModeObject) -> StrEnum:
            return obj.mode

        assert io_object.is_open is False
        assert restricted_method(io_object) == valid_mode
        assert io_object.is_open is False

    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method.

        This test is overridden because asopen requires an object as the first argument when called.
        """
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_bind(self, *args: Any, **kwargs: Any) -> None:
        """Tests the bind method."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_bind_to_attribute(self, *args: Any, **kwargs: Any) -> None:
        """Tests the bind_to_attribute method."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_call(self, *args: Any, **kwargs: Any) -> None:
        """Tests the __call__ method of the decorator."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_as_function(self, *args: Any, **kwargs: Any) -> None:
        """Tests the as_function method."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_coroutine(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator on a coroutine."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_as_function_coroutine(self, *args: Any, **kwargs: Any) -> None:
        """Tests the as_function method on a coroutine."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_decorator_usage(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator usage."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator with arguments."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_coroutine_decorator(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator on a coroutine."""
        pytest.skip("asopen requires an object as the first argument when called.")

    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property.

        This test is overridden because asopen() returns a partial, which doesn't have the property.
        """
        pytest.skip("asopen() returns a partial when called without arguments.")


class AsOpenAsyncTestSuite(BaseIOModeDecoratorTestSuite):
    """Base test suite for asopenasync.

    This class provides common test functionality for the asopenasync decorator.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: type[asopenasync]
    BindTargetClass: type[Any] = ConcreteIOModeBindTarget

    # Tests #
    @pytest.mark.asyncio
    async def test_as_open_async_decorator(self, io_object: BaseIOModeObject) -> None:
        """Tests the asopenasync decorator.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """

        @asopenasync
        async def restricted_method(obj: BaseIOModeObject) -> bool:  # noqa: RUF029
            return obj.is_open

        try:
            assert io_object.is_open is False
            assert await restricted_method(io_object) is True
            assert io_object.is_open is False
        except NotImplementedError:
            pytest.skip("Async open/close not implemented.")

    @pytest.mark.asyncio
    async def test_as_open_async_decorator_with_args(self, io_object: BaseIOModeObject) -> None:
        """Tests the asopenasync decorator with arguments.

        Args:
            io_object: A fixture providing a test I/O mode object instance.
        """
        valid_mode = next(iter(io_object._valid_modes))

        @asopenasync(mode=valid_mode)  # type: ignore[arg-type]
        async def restricted_method(obj: BaseIOModeObject) -> StrEnum:  # noqa: RUF029
            return obj.mode

        try:
            assert io_object.is_open is False
            assert await restricted_method(io_object) == valid_mode  # type: ignore[operator]
            assert io_object.is_open is False
        except NotImplementedError:
            pytest.skip("Async open/close not implemented.")

    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method.

        This test is overridden because asopenasync requires an object as the first argument when called.
        """
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_call_wrapped(self, *args: Any, **kwargs: Any) -> None:
        """Tests the call_wrapped method."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_bind(self, *args: Any, **kwargs: Any) -> None:
        """Tests the bind method."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_bind_to_attribute(self, *args: Any, **kwargs: Any) -> None:
        """Tests the bind_to_attribute method."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_call(self, *args: Any, **kwargs: Any) -> None:
        """Tests the __call__ method of the decorator."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_as_function(self, *args: Any, **kwargs: Any) -> None:
        """Tests the as_function method."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_coroutine(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator on a coroutine."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_as_function_coroutine(self, *args: Any, **kwargs: Any) -> None:
        """Tests the as_function method on a coroutine."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_decorator_usage(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator usage."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator with arguments."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_coroutine_decorator(self, *args: Any, **kwargs: Any) -> None:
        """Tests the decorator on a coroutine."""
        pytest.skip("asopenasync requires an object as the first argument when called.")

    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property.

        This test is overridden because asopenasync() returns a partial, which doesn't have the property.
        """
        pytest.skip("asopenasync() returns a partial when called without arguments.")
