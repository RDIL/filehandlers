import io


class AbstractFile(object):
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
        return open(str(self), mode="a")


class FileManipulator(object):
    """File handler."""
    def __init__(self, abstract_file):
        """
        Create class instance

        :param abstract_file: the AbstractFile instance
        :return: nothing
        :rtype None:
        :raises: TypeError
        """
        self.cache = []
        if type(abstract_file) == str:
            self.theFile = AbstractFile(abstract_file)
        elif type(abstract_file) == AbstractFile:
            self.theFile = abstract_file
        else:
            raise TypeError("Wrong type! Please pass AbstractFile or string")

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
        return str(self.get_file())

    def refresh(self):
        """
        Update the cached lines

        :return: nothing
        :rtype None:
        """
        with open(self.get_file_name(), mode="r") as fh:
            if not type(fh) is io.TextIOWrapper:
                raise TypeError("Could not create TextIOWrapper for the file")
            else:
                self.cache = fh.readlines()
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

    def clear_file(self):
        """
        Clear the file. WARNING: this may be un-reversal

        :return: nothing
        """
        open(str(self.get_file()), mode="w")
