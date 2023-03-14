from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class Player():
    def __init__(self, player_type: int, starting_money: int, game: 'Game') -> None:

        # Throughout game
        self.game = game
        self.money = starting_money

        # Reset each hand
        self.player_type = player_type
        self.role = None # Picker, Partner, or Good Guy
        self.position = None # Number of seats to the left of dealer - 1
        self.hand = []
        self.played_cards = []
        self.taken_cards = []
        self.public_empty_suits = {
            "Trump": False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick(self, blind: set[Card]) -> Tuple[bool, set[Card]]:
        if self.player_type == MANUAL:
            return self.pickManual(self)
        elif self.player_type == RANDOM:
            return self.pickRandom(self)
        elif self.player_type == ROBERT_M_STRUPP:
            return self.pickRobert(self)
        elif self.player_type == MAUER:
            return self.pickMauer(self)
        else:
            raise Exception("Invalid player type")

    def pickManual(self, blind: set[Card]) -> Tuple[bool, set[Card]]:
        pass

    def pickRandom(self, blind: set[Card]) -> Tuple[bool, set[Card]]:
        return True, blind

    def pickRobert(self, blind: set[Card]) -> Tuple[bool, set[Card]]:
        pass

    def pickMauer(self, blind: set[Card]) -> Tuple[bool, set[Card]]:
        return False, blind
    
    def playCard(self, current_trick_cards: List[Card], called_suit: int) -> Card:
        if self.player_type == MANUAL:
            return self.playCardManual(current_trick_cards, called_suit)
        elif self.player_type == RANDOM:
            return self.playCardRandom(current_trick_cards, called_suit)
        elif self.player_type == ROBERT_M_STRUPP:
            return self.playCardRobert(current_trick_cards, called_suit)
        elif self.player_type == MAUER:
            return self.playCardMauer(current_trick_cards, called_suit)
        else:
            raise Exception("Invalid player type")
    
    def playCardManual(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass
    
    def playCardRandom(self, current_trick_cards: List[Card], called_suit) -> Card:
        
        # Player going first plays a random card
        if current_trick_cards == []:
            return self.hand.pop()
        
        # Determine lead suit
        lead_suit = current_trick_cards[0].suit
        lead_trump = False
        if current_trick_cards[0].is_trump:
            lead_trump = True

        # Have to play called ace if you have it
        if lead_suit == called_suit:
            for card in self.hand:
                if card == Card(ACE, called_suit):
                    self.hand.remove(card)
                    return card

        # Picker can't play called suit
        if self.role == PICKER:
            for card in self.hand:
                if card.suit != called_suit:
                    self.hand.remove(card)
                    return card
        
        # Otherwise play random card of called suit
        for card in self.hand:      # have to follow suit
            if lead_trump and card.is_trump:
                self.hand.remove(card)
                return card
            elif card.suit == lead_suit:
                self.hand.remove(card)
                return card
        
        # If no card of called suit, play a random card
        return self.hand.pop()
    
    def playCardRobert(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def playCardMauer(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def call_ace(self):
        for card in self.hand:
            if (not card.is_trump) and (Card(ACE,card.suit) not in self.hand):
                return card.suit
            
        raise Exception("Give him the book")