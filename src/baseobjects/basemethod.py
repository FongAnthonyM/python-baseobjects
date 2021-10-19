#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemethod.py
An abstract class which implements the basic structure for creating methods.
"""
# Package Header #
from .__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Default Libraries #
from functools import update_wrapper

# Downloaded Libraries #

# Local Libraries #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseMethod(BaseObject):
    """An abstract class which implements the basic structure for creating methods.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.
        _instances: Copies of this object for specific owner instances.

    Args:
        func: The function to wrap.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """
    sentinel = object()

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func=None, collective=True,  init=True):
        # Special Attributes #
        self.__func__ = None
        self.__self__ = None

        # Attributes #
        self._is_collective = True
        self.__get_method = self.get_self
        self._instances = {}

        # Object Construction #
        if init:
            self.construct(func=func, collective=collective)

    @property
    def is_collective(self):
        """Determines if the cache is collective for all method bindings or for each instance.

        When set, the __get__ method will be changed to match the chosen style.
        """
        return self._is_collective

    @is_collective.setter
    def is_collective(self, value):
        if value is True:
            self.__get_method = self.get_self
        else:
            self.__get_method = self.get_subinstance
        self._is_collective = value

    @property
    def _get_method(self):
        """The method that will be used for the __get__ method.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self.__get_method

    @_get_method.setter
    def _get_method(self, value):
        self.set_get_method(value)

    # Descriptors
    def __get__(self, instance, owner=None):
        """When this object is requested by another object as an attribute.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        return self._get_method(instance, owner=owner)

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, func=None, collective=None):
        """The constructor for this object.

            Args:
                func:  The function to wrap.
                collective: Determines if the cache is collective for all method bindings or for each instance.
            """
        if collective is not None:
            self.is_collective = collective

        if func is not None:
            self.__func__ = func
            update_wrapper(self, self.__func__)

    # Descriptor
    def set_get_method(self, method):
        """Sets the __get__ method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the __get__ method to.
        """
        if isinstance(method, str):
            method = getattr(self, method)

        self.__get_method = method

    def get_self(self, instance, owner=None):
        """The __get__ method where it binds itself to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        if instance is not None:
            self.bind(instance)
        return self

    def get_subinstance(self, instance, owner=None):
        """The __get__ method where it binds a registered copy to the other object.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
        """
        if instance is None:
            return self
        else:
            bound = self._instances.get(instance, self.sentinel)
            if bound is self.sentinel:
                self._instances[instance] = bound = self.bind_to_new(instance=instance)
            return bound

    # Binding
    def bind(self, instance, name=None):
        """Binds this object to another object to give this object method functionality.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.
        """
        self.__self__ = instance
        if name is not None:
            setattr(instance, name, self)

    def bind_to_new(self, instance, name=None):
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.

        Returns:
            The new bound deepcopy of this object.
        """
        new_obj = type(self)(func=self.__func__, collective=self._is_collective)
        new_obj.bind(instance, name=name)
        return new_obj
