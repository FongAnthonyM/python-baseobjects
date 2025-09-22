Registered Classes
==================

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
