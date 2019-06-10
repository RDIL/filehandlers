import io


class AbstractFile:
    """A file in instance form."""
    def __init__(self, name):
        """
        Create the class

        :param name: The file name
        :return: nothing
        :rtype None:
        """
        self.name = name

    def __str__(self):
        """
        Override str() and __str__()

        :return: the name
        :rtype str:
        """
        return self.name

    def wrap(self):
        """
        Wrap file in TextIOWrapper

        :return: the wrapper
        :rtype io.TextIOWrapper:
        """
        return open(self.__str__(), mode="a")


class FileHandler:
    """File handler."""
    def __init__(self, absfile):
        """
        Create class instance

        :param absfile: the AbstractFile instance
        :return: nothing
        :rtype None:
        :raises: TypeError
        """
        self.cache = []
        if type(absfile) != AbstractFile:
            raise TypeError("Parameter must be instance of AbstractFile")
        else:
            self.theFile = absfile

    def get_file(self):
        """
        Get the AbstractFile instance.

        :return: the AbstractFile instance
        :rtype AbstractFile:
        """
        return self.theFile

    def get_file_name(self):
        """
        Get the file's name

        :return: file name
        :rtype str:
        """
        return self.get_file().__str__()

    def refresh(self):
        """
        Update the cached lines

        :return: nothing
        :rtype None:
        """
        with open(self.get_file_name(), mode="r") as filehandler:
            if not type(filehandler) is io.TextIOWrapper:
                raise TypeError("Could not create TextIOWrapper for the file")
            else:
                self.cache = filehandler.readlines()
                # strip newlines
                for h, g in enumerate(self.cache):
                    self.cache[h] = self.cache[h].replace("\n", "")

    def get_cache(self):
        """
        Get the cache

        :return: the cache
        :rtype list:
        """
        return self.cache
