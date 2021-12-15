from ..components import game, deck


class SnapGame(game.Game()):
    def __init__(self, loadout, players, instructions):
        nplayers = len(players)
        print("Let's play Snap! You are playing with {} players: {} \n Let's deal!".format(nplayers, players[1:]))
        cards = deck.Deck()
        cards.shuffle()
        cards.deal(players, "all")
