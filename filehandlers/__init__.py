import io


class AbstractFile:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.__str__()

    def wrap(self):
        return open(self.get_name(), mode="a")


class FileHandler:
    def __init__(self, absfile):
        self.cache = []
        if type(absfile) != AbstractFile:
            raise TypeError("the only parameter must be instance of AbstractFile")
        else:
            self.theFile = absfile

    def get_file(self):
        return self.theFile

    def get_file_name(self):
        return self.get_file().get_name()

    def refresh(self):
        with open(self.get_file_name(), mode="r") as filehandler:
            if not type(filehandler) is io.TextIOWrapper:
                raise TypeError("Could not create a TextIOWrapper for the file")
            else:
                self.cache = filehandler.readlines()
                # strip newlines
                for h, g in enumerate(self.cache):
                    self.cache[h] = self.cache[h].replace("\n", "")

    def get_cache(self):
        return self.cache