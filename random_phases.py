import pysat.solvers
from pysat.solvers import Minisat22, Solver
from pysat.solvers import SolverNames
import random
import numpy as np
from pysat.formula import CNF

# #
# # def generate_random_assumptions(num_vars):
#     return [random.choice([1, -1]) * (i + 1) for i in range(num_vars)]

def generate_random_phases(num_vars):
    return [random.choice([1, -1]) * (i + 1) for i in range(num_vars)]

def parse_open_cnf(file):
    with open(file, "r") as cnf_file:
        cnf_lines = cnf_file.readlines()
    header = cnf_lines[0].split()
    num_vars = int(header[2])
    num_clauses = int(header[3])
    return cnf_lines, num_vars, num_clauses

def solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name):
    solver = Solver(name=solver_name)
    for line in cnf_lines[1:]:
        clause = [int(x) for x in line.split()[:-1]]
        solver.add_clause(clause)
    if random_phases is not None:
        solver.set_phases(random_phases)
        if solver.solve():
            time = solver.time_accum()
            model1 = solver.get_model()
            stats = solver.accum_stats()
            print(f'Losowo wygenerowane wartości: {random_phases}')
            print(f"Rozwiązanie z podaniem losowych wartości znalezione: {model1}")
            print(f"Statystyki:{stats}")
            print(f"Czas: {time}")
        else:
            print("Nie znaleziono rozwiązania z podaniem losowych wartości.")

    if solver.solve():
        time = solver.time_accum()
        model2 = solver.get_model()
        stats = solver.accum_stats()
        print(f"Rozwiązanie bez podania wartości znalezione: {model2}")
        print(f"Statystyki:{stats}")
        print(f"Czas: {time}")
        solver.delete()
        return model2
    else:
        print("Nie znaleziono rozwiązania bez podania wartości.")
        solver.delete()
        return None


cnf_lines, num_vars, num_clauses = parse_open_cnf("dimacs.cnf")
random_phases = generate_random_phases(num_vars)
solve(cnf_lines, num_vars, num_clauses, random_phases, "g3")
solve(cnf_lines, num_vars, num_clauses, random_phases, "m22")
