"""staticwrapper.py
A wrapper that creates property descriptors for wrapped objects' attributes and methods.

StaticWrapper calls wrapped attributes/functions by creating property descriptor objects for each of the wrapped objects'
attributes/functions. There are some limitations to how StaticWrapper can be used. First, for any given subclass of
StaticWrapper all object instances must contain the same wrapped object types because descriptors are handled at the
class scope. Second, creating property descriptors does not happen automatically, creation must be invoked through the
_wrap method. This means a subclass must call _wrap to initialize at some point. Also, if the wrapped objects create new
attributes/functions afterwards, then _wrap or _rewrap must be called to add the new attributes/functions. Overall, this
means subclasses should be designed to wrap the same objects and be used to wrap objects that do not create new
attributes/functions after initialization. These limitations are strict, but it leads to great performance preservation
when compared to normal object attribute/method access.
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
from builtins import property
from functools import partial, partialmethod
from types import MethodDescriptorType
from typing import Any, ClassVar, get_type_hints

# Local Packages #
from ..bases import SEARCHSENTINEL, BaseObject
from ..metaclasses import InitMeta
from ..typing import AnyCallable, PropertyCallbacks


# Definitions #
# Classes #
class StaticWrapper(BaseObject, metaclass=InitMeta):
    """An object that can call the attributes/functions of embedded objects, acting as if it is inheriting from them.

    Attribute/method resolution of this object will first look with the object itself then it looks within the wrapped
    objects' attributes/functions. The resolution order of the wrapped objects is based on their order in the
    _wrapped_map_ list.

    This object does not truly use method resolution, but instead creates property descriptors that call the
    attributes/functions of the wrapped objects. To create the property descriptors the _wrap method must be called after
    the objects to wrap are stored in this object. Keep in mind, all objects of this class must have the same type of
    wrapped objects, because descriptors are on the class scope. Additionally, this object cannot detect when wrapped
    objects create new or delete attributes/functions. Therefore, subclasses, or the user, must decide when to call
    _wrap to ensure all the attributes/functions are present. This object is best used to wrap frozen objects or ones
    that do not create or delete attributes/functions after initialization.

    If the objects to wrap can be defined during class instantiation then this class can setup the wrapping by listing
    the types or objects in _wrapped_map_. The setup will occur immediately after class instantiation.

    Class Attributes:
        __original_dir_set: The dir of the original wrapper class.
        _get_previous_wrapped: Determines if temporary attributes should be made from the previous wrapped object.
        _set_next_wrapped: Determines if temporary attributes should be passed to the next wrapped object.
        _wrapped_map_: A list of tuples containing the name of the attribute to wrap and the type of the object to wrap.
        _exclude_attributes: The names of the attributes to exclude from wrapping.
        _wrapped_attributes: The names of the attributes to wrap.
    """

    # Class Attributes #
    __original_dir_set: ClassVar[str | None] = None
    _get_previous_wrapped: ClassVar[bool] = False
    _set_next_wrapped: ClassVar[bool] = True

    _wrapped_map_: ClassVar[list[[str, type[Any]], ...]] = []
    _exclude_attributes: ClassVar[set[str]] = {"__slotnames__"}
    _wrapped_attributes: ClassVar[dict[str, set[str]]] = {}

    # Class Methods #
    # Class Construction
    @classmethod
    def _init_class_(
        cls,
        name: str | None = None,
        bases: tuple[Any, ...] | None = None,
        namespace: dict[str, Any] | None = None,
    ) -> None:
        """A method that runs after class creation, creating the original dir as a set and sets up wrapping.

        Args:
            name: The name of the class.
            bases: The base classes of the class.
            namespace: The namespace of the class.
        """
        cls.__original_dir_set = set(dir(cls)) | set(get_type_hints(cls))
        cls._class_wrapping_setup()

    # Descriptor Factories
    @classmethod
    def _wrapped_factory(cls, store_name: str) -> PropertyCallbacks:
        """Creates property modification functions for the wrapped objects.

        Args:
            store_name: The name of the attribute where the wrapped object is stored.

        Returns:
            _get_wrapped: The get function for a property object.
            _set_wrapped: The set function for a property object.
            _del_wrapped: The del function for a property object.
        """
        get_wrapped = partial(cls._get_wrapped, name=store_name)
        set_wrapped = partial(cls._set_wrapped, name=store_name)
        del_wrapped = partial(cls._del_wrapped, name=store_name)

        return get_wrapped, set_wrapped, del_wrapped

    @classmethod
    def _wrapped_attribute_factory(cls, store_name: str, attribute_name: str) -> PropertyCallbacks:
        """Creates property modification functions for accessing a wrapped objects' attributes.

        Args:
            store_name: The name of the attribute where the wrapped object is stored.
            attribute_name: The attribute name of the attribute to modify from the wrapped object.

        Returns:
            _get_wrapped_attribute: The get function for a property object.
            _set_wrapped_attribute: The set function for a property object.
            _del_wrapped_attribute: The del function for a property object.
        """
        get_wrapped_attribute = partial(
            cls._get_wrapped_attribute,
            wrapped_name=store_name,
            attribute_name=attribute_name,
        )

        set_wrapped_attribute = partial(
            cls._set_wrapped_attribute,
            wrapped_name=store_name,
            attribute_name=attribute_name,
        )

        del_wrapped_attribute = partial(
            cls._del_wrapped_attribute,
            wrapped_name=store_name,
            attribute_name=attribute_name,
        )

        return get_wrapped_attribute, set_wrapped_attribute, del_wrapped_attribute

    @classmethod
    def _wrapped_method_factory(cls, store_name: str, method_name: str) -> AnyCallable:
        """A factory for creating method functions for accessing a wrapped objects' methods.

        Args:
            store_name: The name of the attribute where the wrapped object is stored.
            method_name: The attribute name of the attribute to modify from the wrapped object.

        Returns:
            The function for a method.
        """
        return partialmethod(cls._wrapped_method_call, store_name, method_name)

    # Wrapping
    @classmethod
    def _class_wrapping_setup(cls) -> None:
        """Sets up the class by wrapping what is in _wrapped_map_.

        This method is called after class creation to initialize the wrapping of objects specified in the _wrapped_map_
        class attribute.
        """
        if cls._wrapped_map_:
            cls._class_wrap()

    @classmethod
    def _class_wrap(cls, wrapped: list[[str, type[Any]], ...] | None = None) -> None:
        """Adds attributes from embedded objects as properties.

        Args:
            wrapped: A list of tuples containing the name of the attribute to wrap and the type of the object to wrap.
        """
        remove_names = cls.__original_dir_set | cls._exclude_attributes
        if wrapped is None:
            wrapped = cls._wrapped_map_

        for name, obj in wrapped:
            if obj is not None:
                # Create an attribute name to store the wrapped object
                store_name = f"_{name}"

                # Set wrapped property
                setattr(cls, name, property(*cls._wrapped_factory(store_name)))

                # Set attributes properties
                obj_set = set(dir(obj)) | set(get_type_hints(obj if isinstance(obj, type) else type(obj)))
                cls._wrapped_attributes[store_name] = add_dir = obj_set - remove_names
                remove_names |= obj_set
                for attribute in add_dir:
                    if isinstance(getattr(obj, attribute, None), MethodDescriptorType):
                        item = cls._wrapped_method_factory(store_name, attribute)
                    else:
                        item = property(*cls._wrapped_attribute_factory(store_name, attribute))
                    setattr(cls, attribute, item)

    @classmethod
    def _class_unwrap(cls) -> None:
        """Removes all attributes added from other objects.

        This method removes all property descriptors that were added to the class by the _class_wrap method. It restores
        the class to its original statebefore any wrapping was done.
        """
        for name in set(dir(cls)) - cls.__original_dir_set:
            if isinstance(getattr(cls, name, None), property):
                delattr(cls, name)

    @classmethod
    def _class_rewrap(cls, wrapped: list[[str, type[Any]], ...] | None = None) -> None:
        """Removes all attributes added from other objects then adds attributes from the embedded objects.

        This method is a combination of _class_unwrap and _class_wrap. It first removes all property descriptors that
        were added to the class, then adds new ones based on the provided wrapped objects.

        Args:
            wrapped: A list of tuples containing the name of the attribute to wrap and the type of the object to wrap.
        """
        cls._class_unwrap()
        cls._class_wrap(wrapped)

    # Instance Methods #
    # Wrapping
    def _wrap(self) -> None:
        """Adds attributes from embedded objects as properties.

        This method is the instance-level equivalent of _class_wrap. It adds property descriptors to the class for each
        attribute of the wrapped objects. This allows the instance to access the wrapped objects' attributes as if they
        were its own.

        This method should be called after the wrapped objects have been set on the instance. It may also need to be
        called again if the wrapped objects' attributes change.
        """
        remove_names = self.__original_dir_set | self._exclude_attributes
        cls = self.__class__
        for name, _ in self._wrapped_map_:
            # Create an attribute name to store the wrapped object
            store_name = f"_{name}"

            if (obj := getattr(self, store_name, None)) is not None:
                # Set attributes properties
                old_obj_set = self._wrapped_attributes.get(store_name, set())
                obj_set = set(dir(obj)) | set(get_type_hints(obj if isinstance(obj, type) else type(obj)))
                new_obj_set = obj_set | old_obj_set
                add_dir = obj_set - old_obj_set - remove_names
                self._wrapped_attributes[store_name] = new_obj_set - remove_names
                remove_names |= new_obj_set
                for attribute in add_dir:
                    if isinstance(getattr(obj, attribute, None), MethodDescriptorType):
                        item = self._wrapped_method_factory(store_name, attribute)
                    else:
                        item = property(*self._wrapped_attribute_factory(store_name, attribute))
                    setattr(cls, attribute, item)

    # Wrapped Object
    def _get_wrapped(self, name: str) -> Any:
        """Gets a wrapped object from an attribute.

        Args:
            name: The attribute name to get the wrapped object from.

        Returns:
            The wrapped object.
        """
        return getattr(self, name)

    def _set_wrapped(self, value: Any, name: str) -> None:
        """Sets an attribute to store a wrapped object.

        Args:
            value: The wrapped object.
            name: The attribute name to set the wrapped object to.
        """
        # Get wrapped attribute names
        wrapped_names = self._wrapped_attributes[name]
        old_attributes = {}

        # Get the previous wrapped's attributes as temporary attributes
        if self._get_previous_wrapped:
            previous_wrapped = getattr(self, name)
            if value is None:
                for attribute_name in wrapped_names:
                    if (attribute := getattr(previous_wrapped, attribute_name, SEARCHSENTINEL)) is not SEARCHSENTINEL:
                        setattr(self, f"__{name}_{attribute_name}_", attribute)
            elif self._set_next_wrapped:
                old_attributes.update((a, getattr(previous_wrapped, a, SEARCHSENTINEL)) for a in wrapped_names)

        # Set new attributes
        if self._set_next_wrapped:
            for attribute_name in wrapped_names:
                temp_name = f"__{name}_{attribute_name}_"
                temp_attribute = getattr(self, temp_name, SEARCHSENTINEL)
                if (attribute := old_attributes.get(attribute_name, temp_attribute)) is not SEARCHSENTINEL:
                    setattr(value, attribute_name, attribute)
                if temp_attribute is not SEARCHSENTINEL:
                    delattr(self, temp_name)

        setattr(self, name, value)

    def _del_wrapped(self, name: str) -> None:
        """Deletes the attribute that stores the wrapped object.

        Args:
            name: The attribute name to delete the wrapped object from.
        """
        if self._get_previous_wrapped:
            previous_wrapped = getattr(self, name)
            wrapped_names = self._wrapped_attributes[name]
            for attribute_name in wrapped_names:
                if (attribute := getattr(previous_wrapped, attribute_name, SEARCHSENTINEL)) is not SEARCHSENTINEL:
                    setattr(self, f"__{name}_{attribute_name}_", attribute)

        delattr(self, name)

    # Wrapped Attributes
    def _get_wrapped_attribute(self, wrapped_name: str, attribute_name: str) -> Any:
        """Gets an attribute from a wrapped object.

        Args:
            wrapped_name: The attribute name of the wrapped object.
            attribute_name: The attribute name of the attribute to get from the wrapped object.

        Returns:
            The wrapped object.

        Raises:
            AttributeError: If the attribute cannot be found.
        """
        if (wrapped := getattr(self, wrapped_name, SEARCHSENTINEL)) is not SEARCHSENTINEL:
            return getattr(wrapped, attribute_name)
        else:
            try:
                return getattr(self, f"__{wrapped_name}_{attribute_name}_")
            except AttributeError:
                msg = f"'{self.__class__.__name__}' object has no attribute '{attribute_name}'"
                raise AttributeError(msg) from None

    def _set_wrapped_attribute(self, value: Any, wrapped_name: str, attribute_name: str) -> None:
        """Sets an attribute in a wrapped object.

        Args:
            value: The object to set the wrapped objects attribute to.
            wrapped_name: The attribute name of the wrapped object.
            attribute_name: The attribute name of the attribute to set from the wrapped object.
        """
        if (wrapped := getattr(self, wrapped_name, SEARCHSENTINEL)) is not SEARCHSENTINEL:
            setattr(wrapped, attribute_name, value)
        else:
            setattr(self, f"__{wrapped_name}_{attribute_name}_", value)

    def _del_wrapped_attribute(self, wrapped_name: str, attribute_name: str) -> None:
        """Deletes an attribute in a wrapped object.

        Args:
            wrapped_name: The attribute name of the wrapped object.
            attribute_name: The attribute name of the attribute to delete from the wrapped object.
        """
        if (wrapped := getattr(self, wrapped_name, SEARCHSENTINEL)) is not SEARCHSENTINEL:
            delattr(wrapped, attribute_name)

        temp_name = f"__{wrapped_name}_{attribute_name}_"
        if hasattr(self, temp_name):
            delattr(self, temp_name)

    # Wrapped Methods
    def _wrapped_method_call(self, wrapped_name: str, method_name: str, /, *args: Any, **kwargs: Any) -> Any:
        """Calls a method from a wrapped object.

        Args:
            wrapped_name: The attribute name of the wrapped object.
            method_name: The method name of the method to call from the wrapped object.
            *args: Positional arguments to pass to the method.
            **kwargs: Keyword arguments to pass to the method.

        Returns:
            The return of the wrapped object's method.
        """
        return getattr(getattr(self, wrapped_name), method_name)(*args, **kwargs)
