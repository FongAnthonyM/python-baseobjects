Dataclasses
==========

Overview
--------
baseobjects integrates well with Python dataclasses and may provide helpers that keep copy/deepcopy and reduction semantics consistent with BaseObject.

Example
-------
.. code-block:: python

   from dataclasses import dataclass
   from baseobjects.bases import BaseObject

   @dataclass
   class User(BaseObject):
       id: int
       name: str
       tags: list[str]

   u1 = User(1, "Ada", ["admin"]) 
   u2 = u1.deepcopy()
   assert u1 is not u2 and u1.tags is not u2.tags

Tips
----
- Favor deepcopy() for dataclasses with mutable fields.
- Combine with BaseReducible if you need reliable pickling across processes.
