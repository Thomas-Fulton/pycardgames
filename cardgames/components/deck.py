#!/usr/bin/env python
import random


class Deck:
    def __init__(self):
        self.card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.card_suits = ["diamonds", "hearts", "clubs", "spades"]
        self.all_cards = [(value, suit) for value in self.card_values for suit in self.card_suits]

    def shuffle(self):
        random.shuffle(self.all_cards)  # random shuffle

    def deal(self, ncards, destinations, location):
        '''
        Takes cards from the top of deck, and deals to either the top of bottom of the deck/s listed in destinations
        '''
        for pile in destinations:
            for n in range(ncards):
                if location == "top":
                    pile.insert(0, self.all_cards.pop(0))
                elif location == "bottom":
                    pile.append(self.all_cards.pop(0))

    def upturn(self, ncards):
        print(self.all_cards[0:ncards])

    def empty(self):
        self.all_cards.clear()
