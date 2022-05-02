from pulp import LpVariable, LpProblem, lpSum, LpConstraint, const


def make_objective(stores):
    return lpSum(store.get_objective() for store in stores.values())
