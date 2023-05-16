import Game
from Game import Game, TrickInfo
from typing import List, Tuple
from Player import Player
from Deck import *
import copy

class MCSimulatedGame(Game):
    def __init__(self, 
                 phase: int, 
                 dealer_position: int,
                 picker_position: int,
                 simulator_hand: List[Card],
                 buried_cards: Tuple[Card, Card], 
                 called_ace: Card, 
                 hole_card: Card,
                 leaster: bool, 
                 tricks_so_far: List[TrickInfo], 
                 current_trick: List[Card]):
        super().__init__([RANDOM, RANDOM, RANDOM, RANDOM, RANDOM], 0)
        
        self.phase = phase
        self.dealer_position = dealer_position
        self.picker_position = picker_position
        self.simulator_hand = simulator_hand
        self.buried_cards = buried_cards
        self.called_ace = called_ace
        self.hole_card = hole_card
        self.is_leaster = leaster
        self.tricks_so_far = tricks_so_far
        self.current_trick = current_trick

        # Initialize to current game state (only use known cards so can random simulate later)
        if phase == PICKING:
            pass

        elif phase == CALLING_ACE:
            pass

        elif phase == PLAYING:
            pass

    def simulate(self) -> bool: # returns true if current player wins this simulation
        
        copy_deck = copy.copy(self.deck)
        copy_deck.shuffleDeck()
        
        if self.phase == CALLING_ACE:
            
            # If simulator is the picker
            if self.picker_position == self.simulating_position:
                blind = [copy_deck.deal(), copy_deck.deal()]
                called_ace, hole = self.simulator.call_ace(blind)

            # If they passed
            else:
                pass