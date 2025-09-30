Versioning
==========

Overview
--------
The versioning module defines an abstract Version base class and concrete implementations such as TriNumberVersion. These classes represent versions, support rich comparisons, and convert between string/list/tuple forms.

Key classes
-----------
- Version: Abstract base that defines the interface for version objects (construct, comparisons, str/list/tuple conversion).
- TriNumberVersion: A three-number version (major.minor.patch) with flexible constructors and comparison support.

Examples
--------
Constructing versions

.. code-block:: python

   from baseobjects.versioning import TriNumberVersion

   v1 = TriNumberVersion("1.2.3")
   assert str(v1) == "1.2.3"

   v2 = TriNumberVersion(major=1, minor=2, patch=4)
   assert v2.tuple() == (1, 2, 4)

   v3 = TriNumberVersion([1, 3, 0])
   assert v3.list() == [1, 3, 0]

Comparison and casting
----------------------
.. code-block:: python

   from baseobjects.versioning import TriNumberVersion

   assert TriNumberVersion("1.2.0") < TriNumberVersion("1.2.3")
   assert TriNumberVersion("2.0.0") > "1.9.9"   # casting from str is supported

Dispatch-based construction
---------------------------
TriNumberVersion uses singlekwargdispatch internally to implement set_version based on the type of the input:

.. code-block:: python

   from baseobjects.versioning import TriNumberVersion

   v = TriNumberVersion()
   v.set_version("3.1.4")   # str -> parsed by dots
   v.set_version([3, 1, 5])  # iterable -> assigned in order
   v.set_version(4, minor=0, patch=0)  # int + kwargs

Best Practices
--------------
- Use Version.cast when converting from unknown inputs and you want an option to pass through on failure.
- Prefer tuple() for comparison-friendly operations; use str() for presentation.
