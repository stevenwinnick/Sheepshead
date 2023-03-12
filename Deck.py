from typing import List
from Constants import *
from random import shuffle

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
    
    def beats(self, opponent: 'Card', led_suit: int) -> bool:
        if self.suit == TRUMP:
            if opponent.suit == TRUMP:
                return self.power > opponent.power
            else:
                return True
        else:
            if self.suit == led_suit:
                if opponent.suit == TRUMP:
                    return False
                elif opponent.suit == led_suit:
                    return self.power > opponent.power
                else:
                    return True
            else:
                if opponent.suit == TRUMP:
                    return False
                elif opponent.suit == led_suit:
                    return False
                else:
                    return True # Neither card beats, but this scenario not encountered in game


class Deck():
    def __init__(self) -> None:
        self.cards = List[Card]
        suits = [TRUMP, CLUBS, SPADES, HEARTS]
        values = [7, 8, 9, KING, 10, ACE, JACK, QUEEN]
        for value in values:
            for suit in suits:
                self.cards.append(Card(value, suit))
    
    def shuffleDeck(self) -> None:
        shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()