from pulp import lpSum, LpConstraint, const

# this should be greater than the number of items that will be added to a store. It is used in a number constraints
#  where sys.maxsize*2+1 does not work correctly, nor does anything greater than this number
MAX_STORE_ITEMS = 10000000001


def get_constraints(stores):
    constraints = one_and_all_items(stores)
    for store in stores.values():
        make_shipping_constraints(constraints, store, store.shipping)
    return constraints


def make_shipping_constraints(constraints, store, shipping, modifier=0):
    if shipping.type_ == "flat":
        flat_rate_constraint(constraints, store, modifier)
    elif shipping.type_ == "fixed":
        fixed_rate_constraint(constraints, store, modifier)
    elif shipping.type_ == "dynamic":
        dynamic_rate_constraint(constraints, store, shipping, modifier)
    elif shipping.type_ == "free above":
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


def dynamic_rate_constraint(constraints, store, shipping, modifier):
    constraints.update(
        {
            f"dynamic_{store.name}_{'_'.join(combo['items'])}": LpConstraint(
                (
                    lpSum(
                        store.lp_variables[f"{store.name}_{item}"]
                        for item in combo["items"]
                    )
                    - lpSum(
                        store.lp_variables[
                            f"{store.name}_{'_'.join(constraint_combo['items'])}_shipping"
                        ]
                        * len(
                            list(
                                filter(
                                    lambda inner_item: inner_item in combo["items"],
                                    constraint_combo["items"],
                                )
                            )
                        )
                        for constraint_combo in shipping.combinations
                        if any(
                            item in combo["items"] for item in constraint_combo["items"]
                        )
                    )
                    - modifier * MAX_STORE_ITEMS
                ),
                const.LpConstraintLE,
                rhs=0,
            )
            for combo in shipping.combinations
        }
    )
    constraints[f"dynamic_{store.name}_control"] = LpConstraint(
        lpSum(shipping.get_shipping_variables()) + modifier,
        const.LpConstraintLE,
        rhs=1,
    )


def free_above_constraint(constraints, store):
    constraints[f"free_above_{store.name}"] = LpConstraint(
        (
            lpSum(
                store.lp_variables[f"{store.name}_{item_name}"] * price
                for item_name, price in store.items.items()
            )
            - store.lp_variables[f"{store.name}_shipping_minimum"]
            * store.shipping.minimum_price
        ),
        const.LpConstraintGE,
        rhs=0,
    )
    constraints.update(
        {
            f"free_above_{store.name}_{variable.name}": LpConstraint(
                variable + store.lp_variables[f"{store.name}_shipping_minimum"],
                const.LpConstraintLE,
                rhs=1,
            )
            for variable in store.shipping.other_type.get_shipping_variables()
        }
    )
    make_shipping_constraints(
        constraints,
        store,
        store.shipping.other_type,
        store.lp_variables[f"{store.name}_shipping_minimum"],
    )
