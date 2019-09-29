"""
Main module.

.. moduleauthor:: Reece Dunham <me@rdil.rocks>
"""

import io
import os
import enum


class AbstractFile(object):
    """
    A file in instance form.

    :param name: The file name
    :type name: str
    """

    def __init__(self, name):
        """
        Create the class.

        :param name: The file name
        :type name: str
        :return: None
        :rtype: NoneType
        """
        self.name = name

    def __str__(self):
        """
        Override :meth:`str`.

        :return: the name
        :rtype: str
        """
        return self.name

    def change_file_name(self, n):
        """
        Changes the file name.

        .. important::
           This doesn't change the file's actual name,
           it changes the name of the file focused on by this AbstractFile instance.
           We suggest you don't use this because you can just create different
           AbstractFile instances for different files.

        :return: None
        :rtype: NoneType
        :param n: the new name for the file
        :type n: str
        """
        if type(n) != str or n is None:
            raise TypeError("Wrong type! Please pass 'n' as a string!")
        self.name = n

    def wrap(self, doreturn=True):
        """
        Wrap file in TextIOWrapper.

        :param doreturn: *Just keep this True (or don't pass the keyword argument)*.
        :type doreturn: bool
        :return: The wrapper
        :rtype: io.TextIOWrapper
        :raises PermissionError: If you don't have needed permission to access the file
        """
        if doreturn:
            return open(str(self), mode="a")
        else:
            open(str(self), mode="a").close()

    def touch(self):
        """
        Create the file if it doesn't already exist.

        .. important::
           This is the only method that actually changes/interacts with the file
           inside the AbstractFile class (other than :meth:`wrap` and :meth:`exists`).

        In case you are wondering, the name for this function comes from the Unix command
        (:code:`touch`), which creates a new file with the name as a parameter.

        :return: None
        :rtype: NoneType
        :raises PermissionError: If you don't have needed permission to access the file
        """
        self.wrap(False)

    def exists(self, touch_if_false=False):
        """
        Get if this file exists or not (boolean value).

        :return: If the focused file exists
        :rtype: bool:
        :param touch_if_false: If the file should be created if it doesn't exist. Defaults to False.
        :type touch_if_false: bool
        :throws PermissionError: If you don't have the required permissions to access the file.
        """
        e = False
        if os.path.exists(self.name):
            e = True
            if touch_if_false:
                self.touch()
        return e


class FileManipulator(object):
    """
    Class used for managing it's assigned file.

    :param abstract_file: the file to manage
    :type abstract_file: AbstractFile
    """

    def __init__(self, abstract_file):
        """
        Create class instance.

        :param abstract_file: the AbstractFile instance
        :type abstract_file: AbstractFile
        :return: None
        :rtype: NoneType
        :raises: TypeError
        """
        self.cache = []
        if type(abstract_file) == str:
            self.theFile = AbstractFile(abstract_file)
        elif type(abstract_file) == AbstractFile:
            self.theFile = abstract_file
        else:
            raise TypeError("Wrong type! Please pass AbstractFile or string")
        self.refresh()

    def get_file(self):
        """
        Get the AbstractFile instance.

        :return: the AbstractFile instance
        :rtype: AbstractFile
        """
        return self.theFile

    def get_file_name(self):
        """
        Get the file's name.

        :return: The file's name
        :rtype: str
        """
        return str(self.get_file())

    def refresh(self, slim=False):
        """
        Update the cache.

        :param slim: (Optional) - if empty lines should be removed - defaults to True.
        :type slim: bool
        :return: None
        :rtype: NoneType
        :raises PermissionError: If you don't have needed permission to access the file
        """
        with open(self.get_file_name(), mode="r") as fh:
            if not type(fh) is io.TextIOWrapper:
                raise TypeError("Could not create TextIOWrapper for the file")
            else:
                self.cache = fh.readlines()
                # strip newlines
                for h, g in enumerate(self.cache):
                    if(
                        slim and (
                            self.cache[h] is None or
                            self.cache[h] == ""
                        )
                    ):
                        self.cache.pop(h)
                    else:
                        self.cache[h] = self.cache[h].replace("\n", "")
                fh.close()

    def get_cache(self):
        """
        Get the cache.

        The cache will be a list of the file's lines at the time of the
        last refresh.

        Refreshes are called when this class is created,
        or when manually triggered by :meth:`refresh()`.

        :return: the cache
        :rtype: list
        """
        return self.cache

    def write_to_file(self, string):
        """
        Write to the file.

        Note:
           Please ensure that what you are writing to the file
           is a string.

        :param string: What to write to the file.
        :type string: str
        Raises:
           PermissionError: If you don't have needed permission to access the file
           TypeError: If you pass an unsupported type to be written
        :return: None
        :rtype: NoneType
        """
        e = self.wrap_file()
        e.write(string)
        e.close()

    def wrap_file(self):
        """
        Shortcut for :meth:`get_file().wrap()`.

        See Also
        --------
        :meth:`filehandlers.AbstractFile.wrap`

        :return: Wrapped file
        :rtype: io.TextIOWrapper
        """
        return self.theFile.wrap()

    def clear_file(self):
        """
        Clear the file.

        .. warning:: You may not be able to recover the old contents!

        :return: None
        :rtype: NoneType
        :raises PermissionError: If you don't have needed permission to access the file
        """
        open(str(self.get_file()), mode="w").close()

    def get_file_contents_singlestring(self):
        """
        Get the file's contents, but as one string.

        .. note:: This function does not use the cache.

        :return: The file's contents
        :rtype: str
        :raises PermissionError: If you don't have needed permission to access the file
        """
        return open(str(self.get_file()), mode="r").read()


class OpenModes(enum.Enum):
    """
    :meth:`enum.Enum` for the different options you can pass to the
    keyword argument :code:`mode` in Python's :meth:`builtins.open`
    function.

    It can be used like this:

    .. code-block:: python

       from filehandlers import OpenModes
       open("myfile.txt", mode=OpenModes.READ.value)

    This can help so you don't need to remember all the different
    :code:`mode` options.

    .. warning::
       For the :code:`write` option, the file will be cleared and
       then written to. To avoid this, use :code:`append` instead!
    """
    READ = "r"  #: Read only access to the file
    WRITE = "w"  #: Write only access to the file - ***see warning above***
    CLEAR = WRITE  #: Clear the file
    APPEND = "a"  #: Append to the end of the file (also gives read!)
    CREATE = "x"  #: Create the file - ***raises error if file exists***
    CREATE_AND_WRITE = "w+"  #: Create the file and ready it to be written to
    TEXT = "t"  #: Default
    BINARY = "b"  #: Open in binary mode
    UPDATING = "+"  #: This will open a file for reading and writing (updating)
