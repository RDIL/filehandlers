Model
=====

filehandlers is built on a relatively simple model.

File
----

A file is represented with an instance of :meth:`filehandlers.AbstractFile`.

.. important::
   The actual file will not be changed or even inspected when creating an instance of :meth:`filehandlers.AbstractFile`.

Manipulation
------------

Now, say you want to change that :ref:`file`... that is where :meth:`filehandlers.FileManipulator` comes in.
You need to pass the :meth:`filehandlers.AbstractFile` instance when creating a :meth:`filehandlers.FileManipulator` because
otherwise the manipulator can't do it's job.

The manipulator includes code for a number of common functions that could be replicated with other code, but the goal of creating
this model/API is to simplify it!

Simple Example
--------------

Here is a quick example that shows how to use filehandlers to write to a file:

.. code-block:: python

   # load in filehandlers
   from filehandlers import FileManipulator, AbstractFile
   
   # define data
   my_cool_file = AbstractFile("log.txt")
   debug_message = "my code works :)"
   
   # create FileManipulator
   my_cool_files_changer = FileManipulator(my_cool_file)
   
   # write data to file 5 times
   for i in range(5):
       my_cool_files_changer.wrap_file().write("Message #" + i + ": " + debug_message)
