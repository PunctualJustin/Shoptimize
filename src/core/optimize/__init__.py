from pulp import LpVariable, LpProblem, lpSum, LpConstraint, const
from .objective import make_objective
from .constraints import get_constraints


def optimize(stores):
    problem = LpProblem(name="Shoptimize")
    problem += make_objective(stores)
    problem.constraints.update(get_constraints(stores))
    problem.solve()
    return problem
