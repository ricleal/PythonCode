#!/usr/bin/env python
# coding: utf-8

import numpy as np
"""
Python code for simple Artificial Neural Network with one hidden layer

https://github.com/kiteco/kite-python-blog-post-code/tree/master/neural-networks-intro

"""


def initialize_weights():
    # Generate random numbers
    np.random.seed(1)

    # Assign random weights to a 3 x 1 matrix
    synaptic_weights = np.random.uniform(low=-1, high=1, size=(3, 1))
    return synaptic_weights


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def train(inputs, expected_output, synaptic_weights, bias, learning_rate,
          training_iterations):
    for epoch in range(training_iterations):
        # Forward pass -- Pass the training set through the network.
        predicted_output = learn(inputs, synaptic_weights, bias)

        # Backaward pass
        # Calculate the error
        error = sigmoid_derivative(predicted_output) * \
            (expected_output - predicted_output)

        # Adjust the weights and bias by a factor
        weight_factor = np.dot(inputs.T, error) * learning_rate
        bias_factor = error * learning_rate

        # Update the synaptic weights
        synaptic_weights += weight_factor

        # Update the bias
        bias += bias_factor

        if ((epoch % 10000) == 0):
            print("Epoch", epoch)
            print("Predicted Output = ", predicted_output.T)
            print("Expected Output = ", expected_output.T)
            print()
    return synaptic_weights


def learn(inputs, synaptic_weights, bias):
    return sigmoid(np.dot(inputs, synaptic_weights) + bias)


if __name__ == "__main__":
    # Initialize random weights for the network
    synaptic_weights = initialize_weights()

    # The training set
    inputs = np.array([[0, 1, 1],
                       [1, 0, 0],
                       [1, 0, 1]])

    # Target set
    expected_output = np.array([[1, 0, 1]]).T

    # Test set
    test = np.array([1, 0, 1])

    # Train the neural network
    trained_weights = train(inputs, expected_output, synaptic_weights,
                            bias=0.001, learning_rate=0.98,
                            training_iterations=1000000)

    # Test the neural network with a test example
    accuracy = (learn(test, trained_weights, bias=0.01)) * 100

    print("accuracy =", accuracy[0], "%")
