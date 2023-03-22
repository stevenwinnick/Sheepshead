import Player
from Player import Player
from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING
from random import uniform
from MCSimulatedGame import *

if TYPE_CHECKING:
    from Game import Game

class MCTSPlayer(Player):
    def __init__(self, game: 'Game', starting_money: int, simulations: int = 10000) -> None:
        super().__init__(game, starting_money)
        self.simulations_per_move = simulations

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        
        ## Decide to pick or pass

        # Simulate picking and passing simulations_per_move / 2 times each and do the better one
        pick_wins = 0
        pass_wins = 0
        position = self.game.ordered_players.index(self)
        phase = CALLING_ACE # simulate what would happen if you picked
        picker_position = None
        called_ace = None
        leaster = False
        picker_playing_alone = False
        called_ten = False
        unknown_ace = False
        tricks_so_far = None
        current_trick = None

        simulated_pick_game = MCSimulatedGame(position, phase, picker_position, called_ace, leaster, picker_playing_alone, called_ten, unknown_ace, tricks_so_far, current_trick)
        for i in range(self.simulations_per_move / 2):
            if simulated_pick_game.simulate():
                pick_wins += 1

        phase = PICKING # simulate what would happen if you passed (still picking phase)
        simulated_pass_game = MCSimulatedGame(position, phase, picker_position, called_ace, leaster, picker_playing_alone, called_ten, unknown_ace, tricks_so_far, current_trick)
        for i in range(self.simulations_per_move / 2):
            if simulated_pass_game.simulate():
                pick_wins += 1
        


        # If pass, return blind
        if pass_wins > pick_wins:
            return False, blind

        ## If pick, decide which cards to bury and which ace to call

        # Get all possible combinations of buriable cards
        hand_plus_blind = self.hand + blind
        buriable_combinations = []
        for first_card in range(len(hand_plus_blind)):
            for second_card in range(first_card + 1, len(hand_plus_blind)):
                buriable_combinations.append((hand_plus_blind[first_card], hand_plus_blind[second_card]))
        
        # Get all possible next states
        buried_ace_pairs = []
        for buried in buriable_combinations:
            hand_if_bury_these = hand_plus_blind
            hand_if_bury_these.remove(buried[0])
            hand_if_bury_these.remove(buried[1])
            callable_aces, unknown_ace = self.get_callable_aces(hand_if_bury_these, buried)
            for callable_ace in callable_aces:
                buried_ace_pairs.append(hand_if_bury_these, buried, callable_ace, unknown_ace)
        
        game_tree = [(0, 0)] * len(buried_ace_pairs) # (w, N) pairs for each possible buried/called ace combo

        # Perform MCTS on game_tree

    def get_callable_aces(self, hand: List[Card], buried: List[Card]) -> Tuple[List[Card], bool]: # bool for if unknown ace, LIST MAY BE EMPTY
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