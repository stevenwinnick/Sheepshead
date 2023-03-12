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
        self.position = None # Number of seats to the left of dealer
        self.hand = set[Card]
        self.played_cards = List[Card]
        self.taken_cards = List[Card]
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick(self, blind: Tuple[Card, Card]) -> Tuple[bool, Tuple[Card, Card]]:
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

    def pickManual(self, blind: Tuple[bool, Tuple[Card, Card]]) -> Tuple[bool, Tuple[Card, Card]]:
        pass

    def pickRandom(self, blind: Tuple[bool, Tuple[Card, Card]]) -> Tuple[bool, Tuple[Card, Card]]:
        return True, blind

    def pickRobert(self, blind: Tuple[bool, Tuple[Card, Card]]) -> Tuple[bool, Tuple[Card, Card]]:
        pass

    def pickMauer(self, blind: Tuple[bool, Tuple[Card, Card]]) -> Tuple[bool, Tuple[Card, Card]]:
        return False, blind
    
    def playCard(self, current_trick_cards: List[Card]) -> Card:
        if self.player_type == MANUAL:
            return self.playCardManual(self, current_trick_cards)
        elif self.player_type == RANDOM:
            return self.playCardRandom(self, current_trick_cards)
        elif self.player_type == ROBERT_M_STRUPP:
            return self.playCardRobert(self, current_trick_cards)
        elif self.player_type == MAUER:
            return self.playCardMauer(self, current_trick_cards)
        else:
            raise Exception("Invalid player type")
    
    def playCardManual(self, current_trick_cards: List[Card]) -> Card:
        pass
    
    def playCardRandom(self, current_trick_cards: List[Card]) -> Card:
        lead_suit = current_trick_cards[0].suit
        for card in self.hand:
            if card.suit == lead_suit:
                self.hand.remove(card)
                return card
        return self.hand.pop()
    
    def playCardRobert(self, current_trick_cards: List[Card]) -> Card:
        pass

    def playCardMauer(self, current_trick_cards: List[Card]) -> Card:
        pass