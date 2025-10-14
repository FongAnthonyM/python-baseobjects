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
from types import MethodType
from typing import Any

# Local Packages #
from ..bases import BaseCallable, BaseMethod
from ..typing import AnyCallable, GetObjectMethod
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
        is_coroutine: Checks if this callable is a coroutine.

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
    registry: FunctionRegistry | None = None
    _selected: str | None = None
    _selected_bind_method: Any = None

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
            self._selected_bind_method = None
        elif self.__wrapped__ is not None:
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
        registry: FunctionRegistry | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool = False,
        *args: Any,
        is_binding: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a callable multiplexer.

        Args:
            registry: Optional registry of functions/methods to multiplex.
            instance: Optional instance for method binding.
            owner: Optional owner class for method resolution.
            select: Name of the function/method to initially select.
            binding: When True, wrap the selected callable as a binding descriptor.
            *args: Positional arguments forwarded to BaseMethod.
            is_binding: Determines if this callable will bind to another object.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseMethod.
        """
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(registry, instance, owner, select, binding, *args, is_binding=is_binding, **kwargs)

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the object's state for pickling.

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
        state.pop("_selected_bind_method", None)
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
        if self.is_binding_wrapper:
            return self._selected_bind_method(self._self_(), self.__owner__)(*args, **kwargs)
        else:
            return self.__wrapped__(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        registry: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        select: str | None = None,
        binding: bool | None = None,
        *args: Any,
        is_binding: bool = True,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            registry: The function registry to use for selecting a function/method.
            instance: An object to wrap which will be used to find functions/methods.
            owner: The class of the object used for finding functions/methods.
            select: The name of the function/method to select for use.
            binding: Determines if this object will bind the selected function as a method.
            *args: Arguments for inheritance.
            is_binding: Determines if this callable will bind to another object. Default is True.
            **kwargs: Keyword arguments for inheritance.
        """
        if registry is not None:
            self.registry = registry
        else:
            self.build_registry()

        super().construct(*args, instance=instance, owner=owner, is_binding=is_binding, **kwargs)

        if select is not None:
            self.select(select)

        if binding is not None:
            self._is_binding_wrapper = binding

    def build_registry(self) -> None:
        """Creates the registry this object will use for function/method selection."""
        self.registry = FunctionRegistry()

    # Registry
    def add_function(self, name: str, func: BaseCallable) -> None:
        """Adds a function to the registry.

        Args:
            name: The name of the function being added.
            func: The function to add to the registry.
        """
        self.registry[name] = func

    def add_method(self, name: str, method: BaseCallable) -> None:
        """Adds a method to the registry.

        Args:
            name: The name of the method being added.
            method: The method to add to the registry.
        """
        self.registry[name] = method.__func__

    def bind_selected(self, instance: Any = None, owner: type[Any] | None = None) -> BaseCallable | MethodType:
        """Creates a method of the selected function using python's method binding.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self if instance is None else self.__wrapped__.__get__(instance, owner)

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
            func = getattr(self._self_(), name).__func__
            self._is_binding_wrapper = True
        self.__func__ = func
        self._selected_bind_method = func.__get__
        self._selected = name

    def add_select_function(self, name: str, func: BaseCallable) -> None:
        """Adds a function to the registry and selects it.

        Args:
            name: The name of the function being added.
            func: The function to add to the registry.
        """
        self.registry[name] = self.__func__ = func
        self._selected_bind_method = func.__get__
        self._selected = name

    def add_select_method(self, name: str, method: BaseCallable) -> None:
        """Adds a method to the registry and selects it.

        Args:
            name: The name of the method being added.
            method: The method to add to the registry.
        """
        self.registry[name] = self.__func__ = method.__func__
        self._selected_bind_method = self.__wrapped__.__get__
        self._selected = name

    # Binding
    def bind_self(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
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
    __get__: GetObjectMethod = bind_self


class MethodMultiplexer(CallableMultiplexer):
    """A callable which will treat the selected function as a method, binding it to the stored instance.

    The MethodMultiplexer has a registry which it uses to store the methods to be multiplexed. Additionally, an object
    can be assigned and its methods will be part of multiplex. Having the object being directly multiplexed allows more
    dynamic interaction as the object's methods may change during runtime. Note that the registry's methods take
    priority in selection.
    """

    # Magic Methods #
    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """First binds the wrapped function, then calls it.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self._selected_bind_method(self._self_(), self.__owner__)(*args, **kwargs)


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
        return self.__wrapped__(*args, **kwargs)
