import pysat.solvers
from pysat.solvers import Minisat22, Solver
from pysat.solvers import SolverNames
import random
from pysat.formula import CNF


def generate_random_phases(num_vars):
    return [random.choice([1, -1]) * (i + 1) for i in range(num_vars)]


def parse_open_cnf(file):
    with open(file, "r") as cnf_file:
        header = [line for line in cnf_file if line.startswith('p')]
    header = str(header)[2:]
    header = header[:-4]
    header = str(header).split(" ")
    num_vars = int(header[2])
    num_clauses = int(header[3])
    print(num_vars, num_clauses)

    cnf = CNF(from_file=file)
    clauses = cnf.clauses
    return clauses, num_vars, num_clauses

def solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name):
    solver = Solver(name=solver_name)
    # print(cnf_lines)
    for line in cnf_lines:
        solver.add_clause(line)
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
        return model2, stats, time
    else:
        print("Nie znaleziono rozwiązania bez podania wartości.")
        solver.delete()
        return None, None, None


cnf_lines, num_vars, num_clauses = parse_open_cnf('cnfs/special/dimacs7.cnf')
random_phases = generate_random_phases(num_vars)
print("Glucose: ")
solve(cnf_lines, num_vars, num_clauses, random_phases, "g3")
print("Minisat22: ")
solve(cnf_lines, num_vars, num_clauses, random_phases, "m22")
print("MinisatGH")
solve(cnf_lines, num_vars, num_clauses, random_phases, "mgh")

#Benchmark for glucose3
#wez wszystkie problemy,





#stworzyć benchmark: generowac pliki csv dla minisat, glucose, jeszcze innego
#TODO: benchmark ze względu na pliki cnf, benchmark ze względu na rodzaj solvera
