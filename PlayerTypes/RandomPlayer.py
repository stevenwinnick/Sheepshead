import Player
from Player import Player
from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING
from random import uniform

if TYPE_CHECKING:
    from Game import Game

class RandomPlayer(Player):
    def __init__(self, game: 'Game', starting_money: int):
        super().__init__(game, starting_money)

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        picking_probability = 0.2
        if uniform(0, 1) < picking_probability:
            return True, blind
        else:
            return False, blind
    
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

    def playCard(self, current_trick_cards: List[Card], called_ace: Card, leaster: bool) -> Card:
        
        # Determine playable cards
        playable_cards = []
        if current_trick_cards == []:
            playable_cards = self.get_playable_cards(None, called_ace)
        else:
            playable_cards = self.get_playable_cards(current_trick_cards[0], called_ace)

        # Play hole if required
        if playable_cards[0] == self.hole:
            hole_card = self.hole
            self.hole = None
            return hole_card

        # Otherwise play a random card
        card_to_play = playable_cards[0]
        self.hand.remove(card_to_play)
        return card_to_play