from Deck import Card
from typing import List, Tuple
from Constants import *

class Player():
    def __init__(self, player_type: int, starting_money: int) -> None:

        # Throughout game
        self.money = starting_money

        # Reset each hand
        self.player_type = player_type
        self.role = None # Picker, Partner, or Good Guy
        self.position = None # Number of seats to the left of dealer - 1
        self.hand = set[Card]
        self.played_cards = List[Card]
        self.taken_cards = List[Card]
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick(self, blind: set(Card)) -> Tuple[bool, set(Card)]:
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

    def pickManual(self, blind: Tuple[bool, set(Card)]) -> Tuple[bool, set(Card)]:
        pass

    def pickRandom(self, blind: Tuple[bool, set(Card)]) -> Tuple[bool, set(Card)]:
        return True, blind

    def pickRobert(self, blind: Tuple[bool, set(Card)]) -> Tuple[bool, set(Card)]:
        pass

    def pickMauer(self, blind: Tuple[bool, set(Card)]) -> Tuple[bool, set(Card)]:
        return False, blind
    
    def playCard(self, current_trick_cards: List[Card], called_suit: int) -> Card:
        if self.player_type == MANUAL:
            return self.playCardManual(self, current_trick_cards, called_suit)
        elif self.player_type == RANDOM:
            return self.playCardRandom(self, current_trick_cards, called_suit)
        elif self.player_type == ROBERT_M_STRUPP:
            return self.playCardRobert(self, current_trick_cards, called_suit)
        elif self.player_type == MAUER:
            return self.playCardMauer(self, current_trick_cards, called_suit)
        else:
            raise Exception("Invalid player type")
    
    def playCardManual(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass
    
    def playCardRandom(self, current_trick_cards: List[Card], called_suit) -> Card:
        if current_trick_cards == []:
            return self.hand.pop()
        lead_suit = current_trick_cards[0].suit
        if lead_suit == called_suit:    # have to play called ace
            for card in self.hand:
                if card == Card(ACE, called_suit):
                    return card

        for card in self.hand:      # have to follow suit
            if card.suit == lead_suit:
                self.hand.remove(card)
                return card
        if self.role == PICKER:
            for card in self.hand:     # picker can't get rid of called suit
                if card.suit != called_suit:
                    self.hand.remove(card)
                    return card
        return self.hand.pop()
    
    def playCardRobert(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def playCardMauer(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def call_ace(self):
        for card in self.hand:
            if (card.suit != TRUMP) and (Card(ACE,card.suit) not in self.hand):
                return card.suit
            
        raise Exception("Give him the book")