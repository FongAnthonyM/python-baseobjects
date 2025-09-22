Testing
=======

This project uses pytest and nox to run tests and ensure code quality.

Running the test suite
----------------------

You can run the tests locally with pytest:

.. code-block:: bash

   pip install -e .[tests]
   pytest -q

Alternatively, you can use the provided nox sessions (recommended):

.. code-block:: bash

   pip install nox
   nox -s tests

Test coverage
-------------

To measure test coverage:

.. code-block:: bash

   nox -s coverage

The HTML coverage report will be available under ``.nox/coverage/htmlcov/index.html``.

Type checking and linting
-------------------------

Static type checking and code quality checks are available via dedicated nox sessions:

.. code-block:: bash

   nox -s mypy
   nox -s lint

Continuous integration
----------------------

Tests are also executed in CI. Refer to ``noxfile.py`` for the authoritative list of sessions and their parameters.
