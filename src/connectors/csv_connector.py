import csv


class CSVConnector:
    def __init__(self, file):
        self.filePath = file
        self.__iter = None
        self.__file = None

    def __iter__(self):
        if not self.__file:
            self.__file = open(self.filePath)
            self.__iter = csv.DictReader(self.__file)
        elif not self.__iter:
            self.__iter = csv.DictReader(self.__file)
        else:
            self.__file.seek(0)
        return self

    def __next__(self):
        store = next(self.__iter, None)
        if store is None:
            self.__file.close()
            self.__file = None
            self.__iter = None
            raise StopIteration
        return store
