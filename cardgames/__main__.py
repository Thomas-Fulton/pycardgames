#!/usr/bin/env python

from games import snap_game
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', '-g', type=str, choices=['snap', 'speed'])
    parser.add_argument('--loadout', '-l', type=str, default='new game')
    parser.add_argument("--player", '-p', type=str, dest='players', action='append', help='Player name.')  # append each occurence of player to list of players
    parser.add_argument('--instructions', '-i', action='store_true', help='Displays instructions for a specified game')
    args = parser.parse_args()
    if args.instructions is True and args.game is None:
        parser.error('<game> required with --instructions: please specify for which game you would like\
         instruction.')
    for arg in vars(args):
        print("{} is {}".format(arg, getattr(args, arg)))
    return args


def main():
    try:
        args = parse_args()
    except Exception as e:
        print("Arguments failed to parse: {}".format(e))
        raise

    try:
        print("launching {}".format(args.game))
        if args.game == "snap":
            try:
                game=snap_game.SnapGame(args.loadout, args.players, args.instructions)
            except Exception as e:
                print("Game {} failed: {}".format(args.game, e))
    except Exception as e:
        print(e)

#    def options(self) :
#        print("Options... \n Use \`--help\` to display options")


if __name__ == '__main__':
    import sys
    sys.exit(main())
