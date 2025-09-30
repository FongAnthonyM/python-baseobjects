Typing
======

Overview
--------
The typing utilities provide reusable type aliases and protocols used throughout the package. They make annotations more expressive and help static type checkers verify correct usage.

Examples
--------
Property callbacks alias (illustrative)

.. code-block:: python

   from typing import Callable, Tuple, Any
   # from baseobjects.typing import PropertyCallbacks
   # PropertyCallbacks = tuple[Callable[[Any], Any], Callable[[Any], None], Callable[[], None]]

   def make_callbacks(name: str) -> tuple[Callable[[Any], Any], Callable[[Any], None], Callable[[], None]]:
       def get(self):
           return getattr(self, name)
       def set(self, value):
           setattr(self, name, value)
       def delete():
           delattr(self, name)
       return get, set, delete

Guidelines
----------
- Prefer importing shared aliases from baseobjects.typing to keep annotations consistent across modules.
- Use Protocol and TypedDict where structural typing or shaped dicts improve clarity.
