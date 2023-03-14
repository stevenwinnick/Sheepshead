from collections import deque
from Constants import *
from Player import Player
from Deck import Deck, Card
from typing import List

class Game:
    def __init__(self, player_types: List[int]):
        self.blind = [None] * 2    # Stores two cards
        self.tricks = [None] * 6   # Trickinfo objects
        self.double_on_the_bump = False
        self.deck = Deck()
        self.called_suit = None
        
        self.ordered_players = []    # Players in order, with dealer in position 0
        for idx, player_type in enumerate(player_types):
            self.ordered_players.append(Player(player_type, starting_money=0, game=self))

    def play_game(self, number_rounds):
        for round_number in range(number_rounds):
            self.deal()
            self.picking_phase()
            self.play_hand()

    def deal(self) -> None:
        self.deck.shuffleDeck()
        for player in self.ordered_players:
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
        self.blind[0] = self.deck.deal()
        self.blind[1] = self.deck.deal()
        for player in self.ordered_players:
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())
            player.hand.append(self.deck.deal())

    def picking_phase(self):
        '''
        Assign roles and bury two
        '''
        called_suit = None
        for player in self.ordered_players:
            player.role = GOOD_GUY
        for idx, player in enumerate(self.ordered_players):
            blind = self.blind
            picked, buried = player.pick(blind)
            if picked:
                print(f'Player {idx} picked')
                called_suit = player.call_ace()
                called_suit_string = None
                if called_suit == CLUBS:
                    called_suit_string = 'Clubs'
                elif called_suit == SPADES:
                    called_suit_string = 'Spades'
                elif called_suit == HEARTS:
                    called_suit_string = 'Hearts'
                print('Called suit:', called_suit_string)
                self.blind = buried
                player.role = PICKER
                break
        self.called_suit = called_suit
        for idx, player in enumerate(self.ordered_players):
            for card in player.hand:
                if card.value == ACE and card.suit == called_suit:
                    player.role = PARTNER
                    print(f'Player {idx} is the partner')

    def add_player(self, player):
        assert isinstance(player, Player)
        self.ordered_players.append(player)

    def play_hand(self):
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

        bad_guys_win, multiplier = self.determine_hand_winner()  # figure out who won and how much to pay
        if bad_guys_win:
            print("Bad guys win")
        else:
            print("Good guys win")
        self.pay_up(bad_guys_win, multiplier)
        self.cleanup()   # Reset for next hand

    def pay_up(self, bad_guys_win, multiplier):
        m = multiplier
        if bad_guys_win:
            m *= -1
        for player in self.ordered_players:
            if player.role == PICKER:
                player.money -= (2 * m)
            elif player.role == PARTNER:
                player.money -= m
            elif player.role == GOOD_GUY:
                player.money += m


    def cleanup(self):
        """
        After a hand, reset the cards. 
        """

        ## Reset Players Cards
        for player in self.ordered_players:
            player.taken_cards = []
            player.public_empty_suits = {
            "Trump": False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }
            player.played_cards = []
            player.role = None

        ## Reset global info
        self.tricks = [None] * 6
        self.blind = []

        ## Shift the dealer
        first = self.ordered_players[0]
        self.ordered_players = self.ordered_players[1:]
        self.ordered_players.append(first)

    def determine_hand_winner(self):
        """
        Count cards in taken_cards, determine whether bad guys win and what the points multiplier is
        """
        points = 0
        for player in self.ordered_players:
            if player.role == 'Good Guy':
                for card in player.taken_cards:
                    points += card.points
        multiplier = 1
        if points < 32 or points > 88:  # no schneider
            multiplier *= 2
        if self.double_on_the_bump:
            multiplier *= 2
        return (points < 61, multiplier)

    def determine_trick_winner(self, cards):
        """
        Given cards, return index of winner
        """
        led_suit = cards[0].suit
        winning_card = cards[0]
        winning_index = 0
        for i, card in enumerate(cards[1:]):
            if card.beats(winning_card, led_suit):
                winning_card = card
                winning_index = i
        return winning_index

    def play_trick(self, players):
        """
        Play one trick
        """
        leader = players[0]
        cards_played = []
        for i in range(5):   # Each player plays a card
            card = players[i].playCard(cards_played, self.called_suit)   ####should eventually pass player
            print(f'Player {self.ordered_players.index(players[i])} played: {card}')
            cards_played.append(card)
        taker = players[self.determine_trick_winner(cards_played)] # determine off index of winning card
        taker.taken_cards += cards_played   # taker takes cards
        trick = TrickInfo(leader, taker, cards_played)
        return trick

    
class TrickInfo:
    def __init__(self, leader, taker, cards_played):
        self.leader = leader
        self.taker = taker
        self.cards_played = cards_played


