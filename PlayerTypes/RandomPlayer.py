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
            self.hole = self.hand.pop()
            if len(callable_aces) == 0:
                self.playing_alone = True
                return None, self.hole
            else:
                return callable_aces[0], self.hole
        else:
            if len(callable_aces) == 0:
                self.playing_alone = True
                return None, None
            return callable_aces[0], None

    def playCard(self, current_trick_cards: List[Card], called_ace: Card) -> Card:
        
        # Player going first plays a random card
        if current_trick_cards == []:
            print("Going first, random card")
            return self.hand.pop()
        
        # Determine playable cards
        playable_cards = self.get_playable_cards(current_trick_cards[0], called_ace)

        # Play hole if required
        if playable_cards[0] == self.hole:
            hole_card = self.hole
            self.hole = None
            return hole_card

        # Otherwise play a random card
        self.hand.remove(playable_cards[0])
        return playable_cards[0]