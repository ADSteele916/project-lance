"""An Agent that uses a NEAT genome to construct a neural network that it uses to make decisions."""

from typing import List

import numpy as np
from neat import Config
from neat.genome import DefaultGenome
from neat.nn import FeedForwardNetwork

from simulator.agents.basic_nn_agent import BasicNeuralNetworkAgent


class NEATAgent(BasicNeuralNetworkAgent):
    """An implementation of the BasicNeuralNetworkAgent that uses a NEAT network."""

    def __init__(self, genome: DefaultGenome, config: Config):
        self.genome = genome
        self.genome.fitness = 0
        self.network = FeedForwardNetwork.create(genome, config)

    def reward(self, amount):
        self.genome.fitness += amount

    def evaluate_network(self, input_vector: np.ndarray) -> List[float]:
        list_input = input_vector.flatten().tolist()
        return self.network.activate(list_input)
