Registered Classes
==================

Overview
--------
The registered-classes concept covers class registries used to discover and instantiate subclasses by name and namespace. This enables plug-in like architectures and late binding of behaviors.

Core Class
----------
- BaseRegisteredClass: Base class that manages a class_register mapping and optional namespaces.

Example
-------
.. code-block:: python

   from baseobjects.objects import BaseRegisteredClass

   class ExampleClass(BaseRegisteredClass):
       class_register = {}
       class_registration = True  # enable auto-registration of subclasses

   class ExampleSubClassOne(ExampleClass):
       class_register_namespace = "example"

   class ExampleSubClassTwo(ExampleClass):
       class_register_namespace = "example"

   # Look up by namespace and class name
   cls1 = ExampleClass.get_registered_class("example", "ExampleSubClassOne")
   cls2 = ExampleClass.get_registered_class("example", "ExampleSubClassTwo")
   assert issubclass(cls1, ExampleClass) and issubclass(cls2, ExampleClass)

   # Instantiate
   instance1 = cls1()
   instance2 = cls2()

Tips
----
- Use clear, stable namespaces to avoid collisions.
- For user-extensible systems, expose helper APIs to list namespaces and registered class names.
