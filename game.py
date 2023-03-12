from collections import deque
from Constants import *
from Player import Player

class Game:
    def __init__(self):
        self.blind = [None] * 2    # Stores two cards
        self.ordered_players = list[Player]    # Players in order, with dealer in position 0
        self.tricks = [None] * 6   # Trickinfo objects
        self.double_on_the_bump = False

    def add_player(self, player):
        assert isinstance(player, Player)
        self.ordered_players.append(player)

    def play_hand(self):
        """
        Plays a hand of sheepshead with the given players, consisting of six tricks, 
        once dealing, picking, calling, has happenned
        """
        assert len(self.ordered_players == 5) # make sure it is 5 handed

        players = deque(self.ordered_players)  # dequeue of players that updates who goes first each trick
        for i in range(6):  # play six tricks
            trick = self.play_trick(players) # Run the trick
            self.tricks[i] = trick # Record the trickinfo 
            while players.front() != trick.taker:  # set the taker to be the next leader
                players.append(players.popleft())   # move the first item to the last

        bad_guys_win, multiplier = self.determine_hand_winner()  # figure out who won and how much to pay
        self.pay_up(bad_guys_win, multiplier)
        self.cleanup()   # Reset for next hand

    def pay_up(self, bad_guys_win, multiplier):


    def cleanup(self):
        """
        After a hand, reset the cards. 
        """

        ## Reset Players Cards
        for player in self.ordered_players:
            player.taken_cards = []
            player.public_empty_suits = {
            TRUMP: False, 
            CLUBS: False, 
            SPADES: False, 
            HEARTS: False
        }
            player.played_cards = []
            player.role = None

        ## Reset global info
        self.tricks = [None] * 6
        self.blind = set()

        ## Shift the dealer
        first = self.ordered_players[0]
        self.ordered_players = self.ordered_players[1:]
        self.ordered_players.append(first)

    def determine_hand_winner(self):
        """
        Count cards in taken_cards, determine whether bad guys win and what the points multiplier is
        """
        points = 0
        for player in self.players:
            if player.role == 'Good Guy':
                for card in player.taken_cards:
                    points += card.value
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
            card = players[i].play_card(players, cards_played)   ####align this code
        taker = players[self.determine_trick_winner(cards_played)] # determine off index of winning card
        taker.taken_cards += cards_played   # taker takes cards
        trick = Trickinfo(leader, taker, cards_played)
        return trick
    
class Trickinfo:
    def __init__(self, leader, taker, cards_played):
        self.leader = leader
        self.taker = taker
        self.cards_played = cards_played

