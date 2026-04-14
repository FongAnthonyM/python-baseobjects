Metaclasses
===========

Overview
--------
Metaclasses in the ``baseobjects`` library provide a robust and extensible foundation for class creation. They extend Python's standard ``ABCMeta`` to ensure that classes themselves—not just their instances—behave predictably when copied or deep-copied. Furthermore, they introduce structured initialization hooks that allow for sophisticated post-creation logic, such as automatic registration or attribute validation.

Conceptual Workings
-------------------

Copy-Safe Classes (BaseMeta)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Standard Python classes are sometimes difficult to copy if they hold complex state or participate in custom inheritance patterns. ``BaseMeta`` ensures that ``copy.copy(MyClass)`` and ``copy.deepcopy(MyClass)`` work as expected. This is critical for frameworks that dynamically generate or modify classes at runtime.

Post-Creation Hooks (InitMeta)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``InitMeta`` adds a dedicated lifecycle stage to class creation. After a class is fully constructed by the Python interpreter, ``InitMeta`` automatically invokes the ``_init_class_`` class method.

* **Automatic Setup**: Subclasses can implement ``_init_class_`` to perform tasks like registering themselves in a central registry, setting up class-level caches, or validating that certain attributes are present.
* **MRO Coordination**: The hook is designed to respect the Method Resolution Order (MRO), ensuring that parent initialization logic runs correctly.

Key Components
--------------
* **BaseMeta**: The root metaclass that ensures class-level copying compatibility and inherits from ``ABCMeta``.
* **InitMeta**: A specialized metaclass that adds the ``_init_class_`` hook for automated class configuration.

Performance & Trade-offs
------------------------
+-------------------+--------------------+------------------------+------------------------------------------+
| Component         | Overhead           | Impact                 | Best Use Case                            |
+===================+====================+========================+==========================================+
| ``BaseMeta``      | Negligible         | Standard class creation| Classes requiring ``copy`` safety        |
+-------------------+--------------------+------------------------+------------------------------------------+
| ``InitMeta``      | Very Low           | One extra method call  | Auto-registration, class-level validation|
+-------------------+--------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.metaclasses import InitMeta

   class Registry:
       classes = []

   class Base(metaclass=InitMeta):
       @classmethod
       def _init_class_(cls, **kwargs):
           # Automatically register every subclass
           Registry.classes.append(cls)

   class MyPlugin(Base):
       pass

   assert MyPlugin in Registry.classes

Best Practices
--------------
1. **Use InitMeta for Discovery**: If building a plugin system, use ``InitMeta`` and the ``_init_class_`` hook to automatically register new subclasses as they are defined.
2. **Inherit from Provided Metas**: When creating custom metaclasses, inherit from ``BaseMeta`` or ``InitMeta`` to maintain compatibility with the ``baseobjects`` ecosystem.
3. **Avoid Complex Metaclass __init__**: Move class-level configuration from the metaclass's ``__init__`` to the class's ``_init_class_`` method for better readability and easier debugging.
