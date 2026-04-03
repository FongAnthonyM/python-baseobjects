Operations
==========

Overview
--------
Operations refers to the common dunder and utility operations supported uniformly across baseobjects types: copying, deep copying, comparisons (where provided), and behaviors implemented by collection subclasses.

Examples
--------
Copying and deep copying

.. code-block:: python

   from baseobjects.bases import BaseObject

   class Node(BaseObject):
       def __init__(self, children=None):
           super().__init__()
           self.children = list(children or [])

   n1 = Node([Node(), Node()])
   n2 = n1.copy()      # shallow: shares child objects
   n3 = n1.deepcopy()  # deep: independent copies of children

Collections operations (illustrative)
-------------------------------------
.. code-block:: python

   # For concrete collection classes, see the API reference for the installed version
   # Example only
   # d = OrderableDict({"a": 1, "b": 2})
   # d.move_after("a", "b")

Guidelines
----------
- Use deepcopy when duplicating graphs containing mutable children.
- Prefer provided collection operations for clarity over home-grown helpers.
