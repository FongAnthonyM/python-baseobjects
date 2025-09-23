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


GitHub with Examples & Tutorials
--------------------------------

Clone the repo and install in editable mode (recommended for exploring notebooks or contributing):

.. code-block:: bash

   git clone https://github.com/AnthonyTechnologies/python-baseobjects.git
   cd python-baseobjects
   python -m venv .venv
   .venv\Scripts\activate
   pip install -U pip
   pip install -e .

To run the tutorials (Jupyter notebooks), install Jupyter and open the tutorials folder:

.. code-block:: bash

   pip install jupyter
   jupyter notebook tutorials

Alternatively, open the .ipynb files in your preferred IDE.
