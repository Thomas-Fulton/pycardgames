#!/usr/bin/env python
"""Contains class :Class Deck:: to simulate a deck of cards."""

import random


class Deck:
    """Attributes simulate a deck of cards, and methods simulate some common actions like shuffling and dealing.
    """
    def __init__(self):
        self.card_values = range(2, 15) # ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.card_suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
        self.all_cards = [(value, suit) for value in self.card_values for suit in self.card_suits]
        '''List of tuples: each tuple represents one card (value, suit) currently in the deck.
        
        :rtype: list(tuple)
        '''

    def shuffle(self):
        """
        Randomly reorders :py:attr:`Deck.all_cards` attribute.
        """
        random.shuffle(self.all_cards)  # random shuffle

    def deal(self, ncards, destinations, location):
        """
        Takes cards from the top of deck, and deals to either the top or bottom of the deck/s listed in destinations

        :param ncards: number of cards to deal
        :type ncards: int
        :param destinations: list of :py:attr:`deck.Deck.all_cards` decks for the cards to be delt to.
        :type destinations: list
        :param location: Specifies to deal to the "Top" or "Bottom" of the destination decks
        :type location: str
        """
        for n in range(ncards):
            for pile in destinations:
                try:
                    if location == "top":
                        pile.insert(0, self.all_cards.pop(0))
                    elif location == "bottom":
                        pile.append(self.all_cards.pop(0))
                except Exception as e:
                    print(e)
                    pass



    def upturn(self, ncards):
        """Turns over ncards number of cards to reveal the value and suit.

        :param ncards: The number of cards to turn over and display.
        :type ncards: int
        """
        for k in range(ncards):
            if self.all_cards[k][0] in range(2, 11):
                card_value_name = self.all_cards[k][0]
            elif self.all_cards[k][0] == 11:
                card_value_name = "Jack"
            elif self.all_cards[k][0] == 12:
                card_value_name = "Queen"
            elif self.all_cards[k][0] == 13:
                card_value_name = "King"
            elif self.all_cards[k][0] == 14:
                card_value_name = "Ace"
            print("    {} of {}".format(card_value_name, self.all_cards[k][1]))

    def empty(self):
        """
        Clears all cards from :py:attr:`deck.all_cards` to create an empty deck.
        """
        self.all_cards.clear()

    def order(self):
        """Reorders the deck (ascending). Suit order is random.
        """
        self.all_cards.sort(key=lambda card_val: card_val[0])


