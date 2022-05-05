from pulp import lpSum


class Shipping:
    init_lp_variable = (
        lambda **kwargs: f"{kwargs['store']}_{kwargs['shipping_type_indicator']}"
    )

    variable_name_formats = {
        "free": {},
        "fixed": {
            "item": lambda *args, **kwargs: f"{kwargs['store']}_{kwargs['item']}_shipping"
        },
        "flat": {
            "init": lambda *args, **kwargs: Shipping.init_lp_variable(
                shipping_type_indicator="shipping", **kwargs
            )
        },
        "free above": {
            "init": lambda *args, **kwargs: Shipping.init_lp_variable(
                shipping_type_indicator="shipping_minimum", **kwargs
            )
        },
        "dynamic": {
            "combo": lambda *args, **kwargs: f'{kwargs["store"]}_{"_".join(args)}_shipping'
        },
    }

    def __init__(self, store, **kwargs):
        self.store = store
        if kwargs["type"] not in Shipping.variable_name_formats:
            raise Exception(f'unknown shipping type {kwargs["type"]}')
        self.type_ = kwargs["type"]
        self.lp_variables = self.store.lp_variables
        # todo: add try/except with sensible error message on keyerror
        if self.type_ in ("flat", "fixed"):
            self.price = kwargs["price"]
        elif self.type_ == "free above":
            self.minimum_price = kwargs["minimum_price"]
            self.other_type = Shipping(store, **kwargs["other_type"])
        if self.type_ == "dynamic":
            self.combinations = kwargs["combinations"]
            self.add_combo()

        self.lp_variables.add(self.get_lp_variable_name("init"))

    def __repr__(self) -> str:
        return self.type_

    def get_shipping_variables(self):
        if self.type_ in ["flat", "free_above"]:
            return [self.lp_variables[self.get_lp_variable_name("init")]]
        elif self.type_ == "fixed":
            return [
                self.lp_variables[self.get_lp_variable_name("item", item=item)]
                for item in self.store.items
            ]
        elif self.type_ == "dynamic":
            return [
                self.lp_variables[self.get_lp_variable_name("combo", *combo["items"])]
                for combo in self.combinations
            ]
        return []

    def get_lp_variable_name(self, variable_type, *args, **kwargs):
        return self.variable_name_formats[self.type_].get(
            variable_type, lambda **x: None
        )(*args, store=self.store.name, **kwargs)

    def add_item(self, item):
        self.lp_variables.add(self.get_lp_variable_name("item", item=item))
        if self.type_ == "free above":
            self.other_type.add_item(item)

    def add_combo(self):
        for combo in self.combinations:
            self.lp_variables.add(self.get_lp_variable_name("combo", *combo["items"]))

    def get_item_objective(self, item):
        if self.type_ == "fixed":
            return (
                self.lp_variables[self.get_lp_variable_name("item", item=item)]
                * self.price
            )
        elif self.type_ == "free above":
            return self.other_type.get_item_objective(item)
        return 0

    def get_objective(self):
        if self.type_ == "flat":
            return self.lp_variables[self.get_lp_variable_name("init")] * self.price
        elif self.type_ == "free above":
            return self.other_type.get_objective()
        elif self.type_ == "dynamic":
            return lpSum(
                self.lp_variables[self.get_lp_variable_name("combo", *combo["items"])]
                * combo["price"]
                for combo in self.combinations
            )
        return 0
