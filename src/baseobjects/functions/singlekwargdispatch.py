"""singlekwargdispatch.py
Extends singledispatch to allow kwargs to be used for dispatching.

The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be specified to
have the dispatcher use that kwarg instead of the first kwarg.
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
from abc import get_cache_token
from collections.abc import Callable
from functools import _find_impl, partial, singledispatchmethod, update_wrapper  # type: ignore[attr-defined]
from inspect import signature
from types import NoneType, UnionType
from typing import Any, TypeVar, Union, get_args, get_origin, get_type_hints, overload
from weakref import WeakKeyDictionary

# Local Packages #
from ..typing import AnyCallable, CallMethod
from .basedecorator import BaseDecorator
from .callablemultiplexer import MethodMultiplexer

# Definitions #
FuncT = TypeVar("FuncT", bound=Callable[..., Any])


# Functions #
def _is_union_type(cls: Any) -> bool:
    return get_origin(cls) in {Union, UnionType}


def _is_valid_dispatch_type(cls: Any) -> bool:
    return isinstance(cls, type) or (_is_union_type(cls) and all(isinstance(arg, type) for arg in get_args(cls)))


# Classes #
class singlekwargdispatch(BaseDecorator, singledispatchmethod):  # type: ignore[type-arg] # noqa: N801
    """Extends singledispatch to allow kwargs to be used for dispatching.

    The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
    allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
    specified to have the dispatcher use that kwarg instead of the first kwarg.

    Attributes:
        _kwarg: The name of the kwarg to use of parsing the args for the class to use for dispatching.
        _parse_method: The default method for parsing the args for the class to use for dispatching.
        _default_parse: The default class to use for dispatching if the kwarg is not found.
        parse: The method for parsing the args for the class to use for dispatching.
        arg_position: The index of the arg to use for dispatching.
        registry: The registry of functions to dispatch to.
        dispatch_cache: The cache of functions to dispatch to.
        cache_token: The cache token for the dispatch function.
        dispatch_function: The function which dispatches to the correct function.

    Args:
        kwarg: Either the name of kwarg to dispatch with or the method to wrap.
        func: The func to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _kwarg: str | None = None
    _parse_method: str = "parse_first"
    _default_parse: type[Any] = NoneType

    parse: MethodMultiplexer
    arg_position: int = 0

    registry: dict[type[Any], AnyCallable | classmethod]  # type: ignore[type-arg]
    dispatch_cache: WeakKeyDictionary[type[Any], AnyCallable | classmethod]  # type: ignore[type-arg]
    cache_token: Any | None = None

    dispatch_function: AnyCallable | classmethod  # type: ignore[type-arg]

    # Properties #
    @property
    def kwarg(self) -> str | None:
        """The name of the kwarg to get the class for the dispatching."""
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    @property
    def dispatcher(self) -> AnyCallable | classmethod:  # type: ignore[override, type-arg]
        """The dispatcher function."""
        return self.dispatch_function

    # Magic Methods #
    # Construction/Destruction
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> AnyCallable:
        """Gets the dispatch method for the instance.

        Args:
            instance: The instance to bind to.
            owner: The owner class.

        Returns:
            The bound dispatch method.
        """
        if instance is None:
            if owner is not None and isinstance(self.func, (classmethod, staticmethod)):
                return self.bind_method_dispatcher(owner, owner)
            return self
        return self.bind_method_dispatcher(instance, owner)

    def __init__(
        self,
        func: AnyCallable | classmethod | None = None,  # type: ignore[type-arg]
        kwarg: str | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            func: Optional function to wrap.
            kwarg: Name of the keyword argument used for dispatch.
            *args: Additional positional arguments forwarded to BaseDecorator.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseDecorator.
        """
        # Attributes #
        self.parse: MethodMultiplexer = MethodMultiplexer(instance=self, select=self._parse_method, is_binding=False)
        self.registry = {}
        self.dispatch_cache = WeakKeyDictionary()

        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Creation #
        if init:
            self.construct(func, kwarg, *args, **kwargs)

    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the object's state for pickling.

        This method is called by the pickle module when serializing the object. It extracts the object's state from both
        __dict__ (if present) and __slots__ (if present), and returns it in a format that can be properly restored by
        __setstate__ during unpickling.

        The method handles four different cases:
        1. Neither __dict__ nor __slots__ are present: Returns None
        2. Only __dict__ is present: Returns a copy of the __dict__
        3. Only __slots__ is present: Returns a tuple of (None, slots_dict)
        4. Both __dict__ and __slots__ are present: Returns a tuple of (dict_copy, slots_dict)

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: Neither __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        state_d = state if isinstance(state, dict) else state[0] if isinstance(state, tuple) else None
        if state_d is not None:
            state_d.pop("dispatch_cache", None)
            state_d.pop("dispatch_function", None)
        return state

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        This method is called by the pickle module when deserializing the object. It restores the object's state from
        the data that was previously returned by __getstate__ during pickling. The method handles different state
        formats to properly restore both __dict__ and __slots__ attributes.

        The method handles four different cases based on the type of state:
        1. None: No state to restore, so nothing is done
        2. dict: The state represents __dict__ attributes, which are updated into the object's __dict__
        3. tuple[None, dict]: The state represents __slots__ attributes, which are set individually
        4. tuple[dict, dict]: The state represents both __dict__ and __slots__ attributes, which are restored
           accordingly

        If the state is of an unexpected type, a TypeError is raised.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object. This should be the value previously
                returned by __getstate__.
        """
        super().__setstate__(state)
        self.dispatch_cache = WeakKeyDictionary()
        if hasattr(self, "func"):
            self.create_dispatcher_function()

    # Instance Methods #
    # Constructors
    def construct(
        self,
        func: AnyCallable | classmethod | None = None,  # type: ignore[type-arg]
        kwarg: AnyCallable | str | None = None,
        *args: Any,
        wrapper_method: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            kwarg: The keyword argument name (or callable) to use for dispatch when no positional arg is provided.
            *args: Arguments for inheritance.
            wrapper_method: The name of the method which will act as the wrapper for this decorator.
            **kwargs: Keyword arguments for inheritance.
        """
        if kwarg is not None and isinstance(kwarg, str):
            self.kwarg = kwarg

        if func is not None:
            self.func = func  # type: ignore[assignment]
            self.registry[object] = func
            self.create_dispatcher_function()
            if self.kwarg is not None:
                if isinstance(func, (classmethod, staticmethod)):
                    target = func.__func__
                else:
                    target = func
                parameters = signature(target).parameters
                self._default_parse = parameters[self.kwarg].default.__class__
                self.arg_position = list(parameters).index(self.kwarg)

        # Unwrap for BaseCallable
        callable_func = func
        if isinstance(func, (classmethod, staticmethod)):
            callable_func = func.__func__

        super().construct(callable_func, *args, **kwargs)  # type: ignore[arg-type]

    def create_dispatcher_function(self) -> AnyCallable | classmethod:  # type: ignore[type-arg]
        """Creates the dispatcher function for this object.

        Returns:
            The dispatcher function.
        """
        if isinstance(self.func, classmethod):

            def dispatch_function(self_: Any, *args: Any, **kwargs: Any) -> Any:  # type: ignore[unreachable]
                return self.dispatch(self.parse(args, kwargs, is_method=True)).__get__(None, self_)(*args, **kwargs)

        else:

            def dispatch_function(self_: Any, *args: Any, **kwargs: Any) -> Any:
                return self.dispatch(self.parse(args, kwargs, is_method=True)).__get__(self_)(*args, **kwargs)

        dispatch_function.__isabstractmethod__ = getattr(self.func, "__isabstractmethod__", False)  # type: ignore[attr-defined]
        dispatch_function.registry = self.registry  # type: ignore[attr-defined]
        update_wrapper(dispatch_function, self.func)
        if isinstance(self.func, classmethod):
            dispatch_function = classmethod(dispatch_function)  # type: ignore[unreachable]
        self.dispatch_function = dispatch_function
        return dispatch_function

    # Setters
    def set_kwarg(self, kwarg: str | None) -> None:
        """Sets the name of the kwarg for dispatching and changes the arg parsing to check for the kwarg.

        Args:
            kwarg: The name of the kwarg or None for checking the first kwarg.
        """
        self.parse.select("parse_first" if kwarg is None else "parse_kwarg")
        self._kwarg = kwarg

    # Parameter Parsers
    def parse_first(self, args: tuple[Any, ...], kwargs: dict[str, Any], is_method: bool = False) -> Any:
        """Parses input for the first arg or the first kwarg's class to be used for dispatching.

        Args:
            args: Positional arguments given to the method.
            kwargs: Keyword arguments given to the method.
            is_method: Determines if this is a method. If True, the first arg is not used.

        Returns:
            The class to be used for dispatching.

        Raises:
            TypeError: If no args or kwargs are given to dispatch.
        """
        try:
            return args[0].__class__
        except IndexError:
            try:
                return next(iter(kwargs.values())).__class__
            except StopIteration:
                msg = "No args or kwargs given to dispatch."
                raise TypeError(msg) from None

    def parse_kwarg(self, args: tuple[Any, ...], kwargs: dict[str, Any], is_method: bool = False) -> Any:
        """Parses input for the first arg or a specific kwarg's class to be used for dispatching.

        Args:
            args: Positional arguments given to the method.
            kwargs: Keyword arguments given to the method.
            is_method: Determines if this is a method. If True, the first arg is not used.

        Returns:
            The class to be used for dispatching.
        """
        try:
            return kwargs[self._kwarg].__class__  # type: ignore[index]
        except KeyError:
            index = self.arg_position - 1 if is_method else self.arg_position
            try:
                return args[index].__class__
            except IndexError:
                return self._default_parse

    # Registering
    @overload
    def register(self, cls: type[Any] | UnionType, method: None = None) -> Callable[[FuncT], FuncT]: ...

    @overload
    def register(self, cls: FuncT, method: None = None) -> FuncT: ...

    @overload
    def register(self, cls: type[Any] | UnionType, method: FuncT) -> FuncT: ...

    def register(self, cls: Any, method: AnyCallable | classmethod | None = None) -> AnyCallable | classmethod:  # type: ignore[type-arg]
        """Registers a function for a type or union of types.

        Raises:
            TypeError: If the provided dispatch key or function annotation is not a
                class or a union of classes, or if the decorator is used incorrectly.

        Returns:
            The registered method.
        """
        if _is_valid_dispatch_type(cls):
            if method is None:
                return partial(self._register, cls=cls)
        else:
            if method is not None:
                msg = f"Invalid first argument to `registry()`. {cls!r} is not a class or union type."
                raise TypeError(msg)
            ann = getattr(cls, "__annotations__", {})
            if not ann:
                msg = (
                    f"Invalid first argument to `registry()`: {cls!r}. "
                    f"Use either `@registry(some_class)` or plain `@registry` "
                    f"on an annotated function."
                )
                raise TypeError(
                    msg,
                )
            method = cls

            # only import typing if annotation parsing is necessary
            if self._kwarg is None:
                argname, cls = next(iter(get_type_hints(method).items()))
            else:
                cls = get_type_hints(method)[self._kwarg]
                argname = self._kwarg
            if not _is_valid_dispatch_type(cls):
                if _is_union_type(cls):
                    msg = f"Invalid annotation for {argname!r}. {cls!r} not all arguments are classes."
                    raise TypeError(msg)
                msg = f"Invalid annotation for {argname!r}. {cls!r} is not a class."
                raise TypeError(msg)

        if _is_union_type(cls):
            for arg in get_args(cls):
                self.registry[arg] = method
        else:
            self.registry[cls] = method
        if self.cache_token is None and hasattr(cls, "__abstractmethods__"):
            self.cache_token = get_cache_token()
        self.dispatch_cache.clear()
        return method

    def _register(self, func: AnyCallable | classmethod, cls: type[Any] | UnionType) -> AnyCallable | classmethod:  # type: ignore[type-arg]
        """Alias for register, where the first argument is the function.

        Args:
            func: The function to register.
            cls: The class to register the function for.

        Returns:
            The registered function.
        """
        return self.register(cls, func)  # type: ignore[type-var]

    # Dispatching
    def dispatch(self, cls: type[Any]) -> AnyCallable | classmethod:  # type: ignore[type-arg]
        """Returns the function registered for the given class."""
        if self.cache_token is not None and self.cache_token != (current_token := get_cache_token()):
            self.dispatch_cache.clear()
            self.cache_token = current_token
        try:
            func = self.dispatch_cache[cls]
        except KeyError:
            try:
                func = self.registry[cls]
            except KeyError:
                func = _find_impl(cls, self.registry)
            self.dispatch_cache[cls] = func
        return func

    # Binding
    def bind_method_dispatcher(self, instance: Any = None, owner: type[Any] | None = None) -> AnyCallable:
        """Creates a function which dispatches the correct bound method based on the input.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.

        Returns:
            A function which dispatches the correct bound method.
        """
        return self.dispatch_function.__get__(instance, owner) if instance is not None else self

    # Method Dispatching
    def dispatch_call(self, *args: Any, **kwargs: Any) -> Any:
        """Parses input to decide which method to use in the registry.

        Args:
            *args: Positional arguments to pass to the found method.
            **kwargs: Keyword arguments to pass to the found method.

        Returns:
            The return of the found method.
        """
        return self.dispatch(self.parse(args, kwargs))(*args, **kwargs)  # type: ignore[operator]

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __call__: CallMethod = dispatch_call
