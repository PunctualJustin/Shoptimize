from pulp import LpVariable, lpSum


class Store:
    def __init__(self, ID, Name, shipping, shipping_variable):
        self.id = ID
        self.name = Name
        self.shipping = shipping
        self.shipping_var = (
            int(shipping_variable, 10) if shipping_variable.isdigit() else 0
        )
        self.items = []
        self.lp_variables = {}
        if self.shipping == "flat":
            self.__add_lp_variable(f"{self.id}_shipping")

    def add_item(self, item, price):
        self.items.append({"id": item.id, "price": price, "item": item})
        self.__add_lp_variable(f"{self.id}_{item.id}")
        if self.shipping == "fixed":
            self.__add_lp_variable(f"{self.id}_{item.id}_shipping")

    def __add_lp_variable(self, name):
        self.lp_variables[name] = LpVariable(name, cat="Binary")
        pass

    def __get_item_objective(self, item):
        cost = self.lp_variables[f"{self.id}_{item['id']}"] * item["price"]
        if self.shipping == "fixed":
            return (
                cost
                + self.lp_variables[f"{self.id}_{item['id']}_shipping"]
                * self.shipping_var
            )
        return cost

    def get_objective(self):
        cost = lpSum([self.__get_item_objective(item) for item in self.items])
        if self.shipping == "flat":
            return lpSum(
                [cost, self.lp_variables[f"{self.id}_shipping"] * self.shipping_var]
            )
        return cost
