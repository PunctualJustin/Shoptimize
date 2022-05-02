from .store_loader import add_stores
from .item_loader import add_items


def initialize_items():
    stores = add_stores()
    items = add_items(stores)
    return stores
