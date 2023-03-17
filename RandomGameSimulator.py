from Game import *
from Constants import *

game = Game(player_types=[RANDOM, RANDOM, RANDOM, RANDOM, RANDOM])
game.play_game(number_rounds=10000)