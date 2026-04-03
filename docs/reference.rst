API Reference
=============

.. contents::
    :local:
    :depth: 2
    :backlinks: none


Bases
-----

Core base classes and common primitives that other modules build upon.

.. automodule:: baseobjects.bases

BaseObject
----------

.. autoclass:: baseobjects.bases.baseobject.BaseObject
   :members:

BaseMeta
--------

.. autoclass:: baseobjects.bases.basemeta.BaseMeta
   :members:

Bases Base Callable
-------------------

.. automodule:: baseobjects.bases.basecallable

BaseReducible
-------------

.. autoclass:: baseobjects.bases.basereducible.BaseReducible
   :members:

SentinelObject
---------------

.. autoclass:: baseobjects.bases.sentinelobject.SentinelObject
   :members:

Bases Collections
-----------------

.. automodule:: baseobjects.bases.collections

Bases Collections Base Dict
---------------------------

.. automodule:: baseobjects.bases.collections.basedict
   :members:

BaseList
--------

.. automodule:: baseobjects.bases.collections.baselist
   :members:

Caching Tools
----------------------

Caching utilities and cache abstractions for performance-sensitive workloads.

.. automodule:: baseobjects.cachingtools

Caching Tools Caching Object
--------------------------------

.. automodule:: baseobjects.cachingtools.cachingobject
   :members:

cachingtools.caches
------------------------------

.. automodule:: baseobjects.cachingtools.caches

BaseTimedCache
--------------

.. automodule:: baseobjects.cachingtools.caches.basetimedcache
   :members:

TimedCache
----------

.. automodule:: baseobjects.cachingtools.caches.timedcache
   :members:

TimedKeylessCache
-----------------

.. automodule:: baseobjects.cachingtools.caches.timedkeylesscache
   :members:

TimedLRUCache
-------------

.. automodule:: baseobjects.cachingtools.caches.timedlrucache
   :members:

TimedSingleCache
----------------

.. automodule:: baseobjects.cachingtools.caches.timedsinglecache
   :members:

classregistration
---------------------------

Mechanisms for registering and dispatching classes and instances by keys or namespaces.

.. automodule:: baseobjects.classregistration

BaseClassRegistry
-----------------

.. automodule:: baseobjects.classregistration.baseclassregistry
   :members:

BaseRegisteredClass
-------------------

.. automodule:: baseobjects.classregistration.baseregisteredclass
   :members:

DispatchableClass
-----------------

.. automodule:: baseobjects.classregistration.dispatchableclass
   :members:

NamespaceClassRegistry
----------------------

.. automodule:: baseobjects.classregistration.namespaceclassregistry
   :members:

NamespaceRegisteredClass
------------------------

.. automodule:: baseobjects.classregistration.namespaceregisteredclass
   :members:

collections
---------------------

Specialized collection types extending or complementing Python's built-in containers.

.. automodule:: baseobjects.collections

CircularDoublyLinkedContainer
-----------------------------

.. automodule:: baseobjects.collections.circulardoublylinkedcontainer
   :members:

DeepChainMap
------------

.. automodule:: baseobjects.collections.deepchainmap
   :members:

GroupedList
-----------

.. automodule:: baseobjects.collections.groupedlist
   :members:

OrderableDict
-------------

.. automodule:: baseobjects.collections.orderabledict
   :members:

TimedDict
---------

.. automodule:: baseobjects.collections.timeddict
   :members:

composition
---------------------

Composable object patterns and helper classes for building component-based systems.

.. automodule:: baseobjects.composition

BaseComponent
-------------

.. automodule:: baseobjects.composition.basecomponent
   :members:

BaseComposite
-------------

.. automodule:: baseobjects.composition.basecomposite
   :members:

BaseDispatchingComposite
------------------------

.. automodule:: baseobjects.composition.basedispatchingcomposite
   :members:

DispatchableComposite
---------------------

.. automodule:: baseobjects.composition.dispatchablecomposite
   :members:

CompositeFactoryClass
---------------------

.. automodule:: baseobjects.composition.compositefactoryclass
   :members:

dataclasses
---------------------

Lightweight data containers and parameter helpers to structure configuration and state.

.. automodule:: baseobjects.dataclasses

Parameters
----------

.. automodule:: baseobjects.dataclasses.parameters
   :members:

functions
-------------------

Dynamic function utilities, decorators, and dispatching helpers.

.. automodule:: baseobjects.functions

BaseDecorator
-------------

.. automodule:: baseobjects.functions.basedecorator
   :members:

CallableMultiplexer
-------------------

.. automodule:: baseobjects.functions.callablemultiplexer
   :members:

