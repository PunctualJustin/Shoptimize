import sys
from typing import OrderedDict
from pulp import LpVariable, LpProblem, lpSum, LpConstraint, const

# this should be greater than the number of items that will be added to a store. It is used in a number constraints
#  where sys.maxsize*2+1 does not work correctly, nor does anything greater than this number
MAX_STORE_ITEMS = 10000000001


def get_constraints(stores):
    constraints = one_and_all_items(stores)
    for store in stores.values():
        make_shipping_constraints(constraints, store, store.shipping.type_)
    return constraints


def make_shipping_constraints(constraints, store, shipping, modifier = 0):
    if shipping == "flat":
        flat_rate_constraint(constraints, store, modifier)
    elif shipping == "fixed":
        fixed_rate_constraint(constraints, store, modifier)
    elif shipping == "free above":
        free_above_constraint(constraints, store)


def one_and_all_items(stores):
    items = {}
    for store in stores.values():
        for item in store.items:
            if item in items:
                items[item].append(store)
            else:
                items[item] = [store]
    constraints = {
        f"oaai_{store.name}_{item}": LpConstraint(
            lpSum(store.lp_variables[f"{store.name}_{item}"] for store in stores), rhs=1
        )
        for item, stores in items.items()
    }
    return constraints


def flat_rate_constraint(constraints, store, modifier):
    constraints[f"flat_rate_{store.name}"] = LpConstraint(
        (
            MAX_STORE_ITEMS * store.lp_variables[f"{store.name}_shipping"]
            - lpSum(store.lp_variables[f"{store.name}_{item}"] for item in store.items)
            + MAX_STORE_ITEMS * modifier
        ),
        const.LpConstraintGE,
        rhs=0,
    )


def fixed_rate_constraint(constraints, store, modifier):
    constraints.update(
        {
            f"fixed_rate_{store.name}_{item}": LpConstraint(
                (
                    store.lp_variables[f"{store.name}_{item}"]
                    - store.lp_variables[f"{store.name}_{item}_shipping"]
                    - modifier
                ),
                rhs=0,
            )
            for item in store.items
        }
    )


def free_above_constraint(constraints, store):
    constraints[f"free_above_{store.name}"] = LpConstraint(
        (
            lpSum(store.lp_variables[f"{store.name}_{item_name}"]*price for item_name, price in store.items.items())
            - store.lp_variables[f"{store.name}_shipping_minimum"]*store.shipping.minimum_price
        ),
        const.LpConstraintGE,
        rhs=0,
    )
    constraints.update({f"free_above_{store.name}_{variable.name}": LpConstraint(
        variable + store.lp_variables[f"{store.name}_shipping_minimum"],
        const.LpConstraintLE,
        rhs=1,
    ) for variable in store.shipping.other_type.get_shipping_variables()})
    make_shipping_constraints(constraints, store, store.shipping.other_type.type_, store.lp_variables[f"{store.name}_shipping_minimum"])
