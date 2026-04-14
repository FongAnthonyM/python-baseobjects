Operations
==========

Overview
--------
The ``operations`` package provides a collection of utility functions and algorithms for manipulating data structures and performing common type conversions. These tools extend beyond the standard library to handle complex, nested data and domain-specific formats (like Excel or Windows Filetime dates) with a focus on correctness and recursive safety.

Conceptual Workings
-------------------

Recursive Data Manipulation
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Standard library update methods (like ``dict.update``) are shallow—they replace nested dictionaries entirely. The recursive operations in this module provide deeper control.

* **update_recursive**: Performs an in-place modification of nested mappings. If both dictionaries contain the same key and both values are mappings, it recursively merges the entries instead of overwriting the whole branch.
* **union_recursive**: Similar to ``update_recursive``, but returns a new deep-copied dictionary representing the union of the two, leaving the original inputs untouched.

Specialized Conversions
~~~~~~~~~~~~~~~~~~~~~~~
The module includes highly specific conversion utilities for interoperability with external systems:

* **Date/Time Conversions**: Functions like ``excel_date_to_datetime`` and ``filetime_to_datetime`` handle the nuances of different epoch starts (e.g., Excel's 1899-12-30) and timezone offsets.
* **Data Parsing**: Tools like ``parse_parentheses`` provide robust string manipulation for nested structures, often used in DSL or configuration parsing.

Key Components
--------------
* **update_recursive / union_recursive**: Tools for deep merging and updating of nested dictionaries and mappings.
* **excel_date_to_datetime**: Converts Excel's numeric date format to Python ``datetime``.
* **filetime_to_datetime**: Converts Windows FILETIME (100-nanosecond intervals) to ``datetime``.
* **parse_parentheses**: A utility for extracting and handling nested bracketed strings or expressions.

Performance & Trade-offs
------------------------
+----------------------+--------------------+------------------------+------------------------------------------+
| Operation            | Overhead           | Impact                 | Best Use Case                            |
+======================+====================+========================+==========================================+
| ``update_recursive`` | Moderate (nested)  | In-place modification  | Merging nested configuration dicts       |
+----------------------+--------------------+------------------------+------------------------------------------+
| ``union_recursive``  | High (deepcopy)    | Memory usage           | Creating a combined view of nested data  |
+----------------------+--------------------+------------------------+------------------------------------------+
| Time Conversions     | Low                | Standard arithmetic    | Parsing external data formats            |
+----------------------+----------------------+------------------------+------------------------------------------+

Basic Usage
-----------
.. code-block:: python

   from baseobjects.operations import update_recursive

   base_config = {"api": {"version": 1, "timeout": 30}}
   user_config = {"api": {"timeout": 60}}

   # Standard update would lose "version"
   # update_recursive preserves it
   update_recursive(base_config, user_config)

   assert base_config["api"]["version"] == 1
   assert base_config["api"]["timeout"] == 60

Best Practices
--------------
1. **Prefer union_recursive for Safety**: If the original data must remain unchanged, use ``union_recursive`` to obtain a fresh copy of the merged result.
2. **Contextual Conversions**: Always consider the timezone when converting external dates (like Excel) to ensure the resulting ``datetime`` is unambiguous.
3. **Use update_recursive for Configs**: When merging user-provided overrides into a default configuration, ``update_recursive`` ensures that nested defaults are preserved if the user only overrides specific sub-keys.
4. **Recursive Depth**: While powerful, recursive operations can hit recursion limits or consume significant memory on extremely deep trees. Use with care on untrusted data structures.
