import numpy as np
from deep_neural_network_l2regularization import *
from nn_utils import *
from mnist.loader import MNIST


# Loading data.
db = '/Users/aclaudioquiros/Documents/NN Data/Data/MNIST_database/'
mndata = MNIST(db)
images, labels = mndata.load_training()
images_test, labels_test = mndata.load_testing()
images = np.array(images).T
images_test = np.array(images_test).T
labels = onehot(labels, images.shape)
labels_test = onehot(labels_test, images_test.shape)
images = normalize(images)
images_test = normalize(images_test)



# Playing with data to over fit model.
# samples = 1e+3
# images = images[:, :int(samples)]
# labels = labels[:, :int(samples)]
# images = np.random.normal(0, 1, size=(400, 1000))
# layer_dim = [images.shape[0], 400, 400, 400, 400, 400, 400, 400, 400, 400, labels.shape[0]]
# activations = [None, 'relu', 'relu', 'relu', 'relu', 'relu', 'relu', 'relu', 'relu', 'relu', 'softmax']



layer_dim = [images.shape[0], 40, labels.shape[0]]
activations = [None, 'relu', 'softmax']
deep_nn = NeuralNetwork(layer_dim, activations, learning_rate=0.002, num_iterations=10000, mini_batch_size=1024, lambda_reg=0.2)
deep_nn.train_set(images, labels, images_test, labels_test, print_cost=True)
