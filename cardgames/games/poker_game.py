#!/usr/bin/env python
from components import game, deck, player


class PokerGame(game.Game):
    """A class to simulate a game of poker.
    """

    def __init__(self, loadout, players, instructions):
        super().__init__()
        self.loadout = loadout
        self.player_names = players
        self.players = {}
        self.instructions = instructions
        if instructions is True:
            print("(Instructions would now be printed)")
        else:
            # user playing game (not just reading instructions), so player is required
            assert (self.player_names is not None), "At least one player is required to play. You can add a new " \
                                                    "player using --player"
        # TODO catch excetpion if no players added
        self.nplayers = len(self.player_names)
        print("Let's play Poker! You are playing with {} players: {}".format(self.nplayers, players))

        # Set attributes:
        self.buy_in = self.check_value(message="How much is the buy-in?\nInput: ")
        for p in self.player_names:
            initiated_player = player.Player(p)
            super(player.Player, initiated_player).__init__()
            initiated_player.money = self.buy_in
            # initiated_player.status = None
            self.players[p] = initiated_player
        self.deck = deck.Deck()
        self.deck.shuffle()
        self.community_cards = deck.Deck()
        self.community_cards.empty()
        self.pot_total = 0
        self.pot_min_to_call = 0
        self.big_blind = self.check_value("Please enter the value of the \"big blind\".The \"small blind\" "
                                          "will be half the value of the big blind\nInput: ")
        self.small_blind = self.big_blind / 2
        print("\nThe big blind is £{}, and the small blind is £{}.".format(self.big_blind, self.small_blind))
        self.turn_counter = 0
        self.blind_rotation = len(self.player_names)
        self.cont = True

        # New game until someone wins, or game is exited.
        while self.cont is True:
            self.next_game()
            while True:
                cont = input("\n\nWould you like to continue to the next game (y)? (Input \"Q\" to quit.)\nInput: ").lower()
                if cont == "y":
                    break
                elif cont == "q":
                    self.cont = False
                    # save game?
                    # Print final winnings
                    break
                else:
                    print("\nInvalid response, please try again:")
                    continue

        print("\n\nThank you for playing poker!")


    def next_game(self):
        """
        Simulates one game of poker, consisting of five rounds (Preflop, Flop, Turn, River and Showdown).
        """
        self.turn_counter += 1

        # Setup new game: Deal player and community cards.
        print("\nNew Game of five rounds. \n Dealing player cards...\n\n")
        player_cards = [self.players[p].cards.all_cards for p in self.players]
        self.deck.deal(2, player_cards, "top")
        print("Dealing the first three community cards...")
        self.community_cards.deal(3, self.community_cards.all_cards, "top")

        # rotate player order and blind
        self.player_names.insert(0, self.player_names.pop(self.nplayers - 1))
        print("{} is the big blind, and {} is the small blind. Adding blinds to the pot".format(self.player_names[0],
                                                                                                self.player_names[1]))
        self.players[self.player_names[0]].money -= self.big_blind
        self.players[self.player_names[0]].player_pot += self.big_blind
        self.players[self.player_names[1]].money -= self.small_blind
        self.players[self.player_names[1]].player_pot += self.small_blind
        self.pot_min_to_call = self.big_blind
        self.pot_total = self.small_blind + self.big_blind

        # First round of bets: Preflop
        print("First round: Preflop")
        for n in self.player_names:
            print("\n\n\n\n\nNext player:", n)
            p = self.players[n]
            if p.status == "folded":
                print("\n\n {} has folded.\n")
                continue
            if p.status == "all in":
                print("\n\n{} has gone all in.\n".format(n))
                continue
            self.player_choice(p)

        # Second round of bets: Flop
        print("\n\nNext round: Flop\nHere are the first three community cards:\n\n")
        self.community_cards.upturn(3)
        for n in self.player_names:
            p = self.players[n]
            if p.status == "folded":
                print("\n\n{} has folded.\n".format(n))
                continue
            if p.status == "all in":
                print("\n\n{} has gone all in.\n".format(n))
                continue
            print("\n\nNext player:", n)
            self.player_choice(p)

        # Third round of bets: Turn

        # Fourth round of bets: River

        # Fifth round of bets: Showdown

        # Deal back player and community cards to deck

    def player_choice(self, p):
        """
        Prints the player's options and asks each user for input to check, call, raise or fold. Adjusts the player's
        attributes and the game's attributes accordingly.

        :param p: player
        :type p: :py:class:`player.Player`
        :return: player
        :rtype: :py:class:`player.Player`
        """
        print("\n\n{}, here are your cards:".format(p.name))
        p.cards.upturn(2)
        print(p.cards.all_cards)

        while True:
            to_call = self.pot_min_to_call - p.player_pot
            choice = input("\n\nYou have put £{} into the pot so far, and have £{} remaining. "
                           "The amount needed in the pot from each player in order to match the bet is £{}; "
                           "in order to check/call, you must bet £{}. There is a total of £{} in the pot."
                           "\n\nWould you like to check/call (c), raise (r), or fold (f)?\n"
                           "Input: ".format(p.player_pot, p.money, self.pot_min_to_call,
                                            to_call, self.pot_total)).lower()
            if choice == "r":
                if p.money <= self.pot_min_to_call:
                    print("\nYou do not have enough money to raise; please fold (f) or check/call (c).\n")
                    continue
                raise_by = self.check_value("By how much would you like to raise from the minimum bet?",
                                            val_min=self.pot_min_to_call, val_max=p.money)
                p.money -= (raise_by + to_call)
                p.player_pot += (raise_by + to_call)
                self.pot_min_to_call += raise_by
                self.pot_total += (raise_by + to_call)
                p.status = "raised"
                break
            elif choice == "c":
                if p.money <= to_call:
                    nchoice = input("You do not have enough remaining to match the call; do you want to go all in (a)"
                                    ", or fold (f)? ").lower()
                    if nchoice == "a":
                        p.player_pot += p.money
                        p.money = 0
                        self.pot_total += p.money
                        p.status = "all in"
                        break
                    elif nchoice == "f":
                        pass
                    else:
                        print("Invalid selection, please try again.")
                        continue
                p.money -= to_call
                p.player_pot += to_call
                self.pot_total += to_call
                p.status = "called"
                break
            elif choice == "f":
                p.status = "folded"
                # self.raise_in_round = True (go round players again to call/fold).
                break
            else:
                print("(Invalid selection, please try again.)")
                continue

        return self

    def check_value(self, message, val_min=0, val_max=None):
        """
        Prompts the user for input and checks that the input value is within a specified range. Prompts again if
        the user input is outside the range of accepted values.

        :param message: Message which is printed to describe the requested value from the user.
        :type message: str
        :param val_min: minimum value
        :type val_min: int
        :param val_max: maximum value
        :type val_max: int
        :return: returns integer within range of val_min and val_max
        :rtype: int
        """
        while True:
            try:
                value = int(input(message).strip())
            except ValueError:
                print("Please enter an integer.\n")
                continue

            if value < val_min:
                print("Sorry, your input is below the minimum ({}). Please try again:\n".format(val_min))
                continue
            if val_max is not None and value > val_max:
                print("Sorry, your input is above the maximum ({}) Please try again:\n".format(val_max))
                continue
            else:
                break
        return value


if __name__ == '__main__':
    game = PokerGame(loadout="new_game", players=["Tom", "Bot"], instructions=None)

# TODO bot automation
