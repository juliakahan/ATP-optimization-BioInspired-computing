import random
from pysat.solvers import Minisat22

class Particle:
    def __init__(self, num_variables):
        self.position = [random.choice([-1, 1]) * (i + 1) for i in range(num_variables)]
        self.velocity = [random.uniform(-1, 1) for _ in range(num_variables)]
        self.best_position = self.position.copy()

def evaluate_assumptions(assumptions):
    # Funkcja celu - ocena jakości założeń
    # Im wyższa wartość zwracana, tym lepsze są założenia
    return len(assumptions)  # Przykładowa ocena - liczba założeń

def update_particle_velocity(particle, global_best_position, omega, c1, c2):
    for i in range(len(particle.velocity)):
        r1 = random.random()
        r2 = random.random()
        cognitive_component = c1 * r1 * (particle.best_position[i] - particle.position[i])
        social_component = c2 * r2 * (global_best_position[i] - particle.position[i])
        particle.velocity[i] = omega * particle.velocity[i] + cognitive_component + social_component

def update_particle_position(particle):
    for i in range(len(particle.position)):
        if random.random() < sigmoid(particle.velocity[i]):
            particle.position[i] *= -1

def sigmoid(x):
    return 1 / (1 + pow(2.71828, -x))

def pso_sat_solver(num_particles, num_iterations, num_variables):
    particles = [Particle(num_variables) for _ in range(num_particles)]
    global_best_position = particles[0].position.copy()
    global_best_fitness = evaluate_assumptions(global_best_position)

    for _ in range(num_iterations):
        for particle in particles:
            fitness = evaluate_assumptions(particle.position)
            if fitness > evaluate_assumptions(particle.best_position):
                particle.best_position = particle.position.copy()
                if fitness > global_best_fitness:
                    global_best_position = particle.position.copy()
                    global_best_fitness = fitness

            update_particle_velocity(particle, global_best_position, omega=0.5, c1=2, c2=2)
            update_particle_position(particle)

    return global_best_position

# Przykładowe użycie
num_particles = 50  # liczba cząsteczek w roju
num_iterations = 100  # liczba iteracji w algorytmie PSO
num_variables = 50  # liczba zmiennych w SAT problemie

best_assumptions = pso_sat_solver(num_particles, num_iterations, num_variables)

# Przekształcenie założeń do formatu [1, -2, 4, 5]
assumptions = [variable for variable in best_assumptions if variable > 0]

# Wykorzystanie uzyskanych założeń w solverze MiniSat
solver = Minisat22()


# Otwieranie pliku CNF
with open("/Users/juliakahan/PycharmProjects/pythonProject6/input_cnfs/cnf11.cnf", "r") as cnf_file:
    cnf_lines = cnf_file.readlines()

# # Usuwanie komentarzy
# cnf_lines = [line for line in cnf_lines if not line.startswith("c")]

# Parsowanie nagłówka
header = cnf_lines[0].split()
num_vars = int(header[2])
num_clauses = int(header[3])

# Inicjalizowanie solvera

# Dodawanie klauzul
for line in cnf_lines[1:]:
    clause = [int(x) for x in line.split()[:-1]]
    solver.add_clause(clause)

# Rozwiązywanie SAT problemu
if solver.solve(assumptions=assumptions):
    print("Rozwiązanie znalezione:")
    model = solver.get_model()
    print(model)
else:
    print("Nie znaleziono rozwiązania.")
