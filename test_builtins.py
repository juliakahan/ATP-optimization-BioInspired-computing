from pysat.solvers import Glucose3, Solver
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
    stats = solver.accum_stats()

    print(f'Mini sat result: {result}, stats: {stats}')
    return model


# minisat with changed restart method
def mini_sat2(clauses, restart_strategy="glue"):
    solver = Minisat22(use_timer=True)
    solver.restart_strategy = restart_strategy
    print(solver.restart_strategy)

    for clause in clauses:
        solver.add_clause(clause)

    result = solver.solve()
    time = solver.time_accum()
    model = solver.get_model()

    print(f'Mini sat with restart strategy: {restart_strategy} result: {result}, stats: {solver.accum_stats()}')
    return model


def glucose(clauses):
    solver = Glucose3(use_timer=True)

    for clause in clauses:
        solver.add_clause(clause)
    result = solver.solve()
    time = solver.time_accum()
    model = solver.get_model()
    stats = solver.accum_stats()

    print(f'Glucose result: {result},  stats: {stats}')
    return model


def the_same_model(name1, model1, name2, model2):
    print(f'Model form {name1} is the same as model from {name2}: {model1 == model2}')


def model_count(solver, clauses, vlimit=None, warm_start=False):
    with Solver(name=solver, bootstrap_with=clauses, use_timer=True, warm_start=warm_start) as oracle:
        count = 0
        while oracle.solve():
            model = oracle.get_model()
            if vlimit:
                model = model[:vlimit]
            # print(model)
            oracle.add_clause([-l for l in model])
            count += 1
        print(f'Model count for {solver}: {count} in {oracle.time_accum():.8f} seconds')


if __name__ == '__main__':
    # clauses_t = read_clauses('dimcas.cnf')
    clauses_t = read_clauses('input_cnfs/cnf13.cnf')

    # model_count("minisat22", clauses_t)
    # model_count("glucose3", clauses_t)

    model_minisat = mini_sat(clauses_t)
    model_glucose = glucose(clauses_t)

    the_same_model("MiniSat", model_minisat, "Glucose", model_glucose)

    # the_same_model("MiniSat", model_minisat, "MiniSat with restart method glue", model_glue)
    # the_same_model("MiniSat", model_minisat, "MiniSat with restart method luby", model_luby)
    # the_same_model("MiniSat", model_minisat, "MiniSat with restart method fixed", model_fixed)




