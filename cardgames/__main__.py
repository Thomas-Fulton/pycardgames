import games
import argparse

parser = argparse.ArgumentParser(prog="simple_predict")
parser.add_argument('--game', '-g', type=str),
parser.add_argument('--loadout', '-l', type=str),
parser.add_argument("nplayers", type=int)
args = parser.parse_args()

def main() :
    def __init__(self, game, loadout, nplayers) :
        if game == "snap" :
            games.snap_game()
        elif game == None :
            main.options()

    def options(self) :
        print("Options... \n Use \`--help\` to display options")


if __name__ == '__main__':
    main(**vars(args))
