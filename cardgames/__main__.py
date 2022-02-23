#!/usr/bin/env python
import argparse
from cardgames.games import poker_game
from cardgames.games import snap_game



def create_parser():
    """
    Parses command line arguments for :py:func:`main()`
    :return: args
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--game', type=str, choices=['snap', 'poker'], help='Specify a game, either to start '
                                                                                  'up and play, or to read the game\'s '
                                                                                  'instructions')
    parser.add_argument('-l', '--loadout', type=str, default='new game', help='Resume a saved game (Not currently '
                                                                              'available)')
    parser.add_argument('-p', '--player', type=str, dest='players', action='append', help='Add a single player. (At '
                                                                                          'least two players with '
                                                                                          'unique names are required '
                                                                                          'for a game.)')
    # ='append' adds each occurrence of player to list of players
    parser.add_argument('-i', '--instructions', action='store_true', help='Print instructions for a specified '
                                                                          '<game>.')
    #args = parser.parse_args()
    #if args.instructions is True and args.game is None:
    #    parser.error('<game> required with --instructions: please specify for which game you would like\
    #    to display instructions.')

    
    # for arg in vars(args):
    #    print("{} is {}".format(arg, getattr(args, arg)))
    return parser


def main():
    """Launches game module using parsed command line arguments.
    """
    args = create_parser().parse_args()
    if args.instructions is True and args.game is None:
        args.error('<game> required with --instructions: please specify for which game you would like\
        to display instructions.')


    print("\n\n\n        Welcome to Python cardgames!\n\n\n")

    try:
        if args.game == "snap":
            print("Launching \'{}\'...\n\n\n".format(args.game))
            this_game = snap_game.SnapGame(args.loadout, args.players, args.instructions)

        elif args.game == "poker":
            print("Launching \'{}\'...\n\n\n".format(args.game))
            this_game = poker_game.PokerGame(args.loadout, args.players, args.instructions)

        else:
            print("(Use `--help` for further options)\n")

    except Exception as e:
        print("Game {} failed to launch: \n{}".format(args.game, e))
        raise


if __name__ == '__main__':
    import sys
    sys.exit(main())

# TODO bot automation
