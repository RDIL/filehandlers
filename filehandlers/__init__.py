"""The main module."""

import io
import os
import enum
from json import loads
from json.decoder import JSONDecodeError  # noqa
from typing import Optional, Dict, Any, List


class AbstractFile:
    """A file in instance form."""

    def __init__(self, name: str):
        """
        Create the class.

        Args:
            name: The file name.

        Returns:
            Nothing.
        """
        self.name = name

    def __str__(self) -> str:
        """
        Override of `__str__`.

        Returns:
            The name of the file.
        """
        return self.name

    def wrap(self):
        """
        Wrap the file in a [io.TextIOWrapper].

        Returns:
            The wrapper.
        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        return open(str(self), mode="a")

    def touch(self):
        """
        Create the file if it doesn't already exist.

        Important:
           This is the only method that actually changes/interacts with the file
           inside the AbstractFile class (other then [wrap] and [exists]).

        In case you are wondering, the name for this function comes from the Unix command
        `touch`, which creates a new file with the name as a parameter.

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        self.wrap().close()

    def exists(self, touch_if_false: Optional[bool] = False) -> bool:
        """
        Get if this file exists or not (boolean value).

        Returns:
            If the file exists.

        Arguments:
            touch_if_false: If the file should be created if it doesn't exist.

        Raises:
            PermissionError: If you don't have the required permissions to access the file.
        """
        e = False
        if os.path.exists(self.name):
            e = True
            if touch_if_false:
                self.touch()
        return e


class FileManipulator:
    """Class used for managing an assigned file."""
    cache: List[str]
    theFile: AbstractFile

    def __init__(self, abstract_file: AbstractFile):
        """
        Create class instance.

        Arguments:
            abstract_file: The AbstractFile instance.

        Returns:
            Nothing.

        Raises:
            TypeError: If the argument isn't an [AbstractFile].
        """
        self.cache = []
        if type(abstract_file) == AbstractFile:
            self.theFile = abstract_file
        else:
            raise TypeError("Wrong type! Please pass AbstractFile or string")
        self.refresh()

    def get_file(self) -> AbstractFile:
        """
        Get the AbstractFile instance.

        Returns:
            The AbstractFile instance.
        """
        return self.theFile

    def get_file_name(self) -> str:
        """
        Get the file's name.

        Returns:
            The file's name.
        """
        return str(self.get_file())

    def refresh(self, slim: Optional[bool] = False):
        """
        Update the cache.

        Arguments:
            slim: If empty lines should be removed.

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
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
        or when manually triggered by [refresh].

        Returns:
            The cache.
        """
        return self.cache

    def write_to_file(self, string: str):
        """
        Write to the file.

        Note:
           Please ensure that what you are writing to the file
           is a string.

        Arguments:
            string: What to write to the file.

        Raises:
           PermissionError: If you don't have needed permission to access the file.
           TypeError: If you pass an unsupported type to be written.

        Returns:
            Nothing.
        """
        e = self.wrap_file()
        e.write(string)
        e.close()

    def wrap_file(self) -> io.TextIOWrapper:
        """
        Shortcut for `self.get_file().wrap()`.

        Returns:
            The wrapped file.
        """
        return self.theFile.wrap()

    def clear_file(self):
        """
        Clear the file.

        Warning: You will not be able to recover the old contents!

        Returns:
            Nothing.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        open(str(self.get_file()), mode="w").close()

    def get_file_contents_singlestring(self) -> str:
        """
        Get the file's contents, but as one multi-line string.

        Important: This function does not use the cache.

        Returns:
            The file's contents.

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        return open(str(self.get_file()), mode="r").read()

    def delete(self):
        """
        Delete the file if it exists.

        Returns:
            If it got deleted or not (can be ignored by just calling the method).

        Raises:
            PermissionError: If you don't have needed permission to access the file.
        """
        if self.get_file().exists():
            os.remove(str(self.get_file()))
            return True
        return False

    def load_from_json(self) -> Dict[str, Any]:
        """
        Loads the file, and returns the dictionary containing the data.

        Returns:
            The dictionary with the data.

        Raises:
            JSONDecodeError: If it isn't valid JSON.
        """
        return loads(self.get_file_contents_singlestring())


class OpenModes(enum.Enum):
    """
    [Enum][enum.Enum] for the different options you can pass to the
    keyword argument `mode` in Python's `open` function.

    It can be used like this:

    ```python
    from filehandlers import OpenModes
    open("myfile.txt", mode=OpenModes.READ.value)
    ```

    This can help so you don't need to remember all the different
    `mode` options.

    Warning:
       For the `write` option, the file will be cleared and
       then written to. To avoid this, use `append` instead!

    Note:
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
