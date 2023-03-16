from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class Player():
    def __init__(self, game: 'Game', starting_money: int) -> None:

        # Throughout day
        self.game = game
        self.starting_money = starting_money
        self.money = starting_money

        # Reset each hand
        self.role = None # Picker, Partner, or Good Guy
        self.playing_alone = False
        self.position = None # Number of seats to the left of dealer - 1
        self.hand = []
        self.played_cards = []
        self.taken_cards = []
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        raise Exception("This player type doesn't know how to pick")
    
    def bury_two(self, hand_plus_blind: List[Card]) -> Tuple[List[Card], List[Card]]:
        raise Exception("This player type doesn't know how to bury")

    def call_ace(self, buried: List[Card]) -> Tuple[Card, Card]: # second card in the hole if doing unknown ace
        raise Exception("This player doesn't know how to call an ace")
    
    def get_callable_aces(self, buried: List[Card]) -> Tuple[List[Card], bool]: # bool for if unknown ace, LIST MAY BE EMPTY
        hand_plus_buried = self.hand + buried
        known_aces = []
        for card in hand_plus_buried:
            if card.value == ACE and card.sheep_suit != TRUMP:
                known_aces.append(card)

        callable_cards = []

        # If all 3 fail aces, call a 10
        if len(known_aces) == 3:
            for potential_suit_match in self.hand:
                if potential_suit_match.sheep_suit != TRUMP:
                    can_call_ten = True
                    for already_callable in callable_cards:
                        if already_callable.sheep_suit == potential_suit_match.sheep_suit:
                            can_call_ten = False
                    for potential_ten in hand_plus_buried:
                        if potential_ten.value == 10 and potential_ten.sheep_suit == potential_suit_match.sheep_suit:
                            can_call_ten = False
                    if can_call_ten:
                        callable_cards.append(Card(10, potential_suit_match.sheep_suit))
            return callable_cards, False
        
        # If have matching ace for each suit in hand, call unknown ace
        for potential_suit_match in self.hand:
            if potential_suit_match.sheep_suit != TRUMP:
                newly_callable = True
                for ace in known_aces:
                    if ace.sheep_suit == potential_suit_match.sheep_suit:
                        newly_callable = False
                for callable_card in callable_cards:
                    if callable_card.sheep_suit == potential_suit_match.sheep_suit:
                        newly_callable = False
                if newly_callable:
                    callable_cards.append(Card(ACE, potential_suit_match.sheep_suit))
        if len(callable_cards) == 0:
            for suit_minus_one in range(3):
                suit_known = False
                for known_ace in known_aces:
                    if known_ace.sheep_suit == suit_minus_one + 1:
                        suit_known = True
                if not suit_known:
                    callable_cards.append(Card(ACE, suit_minus_one + 1))
            return callable_cards, True

        # Otherwise, can call normally
        else:
            return callable_cards, False
    
    def get_unknown_aces(hand: List[Card], buried: List[Card], hole: Card):
        unknown_aces = []
        for suit_minus_one in range(3):
            ace_known = False
            for card in hand + buried + hole:
                if card.value == ACE and card.sheep_suit == suit_minus_one:
                    ace_known = True
            if not ace_known:
                unknown_aces.append(Card(ACE, suit_minus_one + 1))
        return unknown_aces

    def playCard(self, current_trick_cards: List[Card], called_suit: int) -> Card:
        raise Exception("This player type doesn't know how to play")
    
    def get_playable_cards(self, led_card: Card) -> List[Card]:
        pass