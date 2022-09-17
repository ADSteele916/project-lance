"""An neural network Agent that uses a NEAT genome to construct its network."""

from typing import List

from neat import Config
from neat.genome import DefaultGenome
from neat.nn import FeedForwardNetwork
import numpy as np

from simulator.agents.basic_nn_agent import BasicNeuralNetworkAgent


class NEATAgent(BasicNeuralNetworkAgent):
    """A version of the BasicNeuralNetworkAgent that uses a NEAT network."""

    def __init__(self, genome: DefaultGenome, config: Config):
        self.genome = genome
        self.genome.fitness = 0
        self.network = FeedForwardNetwork.create(genome, config)

    def reward(self, amount):
        self.genome.fitness += amount

    def evaluate_network(self, input_vector: np.ndarray) -> List[float]:
        list_input = input_vector.flatten().tolist()
        return self.network.activate(list_input)
