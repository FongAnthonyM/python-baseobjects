"""basecallable.py
An abstract class which implements the basic structure for creating functions and methods.
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
from collections.abc import Iterable
from functools import WRAPPER_ASSIGNMENTS
from typing import Any
import weakref

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable, GetObjectMethod
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseCallable(BaseObject):
    """An abstract class which implements the basic structure for creating a callable.

    Attributes:
        _func_: The function to wrap.

    Args:
        func: The function to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Special Attributes #
        self._func_: AnyCallable | None = None

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, *args, **kwargs)

    @property
    def __func__(self):
        """The function which this callable wraps."""
        return self._func_

    @__func__.setter
    def __func__(self, value: AnyCallable | None) -> None:
        if not callable(value) and not hasattr(value, "__get__"):
            raise TypeError(f"{value!r} is not callable or a descriptor")

        self._func_ = value
        # Assign documentation from warped function to this object.
        for attr in WRAPPER_ASSIGNMENTS:
            try:
                value = getattr(value, attr)
            except AttributeError:
                pass
            else:
                setattr(self, attr, value)

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__func__(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if func is not None:
            self.__func__ = func

        super().construct(*args, **kwargs)


class BaseMethod(BaseCallable):
    """An abstract class which implements the basic structure for creating methods.

    Attributes:
        _self_: A weak reference to the object to bind this object to.
        __owner__: The class owner of the object.

    Args:
        func: The function to wrap.
        instance: The other object to bind this method to.
        owner: The class of the other object to bind this method to.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Special Attributes #
        self._self_: weakref.ref | None = None
        self.__owner__: type[Any] | None = None

        self._binding: bool = True

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, instance=instance, owner=owner, *args, **kwargs)

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

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__func__(self.__self__, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            instance: The other object to bind this method to.
            owner: The class of the other object to bind this method to.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if instance is not None:
            self.__self__ = instance

        if owner is not None:
            self.__owner__ = owner

        super().construct(func=func, *args, **kwargs)

    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> "BaseMethod":
        """Binds this object to another.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.

        Returns:
            This object.
        """
        self.__self__ = instance
        self.__owner__ = owner
        return self

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> "BaseMethod":
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind this object to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set this object to. Default is the function name.

        Returns:
            This object.
        """
        if name is None:
            name = self.__func__.__name__

        self.__self__ = instance
        self.__owner__ = owner
        setattr(instance, name, self)

        return self


class BaseFunction(BaseCallable):
    """An abstract class which implements the basic structure for creating functions.

    Class Attributes:
        method_type: The type of method to create when binding.
    """

    method_type: type[BaseMethod] = BaseMethod

    # Instance Methods #
    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> BaseMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self.method_type(func=self, instance=instance, owner=owner)

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> BaseMethod:
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set the method to. Default is the function name.

        Returns:
            The bound method of this function.
        """
        if name is None:
            name = self.__func__.__name__

        method = self.method_type(func=self, instance=instance, owner=owner)
        setattr(instance, name, method)

        return method

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: GetObjectMethod = bind
