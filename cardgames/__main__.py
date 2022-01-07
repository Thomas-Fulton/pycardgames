#!/usr/bin/env python
from games import poker_game
from games import snap_game
import argparse


def parse_args():
    """
    Parses command line arguments for :py:func:`main()`
    :return: args
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', '-g', type=str, choices=['snap', 'poker'])
    parser.add_argument('--loadout', '-l', type=str, default='new game')
    parser.add_argument('--player', '-p', type=str, dest='players', action='append', help='Player name.')  # append each occurence of player to list of players
    parser.add_argument('--instructions', '-i', action='store_true', help='Display instructions for a specified game')
    args = parser.parse_args()
    if args.instructions is True and args.game is None:
        parser.error('<game> required with --instructions: please specify for which game you would like\
         to display instructions.')
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))
    return args


def main():
    """
    Launches game module using parsed command line arguments.
    """
    args = parse_args()
    try:
        if args.game == "snap":
            print("Launching {}\n\n\n".format(args.game))
            this_game = snap_game.SnapGame(args.loadout, args.players, args.instructions)

        elif args.game == "poker":
            print("Launching {}...\n\n\n".format(args.game))
            this_game = poker_game.PokerGame(args.loadout, args.players, args.instructions)

    except Exception as e:
        print("Game {} failed: {}".format(args.game, e))
        raise

#    def options(self) :
#        print("Options... \n Use \`--help\` to display options")


if __name__ == '__main__':
    import sys
    sys.exit(main())

# TODO bot automation
