from pysat.solvers import Glucose3
from pysat.solvers import Minisat22
from pysat.formula import CNF


def read_clauses(filename):
    cnf = CNF(from_file=filename)
    return cnf.clauses


def mini_sat(clauses):
    solver = Minisat22(use_timer=True)

    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()
    time = solver.time_accum()
    model = solver.get_model()

    print(f'Mini sat result: {result} in {time:.11f} seconds')
    return model


# minisat with changed restart method
def mini_sat2(clauses, restart_strategy="glue"):
    solver = Minisat22(use_timer=True)
    solver.restart_strategy = restart_strategy
    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()
    time = solver.time_accum()
    model = solver.get_model()

    print(f'Mini sat with restart strategy: {restart_strategy} result: {result} in {time:.11f} seconds')
    return model


def glucose(clauses):
    solver = Glucose3(use_timer=True)
    for clause in clauses:
        solver.add_clause(clause)
    result = solver.solve()
    time = solver.time_accum()
    model = solver.get_model()

    print(f'Glucose result: {result} in {time:.8f} seconds')
    return model


def the_same_model(name1, model1, name2, model2):
    print(f'Model form {name1} is the same as model from {name2}: {model1 == model2}')


if __name__ == '__main__':
    clauses_t = read_clauses('dimcas.cnf')

    # if solvers return the same model
    model_minisat = mini_sat(clauses_t)
    model_glucose = glucose(clauses_t)

    model_glue = mini_sat2(clauses_t, "glue")
    model_luby = mini_sat2(clauses_t, "luby")
    model_fixed = mini_sat2(clauses_t, "fixed")

    print('----------------------------------------------')
    the_same_model("MiniSat", model_minisat, "Glucose", model_glucose)
    the_same_model("MiniSat", model_minisat, "MiniSat with restart method glue", model_glue)
    the_same_model("MiniSat", model_minisat, "MiniSat with restart method luby", model_luby)
    the_same_model("MiniSat", model_minisat, "MiniSat with restart method fixed", model_fixed)




