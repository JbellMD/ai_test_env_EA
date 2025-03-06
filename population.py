import random
import numpy as np

class Population:
    def __init__(self, size, individual_class):
        self.size = size
        self.individuals = [individual_class() for _ in range(size)]
        self.generation = 0
        self.best_fitness = -float('inf')
        self.best_individual = None

    def evaluate_fitness(self, fitness_function):
        # Evaluate fitness for all individuals in parallel
        for individual in self.individuals:
            individual.fitness = fitness_function(individual)
            if individual.fitness > self.best_fitness:
                self.best_fitness = individual.fitness
                self.best_individual = individual

    def select_parents(self, tournament_size=3):
        # Tournament selection
        parents = []
        while len(parents) < self.size:
            candidates = random.sample(self.individuals, tournament_size)
            winner = max(candidates, key=lambda x: x.fitness)
            parents.append(winner)
        return parents

    def create_next_generation(self, mutation_rate=0.1):
        parents = self.select_parents()
        next_generation = []
        while len(next_generation) < self.size:
            parent1, parent2 = random.sample(parents, 2)
            child = parent1.crossover(parent2)
            child.mutate(mutation_rate)
            next_generation.append(child)
        self.individuals = next_generation
        self.generation += 1

    def get_statistics(self):
        fitnesses = [ind.fitness for ind in self.individuals]
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'average_fitness': sum(fitnesses) / len(fitnesses),
            'std_fitness': np.std(fitnesses)
        }
