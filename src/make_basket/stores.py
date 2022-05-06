from enum import Enum
from typing import List
from pulp import allcombinations
from common.list_printer import ColumnWidths
from common.list_printer import list_printer
from common.input_helpers import set_price

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
        "name": "free above a minimum price",
        "variable": "minimum_price",
        "variable_name": "minimum total?",
        "nested_type": "other_type",
    },
    {
        "type": "dynamic",
        "name": "shipping price changes based on the items",
    },
]


def add_new_store(stores):
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
        while True:
            current_shipping_types = [
                shipping_type
                for shipping_type in shipping_types
                if shipping_type["type"] not in first_level_nesting_types
                or nested_level == 0
            ]
            headers = {
                "": ColumnWidths.INDEX,
                "SHIPPING TYPE"
                if nested_level == 0
                else "NESTED SHIPPING TYPE": ColumnWidths.NAME,
            }
            contents = map(lambda shipping: [shipping["name"]], current_shipping_types)
            list_printer(headers, contents)

            shipping_type_in = input("Select a shipping type for the store? > ")
            if shipping_type_in.isdigit():
                shipping_var_int = int(shipping_type_in)
                if shipping_var_int < 1 or shipping_var_int > len(
                    current_shipping_types
                ):
                    print("That shipping option does not exist")
                    continue
                shipping_type_dict["type"] = current_shipping_types[
                    shipping_var_int - 1
                ]["type"]
                break
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
        elif shipping_type["type"] == "dynamic":
            shipping_type_dict["combinations"] = []

        nested_type = shipping_type.get("nested_type")
        if nested_type is not None:
            shipping_type_dict[nested_type] = {}
            shipping_type_dict = shipping_type_dict[nested_type]
            shipping_var_int = None
            is_nested = True

    base = (" {:<30}" * 2) + " {:<8} {:<30} {:<8}"

    shipping_type = next(
        shipping_type_
        for shipping_type_ in shipping_types
        if shipping_type_["type"] == store["shipping"]["type"]
    )
    headers = {
        "NAME": ColumnWidths.NAME,
        "SHIPPING TYPE": ColumnWidths.NAME,
        "COST"
        if not store["shipping"].get(shipping_type.get("variable")) is None
        else "": ColumnWidths.PRICE,
        "ALTERNATE SHIPPING TYPE"
        if not store["shipping"].get(shipping_type.get("nested_type")) is None
        else "": ColumnWidths.NAME,
        "ALTERNATE SHIPPING COST"
        if not store["shipping"].get(shipping_type.get("nested_type")) is None
        and not store["shipping"][shipping_type["nested_type"]].get(
            next(
                shipping_type_.get("variable")
                for shipping_type_ in shipping_types
                if shipping_type_["type"]
                == store["shipping"][shipping_type["nested_type"]]["type"]
            )
        )
        is None
        else "": ColumnWidths.PRICE,
    }
    contents = [
        [
            store["name"],
            store["shipping"]["type"],
            store["shipping"].get(shipping_type.get("variable")) or "",
            store["shipping"][shipping_type["nested_type"]]["type"]
            if not store["shipping"].get(shipping_type.get("nested_type")) is None
            else "",
            store["shipping"][shipping_type["nested_type"]][
                next(
                    shipping_type_["variable"]
                    for shipping_type_ in shipping_types
                    if shipping_type_["type"]
                    == store["shipping"][shipping_type["nested_type"]]["type"]
                )
            ]
            if not store["shipping"].get(shipping_type.get("nested_type")) is None
            and not store["shipping"][shipping_type["nested_type"]].get(
                next(
                    shipping_type_.get("variable")
                    for shipping_type_ in shipping_types
                    if shipping_type_["type"]
                    == store["shipping"][shipping_type["nested_type"]]["type"]
                )
            )
            is None
            else "",
        ]
    ]
    valid_input = False
    while not valid_input:
        list_printer(headers, contents, index=False)
        val_in = input(
            f"'a' to accept or 'c' to cancel and return to previous menu > "
        ).lower()
        if val_in == "a":
            stores.append(store)
            valid_input = True
        if val_in == "c":
            valid_input = True
        else:
            print("That is not a valid selection")


def add_store(
    stores_with_item: List[dict],
    item_name: str,
    stores: List[dict],
    store_has_items: List[dict],
):
    in_val = None
    while in_val != "r":
        headers = {"": ColumnWidths.INDEX, "NAME": ColumnWidths.NAME}
        store_names = {store["store"] for store in stores_with_item}
        remaining_stores = [
            store_["name"] for store_ in stores if store_["name"] not in store_names
        ]
        print("select a store to add")
        list_printer(headers, [[store] for store in remaining_stores])
        print("\n'n' to add a new store\n'r' to return to the previous menu")

        in_val = input("> ").lower()
        if in_val.isdigit():
            int_val = int(in_val)
            if int_val < 1 or int_val > len(remaining_stores):
                print("That store does not exist")
                continue
            store_name = remaining_stores[int_val - 1]
            break_out = set_store_price(
                store_name, stores_with_item, item_name, store_has_items
            )

            if not break_out:
                store = next(store for store in stores if store_name == store["name"])
                if store["shipping"]["type"] == "dynamic" or (
                    store["shipping"].get("other_type")
                    and store["shipping"]["other_type"]["type"] == "dynamic"
                ):
                    add_dynamic_shipping_prices(store, item_name, store_has_items)

        elif in_val == "n":
            add_new_store(stores)
        elif in_val != "r":
            print("Invalid input")


def set_store_price(
    store_name: str,
    stores_with_item: List[dict],
    item_name: str,
    store_has_items: List[dict],
) -> bool:
    store_with_item = {
        "store": store_name,
        "item": item_name,
    }
    break_out = set_price(store_with_item)
    if not break_out:
        store_has_items.append(store_with_item)
        stores_with_item.append(store_with_item)
    return break_out


def add_dynamic_shipping_prices(store, item_name, store_has_items):
    combos_with_item = get_item_combinations(store_has_items, store, item_name)
    # add prices
    for combo in combos_with_item:
        combo_dict = {"items": combo}
        break_out = set_price(
            combo_dict, f"What is the shipping for {','.join(combo)}?"
        )
        if break_out == True:
            break
        else:
            store["shipping"]["combinations"].append(combo_dict)


def get_item_combinations(store_has_items, store, item_name) -> List[List[str]]:
    # gather new item combos
    store_items = [
        edge["item"] for edge in store_has_items if edge["store"] == store["name"]
    ]
    combos = allcombinations(store_items, len(store_items))
    combos_with_item = filter(lambda combo: item_name in combo, combos)
    if store["shipping"]["type"] == "free_above":
        min_price = store["shipping"]["minimum_price"]
        combos_with_item = [
            combo
            for combo in combos_with_item
            if sum(
                edge["price"]
                for edge in store_has_items
                if edge["item"] in combo and edge["store"] == store
            )
            < min_price
        ]
    return combos_with_item
