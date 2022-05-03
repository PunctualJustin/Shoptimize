import sys
from typing import OrderedDict
from pulp import LpVariable, LpProblem, lpSum, LpConstraint, const

# this should be greater than the number of items that will be added to a store. It is used in a number constraints
#  where sys.maxsize*2+1 does not work correctly, nor does anything greater than this number
MAX_STORE_ITEMS = 10000000001


def get_constraints(stores):
    constraints = one_and_all_items(stores)
    constraints.update(flat_rate_constraints(stores))
    return constraints


def one_and_all_items(stores):
    items = {}
    for store in stores.values():
        for item in store.items:
            if item in items:
                items[item].append(store)
            else:
                items[item] = [store]
    constraints = {
        f"oaai_{store.id}_{item}": LpConstraint(
            lpSum(store.lp_variables[f"{store.name}_{item}"] for store in stores), rhs=1
        )
        for item, stores in items.items()
    }
    return constraints


def flat_rate_constraints(stores):
    constraints = {
        f"flat_rate_{store.id}": LpConstraint(
            (
                MAX_STORE_ITEMS * store.lp_variables[f"{store.name}_shipping"]
                - lpSum(
                    store.lp_variables[f"{store.id}_{item}"]
                    for item in store.items
                )
            ),
            const.LpConstraintGE,
            rhs=0,
        )
        for store in stores.values()
        if store.shipping.type_ == "flat"
    }
    return constraints
