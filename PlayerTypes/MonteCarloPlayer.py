import Player
from Player import Player
from Deck import Card
from Constants import *
from typing import List, Tuple, TYPE_CHECKING
from random import uniform
from MCSimulatedGame import *
import random

if TYPE_CHECKING:
    from Game import Game

class MCTSPlayer(Player):
    def __init__(self, game: 'Game', starting_money: int, simulations: int = 10000) -> None:
        super().__init__(game, starting_money)
        self.simulations_per_move = simulations
        self.order_shift_from_fixed = self.game.fixed_players.index(self)
        self.ace_to_call = None
        self.u_a_hole = False

    def pick_or_pass(self, blind: List[Card]) -> Tuple[bool, List[Card]]:
        
        ## Decide to pick or pass

        # Simulate picking and passing simulations_per_move / 2 times each and do the better one
        pick_wins = 0
        pass_wins = 0
        phase = CALLING_ACE # simulate what would happen if you picked
        dealer_position = - self.game.ordered_players.index(self)
        picker_position = -1 # self is picker
        hand = self.hand
        buried = None
        called_ace = None
        hole_card = None
        leaster = False
        tricks_so_far = None
        current_trick = None

        simulated_pick_game = MCSimulatedGame(phase, dealer_position, picker_position, hand, buried, called_ace, hole_card, leaster, tricks_so_far, current_trick)
        for i in range(self.simulations_per_move / 2):
            if simulated_pick_game.simulate():
                pick_wins += 1

        phase = PICKING # simulate what would happen if you passed (still picking phase)
        picker_position += 1
        simulated_pass_game = MCSimulatedGame(phase, dealer_position, picker_position, hand, buried, called_ace, hole_card, leaster, tricks_so_far, current_trick)
        for i in range(self.simulations_per_move / 2):
            if simulated_pass_game.simulate():
                pass_wins += 1
        
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
        buried_called_combos = []
        for buried in buriable_combinations:
            hand_if_bury_these = hand_plus_blind
            hand_if_bury_these.remove(buried[0])
            hand_if_bury_these.remove(buried[1])
            callable_aces, unknown_ace_possible = self.get_callable_aces(hand_if_bury_these, buried)
            if unknown_ace_possible:
                for callable_ace in callable_aces:
                    for hole_card in self.hand:
                        buried_called_combos.append((hand_if_bury_these, buried, callable_ace, hole_card)) # these will be possible hole cards
            else:
                for callable_ace in callable_aces:
                    buried_called_combos.append((hand_if_bury_these, buried, callable_ace, None))
        
        game_tree = [(0, 0)] * len(buried_called_combos) # (w, N) pairs for each possible buried/called ace combo
        
        sim_games = []

        # Fill sim_games with instances of MCSimulatedGame objects matching game tree to simulate them later
        phase = PLAYING
        for hand, buried, ace, hole in buried_called_combos:
            sim_games.append(MCSimulatedGame(phase, dealer_position, picker_position, hand, buried, ace, hole, leaster, tricks_so_far, current_trick))

        # Perform MCTS on game_tree
        for i in range(self.simulations_per_move):
            sim_game_number = self.selection(game_tree)
            #sim_hand, sim_buried, sim_ace, sim_unknown = buried_called_combos[sim_game_number]
            won = sim_games[sim_game_number].simulate()
            if won:
                game_tree[sim_game_number][0] += 1
            game_tree[sim_game_number][1] += 1
        
        # Pick best move from tree and return
        max_win_rate = 0
        max_win_moves = []
        for idx, game_stats in enumerate(game_tree):
            win_rate = game_stats[0] / game_stats[1]
            if win_rate > max_win_rate:
                max_win_rate = win_rate
                max_win_moves = [buried_called_combos[idx]]
            elif win_rate == max_win_rate:
                max_win_moves.append(buried_called_combos[idx])

        if len(max_win_moves) == 1:
            hand, buried, ace, unknown = max_win_moves[0]
            self.ace_to_call = ace
            self.u_a_hole = unknown
            return True, buried
        else:
            hand, buried, ace, unknown = random.choice(max_win_moves)
            self.ace_to_call = ace
            self.u_a_hole = unknown
            return True, buried

    def selection(game_tree: List[Tuple[int, int]]) -> int: # returns index of selected game from game tree
        EXPLORATION_PARAMETER = 1
        max_win_rate = -1
        max_win_games = []
        for idx, wins, plays in enumerate(game_tree):
            cur_win_rate = wins / plays
            if cur_win_rate > max_win_rate:
                max_win_rate = cur_win_rate
                max_win_games = [idx]
            elif cur_win_rate == max_win_rate:
                max_win_games.append(idx)
        return random.choice(max_win_games)

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
        # Ace to call was already decided during pick or pass
        if self.u_a_hole:
            return None, self.u_a_hole
        else:
            return self.ace_to_call, None

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

        # Otherwise do Monte Carlo simulation to pick a card to play
        dealer_position = - self.game.ordered_players.index(self)
        picker_position = -1 # self is picker
        phase = PLAYING
        if self.role == PICKER:
            buried = self.game.blind_or_buried
        else:
            buried = None
        called_ace = self.game.called_ace
        hole_card = self.game.hole
        leaster = self.game.is_leaster
        tricks_so_far = self.game.tricks
        current_trick = current_trick_cards
        best_cards = []
        max_wins = -1
        for card in self.hand:
            cur_sim_trick = current_trick
            cur_sim_trick.append(card)
            cur_sim_hand = self.hand
            cur_sim_hand.remove(card)
            cur_sim_game = MCSimulatedGame(phase, dealer_position, picker_position, cur_sim_hand, buried, called_ace, hole_card, leaster, tricks_so_far, current_trick)
            wins = cur_sim_game.simulate(self.simulations / len(self.hand))
            if wins > max_wins:
                best_cards = [card]
                max_wins = wins
            elif max_wins == wins:
                best_cards.append(card)
        return random.choice(best_cards)