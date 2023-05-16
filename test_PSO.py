from pysat.solvers import Minisat22
from pysat.formula import CNF
import random
from pyswarms.single.global_best import GlobalBestPSO
from pyswarms.single.local_best import LocalBestPSO


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

# create 10 random instances with 10 variables and 20 clauses each
instances = [generate_random_cnf(10, 20) for i in range(10)]

# Generate 10 random CNF formulas with 20 variables and 50 clauses
# for i in range(10):
#     cnf = generate_random_cnf(20, 50)
#     cnf.to_file(f"cnf{i}.cnf")

def objective_function(restart):
    # perform tests for given restart strategy and return average time per instance
    average_time = 0
    for instance in instances:
        solver = Minisat22()
        solver.restart_first = restart
        solver.solve(instance)
        average_time += solver.time()
    return average_time / len(instances)

lower_bound = 100
upper_bound = 10000


# define the lower,upper bounds for restart strategy, and the search space
bounds = (lower_bound, upper_bound)
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

# run PSO
optimizer = GlobalBestPSO(n_particles=10, dimensions=1, options=options)
print(optimizer.swarm.position)

# # wykonujemy optymalizację

# stats = optimizer.optimize(objective_function, iters=100)





