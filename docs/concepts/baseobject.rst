BaseObject
==========

Overview
--------
The BaseObject class is the foundation of the library, providing predictable object semantics for copying and deep copying. It serves as a minimal base you can safely derive from when you want consistent behavior across your own types.

Purpose
---------
- Establish consistent, well-tested implementations of copy() and deepcopy().
- Provide a small, composable base that plays well with other mixins and metaclasses.

Key Concepts
------------
- copy(): Produce a shallow copy that reuses contained objects where safe.
- deepcopy(): Produce a deep copy that recursively copies contained objects.
- construct(): Low-level constructor helper for advanced scenarios.

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
- As the base class for your public object hierarchies where consistent copy/deepcopy matters.
- In combination with other baseobjects features (composition, wrappers, registries) to get uniform behavior.

Best Practices
--------------
- Derive from BaseObject instead of reinventing copy/deepcopy.
- Prefer deepcopy() when your objects keep internal mutable containers that should not be shared.
