import random
import numpy as np

class Population:
    def __init__(self, size, individual_class):
        self.size = size
        self.individuals = [individual_class() for _ in range(size)]
        self.generation = 0
        self.best_fitness = -float('inf')
        self.best_individual = None
        self.elitism_count = max(1, int(0.1 * size))  # Preserve top 10%
        self.diversity_threshold = 0.7  # Minimum population diversity

    def evaluate_fitness(self, fitness_function):
        # Evaluate fitness with parallel processing
        fitnesses = ParallelExecutor().evaluate_fitness(self.individuals, fitness_function)
        for ind, fitness in zip(self.individuals, fitnesses):
            ind.fitness = fitness
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_individual = ind

    def select_parents(self, tournament_size=3):
        # Tournament selection with diversity consideration
        parents = []
        while len(parents) < self.size:
            candidates = random.sample(self.individuals, tournament_size)
            winner = max(candidates, key=lambda x: x.fitness * self._diversity_score(x))
            parents.append(winner)
        return parents

    def _diversity_score(self, individual):
        # Calculate diversity score based on similarity to population
        similarity = sum(ind.similarity(individual) for ind in self.individuals) / self.size
        return 1 - similarity

    def create_next_generation(self, mutation_rate=0.1):
        # Create new generation with elitism and diversity maintenance
        next_generation = []
        
        # Preserve elite individuals
        elite = sorted(self.individuals, key=lambda x: x.fitness, reverse=True)[:self.elitism_count]
        next_generation.extend(elite)
        
        # Create remaining population
        parents = self.select_parents()
        while len(next_generation) < self.size:
            parent1, parent2 = random.sample(parents, 2)
            child = parent1.crossover(parent2)
            child.mutate(self._adaptive_mutation_rate())
            next_generation.append(child)
            
        self.individuals = next_generation
        self.generation += 1

    def _adaptive_mutation_rate(self):
        # Adjust mutation rate based on population diversity
        diversity = self._calculate_population_diversity()
        if diversity < self.diversity_threshold:
            return min(0.5, 0.1 + (1 - diversity))  # Increase mutation rate
        return 0.1  # Default rate

    def _calculate_population_diversity(self):
        # Calculate population diversity score
        return sum(self._diversity_score(ind) for ind in self.individuals) / self.size

    def get_statistics(self):
        fitnesses = [ind.fitness for ind in self.individuals]
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'average_fitness': sum(fitnesses) / len(fitnesses),
            'std_fitness': np.std(fitnesses),
            'diversity': self._calculate_population_diversity()
        }