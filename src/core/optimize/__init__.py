from pulp import LpVariable, LpProblem, lpSum, LpConstraint, const, PULP_CBC_CMD
from .objective import make_objective
from .constraints import get_constraints


def optimize(stores):
    problem = LpProblem(name="Shoptimize")
    problem += make_objective(stores)
    problem.constraints.update(get_constraints(stores))
    problem.solve(PULP_CBC_CMD(msg=0))
    return problem
