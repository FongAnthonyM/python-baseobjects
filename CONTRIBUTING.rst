Contributor Guide
=================

Interest is appreciated in improving this project.
This project is open-source under the `MIT license`_ and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- `Source Code`_
- `Documentation`_
- `Issue Tracker`_
- `Code of Conduct`_

.. _MIT license: https://opensource.org/licenses/MIT
.. _Source Code: https://github.com/AnthonyTechnologies/python-baseobjects
.. _Documentation: https://python-baseobjects.readthedocs.io/
.. _Issue Tracker: https://github.com/AnthonyTechnologies/python-baseobjects/issues

Reporting Bugs
--------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Operating system and Python version.
- Version of this project.
- Steps taken.
- Expected behavior.
- Actual behavior.

Providing a test case is the best way to get a bug fixed,
and/or steps to reproduce the issue.


Requesting Features
-------------------

Request features on the `Issue Tracker`_.


Development Environment Setup
------------------------------

Python 3.14+ and the following tools are required:

- Nox_

Install the package with development requirements:

.. code:: console

   $ pip install -e .[dev]

An interactive Python session can now be run:

.. code:: console

   $ python

.. _Nox: https://nox.thea.codes/


Project Tools
-------------

This project uses several tools to ensure code quality and consistency.

- **Nox**: A flexible test automation tool.
- **uv**: A fast Python package installer and resolver.
- **pre-commit**: A framework for managing and maintaining multi-language pre-commit hooks.
- **mypy**: Optional static typing for Python.
- **pytest**: The pytest framework makes it easy to write small tests.
- **coverage**: Code coverage measurement for Python.
- **typeguard**: Run-time type checker for Python.
- **xdoctest**: A rewrite of the standard library doctest module.
- **Sphinx**: Python documentation generator.

Testing the Project
-------------------

This project uses `Nox`_ for test automation. It orchestrates testing, linting, and documentation building across different environments.

Run the full default test suite (creates new virtual environments):

.. code:: console

   $ nox

List the available Nox sessions:

.. code:: console

   $ nox --list-sessions

Nox Sessions
~~~~~~~~~~~~

The Nox sessions are categorized into two main groups based on how they run:

New Environments
^^^^^^^^^^^^^^^^

These sessions create isolated virtual environments for each run. This ensures that tests run in a clean, reproducible state with the exact dependencies specified for the project. These are the default sessions.

**Tag:** ``new_venv``

- ``tests``: Run the test suite using pytest.
- ``mypy``: Run static type checking.
- ``typeguard``: Run runtime type checking.
- ``xdoctest``: Run doctests.
- ``docs-build``: Build the documentation.
- ``pre-commit``: Run pre-commit hooks.
- ``coverage``: Produce coverage reports.

Active Environment
^^^^^^^^^^^^^^^^^^

These sessions run tools in the currently active Python environment. This is useful for testing with different dependencies (e.g., experimental versions) or for faster iteration if valid dependencies are already installed.

**Tag:** ``active_venv``

- ``tests_active``
- ``mypy_active``
- ``typeguard_active``
- ``xdoctest_active``
- ``docs-build_active``
- ``pre-commit_active``
- ``coverage_active``

Running Specific Sessions
~~~~~~~~~~~~~~~~~~~~~~~~~

Individual sessions can be run by name:

.. code:: console

   $ nox -s tests

Or run a group of sessions using tags:

.. code:: console

   $ nox -t new_venv
   $ nox -t active_venv

Submitting Changes
------------------

Open a `pull request`_ to submit changes to this project.

Pull requests must meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If changes add functionality, update the documentation accordingly.

Submitting changes early is encouraged to allow for iterative improvements and discussion.

To run linting and code formatting checks before committing a change, install pre-commit as a Git hook by running the following command:

.. code:: console

   $ nox --session=pre-commit -- install

It is recommended to open an issue before starting work on anything.
This allows a chance to discuss the work with the owners and validate the approach.

.. _pull request: https://github.com/AnthonyTechnologies/python-baseobjects/pulls
.. github-only
.. _Code of Conduct: CODE_OF_CONDUCT.rst
