from collections import deque
from Constants import *
from Deck import Deck, Card
from Player import Player
from PlayerTypes.RandomPlayer import RandomPlayer
from typing import List, Tuple

class Game:
    def __init__(self, player_types: List[int]):
        self.blind_or_buried = []    # Stores two cards
        self.tricks = [None] * 6   # Trickinfo objects
        self.deck = Deck()
        self.called_ace = None
        
        self.ordered_players = []    # Players in order, with dealer in position 0
        for player_type in player_types:
            if player_type == MANUAL:
                pass
            elif player_type == RANDOM:
                self.ordered_players.append(RandomPlayer(game=self, starting_money=5))
            elif player_type == ROBERT_M_STRUPP:
                pass
            elif player_type == MAUER:
                pass
        self.fixed_players = self.ordered_players

        # Unusual game types
        self.is_leaster = False
        self.double_on_the_bump = False
        self.picker_playing_alone = False
        self.called_ten = False
        self.unknown_ace = False

    def add_player(self, player):
        assert isinstance(player, Player)
        self.ordered_players.append(player)        

    def play_game(self, number_rounds):
        for round_number in range(number_rounds):
            self.deal()
            self.picking_phase()
            bad_guys_won, multiplier, leaster_winners = self.play_hand()
            if self.is_leaster:
                self.leaster_pay(leaster_winners)
            else:
                self.pay_up(bad_guys_won, multiplier)
            self.cleanup()

    def deal(self) -> None:
        self.deck.shuffleDeck()
        for player in self.ordered_players:
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
        self.blind_or_buried.append(self.deck.deal())
        self.blind_or_buried.append(self.deck.deal())
        for player in self.ordered_players:
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())

    def picking_phase(self):
        '''
        Assign roles and bury two
        '''
        self.called_ace = None
        someone_picked = False
        for player in self.ordered_players:
            player.role = GOOD_GUY
        for idx, player in enumerate(self.ordered_players):
            blind = self.blind_or_buried
            picked, buried = player.pick_or_pass(blind)
            if picked:
                someone_picked = True
                self.called_ace, hole = player.call_ace(blind)

                # printing
                called_suit_string = None
                if self.called_ace == None:
                    called_suit_string = 'I play alone'
                elif self.called_ace.sheep_suit == CLUBS:
                    called_suit_string = 'Clubs'
                elif self.called_ace.sheep_suit == SPADES:
                    called_suit_string = 'Spades'
                elif self.called_ace.sheep_suit == HEARTS:
                    called_suit_string = 'Hearts'
                print(f'Player {idx} picked')
                print('Called suit:', called_suit_string)

                self.blind_or_buried = buried
                self.hole = hole
                player.role = PICKER
                break
        if not someone_picked:
            self.is_leaster = True
        else:
            if self.called_ace == None:
                self.picker_playing_alone = True
            else:
                for idx, player in enumerate(self.ordered_players):
                    for card in player.hand:
                        if card == self.called_ace:
                            player.role = PARTNER
                            print(f'Player {idx} is the partner')
                            break

    def play_hand(self) -> Tuple[bool, int, List[Player]]:
        """
        Plays a hand of sheepshead with the given players, consisting of six tricks, 
        once dealing, picking, calling, has happenned
        """
        assert len(self.ordered_players) == 5 # make sure it is 5 handed

        players = deque(self.ordered_players)  # dequeue of players that updates who goes first each trick
        for i in range(6):  # play six tricks
            trick = self.play_trick(players) # Run the trick
            self.tricks[i] = trick # Record the trickinfo
            print(f'Trick taken by player {self.ordered_players.index(trick.taker)}')
            while players[0] != trick.taker:  # set the taker to be the next leader
                players.append(players.popleft())   # move the first item to the last

        if self.is_leaster:
            return None, None, self.determine_leaster_winner()
        else:
            bad_guys_win, multiplier = self.determine_hand_winner()  # figure out who won and how much to pay
            if bad_guys_win:
                print("Bad guys win")
            else:
                print("Good guys win")
            return(bad_guys_win, multiplier, [])

    def play_trick(self, players):
        """
        Play one trick
        """
        leader = players[0]
        cards_played = []
        for i in range(5):   # Each player plays a card
            card = players[i].playCard(cards_played, self.called_ace, self.is_leaster)   ####should eventually pass player
            print(f'Player {self.ordered_players.index(players[i])} played: {card}')
            cards_played.append(card)
        taker = players[self.determine_trick_winner(cards_played)] # determine off index of winning card
        taker.taken_cards += cards_played   # taker takes cards
        return TrickInfo(leader, taker, cards_played)

    def determine_trick_winner(self, cards: List[Card]):
        """
        Given cards, return index of winner
        """
        winning_card = cards[0]
        winning_index = 0
        for i, card in enumerate(cards[1:]):
            if card.beats(opponent=winning_card, led_card=cards[0]):
                winning_card = card
                winning_index = i + 1 # since only enumerating from cards[1]
        return winning_index
    
    def determine_hand_winner(self):
        
        """
        Count cards in taken_cards, determine whether bad guys win and what the points multiplier is
        """
        points = 0
        for player in self.ordered_players:
            if player.role == GOOD_GUY:
                for card in player.taken_cards:
                    points += card.points
        multiplier = 1
        if points < 32 or points > 88:  # no schneider
            multiplier *= 2
        if self.double_on_the_bump:
            multiplier *= 2
        return (points < 61, multiplier)

    def determine_leaster_winner(self) -> List[Card]:
        winning_players = []
        winning_points = 0
        for player in self.ordered_players:
            points = 0
            for card in player.taken_cards:
                points += card.points
            if points > winning_points:
                winning_points = points
                winning_players = [player]
            elif points == winning_points:
                winning_players.append(player)
        return winning_players

    def pay_up(self, bad_guys_win, multiplier):
        m = multiplier
        if bad_guys_win:
            m *= -1
        for player in self.ordered_players:
            if player.role == PICKER:
                if self.picker_playing_alone:
                    player.money -= (4 * m)
                else:
                    player.money -= (2 * m)
            elif player.role == PARTNER:
                player.money -= m
            elif player.role == GOOD_GUY:
                player.money += m

    def leaster_pay(self, winners):
        number_winners = len(winners)
        print("Leaster winners:", winners)
        for player in self.ordered_players:
            is_winner = False
            for winner in winners:
                if winner == player:
                    is_winner = True
                    player.money += 4 * self.double_on_the_bump / number_winners
            if not is_winner:
                player.money -= 1 * self.double_on_the_bump


    def cleanup(self):
        """
        After a hand, reset the cards. 
        """

        ## Reset Players Cards
        for player in self.ordered_players:
            self.deck.cards += player.taken_cards
            player.taken_cards = []
            player.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }
            player.played_cards = []
            player.role = None
            player.playing_alone = False

        ## Shuffle the deck
        self.deck.cards += self.blind_or_buried
        self.deck.shuffleDeck()

        ## Reset global info
        self.tricks = [None] * 6
        self.blind_or_buried = []
        self.called_ace = None
        self.picker_playing_alone = False
        self.is_leaster = False

        ## Shift the dealer
        first = self.ordered_players[0]
        self.ordered_players = self.ordered_players[1:]
        self.ordered_players.append(first)

    
class TrickInfo:
    def __init__(self, leader, taker, cards_played):
        self.leader = leader
        self.taker = taker
        self.cards_played = cards_played


