"""An neural network Agent that uses a NEAT genome to construct its network."""

from typing import List

from neat import Config
from neat.genome import DefaultGenome
from neat.nn import FeedForwardNetwork

from simulator.agents.basic_nn_agent import BasicNeuralNetworkAgent


class NEATAgent(BasicNeuralNetworkAgent):
    """A version of the BasicNeuralNetworkAgent that uses a NEAT network."""

    def __init__(self, genome: DefaultGenome, config: Config):
        self.genome = genome
        self.genome.fitness = 0
        self.network = FeedForwardNetwork.create(genome, config)

    def reward(self, amount):
        self.genome.fitness += amount

    def evaluate_network(self, input_vector: List[float]) -> List[float]:
        return self.network.activate(input_vector)
