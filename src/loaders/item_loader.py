from connectors.json_connector import JSONConnector
from core.item import Item


items_json_file = "inputs/items.json"


def add_items(stores):
    items = {}
    obj = JSONConnector(items_json_file)
    for item in obj:
        new_item = Item(**item)
        items[item["name"]] = new_item
        for store in item["stores"]:
            stores[store["store id"]].add_item(new_item, store["price"])
    return items
