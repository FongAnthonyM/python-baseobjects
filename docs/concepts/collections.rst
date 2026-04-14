Collections
===========

Overview
--------
The ``collections`` package provides a suite of specialized container types that extend Python's built-in data structures with ``BaseObject`` semantics. These collections are designed for predictability, especially regarding copying and serialization, while offering advanced features like time-based expiration and hierarchical grouping.

Conceptual Workings
-------------------

Standardized Container Bases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By inheriting from both ``BaseObject`` and standard library classes like ``UserDict`` or ``UserList``, ``BaseDict`` and ``BaseList`` ensure that custom containers behave like standard Python collections while supporting reliable ``copy()`` and ``deepcopy()`` operations. Unlike standard ``dict`` or ``list``, these bases handle complex inheritance chains and metadata preservation during duplication.

Time-Based Expiration (TimedDict)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``TimedDict`` class introduces a "Time-to-Live" (TTL) mechanism for stored data. It tracks an expiration timestamp and automatically clears its contents once the lifetime has elapsed.

* **Automatic Clearing**: The dictionary checks the current time during access and clears itself if the lifetime has expired.
* **Use Case**: Ideal for caching transient data or managing temporary state that should not persist indefinitely.

Hierarchical Grouping (GroupedList)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``GroupedList`` provides a way to organize data into logical groups while maintaining a flat iteration interface. Nested ``GroupedList`` instances are treated as if their contents are direct elements of the parent.

* **Named Groups**: Items can be organized into specifically named sub-lists.
* **Flat Iteration**: Iterating over a parent ``GroupedList`` seamlessly yields items from all its nested groups as if they were in a single flat list.

Key Components
--------------
* **BaseDict / BaseList**: Foundation classes combining standard container behavior with ``BaseObject`` features.
* **TimedDict**: A dictionary that automatically clears its contents after a specified lifetime.
* **GroupedList**: A hierarchical list structure with named groups and flat iteration support.
* **OrderableDict**: A dictionary with enhanced ordering and sorting capabilities.
* **DeepChainMap**: An extension of ``ChainMap`` that supports recursive lookups and deep merging.

Performance & Trade-offs
------------------------
+-------------------+--------------------+------------------------+------------------------------------------+
| Collection        | Overhead           | Impact                 | Best Use Case                            |
+===================+====================+========================+==========================================+
| ``BaseDict/List`` | Low                | Minimal delegation     | Standard collections with ``copy`` safety|
+-------------------+--------------------+------------------------+------------------------------------------+
| ``TimedDict``     | Moderate           | Expiration checks      | Temporary caches, self-cleaning state    |
+-------------------+--------------------+------------------------+------------------------------------------+
| ``GroupedList``   | Moderate           | Hierarchical tracking  | Organizing items into logical categories |
+-------------------+--------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.collections import TimedDict, GroupedList

   # TimedDict with 5-second lifetime
   cache = TimedDict(lifetime=5)
   cache["key"] = "value"
   # ... 6 seconds later ...
   assert "key" not in cache

   # GroupedList for organization
   main_list = GroupedList()
   sub_group = main_list.groups.create("sub")
   sub_group.append("item1")
   main_list.append("item2")

   # Iterates over both "item1" and "item2"
   assert list(main_list) == ["item1", "item2"]

Best Practices
--------------
1. **Inherit from Bases**: When creating custom domain-specific containers, inherit from ``BaseDict`` or ``BaseList`` instead of ``dict`` or ``list`` to maintain ``BaseObject`` compatibility.
2. **Use TimedDict for Volatile Data**: Prevent memory bloat in long-running processes by using ``TimedDict`` for data that is only valid for a short period.
3. **Flat Iteration with GroupedList**: Use ``GroupedList`` when you need to group objects for organization but still want to process all objects in a single loop.
