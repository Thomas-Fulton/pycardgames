#!/usr/bin/env python
from components.deck import Deck


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = Deck()
        self.cards.empty()
        self.status = None
        self.money = 0
        self.player_pot = 0
        self.best_cards = None