DynamicCallable
---------------

.. automodule:: baseobjects.functions.dynamiccallable
   :members:

DynamicDecorator
----------------

.. automodule:: baseobjects.functions.dynamicdecorator
   :members:

FunctionRegistry
----------------

.. automodule:: baseobjects.functions.functionregistry
   :members:

MethodRegistry
--------------

.. automodule:: baseobjects.functions.methodregistry
   :members:

singlekwargdispatch
-------------------

.. automodule:: baseobjects.functions.singlekwargdispatch
   :members:

metaclasses
---------------------

Metaclass utilities to control class creation and initialization behavior.

.. automodule:: baseobjects.metaclasses

InitMeta
--------

.. automodule:: baseobjects.metaclasses.initmeta
   :members:

objects
-----------------

Object helpers for property management, callbacks, and utility behaviors.

.. automodule:: baseobjects.objects

AutomaticProperties
-------------------

.. automodule:: baseobjects.objects.automaticproperties
   :members:

CallbackManager
---------------

.. automodule:: baseobjects.objects.callbackmanager
   :members:

operations
--------------------

General-purpose operations and algorithms for data transformation and inspection.

.. automodule:: baseobjects.operations

bytes_to_bin
------------

.. automodule:: baseobjects.operations.bytestobin
   :members:

excel_date_to_datetime
----------------------

.. automodule:: baseobjects.operations.exceldatetodatetime
   :members:

filetime_to_datetime
--------------------

.. automodule:: baseobjects.operations.filetimetodatetime
   :members:

get_method_names
----------------

.. automodule:: baseobjects.operations.methodnames
   :members:

parse_parentheses
-----------------

.. automodule:: baseobjects.operations.parseparentheses
   :members:

timezone_offset
---------------

.. automodule:: baseobjects.operations.timezoneoffset
   :members:

union_recursive
---------------

.. automodule:: baseobjects.operations.unionrecursive
   :members:

update_recursive
----------------

.. automodule:: baseobjects.operations.updaterecursive
   :members:

testsuite
-------------------

Test suites for validating behaviors of the corresponding modules.

.. automodule:: baseobjects.testsuite

# testsuite subpackages and modules

testsuite.bases
-----------------------

.. automodule:: baseobjects.testsuite.bases

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

.. automodule:: baseobjects.testsuite.cachingtools.basetimedcachecallabletestsuite
   :members:

.. automodule:: baseobjects.testsuite.cachingtools.cachingtoolstestsuite
   :members:


testsuite.classregistration
-----------------------------------

.. automodule:: baseobjects.testsuite.classregistration

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

.. automodule:: baseobjects.testsuite.composition.basecomponenttestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.basecompositetestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.basedispatchingcompositetestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.dispatchablecompositetestsuite
   :members:

.. automodule:: baseobjects.testsuite.composition.compositefactoryclasstestsuite
   :members:


testsuite.functions
---------------------------

.. automodule:: baseobjects.testsuite.functions

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

.. automodule:: baseobjects.testsuite.objects.automaticpropertiestestsuite
   :members:


testsuite.misc
--------------------

.. automodule:: baseobjects.testsuite.versioning.versiontestsuite
   :members:


testsuite.wrappers
--------------------------

.. automodule:: baseobjects.testsuite.wrappers

.. automodule:: baseobjects.testsuite.wrappers.wrapperperformancetestsuite
   :members:

.. automodule:: baseobjects.testsuite.wrappers.wrappertestsuite
   :members:

typing
----------------

Additional typing helpers and generic protocols used across the project.

.. automodule:: baseobjects.typing

Callables
---------

.. automodule:: baseobjects.typing.callables
   :members:

Generic Types
-------------

.. automodule:: baseobjects.typing.generic
   :members:

versioning
--------------------

Version representation and utilities for handling semantic-like versions.

.. automodule:: baseobjects.versioning

TriNumberVersion
----------------

.. automodule:: baseobjects.versioning.trinumberversion
   :members:

Version
-------

.. automodule:: baseobjects.versioning.version
   :members:

warnings
------------------

Warning categories and helpers for runtime diagnostics.

.. automodule:: baseobjects.warnings

Runtime Warnings
----------------

.. automodule:: baseobjects.warnings.runtime
   :members:

wrappers
------------------

Wrapper utilities to add behavior dynamically at runtime or statically at definition time.

.. automodule:: baseobjects.wrappers

DynamicWrapper
--------------

.. automodule:: baseobjects.wrappers.dynamicwrapper
   :members:

StaticWrapper
-------------

.. automodule:: baseobjects.wrappers.staticwrapper
   :members:
