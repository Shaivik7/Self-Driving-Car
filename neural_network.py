import numpy as np


class NeuralNetwork:
    def __init__(self, input_size, hidden_sizes, output_size):
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        self.weights, self.biases = self.initialize_weights_and_biases()

    def initialize_weights_and_biases(self):
        sizes = [self.input_size] + self.hidden_sizes + [self.output_size]
        weights = [
            np.random.randn(size_out, size_in)
            for size_in, size_out in zip(sizes[:-1], sizes[1:])
        ]
        biases = [np.zeros((size, 1)) for size in sizes[1:]]
        return weights, biases

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def feedforward(self, input_vector):
        for b, w in zip(self.biases, self.weights):
            input_vector = self.sigmoid(np.dot(w, input_vector) + b)
        return input_vector
