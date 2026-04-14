Typing
======

Overview
--------
The ``typing`` package provides a collection of reusable type aliases, protocols, and generic types used throughout the library. These utilities make type annotations more expressive, improve code readability, and help static type checkers (like MyPy) verify correct usage of the library's complex components.

Conceptual Workings
-------------------

Standardizing Callables
~~~~~~~~~~~~~~~~~~~~~~~
The library frequently uses complex callable structures in its decorators, registries, and callback managers.

* **AnyCallable**: A broad alias for any callable object (function, method, or class with a ``__call__`` method).
* **PropertyCallbacks**: A specialized type alias used by ``AutomaticProperties`` and its factories to ensure that property implementations follow the expected ``(getter, setter, deleter)`` structure.

Structural Typing (Protocols)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Instead of relying solely on inheritance, many components use structural typing to define interfaces.

* **CallMethod**: A protocol that defines objects capable of being called with specific signatures. This allows the library to work with both standard functions and complex callable objects (like ``BaseCallable`` subclasses) interchangeably.

Key Components
--------------
* **AnyCallable**: The primary alias for flexible callable type hinting.
* **PropertyCallbacks**: A tuple-based alias for defining property logic components.
* **CallMethod**: A protocol for structural verification of callable interfaces.

Performance & Trade-offs
------------------------
+-------------------+--------------------+------------------------+------------------------------------------+
| Component         | Overhead           | Impact                 | Best Use Case                            |
+===================+====================+========================+==========================================+
| Type Aliases      | None               | Static analysis only   | Annotating function signatures           |
+-------------------+--------------------+------------------------+------------------------------------------+
| Protocols         | None (Runtime)     | Structural verification| Decoupling interfaces from inheritance   |
+-------------------+--------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.typing import AnyCallable

   def execute_all(tasks: list[AnyCallable], data: any):
       for task in tasks:
           task(data)

Best Practices
--------------
1. **Consistency**: Prefer importing shared aliases from ``baseobjects.typing`` rather than redefining them locally to ensure consistent annotations across your project.
2. **Use Protocols for Decoupling**: Instead of strict type checks, use protocols to verify that an object provides the required interface, allowing for better interoperability with external code.
3. **Annotate Factories**: Use ``PropertyCallbacks`` when writing custom property factories for ``AutomaticProperties`` to ensure the factory returns the correct three-tuple structure.
