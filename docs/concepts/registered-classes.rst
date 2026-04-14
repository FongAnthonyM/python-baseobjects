Registered Classes
==================

Overview
--------
The ``classregistration`` package provides a powerful mechanism for class discovery, registration, and dynamic instantiation. It enables developers to build highly extensible systems where new functionality can be added by simply defining a subclass, without needing to modify existing code. This "plug-in" architecture is ideal for applications requiring late binding of behaviors or factory patterns that select implementations based on runtime data.

Conceptual Workings
-------------------

The Registration Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~
Registration begins with a "head class." When a class has its ``class_registration`` attribute set to ``True``, it starts tracking its own subclasses in a dedicated registry.

* **Automatic Registration**: Any subclass of a head class that maintains ``class_registration = True`` is automatically added to the parent's registry upon definition (via metaclass hooks).
* **Controlled Inheritance**: Setting ``class_registration = False`` in a subclass allows it to opt-out of the registry while still inheriting from the parent's base logic.

Namespacing for Organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To prevent name collisions in large systems, ``NamespaceClassRegistry`` and ``NamespaceRegisteredClass`` allow classes to be organized into logical groups (namespaces).

* **Lookup by Namespace**: Classes are retrieved using both a namespace identifier and a class name, providing a scoped lookup environment.
* **Registry Independence**: Different hierarchies can maintain independent registries, ensuring that registration in one domain does not pollute another.

Dynamic Dispatch (DispatchableClass)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``DispatchableClass`` takes registration a step further by implementing a factory pattern directly in the ``__new__`` method.

* **Self-Selection**: When attempting to instantiate a ``DispatchableClass``, it automatically looks up the most appropriate registered subclass based on the constructor arguments and returns an instance of that subclass instead.
* **Transparency**: This provides a seamless user experience where the correct implementation is chosen automatically at runtime without explicit factory calls.

Key Components
--------------
* **BaseRegisteredClass**: The foundational interface for class registration hierarchies.
* **NamespaceClassRegistry**: A registry that organizes classes by namespace and name for structured lookup.
* **NamespaceRegisteredClass**: A base class for participating in a namespaced registration system.
* **DispatchableClass**: A base class that automatically dispatches to its subclasses upon instantiation.

Performance & Trade-offs
------------------------
+-------------------------+---------------------+-----------------+------------------------------------------+
| Pattern                 | Overhead            | Complexity      | Primary Benefit                          |
+=========================+=====================+=================+==========================================+
| Static Registration     | Class creation only | Low             | Easy discovery of available subclasses   |
+-------------------------+---------------------+-----------------+------------------------------------------+
| Namespaced Registry     | Low (nested lookup) | Moderate        | Avoids collisions in plugin systems      |
+-------------------------+---------------------+-----------------+------------------------------------------+
| ``DispatchableClass``   | Moderate (dispatch) | High            | Automatic factory behavior on init       |
+-------------------------+---------------------+-----------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.classregistration import NamespaceRegisteredClass

   class Plugin(NamespaceRegisteredClass):
       class_registration = True  # Make this the head class
       class_register = {}        # Initialize the registry mapping

   class MyPlugin(Plugin):
       class_register_namespace = "system"

   # Retrieve the class later
   cls = Plugin.get_registered_class("system", "MyPlugin")
   instance = cls()

Best Practices
--------------
1. **Use Stable Namespaces**: Choose namespace names that are unique and descriptive (e.g., based on the package or domain) to avoid collisions with other extensions.
2. **Explicit Head Classes**: Clearly define which class is the "head" of a registration hierarchy to keep the registry structure predictable.
3. **Handle Missing Classes**: When using ``get_registered_class``, always handle cases where the requested class might not be registered to prevent runtime errors.
4. **Document Registry Keys**: If your registry is intended for third-party extensions, document the expected namespaces and class naming conventions.
