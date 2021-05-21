#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" wrappers.py
Abstract classes for objects that can wrap any objects and make their attributes/methods accessible from the wrapper.

StaticWrapper calls wrapped attributes/methods by creating property descriptor objects for each of the wrapped objects'
attributes/methods. There some limitations to how StaticWapper can be used. First, for any given subclass of
StaticWrapper all object instances must contain the same wrapped object types because descriptor are handled at the
class scope. Second, creating property descriptors does not happen automatically, creation must be invoked though the
_wrap method. This means a subclass must call _wrap to initialize at some point. Also, if the wrapped objects create new
attributes/methods afterwards, then _wrap or _rewrap must be called to add the new attributes/methods. Overall, this
means subclasses should be designed to wrap the same objects and be used to wrap objects that do not create new
attributes/methods after initialization. These limitation are strict, but it leads to great performance preservation
when compared to normal object attribute/method access.

DynamicWrapper calls wrapped attribute methods by changing the __getattribute__ method to check the wrapped classes
after checking itself. This makes DynamicWrapper very flexible with its wrapped objects. DynamicWrapper does not have
any usage limitation, but it is significantly slower than normal object attribute/method access, because it handles
every get, set, and delete. Performance would be better if DynamicWrapper was written in C.

Ultimately, StaticWrapper and DynamicWrapper are solutions for two different case. StaticWrapper should be used when
if the application is within the limitations StaticWrapper has. DynamicWrapper would be used if the application involves
wrapping various indeterminate object types and/or if the objects change available attributes/methods frequently.

Here are some tested relative performance metrics to highlight those differences: let normal attribute access be 1, when
StaticWrapper accesses a wrapped attribute it takes about 1.7 while DynamicWrapper takes about 4.4. StaticWrapper's
performance loss is debatable depending on the application, but DynamicWrapper takes about x4 longer a normal attribute
access which is not great for most applications.

