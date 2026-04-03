"""callablemultiplexer.py
Callables which select between either functions or methods to be used as the call method.
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
import sys
from types import MethodType
from typing import Any

# Local Packages #
from ..bases import BaseCallable, BaseMethod
from ..typing import AnyCallable
from .functionregistry import FunctionRegistry


# Definitions #
# Classes #
class CallableMultiplexer(BaseMethod):
    """A callable which select between either functions or methods to be used as the call method.

    The CallableMultiplexer has a registry which it uses to store the functions/methods to be multiplexed.
    Additionally, an object can be assigned and its methods will be part of the multiplex. Having the object being
    directly multiplexed allows more dynamic interaction as the object's methods may change during runtime. Note that
    the registry's functions/methods take priority in selection.

    Attributes:
        registry: The function registry to use for selecting a function/method.
        _selected: The name of the function/method to select for use.
        _is_binding_wrapper: Determines if this callable will bind the selected function to the contained instance.

    Args:
        registry: The function registry to use for selecting a function/method.
        instance: An object to wrap which will be used to find functions/methods.
        owner: The class of the object used for finding functions/methods.
        select: The name of the function/method to select for use.
        binding: Determines if this object will bind the selected function as a method.
        *args: Arguments for inheritance.
        is_binding: Determines if this callable will bind to another object. Default is True.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    registry: FunctionRegistry
    _selected: str | None = None
    _selected_bind_method: AnyCallable

    _is_binding_wrapper: bool = False

    # Properties #
    @property
    def is_binding_wrapper(self) -> bool:
        """Determines if this callable will bind the selected function to the contained instance."""
        return self._is_binding_wrapper

    @is_binding_wrapper.setter
    def is_binding_wrapper(self, value: bool) -> None:
        self._is_binding_wrapper = value
        if not value:
            del self._selected_bind_method
        elif self.__wrapped__ is not None and hasattr(self.__wrapped__, "__get__"):
            self._selected_bind_method = self.__wrapped__.__get__

    @property
    def selected(self) -> str | None:
        """The name of the selected function/method."""
        return self._selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.select(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: FunctionRegistry | AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool = False,
        *args: Any,
        is_binding: bool = True,
        registry: FunctionRegistry | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            func: Optional callable to wrap.
            instance: Optional instance for method binding.
            owner: Optional owner class for method resolution.
            select: Name of the function/method to initially select.
            binding: When True, wrap the selected callable as a binding descriptor.
            *args: Positional arguments forwarded to BaseMethod.
            is_binding: Determines if this callable will bind to another object.
            registry: Optional registry of functions/methods to multiplex.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseMethod.
        """
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                func,
                instance,
                owner,
                select,
                binding,
                *args,
                is_binding=is_binding,
                registry=registry,
                **kwargs,
            )

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

        This method prepares the object for pickling by converting the weak reference to the bound instance into a
        strong reference. This is necessary because weak references cannot be pickled directly. The method first gets
        the state from the parent class, then adds the bound instance as a strong reference.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: Neither __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        match state:
            case dict():
                state.pop("_selected_bind_method", None)
            case tuple() if state[0] is not None:
                state[0].pop("_selected_bind_method", None)
        return state

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        This method restores the object from a pickled state by first extracting the bound instance from the state. Then
        sets the state using the parent class's __setstate__ method. Finally, it converts the strong reference to the
        bound instance back into a weak reference.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object.
        """
        super().__setstate__(state)
        if self.__wrapped__ is not None:
            self._selected_bind_method = self.__wrapped__.__get__

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument if is_binding is True.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        print(f"DEBUG: CallableMultiplexer.__call__ for {self} (wrapped={self.__wrapped__}, binding={self.is_binding_wrapper})")
        if self.__wrapped__ is None:
            raise TypeError("No function selected")

        if self.is_binding_wrapper:
            return self._selected_bind_method(self.__self__, self.__owner__)(*args, **kwargs)
        else:
            func = self.__wrapped__
            return func(*args, **kwargs)  # type:ignore[misc]

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: FunctionRegistry | AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool | None = None,
        *args: Any,
        is_binding: bool = True,
        registry: FunctionRegistry | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: Optional callable to wrap.
            instance: An object to wrap which will be used to find functions/methods.
            owner: The class of the object used for finding functions/methods.
            select: The name of the function/method to select for use.
            binding: Determines if this object will bind the selected function as a method.
            *args: Arguments for inheritance.
            is_binding: Determines if this callable will bind to another object. Default is True.
            registry: The function registry to use for selecting a function/method.
            **kwargs: Keyword arguments for inheritance.
        """
        # Resolve func
        if isinstance(func, FunctionRegistry):
            if registry is None:
                registry = func
            func = None

        if registry is not None:
            self.registry = registry
        else:
            self.build_registry()

        super().construct(func, instance, owner, *args, is_binding=is_binding, **kwargs)

        if select is not None:
            self.select(select)
        elif self.__wrapped__ is not None and hasattr(self.__wrapped__, "__get__"):
            self._selected_bind_method = self.__wrapped__.__get__

        if binding is not None:
            self._is_binding_wrapper = binding

    def build_registry(self) -> None:
        """Creates the registry this object will use for function/method selection."""
        self.registry = FunctionRegistry()

    # Registry
    def add_function(self, name: str, func: AnyCallable) -> None:
        """Adds a function to the registry.

        Args:
            name: The name of the function being added.
            func: The function to add to the registry.
        """
        self.registry[name] = func

    def add_method(self, name: str, method: AnyCallable) -> None:
        """Adds a method to the registry.

        Args:
            name: The name of the method being added.
            method: The method to add to the registry.
        """
        if hasattr(method, "__func__"):
            self.registry[name] = method.__func__
        else:
            self.registry[name] = method

    def bind_selected(self, instance: Any = None, owner: type[Any] | None = None) -> BaseCallable | MethodType:
        """Creates a method of the selected function using python's method binding.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self if instance is None else self.__wrapped__.__get__(instance, owner)  # type:ignore[union-attr]

    # Callable Selection
    def select(self, name: str | None) -> None:
        """Selects a function/method to use within the registry or the wrapped object.

        Args:
            name: The name of function/method in the registry or object to use.
        """
        if name is None:
            func = None
        elif (func := self.registry.get(name, None)) is not None:
            self._is_binding_wrapper = False
        elif self._self_ is not None:
            func = getattr(self._self_(), name)
            self._is_binding_wrapper = True
        else:
            func = None

        self.__func__ = func

        if func is not None:
            if hasattr(func, "__get__"):
                self._selected_bind_method = func.__get__
        elif hasattr(self, "_selected_bind_method"):
            del self._selected_bind_method

        self._selected = name

    def add_select_function(self, name: str, func: AnyCallable) -> None:
        """Adds a function to the registry and selects it.

        Args:
            name: The name of the function being added.
            func: The function to add to the registry.
        """
        self.registry[name] = self.__wrapped__ = func
        self._is_binding_wrapper = False
        if hasattr(func, "__get__"):
            self._selected_bind_method = func.__get__
        self._selected = name

    def add_select_method(self, name: str, method: AnyCallable) -> None:
        """Adds a method to the registry and selects it.

        Args:
            name: The name of the method being added.
            method: The method to add to the registry.
        """
        if hasattr(method, "__func__"):
            method = method.__func__
        self.registry[name] = self.__wrapped__ = method
        self._is_binding_wrapper = False
        if hasattr(method, "__get__"):
            self._selected_bind_method = method.__get__
        self._selected = name

    # Binding
    def bind_self(self, instance: Any = None, owner: Any = None) -> Any:
        """Binds this method to an instance and/or owner class.

        Args:
            instance: The object to bind this method to. This becomes the 'self' parameter when the method is called.
            owner: The class of the object being bound to. This is used for proper method binding and to support
                inheritance.

        Returns:
            This method object, now bound to the specified instance and/or owner class.
        """
        if self.is_binding:
            if instance is not None:
                self.__self__ = instance
            if owner is not None:
                self.__owner__ = owner
            self.is_binding_wrapper = True
        return self

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    def __get__(self, instance: Any = None, owner: type[Any] | None = None) -> Any:
        """Returns the bound method."""
        return self.bind_self(instance, owner)


class MethodMultiplexer(CallableMultiplexer):
    """A callable which will treat the selected function as a method, binding it to the stored instance.

    The MethodMultiplexer has a registry which it uses to store the methods to be multiplexed. Additionally, an object
    can be assigned and its methods will be part of multiplex. Having the object being directly multiplexed allows more
    dynamic interaction as the object's methods may change during runtime. Note that the registry's methods take
    priority in selection.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """First binds the wrapped function, then calls it.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        selected_func = self.__func__
        print(f"DEBUG: MethodMultiplexer.__call__ for {self} (selected_func={selected_func})")
        if selected_func is None:
            raise TypeError("No function selected")

        instance = self.__self__
        owner = self.__owner__

        if hasattr(selected_func, "call_wrapped"):
            return selected_func.call_wrapped(*(instance,) + args, **kwargs)
        else:
            try:
                bound = self._selected_bind_method(instance, owner)
            except TypeError as e:
                raise TypeError(f"{self._selected_bind_method}({instance}, {owner}) is invalid: {e}")
            return bound(*args, **kwargs)


class FunctionMultiplexer(CallableMultiplexer):
    """A callable which will treat the selected function as a function, not binding it to the stored instance.

    The FunctionMultiplexer has a registry which it uses to store the methods to be multiplexed. Additionally, an object
    can be assigned and its methods will be part of multiplex. Having the object being directly multiplexed allows more
    dynamic interaction as the object's methods may change during runtime. Note that the registry's methods take
    priority in selection.
    """

    # Magic Methods #
    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        if self.__wrapped__ is None:
            raise TypeError("No function selected")

        func = self.__wrapped__
        if (
            hasattr(func, "__func__") and
            getattr(func, "__self__", None) is self.__self__ and
            args and args[0] is self.__self__
        ):
            func = func.__func__

        return func(*args, **kwargs)  # type:ignore[misc]
