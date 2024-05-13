import warnings
import numpy as np


class AnnealingAlgorithm:
    def __init__(self, temperature=5000, alpha=0.99, stable=1500):
        self.temperature = temperature
        self.alpha = alpha
        self.stable = stable

    def optimize(self, graph):
        warnings.filterwarnings('ignore')

        best_solution = None
        best_fitness = float('inf')

        solution = self.__initial_solution(graph.get_vertices())
        fitness = self.__compute_fitness(graph, solution)
        current_step, accept = 0, 0
        while current_step < self.stable and self.temperature >= 0:
            new_solution = self.__mutate(solution)
            new_fitness = self.__compute_fitness(graph, new_solution)
            dE = new_fitness - fitness

            if np.random.rand() < np.exp(np.float128(-dE / self.temperature)):
                fitness = new_fitness
                solution = new_solution
                accept += 1

            if new_fitness < best_fitness:
                best_fitness = new_fitness
                best_solution = new_solution

            self.temperature *= self.alpha
            current_step += 1
        return best_solution, best_fitness

    def __initial_solution(self, graph_nodes):
        """Return string of random permutation of graph_nodes.

        :param: graph_nodes: list of graph nodes

        :return: string: string of random permutation of graph_nodes"""
        return ''.join(v for v in np.random.permutation(graph_nodes))

    def __compute_fitness(self, graph, path):
        return graph.get_path_cost(path)

    def __mutate(self, path):
        index_low, index_high = self.__compute_low_high_indexes(path)
        return self.__swap(index_low, index_high, path)

    def __compute_low_high_indexes(self, string):
        index_low = np.random.randint(len(string) - 1)
        index_high = np.random.randint(index_low + 1, len(string))
        return index_low, index_high

    def __swap(self, index_low, index_high, string):
        string = list(string)
        string[index_low], string[index_high] = string[index_high], string[index_low]
        return ''.join(string)
