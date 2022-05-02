import csv
import json

items_file = "inputs/items.json"

ITEMS = None
STORES = None
STORE_HAS_ITEMS = None

# todo: add delete store (from item)

def init():
    global ITEMS
    global STORES
    global STORE_HAS_ITEMS
    file_obj = None
    with open(items_file, "r") as jsonfile:
        file_obj = json.load(jsonfile)
    ITEMS = file_obj["items"]
    STORES = file_obj["stores"]
    STORE_HAS_ITEMS = file_obj["storeHasItem"]


shipping_types = [
    {"type": "free", "name": "free"},
    {
        "type": "flat",
        "name": "flat rate",
        "variable": "price",
        "variable_name": "flat rate shipping cost",
    },
    {
        "type": "fixed",
        "name": "fixed rate per item",
        "variable": "price",
        "variable_name": "shipping cost per item",
    },
    {
        "type": "free above",
        "name": "free above",
        "variable": "minimum_price",
        "variable_name": "minimum total?",
        "nested_type": "other_type",
    },
]


def add_new_store():
    first_level_nesting_types = ["free above"]
    store_name = input("What is the new store name? > ")
    store = {"name": store_name, "shipping": {}}
    shipping_type_dict = store["shipping"]
    shipping_var_int = None
    is_nested = True
    nested_level = -1
    while is_nested:
        is_nested = False
        nested_level += 1
        while not shipping_var_int:
            current_shipping_types = [
                shipping_type
                for shipping_type in shipping_types
                if shipping_type["type"] not in first_level_nesting_types
                or nested_level == 0
            ]
            print(
                "{:<6} {}".format(
                    "", "SHIPPING TYPE" if nested_level == 0 else "NESTED SHIPPING TYPE"
                )
            )
            for index, shipping in enumerate(current_shipping_types):
                print("{:<6} {}".format(index + 1, shipping["name"]))

            shipping_type_in = input("Select a shipping type for the store? > ")
            if shipping_type_in.isdigit():
                shipping_var_int = int(shipping_type_in)
                if shipping_var_int < 1 or shipping_var_int > len(
                    current_shipping_types
                ):
                    print("That shipping option does not exist")
                    continue
                shipping_type_dict['type'] = current_shipping_types[shipping_var_int - 1]["type"]
            else:
                print("That is not a valid selection")

        shipping_type = current_shipping_types[shipping_var_int - 1]
        if shipping_type.get("variable_name"):
            valid_number = False
            while not valid_number:
                shipping_var_in = input(f"{shipping_type['variable_name']} > ")
                if shipping_var_in.isdigit():
                    shipping_var_int = int(shipping_var_in)
                    shipping_type_dict[shipping_type["variable"]] = shipping_var_int
                    valid_number = True
                else:
                    print("That is not a valid number")

        nested_type = shipping_type.get("nested_type")
        if nested_type is not None:
            shipping_type_dict[nested_type] = {}
            shipping_type_dict = shipping_type_dict[nested_type]
            shipping_var_int = None
            is_nested = True

    base = (" {:<30}" * 2) + " {:<8} {:<30} {:<8}"
    shipping_type = next(shipping_type_ for shipping_type_ in shipping_types if shipping_type_['type'] == store["shipping"]["type"])
    valid_input = False
    while not valid_input:
        print(
            base.format(
                "NAME",
                "SHIPPING TYPE",
                "COST"
                if not store["shipping"].get(shipping_type.get("variable")) is None
                else "",
                "ALTERNATE SHIPPING TYPE"
                if not store["shipping"].get(shipping_type.get("nested_type")) is None
                else "",
                "ALTERNATE SHIPPING COST"
                if not store["shipping"].get(shipping_type.get("nested_type")) is None
                and not store["shipping"][shipping_type["nested_type"]].get(
                    next(shipping_type_.get("variable") for shipping_type_ in shipping_types if shipping_type_['type'] == store["shipping"][shipping_type["nested_type"]]["type"])
                )
                is None
                else "",
            )
        )
        print(
            base.format(
                store["name"],
                store["shipping"]["type"],
                store["shipping"].get(shipping_type.get("variable")) or "",
                store["shipping"][shipping_type["nested_type"]]["type"]
                if not store["shipping"].get(shipping_type.get("nested_type")) is None
                else "",
                store["shipping"][shipping_type["nested_type"]][
                    next(shipping_type_["variable"] for shipping_type_ in shipping_types if shipping_type_['type'] == store["shipping"][shipping_type["nested_type"]]["type"])
                ]
                if not store["shipping"].get(shipping_type.get("nested_type")) is None
                and not store["shipping"][shipping_type["nested_type"]].get(
                    next(shipping_type_.get("variable") for shipping_type_ in shipping_types if shipping_type_['type'] == store["shipping"][shipping_type["nested_type"]]["type"])
                )
                is None
                else "",
            )
        )
        val_in = input(
            f"'a' to accept or 'c' to cancel and return to previous menu > "
        ).lower()
        if val_in == "a":
            STORES.append(store)
            valid_input = True
        if val_in == "c":
            valid_input = True
        else:
            print("That is not a valid selection")


