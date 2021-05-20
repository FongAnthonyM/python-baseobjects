#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" wrappers.py



"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Production/Stable"

# Default Libraries #
from builtins import property

# Downloaded Libraries #

# Local Libraries #
from .baseobject import BaseObject


# Definitions #
# Functions #
def create_callback_functions(call_name, name):
    """A factory for creating property modification functions which accesses an embedded objects attributes.

    Args:
        call_name (str): The name attribute the object to call is stored.
        name (str): The name of the attribute that this property will mask.

    Returns:
        get_: The get function for a property object.
        set_: The wet function for a property object.
        del_: The del function for a property object.
    """
    def get_(obj):
        return getattr(getattr(obj, call_name), name)

    def set_(obj, value):
        setattr(getattr(obj, call_name), name, value)

    def del_(obj):
        delattr(getattr(obj, call_name), name)

    return get_, set_, del_


# Classes #
class StaticWrapper(BaseObject):
    """An object that can call the attributes/methods of embedded objects, acting as if it is inheriting from them.

    Attribute/method resolution of this object will first look with the object itself then it look within the wrapped
    objects' attributes/methods. The resolution order of the wrapped objects is based on _wrap_attributes, first element
    to last.

    This object does not truly use method resolution, but instead creates property descriptors that call the
    attributes/methods of the wrapped objects. To create the property descriptors the _wrap method must be called after
    the objects to wrap are store in this object. Keep in mind, all objects of this class must have the same type of
    wrapped objects, because descriptors are on the class scope. Additionally, this object cannot detect when wrapped
    objects create new or delete attributes/methods. Therefore, subclasses or the user must decide when to call _wrap to
    ensure all the attributes/methods are present. This object is best used to wrap frozen objects or ones that do not
    create or delete attributes/methods after initialization.

    Class Attributes:
        _wrap_attributes (:obj:'list' of :obj:'str'): The list of attribute names that will contain the objects to
            dynamically wrap from where the resolution order is descending inheritance.
    """
    __original_dir_set = None
    _wrap_attributes = []
    _exclude_attributes = {"__slotnames__"}

    def __init_subclass__(cls, **kwargs):
        """Initializes the subclass of this class setting the original dir.

        Args:
            **kwargs: Keyword arguments that might be used by a superclass.
        """
        super().__init_subclass__(**kwargs)
        cls.__original_dir_set = set(dir(cls))

    def _wrap(self):
        """Adds attributes from embedded objects as properties."""
        for name in reversed(self._wrap_attributes):
            obj = getattr(self, name, None)
            if obj is not None:
                add_dir = set(dir(obj)) - self.__original_dir_set - self._exclude_attributes
                for attribute in add_dir:
                    get_, set_, del_ = create_callback_functions(name, attribute)
                    setattr(type(self), attribute, property(get_, set_, del_))

    def _unwrap(self):
        """Removes all attributes added from other objects."""
        for name in set(dir(self)) - self.__original_dir_set:
            if isinstance(getattr(type(self), name, None), property):
                delattr(type(self), name)

    def _rewrap(self):
        """Removes all the attributes added from other objects then adds attributes from embedded the objects."""
        self._unwrap()
        self._wrap()


class DynamicWrapper(BaseObject):
    """An object that can call the attributes/methods of embedded objects, acting as if it is inheriting from them.

    When an object of this class has an attribute/method call it will call a listed object's attribute/method. This is
    similar to what an @Property decorator can do but without having to write a decorator for each attribute. Attribute/
    method calling is done dynamically where the objects in the list can change during runtime so the available
    attributes/methods will change based on the objects in the list. Since the available attributes/methods cannot be
    evaluated until runtime, an IDE's auto-complete cannot display all the callable options.

    _attribute_as_parents is the list of attributes of this object that contains the objects that will be used for the
    dynamic calling. This class and subclasses can still have its own defined attributes and methods that are called.
    Which attribute/method is used for the call is handled in the same manner as inheritance where it will check if the
    attribute/method is present in this object, if not it will check in the next object in the list. Therefore, it is
    important to ensure the order of _attribute_as_parents is the order of descending inheritance.

    Class Attributes:
        _attributes_as_parents (:obj:'list' of :obj:'str'): The list of attribute names that will contain the objects to
            dynamically wrap from where the order is ascending inheritance.
    """
    _attributes_as_parents = []

    # Attribute Access
    def __getattribute__(self, name):
        """Overrides the get_attribute magic method to get the attribute of another object if that attribute name is not
        present.

        Args:
            name (str): The name of the attribute to get.

        Returns:
            obj: Whatever the attribute contains.
        """
        try:
            return super().__getattribute__(name)
        except AttributeError as error:
            # Iterate through all object parents to find the attribute
            for attribute in self._attributes_as_parents:
                try:
                    return getattr(super().__getattribute__(attribute), name)
                except AttributeError:
                    pass

            raise error

    def __setattr__(self, name, value):
        """Overrides the setattr magic method to set the attribute of another object if that attribute name is not
        present.

        Args:
            name (str): The name of the attribute to get.
            value: Whatever the attribute will contain.
        """
        # Check if item is in self and if not check in object parents
        if name not in self._attributes_as_parents and name not in dir(self):
            # Iterate through all indirect parents to find attribute
            for attribute in self._attributes_as_parents:
                if attribute in dir(self):
                    parent_object = super().__getattribute__(attribute)
                    if name in dir(parent_object):
                        return setattr(parent_object, name, value)

        # If the item is an attribute in self or not in any indirect parent set as attribute
        super().__setattr__(name, value)

    def _setattr(self, name, value):
        """An override method that will set an attribute of this object without checking its presence in other objects.

        This is useful for setting new attributes after class the definition.

        Args:
            name (str): The name of the attribute to get.
            value: Whatever the attribute will contain.
        """
        super().__setattr__(name, value)
