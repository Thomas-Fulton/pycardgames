#!/usr/bin/env python
import random


class Deck:
    """
    Simulates a deck of cards using lists.
    """
    def __init__(self):
        self.card_values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        self.card_suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
        self.all_cards = [(value, suit) for value in self.card_values for suit in self.card_suits]

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
                    print(e, pile)
                    pass



    def upturn(self, ncards):
        """
        :param ncards: The number of cards to turn over and display.
        :type ncards: int
        """
        for k in range(ncards):
            print("{} of {}".format(self.all_cards[k][0], self.all_cards[k][1]))

    def empty(self):
        """
        Clears all cards from :py:attr:`deck.all_cards` to create an empty deck.
        """
        self.all_cards.clear()
