Model
-----

filehandlers is built on a relatively simple model.
A file is represented with an instance of :meth:`filehandlers.AbstractFile`.
The actual file will not be changed or even inspected when creating an instance of :meth:`filehandlers.AbstractFile`.
Now, say you want to change that file... that is where :meth:`filehandlers.FileManipulator` comes in.
