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

SATS = ['cnfs/special/dimacs2.cnf','cnfs/special/dimacs8.cnf', 'cnfs/special/dimacs9.cnf']
unknown = ['cnfs/special/dimacs3.cnf', 'cnfs/special/dimacs7.cnf', 'cnfs/randomly_generated/cnf.cnf', 'cnfs/randomly_generated/cnf2.cnf', 'cnfs/randomly_generated/cnf3.cnf', 'cnfs/randomly_generated/cnf4.cnf', 'cnfs/randomly_generated/cnf5.cnf', 'cnfs/randomly_generated/cnf6.cnf']
UNSATS = ['cnfs/special/dimacs1.cnf', 'cnfs/special/dimacs4.cnf', 'cnfs/special/dimacs5.cnf', 'cnfs/special/dimacs6.cnf']

#TODO: modify method so that each of the solvers has the same set of random phases per file
def generate_csv_table(cnf_files, solver_names):
    phases = {}
    for solver_name in solver_names:
        with open(f"results_separate_solvers/{solver_name}_results.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            header = ["CNF File", "Random Phases", "Restarts", "Conflicts", "Decisions", "Propagations", "Variables", "Clauses",  "If should be SAT?"]
            writer.writerow(header)

            for cnf_file in cnf_files:
                cnf_lines, num_vars, num_clauses = parse_open_cnf(cnf_file)

                rand_ph = generate_random_phases(num_vars)
                if cnf_file not in phases:
                    phases[cnf_file] = rand_ph
                random_phases = phases[cnf_file]

                model_with_random, stats_with_random, time_with_random = solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name)
                model_without_random, stats_without_random, time_without_random = solve(cnf_lines, num_vars, num_clauses, None, solver_name)
                if model_with_random is not None:
                    row = [cnf_file, random_phases, stats_with_random["restarts"], stats_with_random["conflicts"], stats_with_random["decisions"], stats_with_random["propagations"], num_vars, num_clauses]
                    if cnf_file in SATS:
                        row.append("SAT")
                    elif cnf_file in UNSATS:
                        row.append("UNSAT")
                    else:
                        row.append("UNKNOWN")
                    writer.writerow(row)
                else:
                    row = [cnf_file, random_phases, "-", "-", "-", "-", "-", num_vars, num_clauses]
                    writer.writerow(row)

                if model_without_random is not None:
                    row = [cnf_file, "None", stats_without_random["restarts"], stats_without_random["conflicts"], stats_without_random["decisions"], stats_without_random["propagations"], num_vars, num_clauses]
                    writer.writerow(row)
                else:
                    row = [cnf_file, "None", "-", "-", "-", "-", "-",  num_vars, num_clauses]
                    writer.writerow(row)


cnf_files = ['cnfs/special/dimacs1.cnf', 'cnfs/special/dimacs2.cnf', 'cnfs/special/dimacs3.cnf', 'cnfs/special/dimacs4.cnf', 'cnfs/special/dimacs5.cnf', 'cnfs/special/dimacs6.cnf', 'cnfs/special/dimacs7.cnf', 'cnfs/special/dimacs8.cnf', 'cnfs/randomly_generated/cnf.cnf', 'cnfs/randomly_generated/cnf2.cnf', 'cnfs/randomly_generated/cnf3.cnf', 'cnfs/randomly_generated/cnf4.cnf', 'cnfs/randomly_generated/cnf5.cnf', 'cnfs/randomly_generated/cnf6.cnf']
solver_names = ["g3", "g4", "m22", "mgh", "lgl"]

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
#TODO: modify the method so that each solver has the same set of randomly generated random phases per file
def generate_csv_table_2(cnf_files, solver_names):
    #init the dictionary storing the random phases set for each file
    phases = {}
    for solver_name in solver_names:
        with open(f"results_multiple_randomphase_generation/{solver_name}_results.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            header = ["CNF File", "Random Phases", "Restarts", "Conflicts", "Decisions", "Propagations"]
            writer.writerow(header)
            for cnf_file in cnf_files:
                phases_tab = []

                cnf_lines, num_vars, num_clauses = parse_open_cnf(cnf_file)
                model_without_random, stats_without_random, time_without_random = solve(cnf_lines, num_vars, num_clauses, None, solver_name)
                if model_without_random is not None:
                    row = [cnf_file, "None", stats_without_random["restarts"], stats_without_random["conflicts"], stats_without_random["decisions"], stats_without_random["propagations"]]
                    if cnf_file in SATS:
                        row.append("SAT")
                    elif cnf_file in UNSATS:
                        row.append("UNSAT")
                    else:
                        row.append("UNKNOWN")
                    writer.writerow(row)
                    #create a tab of random phases for each file
                    for i in range(10):
                        #if the file is not in the dictionary, generate a new set of random phases
                        if cnf_file not in phases:
                            rand_ph = generate_random_phases(num_vars)
                            phases_tab.append(rand_ph)
                            # phases[cnf_file] = phases_tab
                        #if the file is in the dictionary, use the set of random phases already generated
                        else:
                            phases_tab = phases[cnf_file]
                            rand_ph = phases_tab[i]

                        random_phases = rand_ph
                        model_with_random, stats_with_random, time_with_random = solve(cnf_lines, num_vars, num_clauses, random_phases, solver_name)
                        if model_with_random is not None:
                            row = [cnf_file, random_phases, stats_with_random["restarts"], stats_with_random["conflicts"], stats_with_random["decisions"], stats_with_random["propagations"]]
                            if cnf_file in SATS:
                                row.append("SAT")
                            elif cnf_file in UNSATS:
                                row.append("UNSAT")
                            else:
                                row.append("UNKNOWN")
                            writer.writerow(row)
                        else:
                            row = [cnf_file, random_phases, "-", "-", "-", "-", "-"]
                            if cnf_file in SATS:
                                row.append("SAT")
                            elif cnf_file in UNSATS:
                                row.append("UNSAT")
                            else:
                                row.append("UNKNOWN")
                            writer.writerow(row)


                else:
                    row = [cnf_file, "None", "-", "-", "-", "-", "-"]
                    if cnf_file in SATS:
                        row.append("SAT")
                    elif cnf_file in UNSATS:
                        row.append("UNSAT")
                    else:
                        row.append("UNKNOWN")
                    writer.writerow(row)

                #add the random phases set to the dictionary
                phases[cnf_file] = phases_tab

generate_csv_table_2(cnf_files, solver_names)


def generate_csv_table_3(cnf_files, solver_names):
    with open(f"satisfiability_results_per_problem/results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        header = ["CNF File"]
        for solver_name in solver_names:
            header.append(solver_name)
        header.append("If should be SAT")
        writer.writerow(header)
        for cnf_file in cnf_files:
            cnf_lines, num_vars, num_clauses = parse_open_cnf(cnf_file)
            row = [cnf_file]
            for solver_name in solver_names:
                model_without_random, stats_without_random, time_without_random = solve(cnf_lines, num_vars, num_clauses, None, solver_name)
                if model_without_random is not None:
                    row.append("SAT")
                else:
                    row.append("UNSAT")
            if cnf_file in SATS:
                row.append("SAT")
            elif cnf_file in UNSATS:
                row.append("UNSAT")
            else:
                row.append("UNKNOWN")
            writer.writerow(row)

generate_csv_table_3(cnf_files, solver_names)