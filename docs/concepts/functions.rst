Functions
=========

Overview
--------
The functions module provides building blocks for constructing, combining, and dispatching callables. It treats functions and methods as first-class objects that can carry configuration and state while remaining ergonomic to use.

Purpose
--------
- Encapsulate behavior and state in callable objects beyond plain def functions.
- Provide flexible dispatch mechanisms where behavior depends on argument values or types.
- Enable composition of related callables under a unified interface.

Key Components
--------------
- singlekwargdispatch: Dispatch based on a single keyword argument, avoiding large if/elif trees.
- Multiplexers/registries: Organize groups of callables and route calls.
- BaseCallable: Foundational contract (from bases) for building callable objects.

Example: Dispatch by Keyword
----------------------------
.. code-block:: python

   from baseobjects.functions.singlekwargdispatch import singlekwargdispatch

   @singlekwargdispatch("op")
   def operate(*, op, x, y):
       raise NotImplementedError

   @operate.register("add")
   def _operate_add(*, op, x, y):
       return x + y

   @operate.register("mul")
   def _operate_mul(*, op, x, y):
       return x * y

   assert operate(op="add", x=2, y=3) == 5
   assert operate(op="mul", x=2, y=3) == 6

Best Practices
--------------
- Keep dispatch predicates small and testable; avoid side effects in registration.
- Prefer registries/multiplexers over ad-hoc if/elif trees for extensibility.
- Document selection rules clearly for users extending or integrating custom callables.