def add_store(stores_with_item, item_name):
    in_val = None
    while in_val != "r":
        print("select a store to add")
        print("{:<6} {}".format("", "NAME"))
        store_names = {store["store"] for store in stores_with_item}
        remaining_stores = [
            store_["name"] for store_ in STORES if store_["name"] not in store_names
        ]
        for index, store in enumerate(remaining_stores):
            print("{:<6} {}".format(index + 1, store))
        print("\n'n' to add a new store\n'r' to return to the previous menu")
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(remaining_stores):
                print("That store does not exist")
                continue
            valid_price = False
            while not valid_price:
                store_with_item = {
                    "store": remaining_stores[int_val - 1],
                    "item": item_name,
                }
                new_price = input("What is the price at the store? > ")
                if new_price.isdigit():
                    store_with_item["price"] = new_price
                    stores_with_item.append(store_with_item)
                    STORE_HAS_ITEMS.append(store_with_item)
                    valid_price = True
                elif new_price == "r":
                    break
                else:
                    print("That is not a valid price")
        elif in_val == "n":
            add_new_store()
        elif in_val != "r":
            print("Invalid input")


def edit_item(item):
    global STORE_HAS_ITEMS
    in_val = None
    while in_val != "r":
        item_name = item["name"]
        stores_with_item = [
            {"original index": index, **value}
            for index, value in enumerate(STORE_HAS_ITEMS)
            if value["item"] == item_name
        ]
        print(f"EDIT ITEM {item_name}")
        print("select an store number to edit store price")
        print("{:<6} {:<20} {}".format("", "NAME", "PRICE"))
        for index, store in enumerate(stores_with_item):
            print("{:<6} {:<20} {}".format(index + 1, store["store"], store["price"]))
        print(
            "\n'e' to edit item name\n'd' to delete item\n'a' to add a store\n'r' to return to the previous menu"
        )
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(stores_with_item):
                print("That store does not exist")
                continue
            valid_price = False
            while not valid_price:
                new_price = input("What is the new price? > ")
                if new_price.isdigit():
                    STORE_HAS_ITEMS[stores_with_item[int_val - 1]["original index"]][
                        "price"
                    ] = float(new_price)
                    valid_price = True
                elif new_price == "r":
                    break
                else:
                    print("That is not a valid price")
        elif in_val == "e":
            item['name'] = input("What is the new name? > ")
            for edge in stores_with_item:
                STORE_HAS_ITEMS[edge['original index']]['item'] = item['name']
        elif in_val == "d":
            delete_confirm = input("type 'y' if you are sure you want to delete the item and all of its associated prices > ")
            if delete_confirm == 'y':
                ITEMS.remove(item)
                STORE_HAS_ITEMS = list(filter(lambda x: x['item'] != item_name, STORE_HAS_ITEMS))
                in_val = 'r'
        elif in_val == "a":
            add_store(stores_with_item, item_name)
        elif in_val != "r":
            print("Invalid input")


def add_item():
    item_name = input("What is the new item name? > ")
    item = {'name': item_name}
    ITEMS.append(item)
    return edit_item(item)
    

def save():
    file_obj = {"stores": STORES, "storeHasItem": STORE_HAS_ITEMS, "items": ITEMS}
    with open(items_file, "w") as jsonfile:
        json.dump(file_obj, jsonfile)


def main():
    init()
    in_val = None
    while in_val != "q":
        print(f"EDIT ITEMS")
        print("select an item number to edit stores or remove it")
        print("{:<6} {}".format("", "NAME"))
        for index, item in enumerate(ITEMS):
            print("{:<6} {}".format(index + 1, item.get("name")))
        print("\n'a' to add an item\n's' to save and quit\n'q' to quit without saving")
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(ITEMS):
                print("That item does not exist")
                continue
            edit_item(ITEMS[int_val - 1])
        if in_val == "a":
            add_item()
        elif in_val == "s":
            save()
            in_val = "q"
        elif in_val != "q":
            print("Invalid input")


if __name__ == "__main__":
    main()
