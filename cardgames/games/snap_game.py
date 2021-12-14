from ..components import game, deck


class snap_game(game) :
    def __init__(self, nplayers):
        print("Welcome to Snap! You are playing with {} players.\n Let's deal!".format(nplayers))
        cards = deck
        cards.shuffle()
        cards.deal(nplayers, "all")
