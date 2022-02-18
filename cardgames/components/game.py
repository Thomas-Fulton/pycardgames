#!/usr/bin/env python
"""Provides base Game class for the cardgames in games module."""

class Game:
    """Base class for a card game
    """
    def __init__(self):
        self.min_nplayers = None
        self.max_nplayers = None
        self.rules = str()  # read from file
