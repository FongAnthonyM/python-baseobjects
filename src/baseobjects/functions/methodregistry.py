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
from types import MethodType
from typing import Any
from weakref import ReferenceType

# Local Packages #
from ..bases import BaseReducible
from ..typing import AnyCallable
from .functionregistry import FunctionRegistry


# Definitions #
# Classes #
class BaseMethodRegistry(FunctionRegistry, BaseReducible):
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

    # Pickling
    def __getstate__(self) -> None | dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]]:
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
        # Convert weak reference to strong reference for pickling
        state["_self_"] = self.__self__
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
        _self_ = state.pop("_self_", None)
        super().__setstate__(state)
        self.__self__ = _self_

    # Descriptor
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> "BoundMethodRegistry":
        """Descriptor protocol implementation for binding the registry to an instance.

        This method is called when the registry is accessed as an attribute of another object. It returns a new
        BoundMethodRegistry that is bound to the provided instance.

        Args:
            instance: The instance to bind this registry to.
            owner: The class of the instance.

        Returns:
            A new BoundMethodRegistry bound to the provided instance.
        """
        return BoundMethodRegistry(registry=self, instance=instance, owner=owner)

    # Container Methods
    def __getitem__(self, key: str) -> AnyCallable:
        """Gets a method from the registry and binds it to the instance.

        This method retrieves a function from the underlying registry using the provided keyand binds it to the instance
        this registry is bound to, creating a bound method.

        Args:
            key: The key of the function to retrieve from the registry.

        Returns:
            The function bound as a method to the instance.

        Raises:
            KeyError: If the key is not found in the registry.
        """
        return MethodType(self.data[key], self._self_())

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
    """A registry which holds functions and binds them as methods to instances.

    This class extends BaseMethodRegistry to provide descriptor protocol functionality, allowing the registry to be used
    as a class attribute. When accessed through an instance, it returns a BoundMethodRegistry that binds the functions
    to that instance.
    """

    # Magic Methods #
    # Descriptor
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> BoundMethodRegistry:
        """Descriptor protocol implementation for binding the registry to an instance.

        Args:
            instance: The instance to bind this registry to.
            owner: The class of the instance.

        Returns:
            A new BoundMethodRegistry bound to the provided instance.
        """
        return BoundMethodRegistry(registry=self, instance=instance, owner=owner)
