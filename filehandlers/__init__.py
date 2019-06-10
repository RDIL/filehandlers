import io


class AbstractFile:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def wrap(self):
        return open(self.__str__(), mode="a")


class FileHandler:
    def __init__(self, absfile):
        self.cache = []
        if type(absfile) != AbstractFile:
            raise TypeError("Parameter must be instance of AbstractFile")
        else:
            self.theFile = absfile

    def get_file(self):
        return self.theFile

    def get_file_name(self):
        return self.get_file().__str__()

    def refresh(self):
        with open(self.get_file_name(), mode="r") as filehandler:
            if not type(filehandler) is io.TextIOWrapper:
                raise TypeError("Could not create TextIOWrapper for the file")
            else:
                self.cache = filehandler.readlines()
                # strip newlines
                for h, g in enumerate(self.cache):
                    self.cache[h] = self.cache[h].replace("\n", "")

    def get_cache(self):
        return self.cache
