import csv
import json

items_file = "inputs/items.json"
stores_file = "inputs/stores.csv"

items_file1 = "inputs/items1.json"
stores_file1 = "inputs/stores1.csv"

ITEMS = None
STORES = None


def get_stores():
    global STORES
    with open(stores_file, "r") as csvfile:
        STORES = [store for store in csv.DictReader(csvfile)]


def get_items():
    global ITEMS
    with open(items_file, "r") as jsonfile:
        ITEMS = json.load(jsonfile)


def store_stores():
    with open(stores_file1, "w") as csvfile:
        writer = csv.DictWriter(csvfile, STORES[0])
        writer.writeheader()
        writer.writerows(STORES)


def store_items():
    with open(items_file1, "w") as jsonfile:
        json.dump(ITEMS, jsonfile)


def init():
    get_stores()
    get_items()


shipping_types = [
    {"type": "free", "name": "free"},
    {
        "type": "fixed",
        "name": "fixed flat rate",
        "variable_name": "flat rate shipping cost",
    },
    {
        "type": "flat rate",
        "name": "fixed rate per item",
        "variable_name": "flat rate shipping cost",
    },
    {"type": "free above", "name": "free above", "variable_name": "minimum total?"},
]


def add_new_store():
    store_name = input("What is the new store name? > ")
    store = {"ID": store_name, "Name": store_name}
    shipping_var_int = None
    while not shipping_var_int:
        print("{:<6} {}".format("", "SHIPPING TYPE"))
        for index, shipping in enumerate(shipping_types):
            print("{:<6} {}".format(index + 1, shipping["name"]))

        shipping_type_in = input("Select a shipping type for the store? > ")
        if shipping_type_in.isdigit():
            shipping_var_int = int(shipping_type_in)
            store["shipping"] = shipping_types[shipping_var_int - 1]["type"]
        else:
            print("That is not a valid selection")
    if shipping_types[shipping_var_int - 1].get("variable_name"):
        valid_number = False
        while not valid_number:
            shipping_var_in = input(
                f"{shipping_types[shipping_var_int-1]['variable_name']} > "
            )
            if shipping_var_in.isdigit():
                shipping_var_int = int(shipping_var_in)
                store["shipping_variable"] = shipping_var_int
                valid_number = True
            else:
                print("That is not a valid number")

    base = (" {:<30}" * 2) + " {:<8}"
    valid_input = False
    while not valid_input:
        print(
            base.format(
                "NAME",
                "SHIPPING TYPE",
                "COST" if store.get("shipping_variable") else "",
            )
        )
        print(
            base.format(
                store["Name"], store["shipping"], store.get("shipping_variable") or ""
            )
        )
        val_in = input(
            f"'a' to accept or 'c' to cancel and return to previous menu > "
        ).tolower()
        if val_in == "a":
            STORES.append(store)
            valid_input = True
        if val_in == "c":
            valid_input = True
        else:
            print("That is not a valid selection")


def add_store(stores):
    in_val = None
    while in_val != "r":
        print("select a store to add")
        print("{:<6} {}".format("", "NAME"))
        store_names = {store["store id"] for store in stores}
        remaining_stores = [
            store_["Name"] for store_ in STORES if store_["ID"] not in store_names
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
                store = {
                    "store id": next(
                        (
                            store_["ID"]
                            for store_ in STORES
                            if store_["Name"] == remaining_stores[int_val - 1]
                        )
                    )
                }
                stores.append(store)
                new_price = input("What is the price at the store? > ")
                if new_price.isdigit():
                    store["price"] = new_price
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
    in_val = None
    while in_val != "r":
        stores = item["stores"]
        item_name = item["name"]
        print(f"EDIT ITEM {item_name}")
        print("select an store number to edit store price")
        print("{:<6} {:<20} {}".format("", "NAME", "PRICE"))
        for index, store in enumerate(stores):
            print(
                "{:<6} {:<20} {}".format(index + 1, store["store id"], store["price"])
            )
        print(
            "\n'e' to edit item name\n'a' to add a store\n'r' to return to the previous menu"
        )
        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(ITEMS):
                print("That store does not exist")
                continue
            valid_price = False
            while not valid_price:
                new_price = input("What is the new price? > ")
                if new_price.isdigit():
                    stores[int_val - 1]["price"] = float(new_price)
                    valid_price = True
                elif new_price == "r":
                    break
                else:
                    print("That is not a valid price")
        if in_val == "e":
            item["name"] = input("What is the new name? > ")
        elif in_val == "a":
            add_store(stores)
        elif in_val != "r":
            print("Invalid input")


def save():
    store_items()
    store_stores()


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
            pass
        elif in_val == "s":
            save()
            in_val = "q"
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()
