import json
from items import add_item
from items import edit_item

items_file = "inputs/items.json"

ITEMS = None
STORES = None
STORE_HAS_ITEMS = None

# todo: add delete store (from item)
# todo: change text from list to message when list is empty (e.g., when an item has no stores, display "item has not stores" instead of the list headings)


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
            edit_item(ITEMS[int_val - 1], ITEMS, STORE_HAS_ITEMS, STORES)
        if in_val == "a":
            add_item(ITEMS, STORE_HAS_ITEMS, STORES)
        elif in_val == "s":
            save()
            in_val = "q"
        elif in_val != "q":
            print("Invalid input")


if __name__ == "__main__":
    main()
