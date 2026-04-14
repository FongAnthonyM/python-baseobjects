Functions
=========

Overview
--------
The ``functions`` package provides a set of advanced tools for constructing, combining, and dispatching callables. It extends standard Python functions and methods with features like keyword-based dispatching, multiplexing, and dynamic binding. These tools are designed to build extensible APIs where behavior can be cleanly separated from the calling interface.

Conceptual Workings
-------------------

Enhanced Dispatching (singlekwargdispatch)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Standard Python ``singledispatch`` is limited to the first positional argument. ``singlekwargdispatch`` removes this limitation by allowing dispatch based on keyword arguments.

* **Keyword Dispatch**: Specify a parameter name (e.g., ``op``) to use for implementation lookup.
* **Hybrid Support**: Automatically falls back to traditional positional dispatch if no keyword is provided or matched.
* **Why it matters**: It enables clean, extensible command patterns and API routers without deep ``if/elif`` trees.

Multiplexing and Registries
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``CallableMultiplexer`` and ``FunctionRegistry`` classes allow for grouping related callables under a single interface:

* **FunctionRegistry**: A specialized container (derived from ``BaseDict``) that stores and manages groups of functions. It can even ingest methods directly from an object.
* **Multiplexer**: Acts as a "switchboard." It holds a registry of functions and dynamically selects which one to execute based on its internal state (e.g., the ``_selected`` attribute).

Dynamic Callables
~~~~~~~~~~~~~~~~~
The ``DynamicCallable`` hierarchy provides wrappers that can change their behavior or target at runtime. They are particularly useful for building proxies, adaptive decorators, or systems where the underlying implementation is hot-swapped without changing the caller's reference.

Key Components
--------------
* **singlekwargdispatch**: A decorator for multi-dispatch based on positional or keyword arguments.
* **FunctionRegistry / MethodRegistry**: Optimized containers for organizing and looking up callables.
* **CallableMultiplexer**: A callable object that routes calls to one of many internal functions.
* **DynamicCallable**: A foundation for callables that dynamically determine their execution logic.

Performance & Trade-offs
------------------------
+--------------------------+---------------------+-----------------+------------------------------------------+
| Tool                     | Overhead            | Complexity      | Primary Benefit                          |
+==========================+=====================+=================+==========================================+
| ``singlekwargdispatch``  | Moderate (dispatch) | Low             | Clean, extensible keyword-based API      |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``CallableMultiplexer``  | Moderate (lookup)   | Moderate        | Runtime switching between implementations|
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``FunctionRegistry``     | Low (dict lookup)   | Low             | Centralized management of callables      |
+--------------------------+---------------------+-----------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.functions import singlekwargdispatch

   @singlekwargdispatch("action")
   def process(*, action, data):
       raise NotImplementedError(f"No handler for {action}")

   @process.register("clean")
   def _(action, data):
       return data.strip()

   @process.register("upper")
   def _(action, data):
       return data.upper()

   assert process(action="clean", data=" hello ") == "hello"
   assert process(action="upper", data="hello") == "HELLO"

Best Practices
--------------
1. **Prefer Dispatch over Conditionals**: Use ``singlekwargdispatch`` to avoid growing ``if/elif`` blocks in router-like functions.
2. **Use Registries for Plugins**: Build extensible systems by allowing third-party code to register new functions into a central ``FunctionRegistry``.
3. **Multiplex for Strategy Patterns**: Use ``CallableMultiplexer`` to implement the Strategy pattern, allowing an object to switch its algorithm at runtime by simply changing the "selected" function.
