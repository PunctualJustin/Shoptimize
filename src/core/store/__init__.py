from pulp import LpVariable, lpSum

from .shipping import Shipping
from .variable_map import LpVariableMap


class Store:
    def __init__(self, name, tax, exchange, shipping):
        self.name = name
        self.tax = tax + 1
        self.exchange = exchange
        self.lp_variables = LpVariableMap()
        self.shipping = Shipping(self, **shipping)
        self.items = {}

    def add_item(self, **kwargs):
        item = kwargs["item"]
        price = kwargs["price"]
        self.items[item] = price
        self.lp_variables.add(f"{self.name}_{item}")
        self.shipping.add_item(item)

    def __repr__(self) -> str:
        return self.name

    def get_objective(self):
        return (
            lpSum(
                [
                    self.lp_variables[f"{self.name}_{item_name}"]
                    * price
                    * self.tax
                    * self.exchange
                    + self.shipping.get_item_objective(item_name)
                    for item_name, price in self.items.items()
                ]
            )
            + self.shipping.get_objective()
        )
