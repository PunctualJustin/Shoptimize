# objective:
#  item_store_indicator*{price} [+ item_store_shipping_indicator*{price}] | [+ store_shipping_indicator*{price}] =

# variables_format:
#  item_store_shipping_indicator = (0 || 1) shipping for items with flat rate or dynamic shipping fees
#  store_shipping_indicator = (0 || 1) shipping for item with
#  item_store_indicator = (0 || 1) indicates whether an item store combo is purchased

# constraints:
#  charge fixed rate shipping if item
#   item_store_indicator == item_store_shipping_indicator
#  make sure you are only buying 1 of an item
#   item_x_store_1_indicator + item_x_store_2_indicator + ... + item_x_store_n_indicator == 1
#  charge flat rate shipping
#   item_1_store_x_indicator*{price} + item_2_store_x_indicator*{price} + ... + item_n_store_x_indicator*{price} >= store_shipping_indicator * 1
#  check all the items for the store to see if there is free shipping over minimum
#   item_1_store_x_indicator*{price} + item_2_store_x_indicator*{price} + ... + item_n_store_x_indicator*{price} <= store_shipping_indicator * {minimum cost}
from loaders import initialize_items
from core.optimize import optimize
from report import report


def main():
    stores = initialize_items()
    problem = optimize(stores)
    report(stores, problem)
    pass


if __name__ == "__main__":
    main()
