import math
import numpy as np


class GeneticAlgorithm:
    def __init__(self, generations=100, population_size=10,
                 tournament_size=4, mutation_rate=0.1,
                 elitism_rate=0.1):
        self.generations = generations
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.elitism_rate = elitism_rate

    def optimize(self, graph):
        population = self.__make_population(graph.get_vertices())
        elitism_offset = math.ceil(self.population_size * self.elitism_rate)

        if elitism_offset > self.population_size:
            raise ValueError('Elitism Rate must be in [0, 1]')

        for generation in range(self.generations):
            # print(f'Generation: {generation + 1}')
            # print(f'Population: {population}')

            new_population = []
            fitness = self.__compute_fitness(graph, population)
            # print(f'Fitness: {fitness}')
            fittest = np.argmin(fitness)

            # print(f'Fittest Route: {population[fittest]} ({fitness[fittest]})')

            if elitism_offset:
                elites = np.array(fitness).argsort()[:elitism_offset]     # sort by fitness, select by elitism factor
                [new_population.append(population[e]) for e in elites]    # append best to new population
            for gen in range(elitism_offset, self.population_size):
                parent1 = self.__tournament_selection(graph, population)  # select first parent from tournament
                parent2 = self.__tournament_selection(graph, population)  # select second parent from tournament
                offspring = self.__crossover(parent1, parent2)
                new_population.append(offspring)
            for gen in range(elitism_offset, self.population_size):
                new_population[gen] = self.__mutate(new_population[gen])

            population = new_population

            if self.__converged(population):
                # print('Converged to a local minima')
                break
        return population[fittest], fitness[fittest]

    def __make_population(self, graph_nodes):
        """Make population for graph_nodes

        :param: graph_nodes: list of graph nodes representing cities

        :return: population: list of string representing routes."""
        return [''.join(v for v in np.random.permutation(graph_nodes))
                for i in range(self.population_size)]

    def __compute_fitness(self, graph, population):
        """Compute fitness on given population (list of routes)

        :param: graph: graph representing cities
        :param: population: list of available routes

        :return: fitness_list: list of fitness for each route."""
        return [graph.get_path_cost(path) for path in population]

    def __tournament_selection(self, graph, population):
        """Perform tournament selection on population (list of routes)

        :param: graph: graph representing cities
        :param: population: list of available routes

        :return: tournament_winners: array of routes with the best fitness."""
        # choose random tournament_size elements from population
        tournament_contestants = np.random.choice(population, size=self.tournament_size)
        # compute fitness function over tournament population
        tournament_contestants_fitness = self.__compute_fitness(graph, tournament_contestants)
        return tournament_contestants[np.argmin(tournament_contestants_fitness)]

    def __crossover(self, parent1, parent2):
        """Preform crossover between two parents (string - path)

        :param: parent1: first parent (string1)
        :param: parent2: second parent (string2)

        :return: offspring: new string which was made from two parents."""
        offspring = ['' for allele in range(len(parent1))]
        index_low, index_high = self.__compute_low_high_indexes(parent1)

        # slice of parent1
        offspring[index_low:index_high + 1] = list(parent1)[index_low:index_high + 1]
        # remains of string after slicing
        offspring_available_index = list(range(index_low)) + list(range(index_high + 1, len(parent1)))
        for allele in parent2:                                        # loop through parent2
            if '' not in offspring:                                   # if there are no free places in string
                break
            if allele not in offspring:                               # if not in offspring of parent1
                offspring[offspring_available_index.pop(0)] = allele  # write to offspring
        return ''.join(v for v in offspring)                          # return string from offspring list

    def __mutate(self, genome):
        """Swap indices in genome (string) if randomly generated number less than mutation_rate

        :param: genome: string representing genome (route)

        :return: genome: string in which indices were swapped."""
        if np.random.random() < self.mutation_rate:  # generate random number less than mutation_rate
            index_low, index_high = self.__compute_low_high_indexes(genome)
            return self.__swap(index_low, index_high, genome)
        else:
            return genome

    def __compute_low_high_indexes(self, string):
        """Compute low and high indices in the given string

        :param string: string in which indices are computed

        :return index_low, index_high: tuple which contains low and high indices."""
        # choose random integer (no bigger than length of parent)
        index_low = np.random.randint(len(string) - 1)
        # choose random integer (from low to length)
        index_high = np.random.randint(index_low + 1, len(string))
        # difference between indices must be greater than half of length
        while index_high - index_low < math.ceil(len(string) // 2):
            try:
                index_low = np.random.randint(len(string))
                index_high = np.random.randint(index_low + 1, len(string))
            except ValueError:
                pass
        return index_low, index_high

    def __swap(self, index_low, index_high, string):
        """Swap letters by indices in string.

        :param index_low: low index in string
        :param index_high: high index in string
        :param string: string in which letters will be swapped

        :return string: string in which letters were swapped."""
        string = list(string)
        string[index_low], string[index_high] = string[index_high], string[index_low]
        return ''.join(string)

    def __converged(self, population):
        return all(genome == population[0] for genome in population)
