"""
	Author - Devesh
	IMPLEMENTING NEURAL NETWORK FROM SCRATCH USING NUMPY
"""
import numpy as np
import random

class neuralNet():
	def __init__(self, sizes):
		self.num_layers = len(sizes)	# Total layers
		self.sizes = sizes
		self.biases = [np.random.randn(y, 1) for y in sizes[1::]]		# Initalizing random biases
		self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]		# Initalizing random weights

	def feedForward(self, inp):
		for b, w in zip(self.biases, self.weights):
			inp = self.activationFunction(np.dot(w, inp) + b)
		return inp						# Returning the overall O/P of the network

	def activationFunction(self, x):	# Using sigmoid as the activation function
		return 1.0/(1.0 + np.exp(-x))

	# Calculating MEAN SQUARE ERROR b/w O/P and Expected Result
	def cost(out, res):					
		mse = np.square(out-res)		
		mse = np.sum(mse)/len(res)
		return mse

	# Train Neural network with Mini Batch Stochastic gradient descent (Mixture of SGD and Batch Gradient Descet)
	def SGD(self, trainingData, epochs, miniBatchSize, learningRate, testData): 
		totalTest = len(testData)
		totalTrain = len(totalTrain)
		for i in range(epochs):	
			random.shuffle(trainingData)
			# Dividing training data into several batches of size miniBactchSize
			miniBatches = [ trainingData[k:miniBatchSize+k] for k in range(0, n, miniBatchSize)]
			for eachBatch in miniBatches:
				self.update_batch(eachBatch, learningRate)
			if testData:
				print ("Epoch {0}: {1} / {2}".format(j, self.evaluate(testData), totalTest))
			else
				print (f"Epoch {j} complete")

	# Test data for every epoch
	def evaluate(self, testData):
		# Return the number of test inputs for which the neural network o/p's the correct result

if __name__ == "__main__":
	net = neuralNet([2, 3, 1])	# No of neurons in each Layer
	print(net.feedForward(np.array([[1], [1]])))


