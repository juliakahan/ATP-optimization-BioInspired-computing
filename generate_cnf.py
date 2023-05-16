from pysat.formula import CNF
import random


def generate_random_cnf(num_vars, num_clauses):
    # Generate random CNF formula with given number of variables and clauses
    cnf = CNF()

    for _ in range(num_clauses):
        clause = []
        for _ in range(random.randint(1, num_vars)):
            literal = random.randint(1, num_vars) * random.choice([-1, 1])
            clause.append(literal)
        cnf.append(clause)
    return cnf


if __name__ == "__main__":
    # Generate random CNF formulas with n variables and k clauses
    num_vars = 20
    num_clauses = 50
    # clause_length = 200

    for i in range(2):
        cnf = generate_random_cnf(num_vars, num_clauses)
        cnf.to_file(f"input_cnfs/cnf{i+11}.cnf")
