"""
Main module.

.. moduleauthor:: Reece Dunham <me@rdil.rocks>
"""

import io
import os
import enum
from json import loads
from json.decoder import JSONDecodeError  # noqa
from typing import Optional, Dict, Any, List


class AbstractFile(object):
    """
    A file in instance form.

    :param name: The file name.
    :type name: str
    """

    def __init__(self, name: str):
        """
        Create the class.

        :param name: The file name.
        :type name: str
        :returns: None
        :rtype: None
        """
        self.name = name

    def __str__(self) -> str:
        """
        Override :meth:`str`.

        :returns: The name of the file.
        :rtype: str
        """
        return self.name

    def wrap(self):
        """
        Wrap file in TextIOWrapper.

        :returns: The wrapper.
        :rtype: io.TextIOWrapper
        :raises PermissionError: If you don't have needed permission to access the file.
        """
        return open(str(self), mode="a")

    def touch(self):
        """
        Create the file if it doesn't already exist.

        .. important::
           This is the only method that actually changes/interacts with the file
           inside the AbstractFile class (other than :meth:`wrap` and :meth:`exists`).

        In case you are wondering, the name for this function comes from the Unix command
        (:code:`touch`), which creates a new file with the name as a parameter.

        :returns: None
        :rtype: None
        :raises PermissionError: If you don't have needed permission to access the file.
        """
        self.wrap().close()

    def exists(self, touch_if_false: Optional[bool] = False) -> bool:
        """
        Get if this file exists or not (boolean value).

        :returns: If the focused file exists.
        :rtype: bool
        :param touch_if_false: If the file should be created if it doesn't exist. Defaults to False.
        :type touch_if_false: Optional[bool]
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

    :param abstract_file: The file to manipulate.
    :type abstract_file: AbstractFile
    """

    def __init__(self, abstract_file):
        """
        Create class instance.

        :param abstract_file: The AbstractFile instance.
        :type abstract_file: AbstractFile
        :returns: None
        :rtype: None
        :raises: TypeError
        """
        self.cache: List[str] = []
        if type(abstract_file) == str:
            self.theFile = AbstractFile(abstract_file)
        elif type(abstract_file) == AbstractFile:
            self.theFile = abstract_file
        else:
            raise TypeError("Wrong type! Please pass AbstractFile or string")
        self.refresh()

    def get_file(self) -> AbstractFile:
        """
        Get the AbstractFile instance.

        :returns: The AbstractFile instance.
        :rtype: AbstractFile
        """
        return self.theFile

    def get_file_name(self) -> str:
        """
        Get the file's name.

        :returns: The file's name.
        :rtype: str
        """
        return str(self.get_file())

    def refresh(self, slim=False):
        """
        Update the cache.

        :param slim: if empty lines should be removed - defaults to True.
        :type slim: Optional[bool]
        :returns: None
        :rtype: None
        :raises PermissionError: If you don't have needed permission to access the file.
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

    def get_cache(self) -> List[str]:
        """
        Get the cache.

        The cache will be a list of the file's lines at the time of the
        last refresh.

        Refreshes are called when this class is created,
        or when manually triggered by :meth:`refresh()`.

        :returns: The cache.
        :rtype: List[str]
        """
        return self.cache

    def write_to_file(self, string: str):
        """
        Write to the file.

        Note:
           Please ensure that what you are writing to the file
           is a string.

        :param string: What to write to the file.
        :type string: str
        Raises:
           PermissionError: If you don't have needed permission to access the file.
           TypeError: If you pass an unsupported type to be written.
        :returns: None
        :rtype: None
        """
        e = self.wrap_file()
        e.write(string)
        e.close()

    def wrap_file(self) -> io.TextIOWrapper:
        """
        Shortcut for :meth:`get_file().wrap()`.

        See Also
        --------
        :meth:`filehandlers.AbstractFile.wrap`

        :returns: The wrapped file.
        :rtype: io.TextIOWrapper
        """
        return self.theFile.wrap()

    def clear_file(self):
        """
        Clear the file.

        .. warning:: You will not be able to recover the old contents!

        :returns: None
        :rtype: None
        :raises PermissionError: If you don't have needed permission to access the file.
        """
        open(str(self.get_file()), mode="w").close()

    def get_file_contents_singlestring(self):
        """
        Get the file's contents, but as one multi-line string.

        .. important:: This function does not use the cache.

        :returns: The file's contents.
        :rtype: str
        :raises PermissionError: If you don't have needed permission to access the file.
        """
        return open(str(self.get_file()), mode="r").read()

    def delete(self):
        """
        Delete the file if it exists.

        :returns: If it got deleted or not (can be ignored by just calling the method).
        :rtype: bool
        :raises PermissionError: If you don't have needed permission to access the file.
        """
        if self.get_file().exists():
            os.remove(str(self.get_file()))
            return True
        return False

    def load_from_json(self) -> Dict[Any, Any]:
        """
        Loads the file, and returns the dictionary containing the data.

        :returns: The dictionary with the data.
        :rtype: Dict[Any, Any]
        :raises JSONDecodeError: If it isn't valid JSON.
        """
        return loads(self.get_file_contents_singlestring())


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

    .. note::
        Text mode should be used when writing text files
        (whether using plain text or a text-based format like TXT),
        while binary mode must be used when writing non-text files like images.
    """
    READ = "r"  #: Read only access to the file.
    READ_BINARY = "rb"  # Read only access to the file (binary enabled).
    WRITE = "w"  #: Write only access to the file - ***see warning above***.
    WRITE_BINARY = "wb"  # Write only access to the file - ***see warning above*** (binary enabled).
    CLEAR = WRITE  #: Clear the file.
    APPEND = "a"  #: Append to the end of the file (also gives read!).
    CREATE = "x"  #: Create the file - ***raises error if file exists***.
    CREATE_AND_WRITE = "w+"  #: Create the file and ready it to be written to.
    TEXT = "t"  #: Default.
    BINARY = "b"  #: Open in binary mode.
    UPDATING = "+"  #: This will open a file for reading and writing (updating).
