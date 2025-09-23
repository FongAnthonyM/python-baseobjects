Caching Tools
=============

The cachingtools module provides utilities for caching:

.. code-block:: python

   from baseobjects.cachingtools.caches import TimedCache

   # Create a cache with a 60-second timeout
   cache = TimedCache(timeout=60)

   # Cache a value
   cache["key"] = "value"

   # Retrieve a value
   value = cache["key"]
