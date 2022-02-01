#!/usr/bin/env python
from cardgames.components import game, deck, player


class SnapGame(game.Game):
    def __init__(self, loadout, players, instructions):
        self.loadout = loadout
        self.players = players
        self.instructions = instructions
        if instructions is True:
            print("Instructions would now be printed")
        else:
            assert(self.players is not None), "At least one player is required to play. You can add a new player using --player"
            #print("Let's play Snap! You are playing with {} players: {}".format(nplayers, players[1:]))
            self.setup_game(loadout, players, instructions)


    def setup_game(self, loadout, players, instructions):
        # for player in players:
        #    player=deck.player
        # cards = deck.Deck()
        # cards.shuffle()
        # cards.deal(self.players, "all")
        print("Starts the game. Let's deal!")
