"""
Main module.

.. moduleauthor:: Reece Dunham <me@rdil.rocks>
"""

import io


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
        :return: the wrapper
        :rtype: io.TextIOWrapper
        :raises PermissionError: If you don't have needed permission to access the file
        """
        if doreturn:
            return open(str(self), mode="a")
        else:
            open(str(self), mode="a")

    def touch(self):
        """
        Create the file if it doesn't already exist.

        .. important::
           This is the only method that actually changes/interacts with the file
           inside the AbstractFile class (other than :meth:`wrap`).

        In case you are wondering, the name for this function comes from the Unix command
        (:meth:`touch`), which creates a new file with the name as a parameter.

        :return: None
        :rtype: NoneType
        :raises PermissionError: If you don't have needed permission to access the file
        """
        self.wrap(False)


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

    def wrap_file(self):
        """
        Shortcut for :meth:`get_file().wrap()`.

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
        open(str(self.get_file()), mode="w")
