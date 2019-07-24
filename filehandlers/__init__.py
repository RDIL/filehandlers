import io


class AbstractFile(object):
    """A file in instance form."""

    def __init__(self, name):
        """
        Create the class.

        :param name: The file name
        :return: None
        :rtype: NoneType
        """
        self.name = name

    def __abs__(self):
        """
        Override :meth:`abs(self)` and :meth:`self.__abs__()`

        :return: self
        :rtype: filehandlers.AbstractFile
        """
        return self

    def __str__(self):
        """
        Override :meth:`str(self)` and :meth:`self.__str__()`

        :return: the name
        :rtype: str
        """
        return self.name

    def change_file_name(self, n):
        """
        Changes the file name

        .. important::
           This doesn't change the file's actual name,
           it changes the name of the file focused on by this AbstractFile instance.
           We suggest you don't use this because you can just create different
           AbstractFile instances for different files.

        :return: None
        :rtype: NoneType
        :param n: the new name for the file (must be a string)
        """
        if type(n) != str or n is None:
            raise TypeError("Wrong type! Please pass 'n' as a string!")
        self.name = n

    def wrap(self):
        """
        Wrap file in TextIOWrapper

        :return: the wrapper
        :rtype: io.TextIOWrapper
        """
        return open(str(self), mode="a")


class FileManipulator(object):
    """File handler."""

    def __init__(self, abstract_file):
        """
        Create class instance

        :param abstract_file: the AbstractFile instance
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
        Get the file's name

        :return: The file's name
        :rtype: str
        """
        return str(self.get_file())

    def refresh(self, slim=False):
        """
        Update the cache.

        :param slim: :class:`bool` (Optional) - if empty lines should be removed - defaults to True.
        :return: None
        :rtype: NoneType
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

    def get_cache(self):
        """
        Get the cache.
        The cache will be a list of the file's lines at the time of the
        last refresh.

        Refreshes are called when this class is created,
        or when manually triggered by :meth:`self.refresh()`.

        :return: the cache
        :rtype: list
        """
        return self.cache

    def wrap_file(self):
        """
        Shortcut for :meth:`self.get_file().wrap()`

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
        """
        open(str(self.get_file()), mode="w")
