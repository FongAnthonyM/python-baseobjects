Collections
===========

Overview
--------
Collections in baseobjects provide specialized container behaviors that integrate with the BaseObject semantics. They aim to be predictable to copy/deepcopy and friendly to composition and wrappers.

Example: typed list-like collection
-----------------------------------
.. code-block:: python

   # Example only: actual collection classes and names may differ.
   from baseobjects.bases.collections import BaseList  # if available in the installed version

   class IntList(BaseList):  # hypothetical example for illustration
       item_type = int

   nums = IntList([1, 2, 3])
   nums.append(4)
   assert nums.copy() != nums

Guidelines
----------
- Prefer explicit item typing when early validation and clearer errors are desired.
- Leverage BaseObject.copy()/deepcopy() semantics for safe duplication of container state.

Note
----
The exact collection classes available can vary by version. Consult the API reference for the list of concrete classes in the installed version.
