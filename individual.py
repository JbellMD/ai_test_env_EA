from abc import ABC, abstractmethod
import random
import numpy as np

class Individual(ABC):
    def __init__(self):
        self.fitness = None

    @abstractmethod
    def mutate(self, mutation_rate):
        pass

    @abstractmethod
    def crossover(self, other):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    def similarity(self, other):
        """
        Calculate similarity between two individuals
        Returns a value between 0 (completely different) and 1 (identical)
        """
        if type(self) != type(other):
            return 0.0
            
        if isinstance(self, NeuralNetworkIndividual):
            # Compare neural network architectures and weights
            arch_sim = self._architecture_similarity(other)
            weight_sim = self._weights_similarity(other)
            return 0.5 * arch_sim + 0.5 * weight_sim
            
        elif isinstance(self, SymbolicProgramIndividual):
            # Compare program structures
            return self._program_similarity(other)
            
        return 0.0  # Default for unknown types

class NeuralNetworkIndividual(Individual):
    def _architecture_similarity(self, other):
        # Compare layer structure
        if len(self.architecture) != len(other.architecture):
            return 0.0
            
        similarity = 0.0
        for layer1, layer2 in zip(self.architecture, other.architecture):
            if layer1 == layer2:
                similarity += 1.0
            elif layer1['type'] == layer2['type']:
                similarity += 0.5
                
        return similarity / len(self.architecture)

    def _weights_similarity(self, other):
        # Compare weight matrices using cosine similarity
        similarities = []
        for w1, w2 in zip(self.weights, other.weights):
            if w1.shape != w2.shape:
                similarities.append(0.0)
                continue
                
            # Flatten and normalize
            w1_flat = w1.flatten()
            w2_flat = w2.flatten()
            
            # Cosine similarity
            dot = np.dot(w1_flat, w2_flat)
            norm = np.linalg.norm(w1_flat) * np.linalg.norm(w2_flat)
            similarities.append(dot / (norm + 1e-8))
            
        return np.mean(similarities)

class SymbolicProgramIndividual(Individual):
    def _program_similarity(self, other):
        # Compare program structure
        if len(self.program) != len(other.program):
            return 0.0
            
        matches = sum(1 for x, y in zip(self.program, other.program) if x == y)
        return matches / len(self.program)
