import imp
from pulp import LpVariable, lpSum

from .variable_map import LpVariableMap


class Shipping:
    init_lp_variable = (
        lambda **kwargs: f"{kwargs['store']}_{kwargs['shipping_type_indicator']}"
    )

    variable_types = {
        "free": {},
        "fixed": {
            "item": lambda **kwargs: f"{kwargs['store']}_{kwargs['item']}_shipping"
        },
        "flat": {
            "init": lambda **kwargs: Shipping.init_lp_variable(
                shipping_type_indicator="shipping", **kwargs
            )
        },
        "free above": {
            "init": lambda **kwargs: Shipping.init_lp_variable(
                shipping_type_indicator="shipping_minimum", **kwargs
            )
        },
    }

    def __init__(self, store, **kwargs):
        self.store = store
        if kwargs["type"] not in Shipping.variable_types:
            raise Exception(f'unknown shipping type {kwargs["type"]}')
        self.type_ = kwargs["type"]
        self.lp_variables = self.store.lp_variables
        # todo: add try/except with sensible error message on keyerror
        if self.type_ in ("flat", "fixed"):
            self.price = kwargs["price"]
        elif self.type_ == "free above":
            self.minimum_price = kwargs["minimum_price"]
            self.other_type = Shipping(store, **kwargs["other_type"])

        self.lp_variables.add(self.get_lp_variable("init"))

    def __repr__(self) -> str:
        return self.type_

    def get_shipping_variables(self):
        if self.type_ in ['flat', 'free_above']:
            return [self.lp_variables[self.get_lp_variable('init')]]
        elif self.type_ == 'fixed':
            return [self.lp_variables[self.get_lp_variable('item', item=item)] for item in self.store.items]
        return []
    
    def get_lp_variable(self, variable_type, **kwargs):
        return self.variable_types[self.type_].get(variable_type, lambda **x: None)(
            store=self.store.name, **kwargs
        )

    def add_item(self, item):
        self.lp_variables.add(self.get_lp_variable("item", item=item))
        if self.type_ == "free above":
            self.other_type.add_item(item)

    def get_item_objective(self, item):
        if self.type_ == "fixed":
            return (
                self.lp_variables[self.get_lp_variable("item", item=item)] * self.price
            )
        elif self.type_ == "free above":
            return self.other_type.get_item_objective(item)
        return 0

    def get_objective(self):
        if self.type_ == "flat":
            return self.lp_variables[self.get_lp_variable("init")] * self.price
        elif self.type_ == "free above":
            return self.other_type.get_objective()
        return 0
