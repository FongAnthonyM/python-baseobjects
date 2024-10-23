#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dipatchableclass_example.py
An example of how to create and use a DispatchableClass.
"""
# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #
from baseobjects.objects import DispatchableClass


# Definitions #
# Classes #
class ExampleClass(DispatchableClass):
    """An example class that inherits from RegisteredClass.

    Attributes:
        class_register (dict): A dictionary to hold registered classes.
        class_registration (bool): A flag to enable class registration.
    """
    class_register = {}
    class_registration = True  # This flag enables class registration and sets this class as the head of the register.

    @classmethod
    def get_class_information(
        cls,
        namespaces: str | None = None,
        name: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[str, str, str | None]:
        """Gets a class namespace and name from a given set of arguments.

        Args:
            *args: The arguments to get the namespace and name from.
            **kwargs: The keyword arguments to get the namespace and name from.

        Returns:
            The namespace and name of the class.
        """
        return namespaces, name, None


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
    # Dispatching classes from the head class through direct instantiation.
    dispatched_class_1 = ExampleClass("example", "ExampleSubClassOne")
    dispatched_class_2 = ExampleClass("example", "ExampleSubClassTwo")
    print(f"Dispatched Class One: {dispatched_class_1} is an instance of {ExampleSubClassOne}")
    print(f"Dispatched Class Two: {dispatched_class_2} is an instance of {ExampleSubClassTwo}")
