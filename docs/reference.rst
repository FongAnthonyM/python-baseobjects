API Reference
=========

.. contents::
    :local:
    :depth: 2
    :backlinks: none


bases
----------------

Core base classes and common primitives that other modules build upon.

.. automodule:: baseobjects.bases
   :members:

BaseObject
----------

.. autoclass:: baseobjects.bases.baseobject.BaseObject
   :members:

BaseMeta
--------

.. autoclass:: baseobjects.bases.basemeta.BaseMeta
   :members:

bases.basecallable
----------------------------

.. automodule:: baseobjects.bases.basecallable
   :members:

BaseReducible
-------------

.. autoclass:: baseobjects.bases.basereducible.BaseReducible
   :members:

SentinelObject
---------------

.. autoclass:: baseobjects.bases.sentinelobject.SentinelObject
   :members:

bases.collections
---------------------------

.. automodule:: baseobjects.bases.collections
   :members:

bases.collections.basedict
---------------------------------

.. automodule:: baseobjects.bases.collections.basedict
   :members:

bases.collections.baselist
---------------------------------

.. automodule:: baseobjects.bases.collections.baselist
   :members:

cachingtools
----------------------

Caching utilities and cache abstractions for performance-sensitive workloads.

.. automodule:: baseobjects.cachingtools
   :members:

cachingtools.cachingobject
--------------------------------

.. automodule:: baseobjects.cachingtools.cachingobject
   :members:

cachingtools.caches
------------------------------

.. automodule:: baseobjects.cachingtools.caches
   :members:

cachingtools.caches.basetimedcache
-------------------------------------------

.. automodule:: baseobjects.cachingtools.caches.basetimedcache
   :members:

cachingtools.caches.timedcache
---------------------------------------

.. automodule:: baseobjects.cachingtools.caches.timedcache
   :members:

cachingtools.caches.timedkeylesscache
----------------------------------------------

.. automodule:: baseobjects.cachingtools.caches.timedkeylesscache
   :members:

cachingtools.caches.timedlrucache
-------------------------------------------

.. automodule:: baseobjects.cachingtools.caches.timedlrucache
   :members:

cachingtools.caches.timedsinglecache
---------------------------------------------

.. automodule:: baseobjects.cachingtools.caches.timedsinglecache
   :members:

classregistration
---------------------------

Mechanisms for registering and dispatching classes and instances by keys or namespaces.

.. automodule:: baseobjects.classregistration
   :members:

classregistration.baseclassregistry
-------------------------------------------

.. automodule:: baseobjects.classregistration.baseclassregistry
   :members:

classregistration.baseregisteredclass
---------------------------------------------

.. automodule:: baseobjects.classregistration.baseregisteredclass
   :members:

classregistration.dispatchableclass
------------------------------------------

.. automodule:: baseobjects.classregistration.dispatchableclass
   :members:

classregistration.namespaceclassregistry
-----------------------------------------------

.. automodule:: baseobjects.classregistration.namespaceclassregistry
   :members:

classregistration.namespaceregisteredclass
-------------------------------------------------

.. automodule:: baseobjects.classregistration.namespaceregisteredclass
   :members:

collections
---------------------

Specialized collection types extending or complementing Python's built-in containers.

.. automodule:: baseobjects.collections
   :members:

collections.circulardoublylinkedcontainer
------------------------------------------------

.. automodule:: baseobjects.collections.circulardoublylinkedcontainer
   :members:

collections.deepchainmap
-------------------------------

.. automodule:: baseobjects.collections.deepchainmap
   :members:

collections.groupedlist
------------------------------

.. automodule:: baseobjects.collections.groupedlist
   :members:

collections.orderabledict
---------------------------------

.. automodule:: baseobjects.collections.orderabledict
   :members:

collections.timeddict
----------------------------

.. automodule:: baseobjects.collections.timeddict
   :members:

composition
---------------------

Composable object patterns and helper classes for building component-based systems.

