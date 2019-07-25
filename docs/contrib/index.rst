Contributing Guide
==================

Welcome to the filehandlers contributing guidelines!
Please follow what is listed here to help keep the project simple, easy to maintain,
and complete.

Style Guide
-----------

Code
++++

When writing code, please follow PEP8 [#PEP8]_, the style guide written for any Python.
One exception for this is our line length - PEP8 says 79 characters is the limit,
but we have decided to extend that to a maximum of 100 characters per line.
Also, wherever possible, please add :ref:`Docstrings`.

Docstrings
++++++++++

We mainly use normal reStructuredText Docstrings for filehandlers.
However, for elements that have more then one field - for example if
a function has the potential to throw multiple exceptions -
we use Google [#googledocstrings]_ and/or
NumPy [#numpydocstrings]_ styled Docstrings.
These are later converted by the Sphinx extension :code:`napoleon` during
documentation builds.
Please add Docstrings to functions, classes, modules (at the top), exceptions
and enumerators.

If you add a class that is not covered by the documentation currently (e.x. you create
a method or class that is *not* in a method/class that has the :code:`:members:`
autodoc method), you will need to add a field so autodoc knows the include the Docstring(s).
To do this, navigate to the API reference page and add this underneath all the other
classes/methods:

For classes/enumerators
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   ,.. autoclass:: ClassName
      ,:members:
      ,:special-members: __init__

For functions
~~~~~~~~~~~~~

.. code-block:: rst

   ,.. autofunction:: function_name

For exceptions
~~~~~~~~~~~~~~

.. code-block:: rst

   ,.. autoexception:: ExceptionName

Notes
~~~~~

* **Make sure to remove the commas, they prevent autodoc from trying to add a method here on this page!**
* You do *not* need to add module Docstrings to the API reference page.

Building the package
--------------------

Simply run :code:`python setup.py sdist bdist_wheel`.
*If you are on Linux/macOS, change* :code:`python` *to* :code:`python3`.
The build shouldn't be long. When it is complete, you can find the :code:`.tar.gz`
and :code:`.whl` in the :code:`dist` directory.

.. [#PEP8] `Python Enhancement Proposal #8 <https://www.python.org/dev/peps/pep-0008/>`_
.. [#googledocstrings] `Google Docstring Guide <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>`_
.. [#numpydocstrings] `NumPy Docstring Guide <https://numpydoc.readthedocs.io/en/latest/format.html#numpydoc-docstring-guide>`_
