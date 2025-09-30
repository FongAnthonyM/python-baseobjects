Metaclasses
===========

Overview
--------
Metaclasses in baseobjects extend ABCMeta to work seamlessly with BaseObject semantics, especially around copying and deep copying of classes and participating in class initialization hooks used by some utilities.

Key class
---------
- BaseMeta: A robust metaclass that integrates with copying/deepcopying and supports coordinated class construction phases.

Example: coordinating class initialization
-----------------------------------------
.. code-block:: python

   from baseobjects.bases import BaseObject, BaseMeta

   class WithHook(BaseObject, metaclass=BaseMeta):
       @classmethod
       def _init_class_(cls, name=None, bases=None, namespace=None):
           # subclasses can participate in post-class-creation logic here
           cls.initialized = True

   class Sub(WithHook):
       pass

   assert hasattr(Sub, "initialized") and Sub.initialized is True

Notes
-----
- BaseMeta underpins helper metaclasses used elsewhere (e.g., InitMeta in AutomaticProperties).
- Prefer the provided metaclasses when mixing advanced behaviors to avoid subtle MRO and copy/deepcopy issues.
