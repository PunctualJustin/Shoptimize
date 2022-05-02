import json


class JSONConnector:
    def __init__(self, file_path):
        with open(file_path) as file:
            self.obj = json.load(file)
        if not isinstance(self.obj, list):
            raise Exception("File object is not a list")
        self.__n = 0
        self.__len = len(self.obj)

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n >= self.__len:
            raise StopIteration
        item = self.obj[self.__n]
        self.__n += 1
        return item
