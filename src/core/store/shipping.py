from pulp import lpSum


class Shipping:
    def __init__(self, store, **kwargs):
        self.store = store
        if kwargs["type"] not in [
            "free",
            "fixed",
            "distinct",
            "dynamic",
            "flat",
            "free above",
        ]:
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

        self.lp_variables.add(shipping_type=self.type_)

    def __repr__(self) -> str:
        return self.type_

    def get_shipping_variables(self):
        if self.type_ in ["flat", "free_above"]:
            return [self.lp_variables.get(shipping_type=self.type_)]
        elif self.type_ in ["fixed", "distinct"]:
            return [
                self.lp_variables.get(item=item, shipping_type=self.type_)
                for item in self.store.items
            ]
        elif self.type_ == "dynamic":
            return [
                self.lp_variables.get(shipping_type=self.type_, combo=combo["items"])
                for combo in self.combinations
            ]
        return []

    def add_item(self, item):
        self.lp_variables.add(item=item, shipping_type=self.type_)
        if self.type_ == "free above":
            self.other_type.add_item(item)

    def add_combo(self):
        for combo in self.combinations:
            self.lp_variables.add(shipping_type=self.type_, combo=combo["items"])

    def get_item_objective(self, item):
        if self.type_ == "fixed":
            return (
                self.lp_variables.get(item=item, shipping_type=self.type_)
                * self.price
                * self.store.tax
                * self.store.exchange
            )
        elif self.type_ == "distinct":
            return (
                self.lp_variables.get(item=item, shipping_type=self.type_)
                * self.store.shipping_prices[item]
                * self.store.tax
                * self.store.exchange
            )
        elif self.type_ == "free above":
            return self.other_type.get_item_objective(item)
        return 0

    def get_objective(self):
        if self.type_ == "flat":
            return (
                self.lp_variables.get(shipping_type=self.type_)
                * self.price
                * self.store.tax
                * self.store.exchange
            )
        elif self.type_ == "free above":
            return self.other_type.get_objective()
        elif self.type_ == "dynamic":
            return lpSum(
                self.lp_variables.get(shipping_type=self.type_, combo=combo["items"])
                * combo["price"]
                * self.store.tax
                * self.store.exchange
                for combo in self.combinations
            )
        return 0
