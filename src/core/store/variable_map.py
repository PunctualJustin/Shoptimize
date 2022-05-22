from pulp import LpVariable


class LpVariableMap(dict):
    def __init__(self, store, *args, **kwargs):
        super(LpVariableMap, self).__init__(*args, **kwargs)
        self.store = store
        self.items = {}

    def add(self, item=None, shipping_type=None, combo=None):
        name = self.get_name(item, shipping_type, combo)
        if name is not None:
            self[name] = LpVariable(name, cat="Binary")

    def get_name(self, item=None, shipping_type=None, combo=None):
        if item is not None and shipping_type is None:
            return f"{self.store.name}_{item}"
        elif shipping_type == "free above":
            return f"{self.store.name}_shipping_minimum"
        elif shipping_type == "flat":
            return f"{self.store.name}_shipping"
        elif shipping_type in ["fixed", "distinct"] and item is not None:
            return f"{self.store.name}_{item}_shipping"
        elif shipping_type == "dynamic" and combo is not None:
            return f'{self.store.name}_{"_".join(combo)}_shipping'
        return None

    def get(self, name=None, item=None, shipping_type=None, combo=None):
        if name is None:
            name = self.get_name(item, shipping_type, combo)
        return super(LpVariableMap, self).get(name)
