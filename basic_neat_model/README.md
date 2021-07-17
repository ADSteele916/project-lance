# Basic NEAT Model

This model uses the NEAT (NeuroEvolution of Augmenting Topologies) genetic algorithm to learn to play a simplified version of Generation I Pokémon battles.

The model competes using single-Pokémon teams based on Blue's starter in the Cerulean City rival battle in the original Pokémon Red and Blue Versions. As such, it does not need to learn when to switch or handle Pokemon with different movesets. However, it still needs to learn about STAB and type effectiveness.

Here are a few games that the winning model played against itself. Note that both `P1` and `P2` use the same winning neural network (with flipped inputs).

```
BATTLE: P1's Bulbasaur vs P2's Bulbasaur
P2's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P1's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P2's Bulbasaur used Tackle!
P1's Bulbasaur lost to P2's Bulbasaur
 
BATTLE: P1's Bulbasaur vs P2's Squirtle
P2's Squirtle used Water Gun!
P1's Bulbasaur used Vine Whip!
P2's Squirtle used Water Gun!
P1's Bulbasaur used Vine Whip!
P2's Squirtle used Water Gun!
P1's Bulbasaur used Vine Whip!
P1's Bulbasaur beat P2's Squirtle
 
BATTLE: P1's Bulbasaur vs P2's Charmander
P1's Bulbasaur used Tackle!
P2's Charmander used Ember!
P1's Bulbasaur used Tackle!
P2's Charmander used Ember!
P1's Bulbasaur used Tackle!
P2's Charmander used Ember!
P1's Bulbasaur lost to P2's Charmander
 
BATTLE: P1's Squirtle vs P2's Squirtle
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P2's Squirtle used Water Gun!
P1's Squirtle used Water Gun!
P1's Squirtle beat P2's Squirtle
 
BATTLE: P1's Squirtle vs P2's Charmander
P1's Squirtle used Water Gun!
P2's Charmander used Leer!
P1's Squirtle used Water Gun!
P2's Charmander used Leer!
P1's Squirtle used Water Gun!
P1's Squirtle beat P2's Charmander
 
BATTLE: P1's Charmander vs P2's Charmander
P1's Charmander used Scratch!
P2's Charmander used Scratch!
P2's Charmander used Scratch!
P1's Charmander used Scratch!
P2's Charmander used Scratch!
P1's Charmander used Scratch!
P1's Charmander used Scratch!
P2's Charmander used Scratch!
P1's Charmander used Scratch!
P2's Charmander used Scratch!
P1's Charmander used Scratch!
P2's Charmander used Scratch!
P2's Charmander used Scratch!
P1's Charmander used Scratch!
P1's Charmander beat P2's Charmander
```
