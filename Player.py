from Deck import Card
from typing import List
from Constants import *

class Player():
    def __init__(self, starting_money: int) -> None:

        # Throughout game
        self.money = starting_money

        # Reset each hand
        self.role = None # Picker, Partner, or Good Guy
        self.position = None # Number of seats to the left of dealer
        self.hand = List[Card]
        self.played_cards = List[Card]
        self.taken_cards = List[Card]
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }
