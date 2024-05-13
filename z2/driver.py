import numpy as np
import matplotlib.pyplot as plt
from z2.graph import Graph
from z2.genetic import GeneticAlgorithm
from z2.annealing import AnnealingAlgorithm


def read_cities(file):
    with open(file, 'r') as f:
        data = f.read().split()
    return data


def make_graph(cities):
    graph = Graph()
    for c1 in range(0, len(cities) - 3, 3):
        for c2 in range(3, len(cities), 3):
            dist = np.sqrt((float(cities[c1 + 1]) - float(cities[c2 + 1])) ** 2 +
                           (float(cities[c1 + 2]) - float(cities[c2 + 2])) ** 2)
            graph.set_adjacent(str(cities[c1]), str(cities[c2]), dist)
    return graph


def plot_route(route, cities):
    x, y = [], []
    for c in [*route]:
        c_idx = cities.index(c)
        x.append(float(cities[c_idx + 1]))
        y.append(float(cities[c_idx + 2]))
    plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    cities = read_cities('cities')
    graph = make_graph(cities)

    # Parameters tuning:
    generations = [1, 3, 10, 30, 100, 300]
    population_size = [10, 30, 100, 300]
    tournament_size = [1, 3, 10, 30, 100, 300]
    mutation_rate = [0.1, 0.3, 0.5, 0.7]
    elitism_rate = [0.1, 0.3, 0.5, 0.7]

    optimal_path = []
    path_cost = float('inf')
    for i in range(10):
        g = np.random.choice(generations)
        ps = np.random.choice(population_size)
        ts = np.random.choice(tournament_size)
        mt = np.random.choice(mutation_rate)
        er = np.random.choice(elitism_rate)

        ga_tsp = GeneticAlgorithm(generations=g, population_size=ps, tournament_size=ts,
                                  mutation_rate=mt, elitism_rate=er)
        op, pc = ga_tsp.optimize(graph)

        if pc < path_cost:
            path_cost = pc
            optimal_path = op
            print('Parameters:', g, ps, ts, mt, er)

    print(f'\nPath: {optimal_path}, Cost: {path_cost}\n')
    plot_route(optimal_path, cities)

    # Parameters tuning:
    temperatures = [100, 300, 1000, 3000, 5000, 10000]
    alpha = [0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
    stable = [100, 300, 1000, 3000]

    optimal_path = []
    path_cost = float('inf')
    for i in range(10):
        t = np.random.choice(temperatures)
        a = np.random.choice(alpha)
        s = np.random.choice(stable)

        aa_tsp = AnnealingAlgorithm(temperature=t, alpha=a, stable=s)
        op, pc = aa_tsp.optimize(graph)

        if pc < path_cost:
            path_cost = pc
            optimal_path = op
            print('Parameters:', t, a, s)

    print(f'\nPath: {optimal_path}, Cost: {path_cost}\n')
    plot_route(optimal_path, cities)
