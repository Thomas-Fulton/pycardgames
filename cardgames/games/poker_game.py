#!/usr/bin/env python
import itertools
from cardgames.components import game, deck, player


def check_value(message, val_min=0, val_max=None):
    """
    Prompts the user for input until the input value is within a specified range.

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
        # user playing game (not just reading instructions), so player is required
        assert (self.player_names is not None), "\n\nNo players have been specified: at least two players are required " \
                                                "to play. You can add a new player " \
                                                "using --player or -p flag.\n\n "
        self.nplayers = len(self.player_names)
        assert (self.nplayers > 1), "\n\nOnly one player has been specified: at least two players are required " \
                                    "to play. You can add a new player " \
                                    "using --player or -p flag.\n\n "
        print("Let's play Poker! You are playing with {} players: {}".format(self.nplayers, players))

        # Set attributes:
        self.buy_in = check_value(message="How much is the buy-in?\nInput: ")
        for p in self.player_names:
            initiated_player = player.Player(p)
            super(player.Player, initiated_player).__init__()
            initiated_player.money = self.buy_in
            self.players[p] = initiated_player
        self.deck = deck.Deck()
        self.deck.shuffle()
        self.community_cards = deck.Deck()
        self.community_cards.empty()
        self.pot_total = 0
        self.pot_min_to_call = 0
        self.big_blind = check_value("Please enter the value of the \"big blind\".The \"small blind\" "
                                     "will be half the value of the big blind\nInput: ")
        self.small_blind = int(self.big_blind / 2)
        print("\nThe big blind is £{}, and the small blind is £{}.".format(self.big_blind, self.small_blind))
        self.turn_counter = 0
        self.blind_rotation = len(self.player_names)
        self.cont = True
        self.best_cards = ["High Card", [(2, "Spades")]]  # worst card so comparable
        self.round_winner = None
        self.hand_ranks = {"Royal Flush": 1, "Straight Flush": 2, "Four-of-a-kind": 3, "Full House": 4, "Flush": 5,
                           "Straight": 6, "Triple": 7, "Two Pair": 8, "Pair": 9, "High Card": 10}
        self.split_with = None

        # New game until someone wins, or game is exited.
        while self.cont is True:
            self.next_game()
            while True:
                cont = input("\n\nWould you like to continue to the next game (y)? (Input \"Q\" to quit.)\nInput: "
                             "").lower()
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
        """Simulates one game of poker, consisting of five rounds (Preflop, Flop, Turn, River and Showdown).
        """
        self.turn_counter += 1

        # Setup new game: Deal player and community cards.
        self.deck.shuffle()
        print("\nNew Game of five rounds. \nDealing player cards...")
        player_cards = [self.players[p].cards.all_cards for p in self.players]
        self.deck.deal(2, player_cards, "top")
        print("\nDealing the first three community cards...")

        # rotate player order and blinds.
        self.player_names.insert(0, self.player_names.pop(self.nplayers - 1))
        print("\n{} is the big blind (£{}) for this round, and {} is the small blind (£{}). Adding blinds to the pot"
              "...".format(self.player_names[0], self.big_blind, self.player_names[1], self.small_blind))
        self.players[self.player_names[0]].money -= self.big_blind
        self.players[self.player_names[0]].player_pot += self.big_blind
        self.players[self.player_names[1]].money -= self.small_blind
        self.players[self.player_names[1]].player_pot += self.small_blind
        self.pot_min_to_call = self.big_blind
        self.pot_total = self.small_blind + self.big_blind

        # First round of bets: Preflop
        print("\nFirst round: PREFLOP")
        self.player_turns()

        # Second round of bets: Flop
        print("\n\nNext round: FLOP\nDealing the first three community cards:\n")
        self.deck.deal(3, [self.community_cards.all_cards], "top")
        self.community_cards.upturn(3)
        self.player_turns()

        # Third round of bets: Turn
        print("\n\nNext round: TURN\nDealing the fourth community card:\n")
        self.deck.deal(1, [self.community_cards.all_cards], "top")
        self.community_cards.upturn(1)
        self.player_turns()

        # Fourth round of bets: River
        print("\n\nNext round: RIVER\nDealing the final community card:\n")
        self.deck.deal(1, [self.community_cards.all_cards], "top")
        self.community_cards.upturn(1)
        self.player_turns()

        # Fifth round of bets: Showdown
        print("\n\nNext round: SHOWDOWN\nPlease reveal your cards.")
        self.reveal()
        print("\n\n{} won the round, and the pot (£{}) with a {}".format(self.round_winner, self.pot_total,
                                                                         self.best_cards[0]))
        # TODO check blind players have not lost all money/have enough to put in the blind for the next round.

        self.players[self.round_winner].money += self.pot_total
        self.pot_total = 0

        # Reset: Deal back player and community cards to deck
        self.pot_min_to_call = 0
        for n in self.player_names:
            p = self.players[n]
            p.player_pot = 0
            p.status = None
            p.cards.deal(2, [self.deck.all_cards], "bottom")
        self.community_cards.deal(5, [self.deck.all_cards], "bottom")
        self.best_cards = None
        self.round_winner = None

    def player_turns(self):
        """Iterates through list of player names, and checks each player's status to see if player has previously
        folded or gone all in before presenting the player with a choice of actions.
        """
        for n in self.player_names:
            p: player.Player = self.players[n]
            if p.status == "folded":
                print("\n\n{} has folded.\n".format(n))
                continue
            if p.status == "all in":
                print("\n\n{} has gone all in.\n".format(n))
                continue
            print("\n\n\n\nNext player:", n)
            self.player_choice(p)
        return self

    def player_choice(self, p):
        """Prints the player's options and asks each user for input to either: check, call, raise or fold. Adjusts the
        player's attributes and the game's attributes accordingly.

        :param p: player
        :type p: :py:class:`player.Player`
        :return: player
        :rtype: :py:class:`player.Player`
        """
        print("\nHere are the community cards so far:")
        self.community_cards.upturn(len(self.community_cards.all_cards))
        print("\n{}, here are your cards:".format(p.name))
        p.cards.upturn(2)

        # loop to make sure user input is valid, and that the player has enough money for the choice:
        while True:
            to_call = self.pot_min_to_call - p.player_pot
            choice = input("\n\nYou have put £{} into the pot so far, and have £{} remaining.\n"
                           "The minimum bet is at £{}: "
                           "£{} is needed from you to check/call. \nThere is a total of £{} in the pot."
                           "\n\nWould you like to check/call (c), raise (r), or fold (f)?\n"
                           "Input: ".format(p.player_pot, p.money, self.pot_min_to_call,
                                            to_call, self.pot_total)).lower()
            if choice == "r":
                if p.money <= self.pot_min_to_call:
                    print("\nYou do not have enough money to raise; please fold (f) or check/call (c).\n")
                    continue
                print("Minimum bet (to call): {}".format(self.pot_min_to_call))
                raise_by = check_value("By how much would you like to raise beyond the minimum bet?\nInput: ",
                                       val_min=0, val_max=(p.money - to_call))
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

    def reveal(self):
        """

        """
        for n in self.player_names:
            p: player.Player = self.players[n]
            if p.status == "folded":
                print("\n\n{} folded.\n".format(n))
                continue
            if p.status == "all in":
                print("\n\n{} has gone all in.\n".format(n))
                continue
            print("\n\n\n\nNext player:", n)
            p.cards.upturn(2)
            self.assess(p)

            if self.round_winner is None:
                self.round_winner = n
                self.best_cards = p.best_cards
            # if rank of player's hand is better (lower) than rank of the current winner's hand, replace
            # self.round_winner and self.best_cards with player's name and best cards

            if self.hand_ranks[p.best_cards[0]] < self.hand_ranks[self.best_cards[0]]:
                self.round_winner = n
                self.best_cards = p.best_cards
                self.split_with = None
            # if hand ranks are the same, compare best cards to find highest, and update current winner and best cards.
            elif self.hand_ranks[p.best_cards[0]] == self.best_cards[0]:
                if p.best_cards[1][0] > self.players[self.round_winner].best_cards[1][0]:
                    self.round_winner = n
                    self.best_cards = p.best_cards
                    self.split_with = None
                else:
                    # TODO (not working) current round_winner and p essentially have same hand: compare to find who
                    #  has the highest card
                    p_highest_card = 0
                    w_highest_card = 0
                    for i in p.cards.all_cards:
                        if i[0] > p_highest_card:
                            p_highest_card = i[0]
                        else:
                            continue
                    for i in self.players[self.round_winner].cards.all_cards:
                        if i[0] > w_highest_card:
                            w_highest_card = i[0]
                        else:
                            continue
                    if p_highest_card > w_highest_card:
                        self.round_winner = n
                        self.best_cards = p.best_cards
                        self.split_with = None
                    else:
                        self.split_with = n
            print("\n{} is currently winning the round with a {}".format(self.round_winner, self.best_cards[0]))

    def assess(self, p: player.Player):
        """Lists all pairwise combinations of the 5 community and 2 player cards, and uses the combinations to find
        all pairs, triples, and four-of-a-kinds, and sets the players best_cards attribute to the best hand the
        player has. TODO (Straights, flushes and full houses not calculated yet.)

        :param p: player
        :type p: player.Player
        """
        best_hand_status = None
        straight_totals = list()

        community_and_player_cards = p.cards.all_cards + self.community_cards.all_cards

        all_paired_combinations = list(itertools.combinations(community_and_player_cards, r=2))
        pairs = [(card1, card2) for card1, card2 in all_paired_combinations if card1[0] == card2[0]]
        sorted_pairs = sorted(pairs, key=lambda tup: tup[0], reverse=True)
        if len(sorted_pairs) == 1:
            best_pair = sorted_pairs[0]
            best_hand_status = "Pair"
            p.best_cards = [best_hand_status, best_pair]
        elif len(sorted_pairs) >= 2:
            best_hand_status = "Two Pair"
            p.best_cards = [best_hand_status, sorted_pairs]
        elif len(sorted_pairs) == 0:
            best_hand_status = "High Card"
            p.best_cards = [best_hand_status, community_and_player_cards]

        if best_hand_status == "pair" or best_hand_status == "two pair":
            all_triples_combinations = list(itertools.combinations(community_and_player_cards, r=3))
            triples = [(card1, card2, card3) for card1, card2, card3 in
                       all_triples_combinations if card1[0] == card2[0] and
                       card2[0] == card3[0]]
            sorted_triples = sorted(triples, key=lambda tup: tup[0], reverse=True)
            if sorted_triples:
                best_hand_status = "Triple"
                triple = [sorted_triples[0]]
                p.best_cards = [best_hand_status, triple]

        if best_hand_status == "Triple":
            all_quads_combinations = list(itertools.combinations(community_and_player_cards, r=4))
            quads = [(card1, card2, card3, card4) for card1, card2, card3, card4 in
                     all_quads_combinations if card1[0] == card2[0] and card2[0] == card3[0]
                     and card3[0] == card4[0]]
            sorted_quads = sorted(quads, key=lambda tup: tup[0], reverse=True)
            if sorted_quads:
                best_hand_status = "Four-of-a-kind"
                quads = [sorted_quads[0]]
                p.best_cards = [best_hand_status, quads]

        # Find straights: each card value (eg. Ace, 2, 3 etc.) is designated a numerical value, so that the sum of
        # any combination of card values is unique. All possible five card straights combinations can be identified
        # from the unique totals of any combination.
        unique_sum_values = [2 ** i for i in range(2, 15)]
        unique_total_dict = dict(zip(p.cards.card_values, unique_sum_values))  # Keys: range(2, 15), values: 2**keys

        # straight values.
        # Use remainders from 0 to 15 / 13 to get values of straights which loop from J,Q,K back to A,2 for example
        for n in range(0, 13):
            straight_values = [unique_total_dict[((i + n) % 13) + 2] for i in range(0, 5)]
            straight_totals.append(sum(straight_values))
        unique_player_comm_values = [unique_total_dict[i[0]] for i in community_and_player_cards]
        totals = [i for i in list(itertools.combinations(unique_player_comm_values, r=5)) if sum(i) in straight_totals]
        # straight_cards = [k for k, v in unique_total_dict if v in totals]
        # print(straight_cards)
        if totals:
            p.best_cards = ["Straight", totals]  # TODO cards not card values for a straight p.best_cards.

        # TODO full house
        # TODO flush
        # TODO Straight flush

        print(p.best_cards)


if __name__ == '__main__':
    game = PokerGame(loadout="new_game", players=["Tom", "Bot"], instructions=None)

# TODO bot automation
