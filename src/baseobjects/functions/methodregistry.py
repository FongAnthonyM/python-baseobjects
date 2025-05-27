"""methodregistry.py
A registry which holds Methods.
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
from collections.abc import Iterable
from typing import Any
from weakref import ReferenceType

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .functionregistry import FunctionRegistry


# Definitions #
# Classes #
class BaseMethodRegistry(FunctionRegistry):
    """An abstract registry which holds methods.

    Args:
        methods: The functions and their keys to add to the registry.
        object_: An object whose functions will be added to the registry.
        objects: An iterable of objects whose functions will be added to the registry.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        methods: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Override Attributes #
        self.data: FunctionRegistry = FunctionRegistry()

        # Object Construction #
        if init:
            self.construct(methods=methods, object_=object_, objects=objects, *args, **kwargs)

    @property
    def __func__(self) -> FunctionRegistry:
        """The FunctionRegistry this MethodRegistry is wrapping."""
        return self.data

    @__func__.setter
    def __func__(self, value: FunctionRegistry) -> None:
        self.data = value

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        methods: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            methods: The functions and their keys to add to the registry.
            object_: An object whose functions will be added to the registry.
            objects: An iterable of objects whose functions will be added to the registry.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        super().construct(functions=methods, object_=object_, objects=objects, *args, **kwargs)


class BoundMethodRegistry(BaseMethodRegistry):
    """A BaseMethodRegistry which is bound to another object.

    Args:
        registry: The BaseMethodRegistry which this object wraps.
        instance: The other object to bind this registry to.
        owner: The class of the other object to bind this registry to.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _self_: ReferenceType | None = None
    __owner__: type[Any] | None = None

    # Properties #
    @property
    def __self__(self) -> Any:
        """The object to bind this object to."""
        try:
            return self._self_()
        except TypeError:
            return None

    @__self__.setter
    def __self__(self, value: Any) -> None:
        self._self_ = None if value is None else ReferenceType(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        registry: BaseMethodRegistry | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(registry, instance, owner, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        registry: BaseMethodRegistry | None = None,
        instance: Any = None,
        owner: type[Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            registry: The BaseMethodRegistry which this object wraps.
            instance: The other object to bind this registry to.
            owner: The class of the other object to bind this registry to.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if registry is not None:
            self.data = registry.data

        if instance is not None:
            self.__self__ = instance

        if owner is not None:
            self.__owner__ = owner

        super().construct(*args, **kwargs)


class MethodRegistry(BaseMethodRegistry):
    """A registry which holds functions and binds appropriately."""

    # Magic Methods #
    # Descriptor
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> BoundMethodRegistry:
        return BoundMethodRegistry(registry=self, instance=instance, owner=owner)
