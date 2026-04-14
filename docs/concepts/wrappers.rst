Wrappers
========

Overview
--------
The ``wrappers`` package provides a set of tools for creating proxy objects that encapsulate and extend the behavior of other objects. By implementing the Decorator and Proxy patterns, these wrappers allow developers to add functionality such as validation, logging, or access control to an underlying object while maintaining a familiar and compatible interface.

Conceptual Workings
-------------------

Delegation vs. Inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~
Wrappers favor composition over inheritance. Instead of inheriting from a class to modify its behavior, a wrapper embeds an instance of that class and delegates method calls and attribute accesses to it.

* **Attribute Proxying**: Wrappers automatically route requests for attributes they do not possess to the wrapped object.
* **State Isolation**: The wrapper can maintain its own state independently of the object it wraps, preventing unintended side effects in the original object.

Static vs. Dynamic Wrapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The module offers two primary strategies for attribute resolution, allowing for a trade-off between performance and flexibility:

* **StaticWrapper**: Optimized for performance. It uses an explicit ``_wrap()`` step to create property descriptors for the wrapped object's attributes at initialization. This results in very fast attribute access but requires the wrapped interface to be stable.
* **DynamicWrapper**: Optimized for flexibility. It resolves attributes at runtime using dynamic lookup mechanisms. While this incurs more overhead than static wrapping, it can adapt to objects whose interface changes or is unknown until execution.

Key Components
--------------
* **StaticWrapper**: A high-performance wrapper that pre-binds to a stable, known interface.
* **DynamicWrapper**: A flexible wrapper designed for heterogeneous or frequently changing interfaces.
* **_wrapped_map_**: A declarative mapping used by wrappers to identify which internal objects and attributes should be proxied.

Performance & Trade-offs
------------------------
+--------------------+--------------------+------------------------+------------------------------------------+
| Wrapper Type       | Access Overhead    | Initialization         | Best Use Case                            |
+====================+====================+========================+==========================================+
| ``StaticWrapper``  | Very Low           | Moderate (setup)       | Stable interfaces, performance-critical  |
+--------------------+--------------------+------------------------+------------------------------------------+
| ``DynamicWrapper`` | Moderate           | Low                    | Changing interfaces, rapid prototyping   |
+--------------------+--------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.wrappers import StaticWrapper

   class InternalService:
       def perform_action(self):
           return "Success"

   class ServiceWrapper(StaticWrapper):
       # Map the internal attribute to its type for property generation
       _wrapped_map_ = [("_service", InternalService)]

       def __init__(self, service):
           super().__init__()
           self._service = service
           self._wrap()  # Generate the proxy properties

   service = InternalService()
   wrapper = ServiceWrapper(service)

   # Calls InternalService.perform_action via the proxy
   assert wrapper.perform_action() == "Success"

Best Practices
--------------
1. **Prefer Static for Performance**: Use ``StaticWrapper`` whenever the interface of the wrapped object is well-defined and stable.
2. **Explicit Wrapping**: Use the ``_wrapped_map_`` to explicitly define which parts of the inner object should be exposed, preventing the accidental leakage of internal details.
3. **Refresh when Necessary**: If the underlying object's interface changes after the wrapper is initialized, call ``self._wrap()`` again on a ``StaticWrapper`` to refresh the available properties.
4. **Avoid Deep Nesting**: While wrappers can wrap other wrappers, keep the nesting depth minimal to avoid complex debugging and performance degradation from multiple layers of delegation.
