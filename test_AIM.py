from deap import base, creator, tools, algorithms
from pysat.solvers import Solver
import numpy as np
from pysat.solvers import Minisat22


# Ustal rozmiar populacji i liczbę iteracji algorytmu sztucznej immunizacji
POP_SIZE = 100
NUM_ITER = 100

# Ustal liczbę zmiennych w problemie SAT
NUM_VARS = 20

# Zdefiniuj funkcję oceny rozwiązania w problemie SAT
def evaluate_individual(individual):
    assumptions = []
    for i, value in enumerate(individual):
        if value:
            assumptions.append(i + 1)
        else:
            assumptions.append(-(i + 1))

    with Solver() as solver:
        solver.add_clause(assumptions)
        solved = solver.solve()
        if solved:
            return (1.0,)
        else:
            return (0.0,)

# Utwórz klasę Fitness, aby określić, jak oceniać rozwiązania
# creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))


# Utwórz klasę Individual, aby określić, jak reprezentować rozwiązania
creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

# Utwórz narzędzia do inicjalizacji populacji, krzyżowania, mutacji i oceny rozwiązań

# Tworzy obiekt narzędzi toolbox na podstawie klasy base.
# Toolbox z biblioteki DEAP. Narzędzie to jest używane do rejestrowania różnych funkcji i operacji, które będą używane w algorytmie ewolucyjnym.
toolbox = base.Toolbox()

# Rejestruje funkcję "attr_bool", która jest używana do inicjalizacji losowych wartości 0 lub 1 dla
# poszczególnych zmiennych w chromosomie (rozwiązaniu). Wykorzystuje funkcję np.random.randint z biblioteki NumPy,
# aby wygenerować losową liczbę całkowitą z zakresu od 0 do 1 (włącznie).
toolbox.register("attr_bool", np.random.randint, 0, 2)

# Rejestruje funkcję "individual", która służy do tworzenia pojedynczego osobnika (rozwiązania) w populacji.
# Używa funkcji tools.initRepeat, która powtarza operację zarejestrowaną jako "attr_bool"
# (czyli generuje losowe wartości 0 lub 1) dla określonej liczby zmiennych (NUM_VARS).
# Tworzony osobnik jest instancją klasy creator.Individual.
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=NUM_VARS)

# Rejestruje funkcję "population", która tworzy początkową populację osobników.
# Wykorzystuje funkcję tools.initRepeat, która tworzy listę osobników zarejestrowanych jako "individual".
# Cała populacja jest reprezentowana jako lista osobników.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Rejestruje funkcję "mate", która jest operatorem krzyżowania dwupunktowego (two-point crossover).
# Jest to jeden z operatorów krzyżowania dostępnych w bibliotece DEAP.
toolbox.register("mate", tools.cxTwoPoint)

# Rejestruje funkcję "mutate", która jest operatorem mutacji flip-bit. Ta mutacja losowo zmienia
# wartość pojedynczego bitu w chromosomie z 0 na 1 lub odwrotnie.
# Parametr indpb określa prawdopodobieństwo mutacji dla każdego bitu w chromosomie.
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

#Rejestruje funkcję "evaluate", która jest używana do oceny każdego osobnika w populacji.
#W tym przypadku, funkcja evaluate_individual jest zarejestrowana jako ocena.
#Funkcja ta przekształca osobnika w assumptions i używa ich do rozwiązania problemu SAT przy użyciu biblioteki PySAT.
toolbox.register("evaluate", evaluate_individual)


# Utwórz populację i uruchom algorytm sztucznej immunizacji
pop = toolbox.population(n=POP_SIZE)
best_solution = None

individual = pop[3]  # Przykładowy osobnik z populacji
fit = evaluate_individual(individual)  # Testuj funkcję evaluate_individual
print(fit)  # Sprawdź, czy zwraca poprawne wartości


for gen in range(NUM_ITER):
    offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        # print(len(ind.fitness.values), fit[0].type)
        ind.fitness.values = fit
        if best_solution is None or fit[0] > best_solution.fitness.values[0]:
            best_solution = ind
    pop = offspring

# Uzyskaj assumptions na podstawie najlepszego rozwiązania
assumptions = []
for i, value in enumerate(best_solution):
    if value:
        assumptions.append(i + 1)
    else:
        assumptions.append(-(i + 1))

print("Assumptions:", assumptions)

