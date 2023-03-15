from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class Player():
    def __init__(self, game: 'Game', starting_money: int) -> None:

        # Throughout day
        self.game = game
        self.starting_money = starting_money
        self.money = starting_money

        # Reset each hand
        self.role = None # Picker, Partner, or Good Guy
        self.position = None # Number of seats to the left of dealer - 1
        self.hand = []
        self.played_cards = []
        self.taken_cards = []
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        raise Exception("This player type doesn't know how to pick")
    
    def playCard(self, current_trick_cards: List[Card], called_suit: int) -> Card:
        raise Exception("This player type doesn't know how to play")

    def call_ace(self, buried: List[Card]):
        raise Exception("This player doesn't know how to call an ace")