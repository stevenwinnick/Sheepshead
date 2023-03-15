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

    def pick(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        if self.player_type == MANUAL:
            return self.pickManual(blind)
        elif self.player_type == RANDOM:
            return self.pickRandom(blind)
        elif self.player_type == ROBERT_M_STRUPP:
            return self.pickRobert(blind)
        elif self.player_type == MAUER:
            return self.pickMauer(blind)
        else:
            raise Exception("Invalid player type")

    def pickManual(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        pass

    def pickRandom(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        return True, blind

    def pickRobert(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        pass

    def pickMauer(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
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
            print("Going first, random card")
            return self.hand.pop()
        
        # Determine lead suit
        lead_suit = current_trick_cards[0].sheep_suit
        lead_trump = False
        if current_trick_cards[0].sheep_suit == TRUMP:
            lead_trump = True

        # Have to play called ace if you have it and its suit is led
        if lead_suit == called_suit and (not lead_trump):
            for card in self.hand:
                if card == Card(ACE, called_suit):
                    print("Playing called ace")
                    self.hand.remove(card)
                    return card

        # Picker can't play their last fail of the called suit unless the called suit is lead
        if self.role == PICKER:
            if (called_suit == lead_suit) and (not lead_trump):
                number_called = 0
                for card in self.hand:
                    if (card.sheep_suit == called_suit) and (card.sheep_suit != TRUMP):
                        number_called += 1
                if number_called == 1:
                    if (self.hand[0].sheep_suit == called_suit) and (self.hand[0].sheep_suit != TRUMP):
                        print("Picker can't play called suit")
                        playing_card = self.hand[0]
                        self.hand.remove(self.hand[0])
                        return playing_card
                    else:
                        print("Picker can't play called suit")
                        playing_card = self.hand[1]
                        self.hand.remove(self.hand[1])
                        return playing_card

        
        # Otherwise play random card of called suit
        if lead_trump:
            for card in self.hand:      # have to follow suit
                if card.sheep_suit == TRUMP:
                    print("Playing random trump")
                    self.hand.remove(card)
                    return card
        else:
            for card in self.hand:
                if card.sheep_suit == lead_suit:
                    print("Playing random card of led suit")
                    self.hand.remove(card)
                    return card
        
        # If no card of called suit, play a random card
        print("Playing random card")
        return self.hand.pop()
    
    def playCardRobert(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def playCardMauer(self, current_trick_cards: List[Card], called_suit) -> Card:
        pass

    def call_ace(self, buried: List[Card]):
        for card in self.hand:
            if (card.sheep_suit != TRUMP) and (Card(ACE,card.sheep_suit) not in self.hand):
                return card.sheep_suit
        for card in buried:
            if (card.sheep_suit != TRUMP) and (Card(ACE,card.sheep_suit) not in self.hand):
                return card.sheep_suit    
        for card in self.hand:
            print(card)
        for card in buried:
            print(card)
        raise Exception("Give him the book")