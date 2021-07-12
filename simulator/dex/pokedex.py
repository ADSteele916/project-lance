"""Loads a list containing an instance of a PokemonSpecies for every available Pokemon."""

import json
import os.path

from simulator.dex.movedex import MOVEDEX
from simulator.pokemon.pokemon_species import PokemonSpecies
from simulator.type import Type

with open(os.path.join(os.path.dirname(__file__), "pokedex.json")) as json_file:
    __dex_dict_list = json.load(json_file)

POKEDEX = []

for __pokemon in __dex_dict_list:
    POKEDEX.append(
            PokemonSpecies(
                    __pokemon["name"],
                    __pokemon["dex_num"],
                    __pokemon["base_hp"],
                    __pokemon["base_atk"],
                    __pokemon["base_def"],
                    __pokemon["base_spe"],
                    __pokemon["base_spc"],
                    set(map(lambda move: MOVEDEX[move],
                            filter(lambda move: move in MOVEDEX,
                                   __pokemon["learnset"]))),
                    Type[__pokemon["primary_type"].upper()],
                    None if __pokemon["secondary_type"] is None else Type[__pokemon["secondary_type"].upper()],
            )
    )
