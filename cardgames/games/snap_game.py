#!/usr/bin/env python

from components import game, deck


class SnapGame(game.Game):
    def __init__(self, loadout, players, instructions):
        self.loadout = loadout
        self.players = players
        self.instructions = instructions
        nplayers = len(players)
        print("Let's play Snap! You are playing with {} players: {}".format(nplayers, players[1:]))

    def setup_game(self, loadout, players, instructions):
        print("Starts the game. Let's deal!")
        # for player in players:
        #    player=deck.player
        # cards = deck.Deck()
        # cards.shuffle()
        # cards.deal(self.players, "all")
