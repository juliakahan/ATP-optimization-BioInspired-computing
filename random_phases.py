import csv
import pysat.solvers
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

    cnf = CNF(from_file=file)
    clauses = cnf.clauses
    return clauses, num_vars, num_clauses


def solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name):
    solver = pysat.solvers.Solver(name=solver_name)
    for line in cnf_lines:
        solver.add_clause(line)
    if random_phases is not None:
        solver.set_phases(literals=random_phases)

    if solver.solve():
        model = solver.get_model()
        stats = solver.accum_stats()
        time = solver.time_accum()

        print(f"Model: {model}")
        print(f"Stats: {stats}")

        return model, stats, time
    else:
        print(f"Unsatisfiable for solver {solver_name}")
        return None, None, None


def generate_csv_table(cnf_files, solver_names):
    for solver_name in solver_names:
        with open(f"results_separate_solvers/{solver_name}_results.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            header = ["CNF File", "Random Phases", "Restarts", "Conflicts", "Decisions", "Propagations"]
            writer.writerow(header)
            for cnf_file in cnf_files:
                cnf_lines, num_vars, num_clauses = parse_open_cnf(cnf_file)
                random_phases = generate_random_phases(num_vars)
                model_with_random, stats_with_random, time_with_random = solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name)
                model_without_random, stats_without_random, time_without_random = solve(cnf_lines, num_vars, num_clauses, None, solver_name)
                if model_with_random is not None:
                    row = [cnf_file, random_phases, stats_with_random["restarts"], stats_with_random["conflicts"], stats_with_random["decisions"], stats_with_random["propagations"]]
                    writer.writerow(row)
                else:
                    row = [cnf_file, random_phases, "-", "-", "-", "-", "-"]
                    writer.writerow(row)


                if model_without_random is not None:
                    row = [cnf_file, "None", stats_without_random["restarts"], stats_without_random["conflicts"], stats_without_random["decisions"], stats_without_random["propagations"]]
                    writer.writerow(row)
                else:
                    row = [cnf_file, "None", "-", "-", "-", "-", "-"]
                    writer.writerow(row)


cnf_files = ['cnfs/special/dimacs1.cnf', 'cnfs/special/dimacs2.cnf', 'cnfs/special/dimacs3.cnf', 'cnfs/special/dimacs4.cnf', 'cnfs/special/dimacs5.cnf', 'cnfs/special/dimacs6.cnf', 'cnfs/special/dimacs7.cnf', 'cnfs/special/dimacs8.cnf', 'cnfs/randomly_generated/cnf.cnf', 'cnfs/randomly_generated/cnf2.cnf', 'cnfs/randomly_generated/cnf3.cnf', 'cnfs/randomly_generated/cnf4.cnf', 'cnfs/randomly_generated/cnf5.cnf', 'cnfs/randomly_generated/cnf6.cnf']
solver_names = ["g3", "m22", "mgh"]

generate_csv_table(cnf_files, solver_names)

# #
# cnf_lines, num_vars, num_clauses = parse_open_cnf('cnfs/special/dimacs7.cnf')
# random_phases = generate_random_phases(num_vars)
# print("Glucose: ")
# solve(cnf_lines, num_vars, num_clauses, random_phases, "g3")
# print("Minisat22: ")
# solve(cnf_lines, num_vars, num_clauses, random_phases, "m22")
# print("MinisatGH")
# solve(cnf_lines, num_vars, num_clauses, random_phases, "mgh")
#
