Tutorials and Examples
======================

.. contents:: On this page
   :local:
   :backlinks: none

This project includes additional tutorials and examples in the repository to help you learn by doing.

Repository Tutorials
--------------------

- Jupyter notebooks: see the ``tutorials/`` directory.
- Code examples: see the ``examples/`` directory.

Available example categories in ``examples/``:

- ``bases``: Examples of base classes and primitives.
- ``classregistration``: Examples of class registries and dispatching.
- ``collections``: Examples of specialized collection types.
- ``composition``: Examples of component-based systems.
- ``functions``: Examples of dynamic functions and decorators.
- ``objects``: Examples of object helpers and properties.
- ``operations``: Examples of general-purpose operations.
- ``testsuite``: Examples related to testing foundations.
- ``versioning``: Examples of version handling.
- ``wrappers``: Examples of object wrappers.

To run the notebooks locally, install the optional dependencies and launch Jupyter:

.. code-block:: bash

   pip install -e .[jupyter]
   jupyter notebook tutorials/

Note: The documentation site does not render the notebooks directly. Use the links above to explore them locally.
