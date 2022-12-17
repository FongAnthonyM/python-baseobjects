""" basemethod.py
An abstract class which implements the basic structure for creating methods.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #
from collections.abc import Callable
from functools import update_wrapper
from types import MethodType
from typing import Any
import weakref

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable, GetObjectMethod
from .baseobject import BaseObject, search_sentinel


# Definitions #
# Classes #
class BaseMethod(BaseObject):
    """An abstract class which implements the basic structure for creating methods.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.

    Attributes:
        __func__: The function to wrap.
        _self_: The a weak reference to the object to bind this object to.
        __owner__: The class owner of the object.
        _original_func: The original function to wrap.
        _selected_get_method: The __get__ method to use as a Callable or a string.
        _get_method_: The method that will be used as the __get__ method.
        _instances: Copies of this object for specific owner instances.
        _default_call_method: A call method that can be used when a call method is not explicitly given.
        _call_method: The method that will be called when this object is called.

    Args:
        func: The function to wrap.
        get_method: The method that will be used for the __get__ method.
        call_method: The default call method to use.
        init: Determines if this object will construct.
    """
    __slots__ = {
        "__func__",
        "_self_",
        "__owner__",
        "_original_func",
        "_selcted_get_method",
        "_instances",
        "_call_method",
    }
    sentinel = search_sentinel

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        get_method: GetObjectMethod | str | None = None,
        call_method: AnyCallable | str | None = None,
        init: bool | None = True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Attributes #
        super().__init__(*args, int=init, **kwargs)

        # Special Attributes #
        self.__func__: AnyCallable | None = None
        self._self_: weakref | None = None
        self.__owner__: type[Any] | None = None

        # Attributes #
        self._original_func: AnyCallable | None = None

        self._selected_get_method: GetObjectMethod | str = "get_copy_bind"
        self._get_method_: GetObjectMethod = self.get_copy_bind.__func__
        self._instances: dict[Any, "BaseMethod"] = {}

        self._default_call_method: AnyCallable = self.func_call.__func__
        self._call_method: AnyCallable = self.func_call.__func__

        # Object Construction #
        if init:
            self.construct(func=func, get_method=get_method, call_method=call_method)

    @property
    def __self__(self) -> Any:
        """The object to bind this object to."""
        try:
            return self._self_()
        except TypeError:
            return None

    @__self__.setter
    def __self__(self, value: Any) -> None:
        self._self_ = None if value is None else weakref.ref(value)

    @property
    def _get_method(self) -> GetObjectMethod:
        """The method that will be used for the __get__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._get_method_.__get__(self, self.__class__)

    @_get_method.setter
    def _get_method(self, value: GetObjectMethod | str) -> None:
        self.set_get_method(value)

    @property
    def call_method(self) -> AnyCallable:
        """The method that will be used for the __call__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._call_method.__get__(self, self.__class__)

    @call_method.setter
    def call_method(self, value: AnyCallable | str) -> None:
        self.set_call_method(value)

    # Descriptors
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> "BaseMethod":
        """When this object is requested by another object as an attribute.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            The bound BaseMethod which can either self or a new BaseMethod.
        """
        return self._get_method(instance=instance, owner=owner)

    # Callable
    def __call__(self, *args, **kwargs) -> Any:
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.call_method(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        get_method: GetObjectMethod | str | None = None,
        call_method: AnyCallable | str | None = None,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            get_method: The method that will be used for the __get__ method.
            call_method: The default call method to use.
        """
        if func is not None:
            self.set_func(func)

        if get_method is not None:
            self.set_get_method(get_method)

        if call_method is not None:
            self.set_call_method(call_method)

    def copy(self) -> "BaseMethod":
        """The copy method for this object

        Returns:
            A copy of this object.
        """
        new = super().copy()

        new.set_get_method(self._selected_get_method)

        if hasattr(self, self._call_method.__name__):
            new._call_method = getattr(new, self._call_method.__name__)

        return new

    # Function
    def set_func(self, func: AnyCallable) -> None:
        """Sets the function that this class wraps.

        Args:
            func: The function to wrap.
        """
        if not callable(func) and not hasattr(func, "__get__"):
            raise TypeError(f"{func!r} is not callable or a descriptor")

        self._original_func = func
        self.__func__ = func
        update_wrapper(self, func)

    # Descriptor
    def set_get_method(self, method: GetObjectMethod | str) -> None:
        """Sets the __get__ method to another function or a method name within this object can be given to select it.

        Args:
            method: The function to set the __get__ method to.
        """
        if isinstance(method, str):
            self._get_method_ = getattr(self, method).__func__
            self._selected_get_method = method
        else:
            self._get_method_ = method
            self._selected_get_method = method

    def get_self(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it returns itself.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            This object.
        """
        return self

    def get_self_bind(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it binds itself to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            This object.
        """
        if instance is not None or owner is not None:
            self.bind(instance=instance, owner=owner)
        return self

    def get_new_bind(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        new_binding: GetObjectMethod | str = "get_self",
        set_attr: bool = True,
    ) -> "BaseMethod":
        """The __get__ method where it binds a new copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the new object will use.
            set_attr: Determines if the new object will be set as an attribute in the object.

        Returns:
            Either bound self or a new BaseMethod bound to the instance.
        """
        if instance is None and owner is None:
            return self.copy()
        else:
            bound = self.bind_to_new(instance=instance, owner=owner, set_attr=set_attr)
            if instance is not None:
                bound.set_get_method(new_binding)
            return bound

    def get_copy_bind(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        new_binding: GetObjectMethod | str = "get_self",
        set_attr: bool = True,
    ) -> "BaseMethod":
        """The __get__ method where it binds a copy of this object to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the copied object will use.
            set_attr: Determines if the new object will be set as an attribute in the object.

        Returns:
            Either bound self or a new BaseMethod bound to the instance.
        """
        if instance is None and owner is None:
            return self
        else:
            bound = self.bind_to_copy(instance=instance, owner=owner, set_attr=set_attr)
            if instance is not None:
                bound.set_get_method(new_binding)
                setattr(instance, bound.__func__.__name__, bound)
            return bound

    def get_subinstance(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
        """The __get__ method where it binds a registered copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            Either bound self or a BaseMethod bound to the instance.
        """
        if instance is None and owner is None:
            return self
        else:
            if instance is None:
                bound = self._instances.get(instance, search_sentinel)
                if bound is search_sentinel:
                    self._instances[instance] = bound = self.bind_to_new(instance=instance, owner=owner)
            else:
                bound = self._instances.get(owner, search_sentinel)
                if bound is search_sentinel:
                    self._instances[owner] = bound = self.bind_to_new(instance=instance, owner=owner)
            return bound

    # Binding
    def bind(
        self,
        instance: Any,
        owner: type[Any] | None = None,
        name: str | None = None,
        set_attr: bool = True,
    ) -> None:
        """Binds this object to another object to give this object method functionality.

        Args:
            instance: The object to bing this object to.
            owner: The class of the other object requesting this object.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.
        """
        self.__self__ = instance
        self.__owner__ = owner
        self.__func__ = self._original_func.__get__(instance, owner)

        if name is None and set_attr:
            name = self.__func__.__name__

        if name is not None:
            if instance is not None:
                setattr(instance, name, self)
            elif owner is not None:
                setattr(owner, name, self)

    def bind_to_new(
        self,
        instance: Any,
        owner: type[Any] | None = None,
        name: str | None = None,
        set_attr: bool = True,
    ) -> "BaseMethod":
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            owner: The class of the other object requesting this object.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.

        Returns:
            The new bound deepcopy of this object.
        """
        if hasattr(self, self._call_method.__name__):
            call_method = self._call_method.__name__
        else:
            call_method = self._call_method

        new_obj = self.__class__(func=self._original_func, get_method=self._selected_get_method, call_method=call_method)
        new_obj.bind(instance=instance, owner=owner, name=name, set_attr=set_attr)
        return new_obj

    def bind_to_copy(
        self,
        instance: Any,
        owner: type[Any] | None = None,
        name: str | None = None,
        set_attr: bool = True,
    ) -> "BaseMethod":
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            owner: The class of the other object requesting this object.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.

        Returns:
            The new bound deepcopy of this object.
        """
        new_obj = self.copy()
        new_obj.bind(instance=instance, owner=owner, name=name, set_attr=set_attr)
        return new_obj

    # Call Methods
    def set_default_call_method(self, method: AnyCallable | str | None) -> None:
        """Sets the default call method to another function or a method within this object can be given to select it.

        Args:
            method: The function or method name to set the call method to.
        """
        if method is None:
            self._default_call_method = self.func_call.__func__
        elif isinstance(method, str):
            self._default_call_method = getattr(self, method).__func__
        else:
            self._default_call_method = method

    def set_call_method(self, method: AnyCallable | str | None) -> None:
        """Sets the call method to another function or a method within this object can be given to select it.

        Args:
            method: The function or method name to set the call method to.
        """
        if method is None:
            self._call_method = self.func_call.__func__
        elif isinstance(method, str):
            self._call_method = getattr(self, method).__func__
        else:
            self._call_method = method

    def func_call(self, *args, **kwargs) -> Any:
        """Calls the wrapped function with the given parameters.

        Args:
            *args: The arguments to pass to the function.
            **kwargs: The keyword arguments to pass to the function.

        Returns:
            The return of the wrapped function
        """
        return self.__func__(*args, **kwargs)
