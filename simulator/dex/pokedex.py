"""A dictionary containing a PokemonSpecies for every available Pokemon."""

import json
import os.path
from typing import Dict

from simulator.dex.movedex import MOVEDEX
from simulator.pokemon.pokemon_species import PokemonSpecies
from simulator.type import Type


def _gen_pokedex() -> Dict[str, PokemonSpecies]:
    with open(
        os.path.join(os.path.dirname(__file__), "pokedex.json"), encoding="utf-8"
    ) as json_file:
        dex_dict_list = json.load(json_file)

    pokedex = {}

    for pokemon in dex_dict_list:
        pokedex[pokemon["name"]] = PokemonSpecies(
            pokemon["name"],
            pokemon["dex_num"],
            pokemon["base_hp"],
            pokemon["base_atk"],
            pokemon["base_def"],
            pokemon["base_spe"],
            pokemon["base_spc"],
            set(MOVEDEX[move] for move in pokemon["learnset"] if move in MOVEDEX),
            Type[pokemon["primary_type"].upper()],
            None
            if pokemon["secondary_type"] is None
            else Type[pokemon["secondary_type"].upper()],
        )

    return pokedex


POKEDEX = _gen_pokedex()
