def report(stores, problem):
    for store in stores.values():
        for lp_variable in store.lp_variables.values():
            print(lp_variable.name, lp_variable.varValue)

    print("CONSTRAINTS".center(30, "="))
    for constraint_value in problem.constraints.values():
        print(constraint_value)
