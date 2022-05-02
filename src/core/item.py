from connectors.json_connector import JSONConnector


class Item:
    def __init__(self, id, name, stores):
        self.id = id
        self.name = name
        self.stores = stores
