Bases
=====

Overview
--------
The bases package provides the core building blocks used throughout baseobjects. It supplies foundational abstractions and protocols that standardize object behavior in areas like copying, serialization, metaclass functionality, and callability. These classes are designed to be composed and extended, giving you a consistent, predictable baseline for building your own libraries and applications.

Purpose
--------
- Establish consistent behavior for core object operations (copy, deepcopy, reduction/pickling).
- Provide a reliable metaclass that works well with copying and advanced class construction.
- Offer a standard way to build callable objects (objects that behave like functions and methods).
- Provide sentinel values for representing "no value" or special markers in APIs.

Key Concepts and Components
---------------------------
- BaseObject: A minimal, extensible base class that implements sensible defaults for copying and deep copying.
- BaseReducible: Adds explicit support for Python object reduction (pickling) with correct handling of both __dict__ and __slots__.
- BaseMeta: A metaclass derived from ABCMeta that ensures classes themselves can be copied and deep-copied properly.
- BaseCallable, BaseMethod, BaseFunction: Abstract bases for creating callable objects that encapsulate behavior and state.
- SentinelObject: A lightweight singleton type for creating unique sentinel values (e.g., DEFAULTSENTINEL, SEARCHSENTINEL).

Examples
--------
Shallow vs deep copy with BaseObject

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

.. code-block:: python

   from baseobjects.bases import BaseCallable

   class Adder(BaseCallable):
       def __call__(self, a, b):
           return a + b

   add = Adder()
   assert add(2, 3) == 5

Sentinel values

.. code-block:: python

   from baseobjects.bases import DEFAULTSENTINEL, SEARCHSENTINEL

   def get(config, key, default=DEFAULTSENTINEL):
       if default is DEFAULTSENTINEL:
           # sentinel means: error if missing
           return config[key]
       return config.get(key, default)

   cfg = {"a": 1}
   assert get(cfg, "a") == 1
   assert get(cfg, "b", default=0) == 0

Interplay with Other Modules
----------------------------
- functions: Often paired with BaseCallable for advanced callable/multiplexing patterns.
- wrappers: BaseObject semantics help wrappers behave consistently when copying and serializing.
- composition: Base classes provide predictable behavior for complex composite structures.

Best Practices
--------------
- Derive your public base classes from BaseObject to inherit consistent copy/deepcopy behavior.
- Prefer SentinelObject instances over None or magic strings to represent exceptional states.
- Use BaseReducible if your objects need to round-trip through pickle reliably, including across versions (with care).
