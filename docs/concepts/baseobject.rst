BaseObject
==========

Overview
--------
The ``BaseObject`` class is the most fundamental building block in the library. It provides a standardized foundation for Python objects, ensuring predictable behavior for essential operations like copying and initialization. By deriving from ``BaseObject``, developers can create "well-behaved" objects that integrate seamlessly with the rest of the ``baseobjects`` ecosystem.

Conceptual Workings
-------------------
Standardizing Copy Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python's built-in ``copy`` module is powerful but can be inconsistent if objects do not explicitly implement ``__copy__`` or ``__deepcopy__``. ``BaseObject`` addresses this by providing ``copy()`` and ``deepcopy()`` methods that delegate to the standard library while offering a cleaner, more discoverable API.

The ``construct()`` Lifecycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlike ``__init__``, which is called automatically by Python's object creation process, the ``construct()`` method is a lifecycle hook intended for manual or deferred initialization.

* **Why it matters**: It allows for re-initializing an existing object or performing setup that should not happen during every ``__init__`` call (e.g., in complex inheritance or deserialization).
* **Subclassing**: Derived classes should override ``construct()`` to handle their specific setup logic and always call ``super().construct(*args, **kwargs)``.

Key Class: BaseObject
---------------------
* **ABC Integration**: ``BaseObject`` inherits from ``abc.ABC``, signaling that it is an abstract base and should not be instantiated directly.
* **Flexible Initialization**: The ``__init__`` and ``construct`` methods accept arbitrary arguments (``*args``, ``**kwargs``), making it highly compatible with various inheritance patterns.

Performance & Trade-offs
------------------------
+--------------------------+---------------------+-----------------+------------------------------------------+
| Operation                | Implementation      | Overhead        | Primary Benefit                          |
+==========================+=====================+=================+==========================================+
| Shallow Copy             | ``obj.copy()``      | Minimal (1 call)| Discoverable API, consistent semantics   |
+--------------------------+---------------------+-----------------+------------------------------------------+
| Deep Copy                | ``obj.deepcopy()``  | Minimal (1 call)| Discoverable API, circular ref support   |
+--------------------------+---------------------+-----------------+------------------------------------------+
| Lifecycle Hook           | ``obj.construct()`` | Low             | Deferred or multi-stage initialization   |
+--------------------------+---------------------+-----------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.bases import BaseObject

   class MyObject(BaseObject):
       def __init__(self, value=None):
           super().__init__()
           self.value = value
           self.data = {"k": [1, 2, 3]}

   obj = MyObject(value="test")

   # Shallow copy
   c1 = obj.copy()
   assert c1 is not obj
   assert c1.data is obj.data

   # Deep copy
   c2 = obj.deepcopy()
   assert c2 is not obj
   assert c2.data is not obj.data

When to Use
-----------
* **As the base class** for public object hierarchies where consistent copy/deepcopy matters.
* **In combination** with other baseobjects features (composition, wrappers, registries) to get uniform behavior.

Best Practices
--------------
1. **Inherit for Consistency**: Use ``BaseObject`` as the root for any class hierarchy that needs reliable copying behavior.
2. **Use construct() for State Setup**: Move complex setup logic from ``__init__`` to ``construct()`` if you anticipate needing to re-initialize objects.
3. **Always Call super()**: When overriding ``__init__`` or ``construct()``, calling ``super()`` ensures the entire inheritance chain is correctly initialized.
