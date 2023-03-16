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
        self.hole = None
        self.played_cards = []
        self.taken_cards = []
        self.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card], Card, Card]: # picked, buried, called ace, hole
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
    
    def get_unknown_aces(self, hand: List[Card], buried: List[Card]):
        unknown_aces = []
        for suit_minus_one in range(3):
            ace_known = False
            for card in hand + buried + (self.hole):
                if card.value == ACE and card.sheep_suit == suit_minus_one:
                    ace_known = True
            if not ace_known:
                unknown_aces.append(Card(ACE, suit_minus_one + 1))
        return unknown_aces

    def playCard(self, current_trick_cards: List[Card], called_ace: Card) -> Card:
        raise Exception("This player type doesn't know how to play")
    
    def get_playable_cards(self, led_card: Card, called_ace: Card) -> List[Card]:
        
        # If leading, play any card
        if led_card == None:
            return self.hand

        # Partner must play called ace if its suit is led
        if self.role == PARTNER:
            for card in self.hand:
                if card == called_ace and led_card.sheep_suit == called_ace.sheep_suit:
                    return [card]
        
        # Picker must play hole card on unknown ace when called suit led
        # Picker can't play their last fail of the called suit unless the called suit is led or its last card in hand
        if self.role == PICKER:
            
            # Hole card on unknown ace
            if self.playing_alone:
                if led_card.sheep_suit == called_ace.sheep_suit:
                    return self.hole
                
            # Hole if hand empty
            if len(self.hand) == 0:
                return self.hole

            # Can't play last fail usually
            qty_cards_in_called_suit = 0
            for card in self.hand:
                if card.sheep_suit == called_ace.sheep_suit:
                    qty_cards_in_called_suit += 1
            if qty_cards_in_called_suit == 1 and len(self.hand) > 1:
                playable_cards = []
                for card in self.hand:
                    if card.sheep_suit != called_ace.sheep_suit:
                        playable_cards.append(card)
                return playable_cards
        
        # If have cards of led suit, need to play them
        playable_cards = []
        for card in self.hand:
            if card.sheep_suit == called_ace.sheep_suit:
                playable_cards.append(card)
        if len(playable_cards) > 0:
            return playable_cards
        
        # Partner can't play called ace unless it is led or last card
        if self.role == PARTNER:
            playable_cards = self.hand
            for card in playable_cards:
                if card == called_ace:
                    playable_cards.remove(card)
            return playable_cards

        # Otherwise, play any card
        return self.hand