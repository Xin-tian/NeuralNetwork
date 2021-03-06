import numpy as np
import matplotlib.pyplot as plt
import deep_neural_network_base as dnn
from nn_utils import *

class NeuralNetwork(dnn.NeuralNetwork):
    def __init__(self, layer_dim, activations, learning_rate, num_iterations, mini_batch_size, lambda_reg):
        super(NeuralNetwork, self).__init__(layer_dim, activations, learning_rate, num_iterations, mini_batch_size)
        self.lambda_reg = lambda_reg

    def regularization_term(self):
        l2 = 0.0
        for layer in range(1, self.num_layers):
            l2 += np.sum(np.power(self.parameters['W%s' % layer], 2))
        return l2

    # Changed to add the regularization term
    def compute_cost(self, Y):
        AL = self.cache['A%s' % str(self.num_layers)]
        activation = self.activations[self.num_layers]
        if activation == 'softmax':
            loss = -np.sum(np.multiply(Y, np.log(AL)), axis=0, keepdims=True)
            cost = np.sum(loss, axis=1, keepdims=True)/Y.shape[1]
        elif activation == 'sigmoid':
            loss = -(np.multiply(Y, np.log(AL)) + np.multiply((1-Y), np.log(1-AL)))
            cost = np.sum(loss, axis=1, keepdims=True)/Y.shape[1]
        else:
            print('Last activation function not comteplated: %s' % self.activations[-1])
            exit(1)
        cost = np.squeeze(cost + (self.lambda_reg/(2*Y.shape[1]))*self.regularization_term())
        return cost

    def linear_backwards(self, dA, A_prev, Z, W, activation):
        if activation == 'relu':
            dZ = np.multiply(dA, relu_derivative(Z))
        elif activation == 'sigmoid':
            dZ = np.multiply(dA, sigmoid_derivative(Z))
        elif activation == 'tanh':
            dZ = np.multiply(dA, tanh_derivative(Z))
        dW = (np.dot(dZ, A_prev.T)/A_prev.shape[1]) + (self.lambda_reg/A_prev.shape[1])*W
        dB = np.sum(dZ, axis=1, keepdims=True)/A_prev.shape[1]
        dA_prev = np.dot(W.T, dZ)
        return dA_prev, dW, dB

    def nn_backwards(self, Y):
        # Computing L.
        AL = self.cache['A%s' % str(self.num_layers)]
        W = self.parameters['W%s' % str(self.num_layers)]
        A_prev = self.cache['A%s' % str(self.num_layers - 1)]
        if self.activations[-1] == 'softmax':
            dZ = AL - Y
            dW = np.dot(dZ, A_prev.T)/float(A_prev.shape[1]) + (self.lambda_reg/A_prev.shape[1])*W
            dB = np.sum(dZ, axis=1, keepdims=True)/float(A_prev.shape[1])
            dA_prev = np.dot(W.T, dZ)
        else:
            Z = self.parameters['Z%s' % str(self.num_layers)]
            dAL = - (1./AL.shape[1])*np.divide(Y,AL)
            dA_prev, dW, dB = linear_backwards(self, dAL, A_prev, Z, W, self.activations[-1])
        self.grads['dW%s' % str(self.num_layers)] = dW
        self.grads['dB%s' % str(self.num_layers)] = dB
        self.grads['dA%s' % str(self.num_layers - 1)] = dA_prev

        # Starts by L-1
        for l in reversed(range(1, self.num_layers)):
            W = self.parameters['W%s' % l]
            Z = self.cache['Z%s' % l]
            dA_prev_temp, dW_temp, db_temp = self.linear_backwards(self.grads['dA%s' % str(l)], self.cache['A%s' % str(l - 1)], Z, W, self.activations[l])
            self.grads['dA%s' % str(l-1)] = dA_prev_temp
            self.grads['dW%s' % l] = dW_temp
            self.grads['dB%s' % l] = db_temp

    def train_set(self, X_train, Y_train, X_test, Y_test, print_cost=True):
        self.initialize_parameters()
        costs = list()
        num_samples = Y_train.shape[1]
        for i in range(0, self.num_iterations):
            for index in range(0, num_samples, self.mini_batch_size):
                end = index + self.mini_batch_size
                cost = self.train(X_train[:, index:end], Y_train[:, index:end])
                if print_cost and i % 100 == 0:
                    print("Cost after epoch %i:     %f" % (i, cost))
                    costs.append(cost)

        if print_cost:
            plt.figure()
            plt.plot(costs[20:])
            plt.ylabel('Cost Function')
            plt.xlabel('iterations (x100)')
            plt.title('Learning rate =%s' % self.learning_rate)
            plt.show()

        self.nn_forward(X_train)
        accuracy_train = get_accuracy(self.cache['A%s' % self.num_layers], Y_train)
        self.nn_forward(X_test)
        cost_test = self.compute_cost(Y_test)
        accuracy_test = get_accuracy(self.cache['A%s' % self.num_layers], Y_test)

        print('Lr: %s; Reg: %s: Train/Test Cost: %s/%s  Accuracy Train/Test: %s/%s' %
              (np.round(self.learning_rate, 4), np.round(self.lambda_reg, 4), np.round(cost, 4), np.round(cost_test, 4), np.round(accuracy_train, 1), np.round(accuracy_test, 1)))


