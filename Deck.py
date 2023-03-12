from typing import List
from Constants import *

class Deck():
    def __init__(self) -> None:
        self.cards = List[Card]
        suits = [TRUMP, CLUBS, SPADES, HEARTS]
        values = [7, 8, 9, KING, 10, ACE, JACK, QUEEN]
        for value in values:
            for suit in suits:
                self.cards.append(Card(value, suit))


class Card():
    def __init__(self, value: int, suit: int) -> None:
        
        self.value = value
        self.suit = suit

        # Get points and power
        if self.value == 7:
            self.points = 0
            self.power = 0
        if self.value == 8:
            self.points = 0
            self.power = 1
        elif self.value == 9:
            self.points = 0
            self.power = 2
        elif self.value == KING:
            self.points = 4
            self.power = 3
        elif self.value == 10:
            self.points = 10
            self.power = 4
        elif self.value == ACE:
            self.points = 11
            self.power = 5
        elif self.value == JACK:
            self.points = 2
            self.power = 6 + self.suit
        elif self.value == QUEEN:
            self.points = 3
            self.power = 11 + self.suit
        