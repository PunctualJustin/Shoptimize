from pulp import LpVariable


class LpVariableMap(dict):
    def add(self, name):
        if name is not None:
            self[name] = LpVariable(name, cat="Binary")
