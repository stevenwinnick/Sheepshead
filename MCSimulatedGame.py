import Game
from Game import Game, TrickInfo
from typing import List, Tuple
from Player import Player
from Deck import *

class MCSimulatedGame(Game):
    def __init__(self, 
                 position: int, 
                 phase: int, 
                 picker_position: int, 
                 called_ace: Card, 
                 leaster: bool, 
                 picker_playing_alone: bool,
                 called_ten: bool,
                 unknown_ace: bool,
                 tricks_so_far: TrickInfo, 
                 current_trick: List[Card]):
        super().__init__([RANDOM, RANDOM, RANDOM, RANDOM, RANDOM], 0)
        
        self.called_ace = called_ace
        self.is_leaster = leaster
        self.picker_playing_alone = picker_playing_alone
        self.called_ten = called_ten
        self.unknown_ace = unknown_ace
        self.tricks_so_far = tricks_so_far
        self.current_trick = current_trick

        # Initialize to current game state

    def simulate(self) -> bool: # returns true if current player wins this simulation
        pass