import ray
import numpy as np
from typing import List

@ray.remote
class ParallelExecutor:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def evaluate_fitness(self, individuals: List[Individual], fitness_function):
        results = []
        batch_size = min(len(individuals), ray.available_resources().get('CPU', 1))
        
        for i in range(0, len(individuals), batch_size):
            batch = individuals[i:i+batch_size]
            futures = [self._evaluate_individual.remote(ind, fitness_function) 
                      for ind in batch]
            results.extend(ray.get(futures))
        
        return results

    @ray.remote
    def _evaluate_individual(self, individual, fitness_function):
        for attempt in range(self.max_retries):
            try:
                return fitness_function(individual)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                continue

    def shutdown(self):
        ray.shutdown()
