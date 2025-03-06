class Evolution:
    def __init__(self, population_size, individual_class):
        self.population = Population(population_size, individual_class)

    def run(self, generations, fitness_function):
        for generation in range(generations):
            self.population.evaluate_fitness(fitness_function)
            self.population.select_parents()
            self.population.create_next_generation()
