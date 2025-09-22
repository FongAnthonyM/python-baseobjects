Usage
=====

This page provides examples and guidance on how to use the baseobjects library.

Installation
-----------

You can install baseobjects using pip:

.. code-block:: bash

   pip install baseobjects

Basic Usage
----------

The baseobjects library provides a variety of base classes and utilities for Python development.
Here are some examples of how to use the main components:

Using BaseObject
~~~~~~~~~~~~~~~~

The ``BaseObject`` class is the foundation of the library, providing basic functionality like copying:

.. code-block:: python

   from baseobjects.bases import BaseObject

   class MyObject(BaseObject):
       def __init__(self, value=None):
           super().__init__()
           self.value = value
           self.data = {"key": "value"}

   # Create an instance
   obj = MyObject(value="test")

   # Create a shallow copy
   copy_obj = obj.copy()

   # Create a deep copy
   deepcopy_obj = obj.deepcopy()

Composition
~~~~~~~~~~

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

Registered Classes
~~~~~~~~~~~~~~~~

The objects module provides classes for class registration and dispatching:

.. code-block:: python

   from baseobjects.objects import BaseRegisteredClass

   class ExampleClass(BaseRegisteredClass):
       """An example class that inherits from BaseRegisteredClass."""
       class_register = {}
       class_registration = True

   class ExampleSubClassOne(ExampleClass):
       """A subclass with a specific namespace for registration."""
       class_register_namespace = "example"

   class ExampleSubClassTwo(ExampleClass):
       """Another subclass with the same namespace for registration."""
       class_register_namespace = "example"

   # Get registered classes
   cls1 = ExampleClass.get_registered_class("example", "ExampleSubClassOne")
   cls2 = ExampleClass.get_registered_class("example", "ExampleSubClassTwo")

   # Create instances
   instance1 = cls1()
   instance2 = cls2()

Caching Tools
~~~~~~~~~~~~

The cachingtools module provides utilities for caching:

.. code-block:: python

   from baseobjects.cachingtools.caches import TimedCache

   # Create a cache with a 60-second timeout
   cache = TimedCache(timeout=60)

   # Cache a value
   cache["key"] = "value"

   # Retrieve a value
   value = cache["key"]

Command Line Interface
---------------------

The baseobjects package also provides a command-line interface:

.. click:: baseobjects.__main__:main
   :prog: python-baseobjects
   :nested: full

More Examples
------------

For more detailed examples, see the examples directory in the repository:

- Composition examples: ``examples/composition/``
- Object examples: ``examples/objects/``

You can also refer to the tests directory for examples of how to test classes that inherit from baseobjects classes.
