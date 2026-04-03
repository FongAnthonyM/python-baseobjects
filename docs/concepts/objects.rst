Objects
=======

Overview
--------
The objects package contains specialized object types built on the base classes. They provide higher-level behaviors such as automatically generated properties and callback management.

Key Components
--------------
- AutomaticProperties: Creates property descriptors at class creation based on a declarative mapping.
- CallbackManager, CallbackScheduler, ConditionalCallbackEntry: Utilities to register and schedule callbacks under conditions.

AutomaticProperties
-------------------
AutomaticProperties uses a metaclass hook to construct properties from a mapping. Getter/setter creation can be configured via a factory.

.. code-block:: python

   from baseobjects.objects import AutomaticProperties

   class Point(AutomaticProperties):
       # Create properties x and y that get/set attributes _x and _y
       default_property_function_factory = "property_method_factory"
       properties = {
           "x": "_x",
           "y": "_y",
       }

       def __init__(self, x=0, y=0):
           super().__init__()
           self._x = x
           self._y = y

   p = Point(2, 3)
   assert p.x == 2 and p.y == 3
   p.x = 10
   assert p.x == 10

Callbacks (overview)
--------------------
The callback tools allow registering functions and running them later under certain conditions or schedules. See the API reference for concrete usage in the installed version.

Best Practices
--------------
- Keep property maps small and descriptive; avoid generating dozens of dynamic properties without a clear need.
- Prefer explicit names for callbacks and document when they fire to keep behavior discoverable.
