Composition
===========

The composition module allows you to create composite objects with components:

.. code-block:: python

   from baseobjects.composition import BaseComposite, BaseComponent

   class PrintingComponent(BaseComponent):
       """A component that prints information from its composite."""
       def print_information(self):
           """Prints the number attribute of the composite."""
           print(self.composite.number)

   class AddingComponent(BaseComponent):
       """A component that adds a value to the composite's number attribute."""
       def add(self, a):
           """Adds a value to the composite's number attribute."""
           self.composite.number += a

   class ExampleComposite(BaseComposite):
       """A composite class that holds and manages components."""
       # Class Attributes #
       default_component_types = {
           "printing": (PrintingComponent, {}),
           "adding": (AddingComponent, {})
       }

       # Attributes #
       number = 0

   # Create the composite
   composite = ExampleComposite()

   # Use the components
   composite.components["printing"].print_information()  # Prints: 0
   composite.components["adding"].add(5)
   composite.components["printing"].print_information()  # Prints: 5

For more advanced composition with dispatching, see the examples directory.
