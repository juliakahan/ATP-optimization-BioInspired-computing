from math import sin, pi, gamma

import numpy as np


def cuckoo_search(n_nests, nd=15):
    # Współczynnik odkrycia
    pa = 0.25

    N_IterTotal = 1000

    # Granice szukania
    Lb = -5 * np.ones(nd)
    Ub = 5 * np.ones(nd)

    # Losowe parametry inicjalizacyjne
    nest = np.random.uniform(Lb, Ub, size=(n_nests, nd))
    fitness = 1e10 * np.ones(n_nests)

    f_min, best_nest, nest, fitness = get_best_nest(nest, nest, fitness)
    N_iter = 0

    # Początek iteracji
    for _ in range(N_IterTotal):
        # Generowanie nowych rozwiązań
        new_nest = get_cuckoos(nest, best_nest, Lb, Ub)
        f_new, best_nest, nest, fitness = get_best_nest(nest, new_nest, fitness)
        N_iter += n_nests

        new_nest = empty_nests(nest, Lb, Ub, pa)
        f_new, best_nest, nest, fitness = get_best_nest(nest, new_nest, fitness)
        N_iter += n_nests

        # Znalezienie najlepszego współczynnika
        if f_new < f_min:
            f_min = f_new

    # Wyświetlenie wyników
    print("Total number of iterations:", N_iter)
    print("fmin:", f_min)
    print("bestnest:", best_nest)


# Zwróć nowe kukułki wykorzystując Loty Levy'ego
def get_cuckoos(nest, best, Lb, Ub):
    # Loty Levy'ego
    n = nest.shape[0]

    # Współczynnik Levy'ego
    beta = 3 / 2
    sigma = (gamma(1 + beta) * sin(pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (
                1 / beta)

    for j in range(n):
        s = nest[j, :]
        u = np.random.randn(s.shape[0]) * sigma
        v = np.random.randn(s.shape[0])
        step = u / abs(v) ** (1 / beta)
        s = s + step * np.random.randn(s.shape[0])
        nest[j, :] = simple_bounds(s, Lb, Ub)

    return nest


# Znajdź obecne najlepsze gniazdo
def get_best_nest(nest, new_nest, fitness):
    # Ocena nowych rozwiązań
    for j in range(nest.shape[0]):
        f_new = f_obj(new_nest[j, :])
        if f_new <= fitness[j]:
            fitness[j] = f_new
            nest[j, :] = new_nest[j, :]

    # Odnalezienie obecnie najlepszego rozwiązania
    K = np.argmin(fitness)
    f_min = fitness[K]
    best = nest[K, :]

    return f_min, best, nest, fitness


# Zastąpienie istniejących gniazd nowymi
def empty_nests(nest, Lb, Ub, pa):
    # Część najgorszych gniazd jest odnaleziona z prawdopodobieństwem pa
    n = nest.shape[0]
    K = np.random.rand(*nest.shape) > pa
    step_size = np.random.rand() * (nest[np.random.permutation(n), :] - nest[np.random.permutation(n), :])
    new_nest = nest + step_size * K

    for j in range(new_nest.shape[0]):
        s = new_nest[j, :]
        new_nest[j, :] = simple_bounds(s, Lb, Ub)

    return new_nest


# Implementacja ograniczeń
def simple_bounds(s, Lb, Ub):
    # Dolne
    ns_tmp = s.copy()
    I = ns_tmp < Lb
    ns_tmp[I] = Lb[I]

    # Górne
    J = ns_tmp > Ub
    ns_tmp[J] = Ub[J]

    return ns_tmp


# Funkcja celu
def f_obj(u):
    return np.sum((u - 1) ** 2)


if __name__ == "__main__":
    cuckoo_search(25)