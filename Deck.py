from typing import List
from Constants import *
from random import shuffle

class Card():
    def __init__(self, value: int, suit: int) -> None:
        
        self.value = value
        self.printed_suit = suit
        self.sheep_suit = suit
        
        # Change sheep suit if Trump
        if self.printed_suit == DIAMONDS:
            self.sheep_suit = TRUMP
        elif self.value == JACK:
            self.sheep_suit = TRUMP
        elif self.value == QUEEN:
            self.sheep_suit = TRUMP

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
            self.power = 6 + self.printed_suit
        elif self.value == QUEEN:
            self.points = 3
            self.power = 10 + self.printed_suit

    def __eq__(self, other: 'Card'):
        return self.value == other.value and self.printed_suit == other.printed_suit
    
    def __str__(self):
        name = self.value
        if name == KING:
            name = "King"
        elif name == ACE:
            name = "Ace"
        else:
            name = str(name)
        
        if self.sheep_suit == TRUMP:
            if self.value != JACK and self.value != QUEEN:
                return name + " of Trump"
            elif self.power == 6:
                return "Jack of Diamonds"
            elif self.power == 7:
                return "Jack of Hearts"
            elif self.power == 8:
                return "Jack of Clubs"
            elif self.power == 9:
                return "Jack of Spades"
            elif self.power == 10:
                return "Queen of Diamonds"
            elif self.power == 11:
                return "Queen of Hearts"
            elif self.power == 12:
                return "Queen of Clubs"
            elif self.power == 13:
                return "Queen of Spades"
        elif self.sheep_suit == CLUBS:
            return name + " of Clubs"
        elif self.sheep_suit == SPADES:
            return name + " of Spades"
        elif self.sheep_suit == HEARTS:
            return name + " of Hearts"
    
    def beats(self, opponent: 'Card', led_card: 'Card') -> bool:
        if self.sheep_suit == TRUMP:
            if opponent.sheep_suit == TRUMP:
                return self.power > opponent.power
            else:
                return True
        else:
            led_suit = led_card.sheep_suit
            if self.sheep_suit == led_suit:
                if opponent.sheep_suit == TRUMP:
                    return False
                elif opponent.sheep_suit == led_suit:
                    return self.power > opponent.power
                else:
                    return True
            else:
                if opponent.sheep_suit == TRUMP:
                    return False
                elif opponent.sheep_suit == led_suit:
                    return False
                else:
                    return True # Neither card beats, but this scenario not encountered meaningfully in game


class Deck():
    def __init__(self) -> None:
        self.cards = []
        suits = [CLUBS, SPADES, HEARTS, DIAMONDS]
        values = [7, 8, 9, KING, 10, ACE, JACK, QUEEN]
        for value in values:
            for suit in suits:
                self.cards.append(Card(value, suit))
    
    def shuffleDeck(self) -> None:
        shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()