Todo: add magic method support for StaticWrapper and DynamicWrapper (requires thorough method resolution handling)
"""
__author__ = "Anthony Fong"
__copyright__ = "Copyright 2021, Anthony Fong"
__credits__ = ["Anthony Fong"]
__license__ = ""
__version__ = "1.1.1"
__maintainer__ = "Anthony Fong"
__email__ = ""
__status__ = "Production/Stable"

# Default Libraries #
from builtins import property

# Downloaded Libraries #

# Local Libraries #
from .baseobject import BaseObject
from .initmeta import InitMeta


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
class StaticWrapper(BaseObject, metaclass=InitMeta):
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

    If the objects to wrap can be defined during class instantiation then this class can setup the wrapping by listing
    the types or objects in _wrapped_types. The setup will occur immediately after class instantiation.

    Class Attributes:
        __original_dir_set (:obj:`set` of :obj:`str`): The dir of the original wrapper class.
        _wrapped_types (:obj:`list` of :obj:): A list of either types or objects to setup wrapping for.
        _wrap_attributes (:obj:`list` of :obj:`str`): The list of attribute names that will contain the objects to wrap
            where the resolution order is descending inheritance.
        _original_dir_set (:obj:`set` of :obj:`str`): The names of the attributes to exclude from wrapping.
    """
    __original_dir_set = None
    _wrapped_types = []
    _wrap_attributes = []
    _exclude_attributes = {"__slotnames__"}

    # Class Methods
    @classmethod
    def _init_class_(cls):
        """A method that runs after class creation, creating the original dir as a set and sets up wrapping."""
        cls.__original_dir_set = set(dir(cls))
        cls._class_wrapping_setup()

    @classmethod
    def _class_wrapping_setup(cls):
        """Sets up the class by wrapping what is is _wrapped_types"""
        if cls._wrapped_types:
            try:
                cls._class_wrap(cls._wrapped_types)
            except IndexError:
                raise IndexError("_wrapped_types must be the same length as _wrap_attributes")

    @classmethod
    def _class_wrap(cls, objects):
        """Adds attributes from embedded objects as properties.

         Args:
            objects: A list of objects or types this object will wrap. Must be in the same order as _wrap_attributes.
        """
        if len(objects) != len(cls._wrap_attributes):
            raise IndexError("objects must be the same length as _wrap_attributes")

        for name, obj in zip(reversed(cls._wrap_attributes), reversed(objects)):
            if obj is not None:
                add_dir = set(dir(obj)) - cls.__original_dir_set - cls._exclude_attributes
                for attribute in add_dir:
                    get_, set_, del_ = create_callback_functions(name, attribute)
                    setattr(cls, attribute, property(get_, set_, del_))

    @classmethod
    def _unwrap(cls):
        """Removes all attributes added from other objects."""
        for name in set(dir(cls)) - cls.__original_dir_set:
            if isinstance(getattr(cls, name, None), property):
                delattr(cls, name)

    @classmethod
    def _class_rewrap(cls, objects):
        """Removes all the attributes added from other objects then adds attributes from embedded the objects.

        Args:
            objects: A list of objects or types this object will wrap. Must be in the same order as _wrap_attributes.
        """
        cls._unwrap()
        cls._class_wrap(objects)

    # Methods
    # Wrapping
    def _wrap(self):
        """Adds attributes from embedded objects as properties."""
        for name in reversed(self._wrap_attributes):
            obj = getattr(self, name, None)
            if obj is not None:
                add_dir = set(dir(obj)) - self.__original_dir_set - self._exclude_attributes
                for attribute in add_dir:
                    get_, set_, del_ = create_callback_functions(name, attribute)
                    setattr(type(self), attribute, property(get_, set_, del_))

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
        _wrap_attributes (:obj:`list` of :obj:`str`): The list of attribute names that will contain the objects to
            dynamically wrap where the order is descending inheritance.
    """
    _wrap_attributes = []

    # Magic Methods
    # Attribute Access
    def __getattr__(self, name):
        """Overrides the getattr magic method to get the attribute of another object if that attribute is not present.

        Args:
            name (str): The name of the attribute to get.

        Returns:
            obj: Whatever the attribute contains.
        """
        # Iterate through all object parents to find the attribute
        for attribute in self._wrap_attributes:
            try:
                return getattr(object.__getattribute__(self, attribute), name)
            except AttributeError:
                pass

        raise AttributeError

    def __setattr__(self, name, value):
        """Overrides the setattr magic method to set the attribute of another object if that attribute name is not
        present.

        Args:
            name (str): The name of the attribute to set.
            value: Whatever the attribute will contain.
        """
        # Check if item is in self and if not check in object parents
        if name not in self._wrap_attributes and name not in dir(self):
            # Iterate through all indirect parents to find attribute
            for attribute in self._wrap_attributes:
                if attribute in dir(self):
                    parent_object = getattr(self, attribute)
                    if name in dir(parent_object):
                        return setattr(parent_object, name, value)

        # If the item is an attribute in self or not in any indirect parent set as attribute
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        """Overrides the delattr magic method to set the attribute of another object if that attribute name is not
        present.

        Args:
            name (str): The name of the attribute to delete.
        """
        # Check if item is in self and if not check in object parents
        if name not in self._wrap_attributes and name not in dir(self):
            # Iterate through all indirect parents to find attribute
            for attribute in self._wrap_attributes:
                if attribute in dir(self):
                    parent_object = getattr(self, attribute)
                    if name in dir(parent_object):
                        return delattr(parent_object, name)

        # If the item is an attribute in self or not in any indirect parent set as attribute
        object.__delattr__(self, name)

    # Methods
    # Attribute Access
    def _setattr(self, name, value):
        """An override method that will set an attribute of this object without checking its presence in other objects.

        This is useful for setting new attributes after class the definition.

        Args:
            name (str): The name of the attribute to set.
            value: Whatever the attribute will contain.
        """
        super().__setattr__(name, value)
