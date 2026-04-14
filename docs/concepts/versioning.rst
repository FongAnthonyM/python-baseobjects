Versioning
==========

Overview
--------
The ``versioning`` package provides a standardized way to represent, compare, and manipulate software version strings. It moves beyond simple string comparison by treating versions as rich objects that understand semantic hierarchies (like Major.Minor.Patch) and can be initialized from various data formats including strings, tuples, and lists.

Conceptual Workings
-------------------

Rich Version Objects (Version Base)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``Version`` base class defines a universal protocol for versioning logic. It ensures that any specialized version type supports:

* **Rich Comparisons**: Implementation of standard Python comparison operators (``<``, ``<=``, ``==``, etc.) to allow natural sorting and version gating.
* **Format Flexibility**: Built-in methods to export and convert the version between ``string``, ``list``, and ``tuple`` representations.
* **Intelligent Casting**: The ``cast()`` method allows for converting raw inputs (like strings or iterables) into full ``Version`` objects automatically, simplifying API development.

Semantic Versioning (TriNumberVersion)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``TriNumberVersion`` is the primary implementation, following the common three-part semantic versioning scheme.

* **Dynamic Initialization**: Leveraging ``singlekwargdispatch``, it can be constructed from a wide variety of inputs: dot-separated strings (``"1.2.3"``), iterables (``[1, 2, 3]``), or individual keyword arguments (``major=1, minor=2, patch=3``).
* **Comparison Consistency**: It ensures that version parts are compared numerically rather than lexicographically, preventing errors like ``"1.10" < "1.2"``.

Key Components
--------------
* **Version**: The abstract base class defining the mandatory interface for all versioning types.
* **TriNumberVersion**: A concrete implementation for the standard ``major.minor.patch`` versioning pattern.

Performance & Trade-offs
------------------------
+----------------------+--------------------+------------------------+------------------------------------------+
| Component            | Overhead           | Impact                 | Best Use Case                            |
+======================+====================+========================+==========================================+
| ``Version`` Objects  | Low                | Minor parsing on init  | Managing package, API, or data versions  |
+----------------------+--------------------+------------------------+------------------------------------------+
| Comparisons          | Very Low           | Tuple-based comparison | Version gates and compatibility checks   |
+----------------------+--------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.versioning import TriNumberVersion

   v1 = TriNumberVersion("1.2.10")
   v2 = TriNumberVersion("1.2.2")

   # Numeric comparison handles multi-digit parts correctly
   assert v1 > v2
   assert v1 > "1.2.0"  # Automatic casting of string for comparison

Best Practices
--------------
1. **Use cast() for Input**: When accepting a version from a user or a configuration file, use ``Version.cast(input)``. This gracefully handles both raw strings and existing ``Version`` objects.
2. **Comparison Safety**: Always compare ``Version`` objects against other ``Version`` objects or strings. The library's casting support ensures that ``my_version > "1.0.0"`` is both safe and readable.
3. **Prefer Tuples for Logic**: When writing custom comparison or sorting logic, use the ``.tuple()`` method to obtain a stable, sortable representation of the version components.
4. **Consistency**: Use the same versioning scheme across your entire project to ensure that comparisons remain valid and predictable.
