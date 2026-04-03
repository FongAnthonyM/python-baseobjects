Wrappers
========

Overview
--------
The wrappers provide objects that proxy attributes and methods of embedded objects. This enables adding behavior (validation, logging, access control, adaptation) around an underlying object while exposing a familiar interface.

Purpose
--------
- Support the Decorator and Proxy patterns with predictable performance.
- Offer static vs dynamic tradeoffs depending on how often the wrapped object’s interface changes.

Key Components
--------------
- StaticWrapper: A performant wrapper for objects with a stable, known interface. It creates property descriptors for wrapped attributes via an explicit _wrap() step.
- DynamicWrapper: A flexible wrapper that adapts to changing attributes/methods at runtime (with higher overhead). If available in the installed version, use when the wrapped interface is heterogeneous.

Basic Example with StaticWrapper
--------------------------------
.. code-block:: python

   from baseobjects.wrappers import StaticWrapper

   class Service:
       def __init__(self, value: int = 0):
           self.value = value
       def inc(self, n: int) -> None:
           self.value += n

   class ServiceWrapper(StaticWrapper):
       _wrapped_map_ = [("svc", Service)]
       def __init__(self, svc: Service | None = None):
           self._svc = svc or Service()
           self._wrap()  # make wrapped attributes available as properties

   w = ServiceWrapper()
   w.inc(3)            # delegates to Service.inc
   assert w.value == 3 # property proxies Service.value

Attribute Resolution and Rewrapping
-----------------------------------
- Resolution order follows the order of entries in _wrapped_map_.
- If new attributes are added to wrapped objects at runtime, call _wrap() again to expose them on the wrapper.

Best Practices
--------------
- Prefer StaticWrapper when the interface is known and stable; choose a dynamic wrapper when heterogeneity is unavoidable.
- Be explicit about which attributes/methods are exposed to avoid accidental leakage of internals.
- Consider thread safety if the wrapped object is used concurrently.
