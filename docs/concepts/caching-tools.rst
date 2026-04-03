Caching Tools
=============

Overview
--------
The caching tools provide lightweight caches to store values with optional time-based expiry. They help avoid recomputation and repeated I/O while keeping memory under control.

Example
-------
.. code-block:: python

   from baseobjects.cachingtools.caches import TimedCache

   # Cache with a 60-second TTL
   cache = TimedCache(timeout=60)

   cache["key"] = "value"
   assert cache["key"] == "value"

When to Use
-----------
- Memoizing expensive computations with predictable invalidation windows.
- Caching small, frequently accessed records in process memory.

Tips
----
- Choose timeouts that reflect freshness requirements of the data.
- Consider thread/process safety requirements for the environment.
