import argparse
import json
from evolution import Evolution
from population import Population
from individual import Individual

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Run Evolutionary AI Model')
parser.add_argument('--population_size', type=int, default=100, help='Population size')
parser.add_argument('--generations', type=int, default=100, help='Number of generations')
parser.add_argument('--mutation_rate', type=float, default=0.1, help='Mutation rate')
parser.add_argument('--output', type=str, default='results.json', help='Output file for results')

# Fitness function example
def fitness_function(individual):
    # Implement your specific fitness evaluation here
    return individual.evaluate()

# Main execution
if __name__ == '__main__':
    args = parser.parse_args()
    evolution = Evolution(args.population_size, Individual)
    results = []

    for gen in range(args.generations):
        evolution.run(fitness_function)
        stats = evolution.population.get_statistics()
        results.append(stats)
        print(f'Generation {gen}: Best Fitness = {stats["best_fitness"]}')

    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f)

    print(f'Evolution completed. Results saved to {args.output}')
