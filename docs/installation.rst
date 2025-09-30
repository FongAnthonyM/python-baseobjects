Installation
============

PyPI (pip) is the recomended way to install BaseObjects, but Github can also be used. If you want to run the examples
and Jupyter tutorials included in this repository, you should clone and install from GitHub.


PyPI
----
You can install baseobjects using pip:

.. code-block:: bash

   pip install baseobjects


GitHub
------

Install the latest code from the main branch without cloning:

.. code-block:: bash

   pip install "git+https://github.com/AnthonyTechnologies/python-baseobjects.git@main"


GitHub Clone
------------

Installing a github clone can be useful for either exploring the examples and tutorials and/or contributing
baseobjects.

For only exlporing examples and tutorials:

.. code-block:: bash

   git clone https://github.com/AnthonyTechnologies/python-baseobjects.git
   cd python-baseobjects
   pip install .[jupyter]

For contributing/developing baseobjects:

.. code-block:: bash

   git clone https://github.com/AnthonyTechnologies/python-baseobjects.git
   cd python-baseobjects
   pip install -e .[dev]
