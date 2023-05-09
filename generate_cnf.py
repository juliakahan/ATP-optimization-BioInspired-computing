from pysat.formula import CNF
import random

def generate_random_cnf(num_vars, num_clauses):
    # Generate random CNF formula with given number of variables and clauses
    cnf = CNF()
    for i in range(num_clauses):
        clause = []
        for j in range(random.randint(1, num_vars)):
            literal = random.randint(1, num_vars) * random.choice([-1, 1])
            clause.append(literal)
        cnf.append(clause)
    return cnf

# Generate 10 random CNF formulas with 20 variables and 50 clauses
for i in range(10):
    cnf = generate_random_cnf(20, 50)
    cnf.to_file(f"cnf{i}.cnf")
