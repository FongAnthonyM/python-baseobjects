#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" composition_example.py
An example of how to create and use a Composite.
"""

# Imports #
# Standard Libraries #

# Third-Party Packages #
from baseobjects.composition import BaseComposite, BaseComponent


# Definitions #
# Classes #
class PrintingComponent(BaseComponent):
    """A component that prints information from its composite."""
    def print_information(self):
        """Prints the number attribute of the composite."""
        print(self.composite.number)


class AddingComponent(BaseComponent):
    """A component that adds a value to the composite's number attribute."""
    def add(self, a):
        """Adds a value to the composite's number attribute.

        Args:
            a (int): The value to add.
        """
        self.composite.number += a


class SubtractingComponent(BaseComponent):
    """A component that subtracts a value from the composite's number attribute."""
    def subtract(self, a):
        """Subtracts a value from the composite's number attribute.

        Args:
            a (int): The value to subtract.
        """
        self.composite.number -= a


class ExampleComposite(BaseComposite):
    """A composite class that holds and manages components.

    Attributes:
        default_component_types (dict): Default types of components.
        number (int): A number attribute managed by the composite.
    """
    # Class Attributes #
    default_component_types = {"printing": (PrintingComponent, {}), "adding": (AddingComponent, {})}

    # Attributes #
    number: int = 0


# Main #
if __name__ == "__main__":
    # Create the composite
    composite = ExampleComposite()

    # Use the components
    composite.components["printing"].print_information()
    composite.components["adding"].add(5)
    composite.components["printing"].print_information()

    # Add a new component
    composite.components["subtracting"] = SubtractingComponent(composite=composite)
    composite.components["subtracting"].subtract(3)
    composite.components["printing"].print_information()
