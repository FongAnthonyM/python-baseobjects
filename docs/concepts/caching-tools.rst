Caching Tools
=============

Overview
--------
The ``cachingtools`` package provides a robust framework for implementing time-based caching (Time-to-Live or TTL) in Python. Unlike standard functional caches, ``cachingtools`` is designed with an object-oriented approach, allowing for granular control, centralized management, and per-instance cache isolation.

How Decorators Work: The Objects Behind the Magic
------------------------------------------------
In most caching libraries, a decorator is a simple closure. In ``cachingtools``, decorators like ``@timed_cache`` or ``@timed_lru_cache`` are actually factory functions that return instances of ``BaseTimedCache`` subclasses.

When decorating a function:

1. An instance of a cache class (e.g., ``TimedCache``) is created.
2. The original function is wrapped within this object.
3. The cache object stores its state (results, expiration times, etc.) in a separate ``CacheInfo`` object.

The Role of ``CacheInfo``
~~~~~~~~~~~~~~~~~~~~~~~~
Each cache object maintains a ``CacheInfo`` instance. This separation ensures that the logic of *how* to cache (the decorator object) is distinct from the *data* being cached. ``CacheInfo`` tracks:

* **is_caching**: Whether the cache is currently active.
* **lifetime**: The TTL in seconds.
* **expiration**: The next ``perf_counter()`` timestamp when the cache will clear.
* **cache_container**: The actual dictionary or container holding the cached results.

Method Binding and ``instanced_cache``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
One of the most powerful features of ``cachingtools`` is its handling of class methods via the ``__get__`` descriptor.

* **Global Caching** (Default): The cache is shared across all instances of a class.
* **Instanced Caching** (``instanced=True``): When the decorated method is accessed on an instance, the decorator creates a unique ``CacheInfo`` object for *that specific instance*. This prevents "data leakage" between objects and ensures that when an object is garbage collected, its specific cache data is also released.

CachingObject: Centralized Management
-------------------------------------
The ``CachingObject`` is a base class designed to manage multiple caches within a single object. It uses a metaclass (``InitMeta``) to automatically discover any ``BaseTimedCache`` instances assigned as class or instance attributes.

Why Inherit from ``CachingObject``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Inheriting from ``CachingObject`` provides several benefits for complex applications:

1. **Discovery**: All caches are automatically registered in the object's internal ``_caches`` dictionary.
2. **Bulk Operations**: Every cache in the object can be cleared, enabled, or disabled with a single call (e.g., ``obj.clear_caches()``).
3. **Memory Management**: It simplifies the lifecycle management of caches, especially when using ``instanced_cache=True``.
4. **Fine-grained Control**: Methods like ``get_any_caching()`` or ``set_lifetimes()`` allow for sophisticated runtime adjustments.

Specialized Caches
-----------------
TimedKeylessCache
~~~~~~~~~~~~~~~~~~
The ``TimedKeylessCache`` (and its decorator ``@timed_keyless_cache``) is an optimized version of the cache that ignores all function arguments.

* **Use Case**: Functions that return a "singleton" value or global state where the input parameters do not change the output.
* **Performance**: Because it skips argument hashing and key creation, it is significantly faster than standard timed caches.

Performance Analysis & Trade-offs
---------------------------------
While ``cachingtools`` offers features not found in Python's built-in ``functools.lru_cache``, these features come with performance implications.

The Speed Trade-off
~~~~~~~~~~~~~~~~~~~~
Python's ``lru_cache`` is implemented in C, making its "hit" performance extremely fast. ``cachingtools`` is implemented in pure Python to support features like TTL and ``CachingObject`` integration.

Generalized Performance Comparison (Hit Speed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------+---------------------+-----------------+------------------------------------------+
| Implementation           | Hit Speed (Relative)| Memory Overhead | Primary Benefit                          |
+==========================+=====================+=================+==========================================+
| ``functools.lru_cache``  | 1x (Fastest)        | Lowest          | Raw speed for static data                |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``timed_lru_cache``      | ~9-10x Slower       | Higher          | TTL Support, Instanced Caching           |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``timed_cache``          | ~8-9x Slower        | Moderate        | TTL Support, Unlimited Size              |
+--------------------------+---------------------+-----------------+------------------------------------------+
| ``timed_keyless_cache``  | ~5-6x Slower        | Low             | Fast TTL for single-value returns        |
+--------------------------+---------------------+-----------------+------------------------------------------+

When to Use cachingtools
~~~~~~~~~~~~~~~~~~~~~~~~
Use ``cachingtools`` when:

* **TTL is Required**: Data must expire automatically after a set time.
* **Instance Isolation**: Each object instance requires its own private cache.
* **Dynamic Control**: Caches must be programmatically enabled, disabled, or cleared at runtime via ``CachingObject``.
* **Argument-Agnostic Caching**: The performance boost of ``TimedKeylessCache`` is required for global data.

Avoid ``cachingtools`` and prefer ``lru_cache`` when:

* **Raw Speed is Critical**: The function is called millions of times in a tight loop.
* **No Expiration Needed**: The data is static or invalidation is handled manually.

Best Practices
--------------

1. **Prefer instanced=True for Methods**: If a class is instantiated many times, using instanced caches prevents cross-object pollution.
2. **Use TimedKeylessCache for Singletons**: If a function doesn't depend on its arguments, save overhead by using the keyless variant.
3. **Inherit CachingObject for Complex Classes**: If a class has more than two caches, ``CachingObject`` will make debugging and management significantly easier.
