Objects
=======

Overview
--------
The ``objects`` package provides high-level components that implement common design patterns and utility behaviors. Built upon the library's foundational bases, these classes offer ready-to-use solutions for declarative property generation and sophisticated callback management. They are designed to reduce boilerplate and improve the maintainability of complex object-oriented systems.

Conceptual Workings
-------------------

Declarative Attributes (AutomaticProperties)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creating many similar properties (getters/setters) can lead to verbose and repetitive code. ``AutomaticProperties`` uses a metaclass hook (from ``InitMeta``) to automatically generate property descriptors at class creation time.

* **Mapping-Based**: Properties are defined in a simple dictionary (``properties``) that maps the property name to its underlying attribute or a configuration tuple.
* **Factory-Driven**: The logic for how getters and setters are created is delegable to a factory function, allowing for customized behavior (e.g., adding logging, validation, or transformation to every property).

Coordinated Events (CallbackManager)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``CallbackManager`` and its associated classes provide a structured way to handle event-driven logic and observer patterns.

* **Conditional Execution**: Callbacks can be registered with specific condition functions, ensuring they only run when certain criteria are met.
* **Async Awareness**: Built-in support for both synchronous and asynchronous (``asyncio``) callbacks, including task management, scheduling, and joining.
* **Decoupling**: Allows components to react to state changes without being tightly coupled to the logic that triggers those changes.

Key Components
--------------
* **AutomaticProperties**: A base class for declarative, factory-driven property generation.
* **CallbackManager**: The central orchestrator for registering, formatting, and triggering callbacks.
* **CallbackScheduler**: Manages the timing, scheduling, and execution order of registered callbacks.
* **ConditionalCallbackEntry**: A structured container for a callback and its specific execution requirements.

Performance & Trade-offs
------------------------
+-------------------------+---------------------+-----------------+------------------------------------------+
| Component               | Overhead            | Complexity      | Primary Benefit                          |
+=========================+=====================+=================+==========================================+
| ``AutomaticProperties`` | Class creation only | Low             | Eliminates boilerplate for properties    |
+-------------------------+---------------------+-----------------+------------------------------------------+
| ``CallbackManager``     | Moderate (lookup)   | Moderate        | Decoupled, conditional event handling    |
+-------------------------+---------------------+-----------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.objects import AutomaticProperties

   class Point(AutomaticProperties):
       # Automatically create 'x' and 'y' properties for '_x' and '_y'
       properties = {"x": "_x", "y": "_y"}

       def __init__(self, x=0, y=0):
           super().__init__()
           self._x = x
           self._y = y

   p = Point(1, 2)
   p.x = 10
   assert p._x == 10

Best Practices
--------------
1. **Use AutomaticProperties for Proxies**: When a class acts as a wrapper or proxy for another object, use ``AutomaticProperties`` to cleanly expose the inner object's attributes.
2. **Limit Property Generation**: While convenient, generating hundreds of properties dynamically can make code harder to navigate. Use it for stable, well-defined attribute sets.
3. **Async Safety**: When using ``CallbackManager`` in an async environment, ensure that long-running callbacks are defined as ``async def`` to avoid blocking the event loop.
