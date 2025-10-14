"""functionregistry.py
A registry which holds functions.
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

# Local Packages #
from ..bases import BaseDict
from ..typing import AnyCallable


# Definitions #
# Classes #
class FunctionRegistry(BaseDict):
    """A registry which holds functions.

    Args:
        functions: The functions and their keys to add to the registry.
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
        functions: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a function registry.

        Args:
            functions: Optional mapping of names to callables to add.
            object_: Optional object whose functions will be registered.
            objects: Optional iterable of objects whose functions will be registered.
            *args: Additional positional arguments forwarded to BaseDict.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseDict.
        """
        # Parent Initialization #
        super().__init__(*args, **kwargs)

        # Object Construction #
        if init:
            self.construct(functions=functions, object_=object_, objects=objects, *args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        functions: dict[str, AnyCallable] | None = None,
        object_: Any = None,
        objects: Iterable[Any, ...] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            functions: The functions and their keys to add to the registry.
            object_: An object whose functions will be added to the registry.
            objects: An iterable of objects whose functions will be added to the registry.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if object_ is not None:
            self.update_from_object(object_=object_)

        if objects is not None:
            self.update_from_objects(*objects)

        if functions is not None:
            self.update(functions)

        super().construct(*args, **kwargs)

    def update_from_object(self, object_: Any) -> None:
        """Updates the registry with an object whose functions will be added to the registry.

        Args:
            object_: The object whose functions will be added to the registry.
        """
        for name in set(dir(object_)) | set(vars(object_).keys()):
            attr = getattr(object_, name, None)
            func = None if attr is None or not callable(attr) else attr.__func__ if hasattr(attr, "__func__") else attr
            if func is not None:
                self.data[name] = func

    def update_from_objects(self, *args: Any) -> None:
        """Updates the registry with objects whose functions will be added to the registry.

        Args:
            *args: The objects whose functions will be added to the registry.
        """
        for object_ in args:
            self.update_from_object(object_=object_)