.. automodule:: baseobjects.composition
   :members:

composition.basecomponent
---------------------------------

.. automodule:: baseobjects.composition.basecomponent
   :members:

composition.basecomposite
--------------------------------

.. automodule:: baseobjects.composition.basecomposite
   :members:

composition.basedispatchingcomposite
--------------------------------------------

.. automodule:: baseobjects.composition.basedispatchingcomposite
   :members:

composition.dispatchablecomposite
-----------------------------------------

.. automodule:: baseobjects.composition.dispatchablecomposite
   :members:

dataclasses
---------------------

Lightweight data containers and parameter helpers to structure configuration and state.

.. automodule:: baseobjects.dataclasses
   :members:

dataclasses.parameters
-----------------------------

.. automodule:: baseobjects.dataclasses.parameters
   :members:

functions
-------------------

Dynamic function utilities, decorators, and dispatching helpers.

.. automodule:: baseobjects.functions
   :members:

functions.basedecorator
-------------------------------

.. automodule:: baseobjects.functions.basedecorator
   :members:

functions.callablemultiplexer
------------------------------------

.. automodule:: baseobjects.functions.callablemultiplexer
   :members:

functions.dynamiccallable
--------------------------------

.. automodule:: baseobjects.functions.dynamiccallable
   :members:

functions.dynamicdecoractor
---------------------------------

.. automodule:: baseobjects.functions.dynamicdecoractor
   :members:

functions.functionregistry
----------------------------------

.. automodule:: baseobjects.functions.functionregistry
   :members:

functions.methodregistry
--------------------------------

.. automodule:: baseobjects.functions.methodregistry
   :members:

functions.singlekwargdispatch
--------------------------------------

.. automodule:: baseobjects.functions.singlekwargdispatch
   :members:

metaclasses
---------------------

Metaclass utilities to control class creation and initialization behavior.

.. automodule:: baseobjects.metaclasses
   :members:

metaclasses.initmeta
---------------------------

.. automodule:: baseobjects.metaclasses.initmeta
   :members:

objects
-----------------

Object helpers for property management, callbacks, and utility behaviors.

.. automodule:: baseobjects.objects
   :members:

objects.automaticproperties
----------------------------------

.. automodule:: baseobjects.objects.automaticproperties
   :members:

objects.callbackmanager
-------------------------------

.. automodule:: baseobjects.objects.callbackmanager
   :members:

operations
--------------------

General-purpose operations and algorithms for data transformation and inspection.

.. automodule:: baseobjects.operations
   :members:

operations.bytestobin
-----------------------------

.. automodule:: baseobjects.operations.bytestobin
   :members:

operations.exceldatetodatetime
--------------------------------------

.. automodule:: baseobjects.operations.exceldatetodatetime
   :members:

operations.filetimetodatetime
--------------------------------------

.. automodule:: baseobjects.operations.filetimetodatetime
   :members:

operations.methodnames
------------------------------

.. automodule:: baseobjects.operations.methodnames
   :members:

operations.parseparentheses
------------------------------------

.. automodule:: baseobjects.operations.parseparentheses
   :members:

operations.timezoneoffset
-----------------------------------

.. automodule:: baseobjects.operations.timezoneoffset
   :members:

operations.unionrecursive
----------------------------------

.. automodule:: baseobjects.operations.unionrecursive
   :members:

operations.updaterecursive
-----------------------------------

.. automodule:: baseobjects.operations.updaterecursive
   :members:

testsuite
-------------------

Test suites for validating behaviors of the corresponding modules.

.. automodule:: baseobjects.testsuite
   :members:

# testsuite subpackages and modules

testsuite.bases
-----------------------

.. automodule:: baseobjects.testsuite.bases
   :members:

.. automodule:: baseobjects.testsuite.bases.basecallabletestsuite
   :members:

.. automodule:: baseobjects.testsuite.bases.baseclasstestsuite
   :members:

.. automodule:: baseobjects.testsuite.bases.basefunctiontestsuite
   :members:

