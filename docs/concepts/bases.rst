Bases
=====

Overview
--------
The ``bases`` package provides the core building blocks used throughout the ``baseobjects`` library. It supplies foundational abstractions and protocols that standardize object behavior in areas like copying, serialization, metaclass functionality, and callability. These classes are designed to be composed and extended, giving a consistent, predictable baseline for building complex libraries and applications.

Conceptual Workings
-------------------

Serialization with BaseReducible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
While Python's ``pickle`` module handles most objects, classes using ``__slots__`` require special care. ``BaseReducible`` implements ``__getstate__`` and ``__setstate__`` to automatically discover and preserve both ``__dict__`` (regular attributes) and ``__slots__`` attributes, ensuring robust serialization across different object layouts.

Advanced Callables
~~~~~~~~~~~~~~~~~~
The ``BaseCallable`` hierarchy (including ``BaseMethod`` and ``BaseFunction``) provides more than simple function wrapping:
* **Attribute Preservation**: Wrappers automatically copy docstrings, annotations, and custom attributes from the wrapped function.
* **Coroutine Support**: Correctly identifies and maintains the async nature of wrapped coroutines.
* **Weak Binding**: ``BaseMethod`` uses weak references (``weakref``) to bind to instances, preventing memory leaks in long-lived method objects.

Identity with SentinelObject
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlike using ``None`` or magic strings, ``SentinelObject`` creates unique, singleton identifiers. These are ideal for distinguishing between a "default" value and a valid user-provided ``None``. They are registry-backed, meaning the same identifier always returns the same object instance.

Key Components
--------------
* **BaseObject**: Standardized copying and lifecycle hooks.
* **BaseReducible**: Reliable pickling for slotted and non-slotted objects.
* **BaseMeta**: A metaclass ensuring classes themselves can be copied.
* **BaseCallable / BaseMethod / BaseFunction**: Customizable wrappers for functions and methods.
* **SentinelObject**: Unique, picklable singleton markers (e.g., ``DEFAULTSENTINEL``).

Performance & Trade-offs
------------------------
+-------------------+--------------------+------------------------+------------------------------------------+
| Component         | Overhead           | Impact                 | Best Use Case                            |
+===================+====================+========================+==========================================+
| ``BaseCallable``  | Low                | Minor call delegation  | Decorators requiring attr preservation   |
+-------------------+--------------------+------------------------+------------------------------------------+
| ``BaseReducible`` | Moderate           | State discovery        | Objects with ``__slots__`` and pickling  |
+-------------------+--------------------+------------------------+------------------------------------------+
| ``SentinelObject``| Very Low           | Singleton lookup       | API markers, distinguishing ``None``     |
+-------------------+--------------------+------------------------+------------------------------------------+

Examples
--------
Shallow vs deep copy with BaseObject
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from baseobjects.bases import BaseObject

   class Cfg(BaseObject):
       def __init__(self):
           super().__init__()
           self.meta = {"tags": ["a", "b"]}

   a = Cfg()
   b = a.copy()
   c = a.deepcopy()
   assert b.meta is a.meta
   assert c.meta is not a.meta

Pickling-ready objects with BaseReducible
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   import pickle
   from baseobjects.bases import BaseReducible

   class Payload(BaseReducible):
       __slots__ = ("data",)
       def __init__(self, data):
           super().__init__()
           self.data = data

   p = Payload({"x": 1})
   round_trip = pickle.loads(pickle.dumps(p))
   assert round_trip.data == {"x": 1}

Callable objects with BaseCallable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   from baseobjects.bases import BaseCallable

   class Adder(BaseCallable):
       def __call__(self, a, b):
           return a + b

   add = Adder()
   assert add(2, 3) == 5

Sentinel values
~~~~~~~~~~~~~~~
.. code-block:: python

   from baseobjects.bases import DEFAULTSENTINEL

   def get(config, key, default=DEFAULTSENTINEL):
       if default is DEFAULTSENTINEL:
           return config[key]
       return config.get(key, default)

Best Practices
--------------
1. **Prefer BaseReducible for State**: If your class uses ``__slots__``, inherit from ``BaseReducible`` to ensure it remains picklable.
2. **Use SentinelObject for APIs**: Stop using ``None`` as a default if ``None`` is a valid value the user might pass; use a ``SentinelObject`` instead.
3. **Async Awareness**: When building decorators, use ``BaseCallable`` to ensure that async functions stay async when wrapped.
4. **Avoid Strong Method Refs**: Use ``BaseMethod`` logic when storing bound methods to avoid circular references and memory leaks.
