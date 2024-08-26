#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" registeredclass_example.py
An example of how to create and use a RegisteredClass.
"""

# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects.objects import RegisteredClass


# Definitions #
# Classes #
class ExampleClass(RegisteredClass):
    """An example class that inherits from RegisteredClass.

    Attributes:
        class_register (dict): A dictionary to hold registered classes.
        class_registration (bool): A flag to enable class registration.
    """
    class_register = {}
    class_registration = True


class ExampleSubClassOne(ExampleClass):
    """A subclass of ExampleClass with a specific namespace for registration.

    Attributes:
        class_register_namespace (str): The namespace for class registration.
    """
    class_register_namespace = "example"


class ExampleSubClassTwo(ExampleClass):
    """Another subclass of ExampleClass with the same namespace for registration.

    Attributes:
        class_register_namespace (str): The namespace for class registration.
    """
    class_register_namespace = "example"


# Main #
if __name__ == "__main__":
    dispatched_class_1 = ExampleClass.get_registered_class("example", "ExampleSubClassOne")
    dispatched_class_2 = ExampleClass.get_registered_class("example", "ExampleSubClassTwo")
    print(f"Dispatched Class One: {dispatched_class_1} == {ExampleSubClassOne}")
    print(f"Dispatched Class Two: {dispatched_class_2} == {ExampleSubClassTwo}")
