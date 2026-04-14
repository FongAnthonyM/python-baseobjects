Composition
===========

Overview
--------
The ``composition`` package provides a robust framework for building objects from smaller, specialized components. Instead of relying on deep inheritance, which can lead to rigid and fragile architectures, this module favors the "Composition over Inheritance" principle. It enables the creation of modular, testable, and highly configurable systems by coordinating independent ``BaseComponent`` instances within a ``BaseComposite`` object.

Conceptual Workings
-------------------

The Composite-Component Relationship
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The architecture centers on the collaboration between a parent (the composite) and its children (the components).

* **BaseComposite**: Orchestrates a set of named components. It handles their lifecycle and configuration, and provides a unified interface for the rest of the application.
* **BaseComponent**: A specialized unit of logic that maintains a reference to its parent composite (``self.composite``). This allows components to share state and call methods on sibling components through the parent orchestrator.

Dynamic Composition & Factories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Beyond simple static composition, the module provides advanced patterns for sophisticated object creation:

* **CompositeFactoryClass**: Enables subclasses to act as named "presets." When a preset subclass is instantiated, it intercepts the call and returns an instance of the "head class" pre-configured with the subclass's unique component types.
* **DispatchableComposite**: Dynamically selects which specialized subclass to instantiate based on the arguments provided to the constructor, allowing for automatic specialization.

Key Components
--------------
* **BaseComposite**: The central coordinator that manages a dictionary of named components.
* **BaseComponent**: The focused building block that contains specific logic and accesses the composite's context.
* **CompositeFactoryClass**: A registry-backed factory pattern for creating pre-configured composite objects as presets.
* **DispatchableComposite**: A mechanism for selecting the correct composite implementation at runtime based on input data.

Performance & Trade-offs
------------------------
+--------------------------+---------------------+-----------------+------------------------------------------+
| Pattern                  | Overhead            | Complexity      | Primary Benefit                          |
+==========================+=====================+=================+==========================================+
| Static Composition       | Low                 | Low             | Decoupled, testable components           |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``CompositeFactoryClass``| Moderate (lookup)   | Moderate        | Declarative presets for complex objects  |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``DispatchableComposite``| Moderate (dispatch) | High            | Automatic specialization based on data   |
+--------------------------+---------------------+-----------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.composition import BaseComposite, BaseComponent

   class PrintingComponent(BaseComponent):
       def print_info(self):
           # Components access the parent via self.composite
           print(f"Current Value: {self.composite.value}")

   class ExampleComposite(BaseComposite):
       default_component_types = {
           "printer": (PrintingComponent, {}),
       }
       def __init__(self, value=0):
           super().__init__()
           self.value = value

   composite = ExampleComposite(value=42)
   composite.components["printer"].print_info()  # Current Value: 42

Best Practices
--------------
1. **Single Responsibility**: Keep components small and focused on a single task. If a component grows too large, consider splitting it further.
2. **Access via self.composite**: Components should avoid holding direct references to sibling components. Instead, they should access shared state or siblings through ``self.composite``.
3. **Leverage default_component_types**: Define standard configurations in the class definition to make object creation predictable.
4. **Use Factories for Presets**: If you have many common configurations of the same composite, use ``CompositeFactoryClass`` to define them as clean, named subclasses.
