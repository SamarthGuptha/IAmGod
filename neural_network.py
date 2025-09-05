import math
import config

class NeuralNetwork:
    def __init__(self, weights):
        self.w1_end = config.NN_INPUTS * config.NN_HIDDEN_NODES
        self.w2_end = self.w1_end + (config.NN_HIDDEN_NODES*config.NN_OUTPUTS)
        self.weights1 = weights[:self.w1_end]
        self.weights2 = weights[self.w1_end:self.w2_end]
    def _sigmoid(self, x):
        try:
            return 1/(1+math.exp(-x))
        except OverflowError:
            return 0 if x<0 else 1
    def process(self, inputs):
        if len(inputs) != config.NN_INPUTS:
            return [0, 0]
        #input
        hidden = [0]*config.NN_HIDDEN_NODES
        for i in range(config.NN_HIDDEN_NODES):
            activation = 0
            for j in range(config.NN_INPUTS):
                activation += inputs[j]*self.weights1[j*config.NN_HIDDEN_NODES+i]
            hidden[i] = self._sigmoid(activation)
        #hidden-->output
        outputs = [0]*config.NN_OUTPUTS
        for i in range(config.NN_OUTPUTS):
            activation = 0
            for j in range(config.NN_HIDDEN_NODES):
                activation += hidden[j]*self.weights2[j*config.NN_OUTPUTS+i]
            outputs[i] = math.tanh(activation)
        return outputs
