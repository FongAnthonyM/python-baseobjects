"""automaticproperties.py
An abstract class which creates properties for this class automatically.
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
from collections.abc import Callable, Iterable
from abc import abstractmethod
from builtins import property
from functools import partialmethod
from typing import Any, ClassVar

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from ..metaclasses import InitMeta
from ..typing import PropertyCallbacks


# Definitions #
# Classes #
class AutomaticProperties(BaseObject, metaclass=InitMeta):
    """An abstract class which creates properties for this class automatically.

    Class Attributes:
        _properties_map: The functions used to create properties.
        _properies: A container that has the names of the properties and some information to build them.
    """

    # Class Attributes #
    default_property_function_factory: ClassVar[Callable]
    properties: ClassVar[dict[str, str | Iterable[Callable, str, dict]]] = {}

    # Class Methods #
    # Class Construction
    @classmethod
    def _init_class_(
        cls,
        name: str | None = None,
        bases: tuple[type, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        """A method that runs after class creation, creating the properties for this class.

        Args:
            name: The name of this class.
            bases: The parent types of this class.
            namespace: The functions and class attributes of this class.
        """
        super().__init__(name, bases, namespace)
        cls._construct_properties_()

    # Property Methods
    @classmethod
    def property_class_get(cls, self, name: str) -> Any:
        """A generic class method get for properties which can be implemented in a subclass.

        Args:
            self: The target object to get the attribute from.
            name: The name of the attribute to get from the object.

        Returns:
            The item to return.
        """
        return getattr(self, name)

    @classmethod
    def property_class_set(cls, self, name: str, value: Any) -> None:
        """A generic class method set for properties which can be implemented in a subclass.

        Args:
            self: The target object to set.
            name: The name of the attribute to set.
            value: The item to set within the target object.
        """
        setattr(self, name, value)

    @classmethod
    def property_class_del(cls, self, name: str) -> None:
        """A generic class method delete for properties which can be implemented in a subclass.

        Args:
            self: The target object to delete an attribute from.
            name: The name of the attribute to delete in the object.
        """
        delattr(self, name)

    # Callback Factories
    @classmethod
    def property_class_method_factory(cls, info: str) -> PropertyCallbacks:
        """A factory method for creating property modification methods using class methods.

        Args:
            info: An object that can be used to create the get, set, and delete functions

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        name = info

        def _property_class_get(self) -> Any:
            """Gets an attribute in the object."""
            return cls.property_class_get(self, name)

        def _property_class_set(self, value: Any) -> None:
            """Sets an attribute in the object."""
            cls.property_class_set(self, name, value)

        def _property_class_del(self) -> None:
            """Deletes an attribute in the object."""
            cls.property_class_del(self, name)

        return _property_class_get, _property_class_set, _property_class_del

    @classmethod
    def property_method_factory(cls, info: str) -> PropertyCallbacks:
        """A factory method for creating property modification methods.

        Args:
            info: An object that can be used to create the get, set, and delete functions

        Returns:
            get_: The get function for a property object.
            set_: The wet function for a property object.
            del_: The del function for a property object.
        """
        name = info

        _property_get = partialmethod(cls.property_get, name)
        _property_set = partialmethod(cls.property_set, name)
        _property_del = partialmethod(cls.property_del, name)

        return _property_get, _property_set, _property_del

    # Properties Constructor
    @classmethod
    def _construct_properties_(cls, property_map: dict[str, str | Iterable[Callable, str, dict]] | None = None) -> None:
        """Constructs all properties from a list which maps the properties and their functionality.

        Args:
            map_: A list to map the properties from.

        Raises:
            AttributeError: If an attribute in the map is not in the object.
        """
        if property_map is None:
            property_map = cls.properties

        for name, info in property_map.items():
            match info:
                case str():
                    new_property = property(*cls.default_property_function_factory(info))
                case _:
                    factory, attribute, factory_kwargs = info
                    new_property = property(*factory(attribute, **factory_kwargs))
            setattr(cls, name, new_property)


    # Instance Methods #
    # Property Methods
    def property_get(self, name: str) -> Any:
        """A generic get for properties which can be implemented in a subclass.

        Args:
            name: The name of the attribute to get from the object.

        Returns:
            The item to return.
        """
        return getattr(self, name)

    def property_set(self, name: str, value: Any) -> None:
        """A generic set for properties which can be implemented in a subclass.

        Args:
            name: The name of the attribute to set.
            value: The item to set within the target object.
        """
        setattr(self, name, value)

    def property_del(self, name: str) -> None:
        """A generic delete for properties which can be implemented in a subclass.

        Args:
            name: The name of the attribute to delete in the object.
        """
        delattr(self, name)
