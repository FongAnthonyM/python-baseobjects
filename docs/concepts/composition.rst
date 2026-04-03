Composition
===========

Overview
--------
The composition module enables building objects from smaller, focused components. A composite coordinates its components, while components can access their composite to collaborate. This yields modular, testable systems without deep inheritance.

Purpose
--------
- Favor composition over inheritance for better modularity and reuse.
- Cleanly separate concerns into components that the composite orchestrates.

Core Classes
------------
- BaseComposite: Manages a set of named components and provides the coordination surface.
- BaseComponent: A component that receives a reference to its composite for collaboration.
- CompositeFactoryClass: A specialized composite that intercepts its own construction to return a pre-configured instance of its head class, acting as a "preset" factory.

Factory Patterns
----------------
Beyond simple composition, the module provides specialized dispatching patterns:

- **DispatchableComposite**: Dynamically selects which specialized subclass to instantiate based on constructor arguments.
- **CompositeFactoryClass**: Enables subclasses to act as named "presets." When a preset subclass is instantiated, it returns an instance of the "head class" pre-configured with the subclass's component types. This is ideal for complex objects with many optional component configurations.

Basic Example
-------------
.. code-block:: python

   from baseobjects.composition import BaseComposite, BaseComponent

   class PrintingComponent(BaseComponent):
       def print_information(self):
           print(self.composite.number)

   class AddingComponent(BaseComponent):
       def add(self, a):
           self.composite.number += a

   class ExampleComposite(BaseComposite):
       default_component_types = {
           "printing": (PrintingComponent, {}),
           "adding": (AddingComponent, {}),
       }
       number = 0

   composite = ExampleComposite()
   composite.components["printing"].print_information()  # 0
   composite.components["adding"].add(5)
   composite.components["printing"].print_information()  # 5

Tips
----
- Keep components small and single-purpose; let the composite orchestrate lifecycle and interactions.
- Prefer explicit component names; use default_component_types to configure standard setups.
