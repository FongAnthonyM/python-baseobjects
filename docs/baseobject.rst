Using BaseObject
================

The ``BaseObject`` class is the foundation of the library, providing basic functionality like copying:

.. code-block:: python

   from baseobjects.bases import BaseObject

   class MyObject(BaseObject):
       def __init__(self, value=None):
           super().__init__()
           self.value = value
           self.data = {"key": "value"}

   # Create an instance
   obj = MyObject(value="test")

   # Create a shallow copy
   copy_obj = obj.copy()

   # Create a deep copy
   deepcopy_obj = obj.deepcopy()
