#!/usr/bin/env python
from ..components import game, deck, player


class PokerGame(game.Game):
    def __init__(self, loadout, players, instructions):
        self.loadout = loadout
        self.player_names = players
        self.players = []
        self.instructions = instructions
        if instructions is True:
            print("(Instructions would now be printed)")
        else:
            assert (self.player_names is not None), "At least one player is required to play. You can add a new player using --player"
            # print("Let's play Poker! You are playing with {} players: {}".format(len(self.player_names), players[1:]))
            # self.setup_game(loadout, players, instructions)
        self.buy_in = input("How much is the buy-in?")
        for p in self.player_names:
            initiated_player = player.Player(p)
            initiated_player.money = self.buy_in
            self.players.append(initiated_player)
        self.deck = deck.Deck()
        self.deck.shuffle()
        self.community_cards = deck.Deck()
        self.community_cards.empty()
        self.pot = 0
        self.big_blind = input("How much is the \"big blind\"?")
        self.small_blind = input("How much is the \"small blind\"?")
        self.blind_rotation = len(self.players)
        while True:
            self.next_round()

    def next_round(self):
        print("Dealing player cards...")
        player_cards = [p.cards.all_cards for p in self.players]
        self.deck.deal(2, player_cards, "top")
        print("Dealing the first three community cards...")
        self.community_cards.deal(3, self.community_cards.all_cards, "top")

        self.blind_rotation = self.blind_rotation + 1
        print("{} is the big blind. Adding blind to the pot")

        for n in self.blind_rotation:
            p = self.players[n]
            print("Viewing {}'s cards:".format(p))
            p.cards.upturn(len(p.cards.all_cards))
            self.player_choice(p)

        self.community_cards.upturn(3)

    def player_choice(self, player):
        choice = input("Would you like to call (c), raise (r), or fold (f)?")
        if choice == "r":
            self.pot_aim = input("How much would you like to raise to?")

