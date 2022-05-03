from .store_loader import add_stores
from .item_loader import add_items

inputs_file = "inputs/items.json"


def initialize_items():
    stores = add_stores(inputs_file)
    add_items(inputs_file, stores)
    return stores
