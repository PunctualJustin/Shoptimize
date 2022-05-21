from common.list_printer import ColumnWidths, list_printer
from common.input_helpers import set_price
from stores import add_store, get_item_combinations


def edit_item(item, items_list, store_has_items, stores):
    in_val = None
    while in_val != "r":
        item_name = item["name"]
        stores_with_item = [
            {"original index": index, **value}
            for index, value in enumerate(store_has_items)
            if value["item"] == item_name
        ]
        print(f"EDIT ITEM {item_name}")
        print("select an store number to edit store price")
        columns = {
            "": ColumnWidths.INDEX,
            "NAME": ColumnWidths.NAME,
            "PRICE": ColumnWidths.PRICE,
        }
        contents = [[store["store"], store["price"]] for store in stores_with_item]
        list_printer(columns, contents)
        print(
            "\n'e' to edit item name\n'd' to delete item\n'a' to add a store\n'x' to remove the item from a store\n'r' to return to the previous menu"
        )
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(stores_with_item):
                print("That store does not exist")
                continue
            edge = store_has_items[stores_with_item[int_val - 1]["original index"]]
            set_price(edge)
        elif in_val == "e":
            edit_item_name(item, stores_with_item, store_has_items)
        elif in_val == "d":
            in_val = delete_item(item, store_has_items, items_list)
        elif in_val == "a":
            add_store(stores_with_item, item_name, stores, store_has_items)
        elif in_val == "x":
            in_val = remove_store(item, stores_with_item, store_has_items, stores, items_list)
        elif in_val != "r":
            print("Invalid input")

def remove_store(item, stores_with_item, store_has_items, stores, items_list):
    in_val = None
    while in_val != "r":
        item_name = item["name"]
        print(f"REMVOE STORE FROM {item_name}")
        print("select an store number to remove")
        columns = {
            "": ColumnWidths.INDEX,
            "NAME": ColumnWidths.NAME,
            "PRICE": ColumnWidths.PRICE,
        }
        contents = [[store["store"], store["price"]] for store in stores_with_item]
        list_printer(columns, contents)
        print(
            "'r' to return to the previous menu"
        )
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(stores_with_item):
                print("That store does not exist")
                continue
            store_with_item = stores_with_item[int_val - 1]
            remove_linkage(store_has_items, store_with_item, stores, item_name)
        elif in_val != "r":
            print("Invalid input")


def remove_linkage(store_has_items, store_with_item, stores, item_name):
    del store_has_items[store_with_item["original index"]]
    store = next(store for store in stores if store_with_item['store'] == store["name"])
    if (
        store["shipping"]["type"] != "dynamic" or 
        store["shipping"].get("other_type") is None or 
        store["shipping"]["other_type"]["type"] != "dynamic"
    ):
        return
    
    if store["shipping"]["type"] == "dynamic":
        shipping_combos = store["shipping"]
    else:
        shipping_combos = store["shipping"]["other_type"]["combinations"]
                    
    # remove combos
    for combo in list(filter(lambda c: item_name in c['items'], shipping_combos)):
        shipping_combos.remove(combo)


def add_item(items, store_has_items, stores):
    item_name = input("What is the new item name? > ")
    item = {"name": item_name}
    items.append(item)
    return edit_item(item, items, store_has_items, stores)


def edit_item_name(item, stores_with_item, store_has_items):
    item["name"] = input("What is the new name? > ")
    for edge in stores_with_item:
        store_has_items[edge["original index"]]["item"] = item["name"]


def delete_item(item, store_has_items, items):
    delete_confirm = input(
        "type 'y' if you are sure you want to delete the item and all of its associated prices > "
    )
    if delete_confirm == "y":
        items.remove(item)
        for edge in store_has_items:
            if edge["item"] == item["name"]:
                store_has_items.remove(edge)
    return "r"
