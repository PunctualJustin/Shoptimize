from connectors.json_connector import JSONConnector
from core.item import Item





def add_items(input_file_path, stores):
    obj = JSONConnector(input_file_path, "storeHasItem")
    for edge in obj:
        stores[edge["store"]].add_item(**edge)
