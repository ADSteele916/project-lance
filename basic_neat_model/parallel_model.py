"""Training script for parallelized NEAT on the basic ruleset."""

import multiprocessing
import os
import pickle
from typing import Optional

import neat

from basic_neat_model.parallel_utils import evaluate
from basic_neat_model.parallel_utils import ParallelSelfPlayEvaluator


def train(config_file: str,
          generations: Optional[int] = 300,
          checkpoint_file: Optional[str] = None):
    """Trains a network using the given configuration. Saves the winner.

    Args:
        config_file: Path to the configuration from this file's directory.
        generations: The number of generations to train for.
        checkpoint_file: Path to a checkpoint from this file's directory.
    """
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    if checkpoint_file is not None:
        pop = neat.Checkpointer.restore_checkpoint(checkpoint_file)
    else:
        pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(
        neat.Checkpointer(generation_interval=1,
                          filename_prefix="checkpoints/neat-checkpoint-"))
    pe = ParallelSelfPlayEvaluator(multiprocessing.cpu_count() - 1, evaluate)

    winner = pop.run(pe.evaluate, generations)

    with open("winner.p", "wb") as file:
        pickle.dump(winner, file)

    print(f"\nBest genome:\n{winner}")


def load_winner(winner_file: str) -> neat.DefaultGenome:
    with open(winner_file, "rb") as file:
        winner = pickle.load(file)
    return winner


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    train(config_path)
