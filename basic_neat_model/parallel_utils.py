"""Utilities for parallel training of a NEAT model for the basic ruleset."""

from itertools import product
from math import sqrt
from typing import Tuple, List, Dict

from neat import ParallelEvaluator, DefaultGenome, Config

from basic_neat_model.agents.neat_agent import NEATAgent
from simulator.battle.battle import Battle, Player
from simulator.team_generators.basic_rival_team_generator import BasicRivalTeamGenerator
from simulator.team_generators.team_generator import NoMorePossibleTeamsException


class ParallelSelfPlayEvaluator(ParallelEvaluator):
    """A version of ParallelEvaluator that can engage in self-play."""

    def evaluate(self, genomes, config):
        jobs = []
        for idx, genome in enumerate(genomes[:-1]):
            competitors = genomes[idx:]
            jobs.append(self.pool.apply_async(self.eval_function, args=(genome, competitors, config)))

        rewards = {genome[0]: (genome[1], 0.0) for genome in genomes}

        for job in jobs:
            job_rewards = job.get(timeout=self.timeout)
            for genome_id, reward in job_rewards.items():
                rewards[genome_id] = (rewards[genome_id][0], rewards[genome_id][1] + reward)

        for _, (genome, reward) in rewards.items():
            genome.fitness = reward


def evaluate(genome: Tuple[int,
                           DefaultGenome],
             competitor_genomes: List[Tuple[int,
                                            DefaultGenome]],
             config: Config) -> Dict[int,
                             float]:
    """Evaluates the given genome against the given competitors, producing the rewards for each.

    Args:
        genome (Tuple[int, DefaultGenome]): A genome id and genome to evaluate.
        competitor_genomes (List[Tuple[int, DefaultGenome]]): A list of genome ids and genomes to compete against.
        config (Config): The Config for the run.

    Returns:
        Dict[int, float]: A dictionary of genome ids and how much to reward them.
    """
    evaluating_bot = (genome[0], NEATAgent(genome[1], config))
    competitor_bots = list(map(lambda g: (g[0], NEATAgent(g[1], config)), competitor_genomes))
    rewards = {genome[0]: 0}

    brtg = BasicRivalTeamGenerator()
    teams = []
    while True:
        try:
            teams.append(brtg.generate_team())
        except NoMorePossibleTeamsException:
            break
    team_matchups = list(product(teams, repeat=2))

    for competitor in competitor_bots:
        rewards[competitor[0]] = 0
        for team_one, team_two in team_matchups:
            battle = Battle(team_one, team_two, evaluating_bot[1], competitor[1])
            winner, turns = battle.play()
            if winner is None:
                rewards[evaluating_bot[0]] += 0.25 / sqrt(turns)
                rewards[competitor[0]] += 0.25 / sqrt(turns)
            if winner == Player.P1:
                rewards[evaluating_bot[0]] += 1.0 / sqrt(turns)
            if winner == Player.P2:
                rewards[competitor[0]] += 1.0 / sqrt(turns)

    return rewards
