"""basecallable.py
Abstract classes for creating customizable callable objects, functions, and methods.

This module provides the BaseCallable class and its derivatives (BaseMethod and BaseFunction), which serve as
foundational classes for creating callable objects in Python. These classes implement the necessary magic methods and
provide utilities for wrapping functions, binding methods to instances, and handling coroutines.

The module includes three main classes:

1. BaseCallable: An abstract base class that implements the core functionality for creating callable objects.
   It provides mechanisms for wrapping existing functions, handling coroutines, and implementing the descriptor
   protocol for method binding. BaseCallable serves as the foundation for all callable objects in the library.

2. BaseMethod: Extends BaseCallable to create method-like objects that can be bound to class instances.
   It maintains a weak reference to the instance it's bound to and implements proper method binding behavior.
   BaseMethod is designed to behave like a standard Python method, but with enhanced capabilities.

3. BaseFunction: Extends BaseCallable to create function-like objects that can be converted to methods
   when bound to instances. It provides utilities for binding to instances and attributes, making it ideal
   for creating decorators and function factories.

These classes are particularly useful for creating decorators, method factories, and other advanced programming
patterns that require customizable callable objects with specific behaviors. They handle edge cases like proper
pickling, coroutine support, and attribute preservation that are often overlooked in custom callable implementations.
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
from functools import WRAPPER_ASSIGNMENTS
from inspect import iscoroutinefunction
from types import MethodType
from typing import Any
from weakref import ReferenceType

# Local Packages #
from ..typing import AnyCallable, CallMethod, DescriptorGetMethod
from .basereducible import BaseReducible


# Definitions #
# Classes #
class BaseCallable(BaseReducible):
    """An abstract class that implements the core functionality for creating callable objects.

    BaseCallable provides a foundation for creating custom callable objects in Python. It wraps an existing function or
    callable and implements the necessary protocols to make the wrapper behave like the wrapped function, including
    attribute copying, docstring preservation, and proper handling of coroutines.

    The class implements both the callable protocol (through __call__) and the descriptor protocol (through __get__),
    allowing instances to be called directly and to be bound to instances when accessed as attributes. It also provides
    utilities for creating function wrappers and binding to instances.

    When a function is wrapped by BaseCallable, all its attributes, including docstrings and annotations, are preserved.
    This ensures that the wrapped function maintains its identity and can be used in contexts that inspect function
    attributes. Additionally, BaseCallable properly handles coroutines, allowing async functions to be wrapped without
    losing their async behavior.

    Attributes:
        __wrapped__: The function or callable that this object wraps. All calls are delegated to this object.
        _exclude_attributes: A set of attribute names that should not be copied from the wrapped function to the wrapper
        _cast_excluded: A set of attribute names that should not be copied from the wrapper to the wrapped function
        _is_coroutine_marker: A flag indicating whether the wrapped function is a coroutine. Used to maintain async
            behavior.
    """

    # Attributes #
    __wrapped__: AnyCallable | None = None
    _exclude_attributes: set[str] = {"__annotate__", "__type_params__"}
    _cast_excluded: set[str] = {"__call__"}
    _is_coroutine_marker: object | None = None

    # Properties #
    @property
    def __func__(self) -> AnyCallable | None:
        """The function which this callable wraps."""
        return self.__wrapped__

    @__func__.setter
    def __func__(self, value: AnyCallable | None) -> None:
        """Sets the function which this callable wraps.

        This setter validates that the provided value is callable or a descriptor, then sets it as the wrapped function.
        It also copies all relevant attributes from the wrapped function to this object, including docstrings,
        annotations, and other metadata.

        Args:
            value: The callable to wrap, or None to clear the current wrapped callable.
        """
        if value is None:
            self.__wrapped__ = None
            self._is_coroutine_marker = None
            for attr in WRAPPER_ASSIGNMENTS:
                try:
                    delattr(self, attr)
                except AttributeError:
                    pass
        else:
            self.__wrapped__ = value
            # Determine if the wrapped function is a coroutine
            is_base_callable = False
            try:
                # Use object.__getattribute__ to check for a marker that only BaseCallable has
                # without triggering descriptors or complex isinstance logic.
                object.__getattribute__(value, "_is_coroutine_marker")
                is_base_callable = True
            except (AttributeError, TypeError):
                pass

            if is_base_callable:
                self._is_coroutine_marker = value._is_coroutine_marker
            elif iscoroutinefunction(value):
                self._is_coroutine_marker = True
            else:
                self._is_coroutine_marker = None

            # Assign standard function attributes from wrapped function to this object
            for attr in WRAPPER_ASSIGNMENTS:
                if attr in self._exclude_attributes:
                    continue
                try:
                    attr_value = getattr(value, attr)
                except AttributeError:
                    pass
                else:
                    setattr(self, attr, attr_value)

            # Assign other custom attributes
            for attr, attr_value in getattr(value, "__dict__", {}).items():
                if attr not in self._exclude_attributes and not hasattr(self, attr):
                    setattr(self, attr, attr_value)

    @__func__.deleter
    def __func__(self) -> None:
        """Deletes the wrapped function."""
        del self.__wrapped__
        self._is_coroutine_marker = None
        for attr in WRAPPER_ASSIGNMENTS:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    @property
    def is_coroutine(self) -> bool:
        """Determines if the wrapped function is a coroutine."""
        return self._is_coroutine_marker is not None

    # Magic Methods #
    # Construction/Destruction
    def __new__(  # type:ignore[misc]
        cls,
        func: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> BaseCallable | MethodType:
        """Dispatches either an unbound instance or a bound instance if the given function is a method.

        This method creates a new instance of the class and handles the special case where the provided function is
        already a bound method. In that case, it extracts the underlying function and the instance it's bound to, then
        creates a new callable bound to the same instance.

        Args:
            func: The function or method to wrap. If this is a bound method, the new callable will also be bound to the
                same instance.
            *args: Positional arguments for building an instance.
            **kwargs: Keyword arguments for building an instance.

        Returns:
            A new instance of BaseCallable, possibly bound to an instance if func was a bound method.
        """
        new_callable = super().__new__(cls)

        # Check if func is a bound method
        if (instance := getattr(func, "__self__", None)) is not None and hasattr(func, "__func__"):
            # Initialize with the underlying function
            new_callable.__init__(func.__func__, *args, **kwargs)  # type:ignore[misc]
            # Binds to the same instance as the original method
            new_callable = new_callable.__get__(instance, instance.__class__)

        return new_callable

    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes a new BaseCallable instance.

        Args:
            func: The function or callable to wrap. If provided, this will be set as the wrapped function.
            *args: Additional positional arguments passed to the construct method or parent class.
            init: Determines if the construct method will be called to complete initialization.
            **kwargs: Additional keyword arguments passed to the construct method or parent class.
        """
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(*args, func=func, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        This method initializes the callable object with the provided function and other arguments. It sets the wrapped
        function and calls the parent class's construct method to handle any additional initialization.

        Args:
            func: The function to wrap. If provided, this will be set as the wrapped function.
            *args: Additional positional arguments passed to the parent class's construct method.
            **kwargs: Additional keyword arguments passed to the parent class's construct method.
        """
        if func is not None:
            self.__func__ = func

        super().construct(*args, **kwargs)

    # Binding
    def bind_builtin(self, instance: Any = None, owner: Any = None) -> Any:
        """Creates a method of this wrapper which is bound to another object using the builtin method.

        Args:
            instance: The object to bind the method to. This becomes the 'self' parameter when the method is called.
            owner: The class of the object being bound to. This parameter is included for API consistency but is not
                used in this method.

        Returns:
            A standard Python method object that binds this callable to the specified instance.
        """
        return self if instance is None else MethodType(self, instance)

    def bind_wrapped(self, instance: Any = None, owner: type[Any] | None = None) -> Any:
        """Creates a method of the wrapped function which is bound to another object.

        This method uses the descriptor protocol to bind the wrapped function directly to the specified instance,
        bypassing this callable object. This is useful to preserve the original binding behavior of the
        wrapped function.

        Args:
            instance: The object to bind the wrapped function to. This becomes the 'self' parameter when the method is
                called.
            owner: The class of the object being bound to. This is used for proper method binding and to determine the
                appropriate binding behavior.

        Returns:
            A method object that binds the wrapped function to the specified instance.
        """
        return self.__wrapped__.__get__(instance, owner)  # type:ignore[union-attr]

    # Calling
    def call_wrapped(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the provided arguments.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of calling the wrapped function.
        """
        return self.__wrapped__(*args, **kwargs)  # type:ignore[misc]

    # Casting
    def as_function(self) -> AnyCallable:
        """Creates a standard Python function that wraps this callable object.

        This method creates a new function that delegates all calls to this callable object. It preserves the coroutine
        behavior of the wrapped function and copies all relevant attributes from this callable to the new function.

        Returns:
            A standard Python function that delegates to this callable object. If the wrapped function is a coroutine
            function, the returned function will also be a coroutine function.
        """
        # Creates appropriate wrapper function based on whether the wrapped function is a coroutine
        if self._is_coroutine_marker is not None:

            async def wrapper_function(*args: Any, **kwargs: Any) -> Any:
                """A function which wraps a callable.

                Returns:
                    The result returned by invoking this callable with the provided arguments.
                """
                return await self(*args, **kwargs)

        else:

            def wrapper_function(*args: Any, **kwargs: Any) -> Any:  # type:ignore[misc]
                """A function which wraps a callable.

                Returns:
                    The result returned by invoking this callable with the provided arguments.
                """
                return self(*args, **kwargs)

        # Copy standard function attributes
        for attr in WRAPPER_ASSIGNMENTS:
            try:
                value = getattr(self, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper_function, attr, value)

        # Copy all attributes from this callable to the wrapper function
        wrapper_function.__dict__.update(self.__dict__)
        wrapper_function.__wrapped__ = self  # type: ignore[attr-defined]

        # Removes excluded attributes from the wrapper function
        wrapper_dict = wrapper_function.__dict__
        for n in (n for n in self._cast_excluded if n in wrapper_dict):
            del wrapper_dict[n]

        return wrapper_function

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: AnyCallable = bind_builtin
    __call__: CallMethod = call_wrapped


class BaseMethod(BaseCallable):
    """An abstract class that implements the structure for creating method-like callable objects.

    BaseMethod extends BaseCallable to create callable objects that behave like methods, maintaining a reference to the
    instance they're bound to and properly handling method binding semantics. This class is particularly useful for
    creating custom method types, method factories, and method decorators.

    Unlike regular functions, methods are bound to a specific instance and receive that instance as their first argument
    (typically named 'self'). BaseMethod implements this behavior by storing a weak reference to the bound instance and
    using it when the method is called. The weak reference prevents memory leaks that could occur if the method held a
    strong reference to the instance.

    When a BaseMethod is accessed through an instance (e.g., `instance.method`), it returns itself with the instance
    bound to it. This mimics Python's standard method binding behavior. When called, it retrieves the bound instance
    from the weak reference and passes it as the first argument to the wrapped function.

    Attributes:
        _self_: A weak reference to the object this method is bound to. Using a weak reference prevents circular
            references that could lead to memory leaks.
        __owner__: The class of the object this method is bound to. This is used for proper method binding and to
            support inheritance.
        is_binding: Determines if this callable will bind to another object when accessed as an attribute. If False, the
            method behaves more like a static method. Default is True.
    """

    # Attributes #
    _self_: ReferenceType[Any] | None = None
    __owner__: type[Any] | None = None

    is_binding: bool = True

    # Properties #
    @property
    def __self__(self) -> Any:
        """The object to which this method is bound."""
        try:
            return self._self_()  # type: ignore[misc]
        except TypeError:
            return None

    @__self__.setter
    def __self__(self, value: Any) -> None:
        """Sets the object to which this method is bound."""
        self._self_ = None if value is None else ReferenceType(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        is_binding: bool = True,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes a new BaseMethod instance.

        Args:
            func: The function or callable to wrap. If provided, this will be set as the wrapped function.
            instance: The object to bind this method to. This becomes the 'self' parameter when the method is called.
            owner: The class of the object to bind this method to. This is used for proper method binding and to support
                inheritance.
            *args: Additional positional arguments passed to the construct method or parent class.
            is_binding: Determines if this callable will bind to another object when accessed as an attribute. If False,
                the method behaves more like a static method.
            init: Determines if the construct method will be called to complete initialization.
            **kwargs: Additional keyword arguments passed to the construct method or parent class.
        """
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func, instance, owner, *args, is_binding=is_binding, **kwargs)

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
        # Converts weak reference to strong reference for pickling
        if isinstance(state, dict):
            state["_self_"] = self.__self__
        elif isinstance(state, tuple) and state[0] is not None:
            state[0]["_self_"] = self.__self__
        elif state is None:
            state = {"_self_": self.__self__}
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
        _self_ = None
        if isinstance(state, dict):
            _self_ = state.pop("_self_", None)
        elif isinstance(state, tuple) and state[0] is not None:
            _self_ = state[0].pop("_self_", None)

        super().__setstate__(state)
        self.__self__ = _self_

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        is_binding: bool = True,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        This method initializes the method object with the provided function, instance, owner, and binding behavior. It
        sets the is_binding flag, binds to the instance if provided, sets the owner class if provided, and calls the
        parent class's construct method to handle the function wrapping.

        Args:
            func: The function to wrap. This will be called when the method is invoked.
            instance: The object to bind this method to. This becomes the 'self' parameter when the method is called.
            owner: The class of the object to bind this method to. This is used for proper method binding and to support
                inheritance.
            *args: Additional positional arguments passed to the parent class's construct method.
            is_binding: Determines if this callable will bind to another object when accessed as an attribute. If False,
                the method behaves more like a static method.
            **kwargs: Additional keyword arguments passed to the parent class's construct method.
        """
        self.is_binding = is_binding

        if instance is not None:
            self.__self__ = instance

        if owner is not None:
            self.__owner__ = owner

        super().construct(func, *args, **kwargs)

    # Binding
    def bind_self(self, instance: Any = None, owner: type[Any] | None = None) -> BaseMethod:
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
        return self

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> BaseMethod:
        """Binds this method to an instance and sets it as an attribute on that instance.

        Args:
            instance: The object to bind this method to and set the attribute on. This becomes the 'self' parameter when
                the method is called.
            owner: The class of the object being bound to. This is used for proper method binding and to support
                inheritance.
            name: The name of the attribute to set on the instance. If None, the name of the wrapped function is used.

        Returns:
            This method object, now bound to the specified instance and set as an attribute.
        """
        if name is None:
            name = self.__wrapped__.__name__  # type:ignore[union-attr]

        if instance is not None:
            self.__self__ = instance
        if owner is not None:
            self.__owner__ = owner
        setattr(instance, name, self)

        return self

    def call_binding(self, *args: Any, **kwargs: Any) -> Any:
        """Binds the wrapped function to the stored instance and calls it.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The result of calling the wrapped function with the bound instance and the provided arguments.
        """
        try:
            return self.__wrapped__.__get__(self._self_(), self.__owner__)(*args, **kwargs)  # type: ignore[union-attr, misc]
        except AttributeError:
            if (instance := self.__self__) is not None:
                return self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]
            return self.__wrapped__(*args, **kwargs)  # type: ignore[misc]
        except TypeError:
            return self.__wrapped__(*args, **kwargs)  # type: ignore[misc]

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: DescriptorGetMethod = bind_self
    __call__: CallMethod = call_binding  # type: ignore[assignment]


class BaseFunction(BaseCallable):
    """An abstract class that implements the structure for creating function-like callable objects.

    BaseFunction extends BaseCallable to create callable objects that behave like functions but can be converted to
    methods when bound to instances. This class is particularly useful for creating decorators, function factories, and
    other callable objects that need to support both function-like and method-like behavior.

    When a BaseFunction is accessed through an instance (e.g., `instance.func`), it creates a new method of type
    `method_type` that is bound to the instance. This allows BaseFunction objects to behave like regular functions
    when called directly, but like methods when accessed through an instance attribute.

    BaseFunction provides methods for explicitly binding to instances (`bind`) and for binding to an instance and
    setting the result as an attribute on the instance (`bind_to_attribute`). These methods give fine-grained
    control over the binding process, which is useful for implementing decorators and other advanced patterns.

    Attributes:
        method_type: The type of method to create when binding this function to an instance. By default, this is
                    BaseMethod, but it can be customized to use different method implementations. This allows
                    for customizing the behavior of bound methods.
    """

    # Attributes #
    method_type: type[BaseMethod] = BaseMethod

    # Instance Methods #
    # Binding
    def bind(self, instance: Any, owner: type[Any] | None = None) -> BaseMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to. This becomes the 'self' parameter when the method is called.
            owner: The class of the object being bound to. This is used for proper method binding and to support
                inheritance.

        Returns:
            A new method object of type method_type that wraps this function and is bound to the specified instance and
            owner class.
        """
        return self.method_type(func=self, instance=instance, owner=owner)

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> BaseCallable:
        """Creates a method of this function which is bound to another object and sets it as an attribute.

        Args:
            instance: The object to bind the method to and set the attribute on. If None, this function is returned
                unchanged.
            owner: The class of the object being bound to. This is used for proper method binding and to support
                inheritance.
            name: The name of the attribute to set on the instance. If None, a unique cache name is used.

        Returns:
            If instance is None, this function is unchanged. Otherwise, the new method object that was created and set
            as an attribute on the instance.
        """
        if instance is None:
            return self

        if name is None:
            name = self.__wrapped__.__name__  # type:ignore[union-attr]

        # Create a new method bound to the instance
        method = self.method_type(func=self, instance=instance, owner=owner)
        setattr(instance, name, method)

        return method
