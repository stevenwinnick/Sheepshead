import Player
from Player import Player
from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class RandomPlayer(Player):
    def __init__(self, game: 'Game', starting_money: int):
        super().__init__(game, starting_money)

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        return True, blind
    
    def call_ace(self, buried: List[Card]) -> Tuple[Card, Card]: # second card in the hole if doing unknown ace
        callable_aces, unknown_ace = self.get_callable_aces(buried)
        if unknown_ace:
            hole = self.hand.pop()
            if len(callable_aces) == 0:
                self.playing_alone = True
                return None, hole
            else:
                return callable_aces[0], hole
        else:
            if len(callable_aces) == 0:
                self.playing_alone = True
                return None, None
            return callable_aces[0], None

    def playCard(self, current_trick_cards: List[Card], called_suit) -> Card:
        
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