.. automodule:: baseobjects.testsuite.bases.basemethodtestsuite
   :members:

.. automodule:: baseobjects.testsuite.bases.baseobjecttestsuite
   :members:

.. automodule:: baseobjects.testsuite.bases.baseperformancetestsuite
   :members:

testsuite.cachingtools
------------------------------

.. automodule:: baseobjects.testsuite.cachingtools
   :members:

.. automodule:: baseobjects.testsuite.cachingtools.basetimedcachecallabletestsuite
   :members:

.. automodule:: baseobjects.testsuite.cachingtoolstestsuite
   :members:


testsuite.classregistration
-----------------------------------

.. automodule:: baseobjects.testsuite.classregistration
   :members:

.. automodule:: baseobjects.testsuite.classregistration.baseclassregistrytestsuite
   :members:

.. automodule:: baseobjects.testsuite.classregistration.baseregisteredclasstestsuite
   :members:

.. automodule:: baseobjects.testsuite.classregistration.dispatchableclasstestsuite
   :members:

.. automodule:: baseobjects.testsuite.classregistration.namespaceregisteredclasstestsuite
   :members:


testsuite.composition
-----------------------------

.. automodule:: baseobjects.testsuite.composition
   :members:

.. automodule:: baseobjects.testsuite.composition.basecomponenttestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.basecompositetestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.basedispatchingcompositetestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.dispatchablecompositetestsuite
   :members:


testsuite.functions
---------------------------

.. automodule:: baseobjects.testsuite.functions
   :members:

.. automodule:: baseobjects.testsuite.functions.basedecoratortestsuite
   :members:

.. automodule:: baseobjects.testsuite.functions.dynamiccallabletestsuite
   :members:

.. automodule:: baseobjects.testsuite.functions.dynamicdecoratortestsuite
   :members:

.. automodule:: baseobjects.testsuite.functions.dynamicfunctiontestsuite
   :members:

.. automodule:: baseobjects.testsuite.functions.dynamicmethodtestsuite
   :members:


testsuite.objects
-------------------------

.. automodule:: baseobjects.testsuite.objects
   :members:

.. automodule:: baseobjects.testsuite.objects.automaticpropertiestestsuite
   :members:


testsuite.misc
--------------------

.. automodule:: baseobjects.testsuite.versiontestsuite
   :members:


testsuite.wrappers
--------------------------

.. automodule:: baseobjects.testsuite.wrappers
   :members:

.. automodule:: baseobjects.testsuite.wrappers.wrapperperformancetestsuite
   :members:

.. automodule:: baseobjects.testsuite.wrappers.wrappertestsuite
   :members:

typing
----------------

Additional typing helpers and generic protocols used across the project.

.. automodule:: baseobjects.typing
   :members:

typing.callables
-----------------------

.. automodule:: baseobjects.typing.callables
   :members:

typing.generic
---------------------

.. automodule:: baseobjects.typing.generic
   :members:

versioning
--------------------

Version representation and utilities for handling semantic-like versions.

.. automodule:: baseobjects.versioning
   :members:

versioning.trinumberversion
----------------------------------

.. automodule:: baseobjects.versioning.trinumberversion
   :members:

versioning.version
-------------------------

.. automodule:: baseobjects.versioning.version
   :members:

warnings
------------------

Warning categories and helpers for runtime diagnostics.

.. automodule:: baseobjects.warnings
   :members:

warnings.runtime
-----------------------

.. automodule:: baseobjects.warnings.runtime
   :members:

wrappers
------------------

Wrapper utilities to add behavior dynamically at runtime or statically at definition time.

.. automodule:: baseobjects.wrappers
   :members:

wrappers.dynamicwrapper
-------------------------------

.. automodule:: baseobjects.wrappers.dynamicwrapper
   :members:

wrappers.staticwrapper
------------------------------

.. automodule:: baseobjects.wrappers.staticwrapper
   :members:
