"""Blackjack bot by Concha Labra, April 2014

You can use this bot as:
- Dealer: computer takes dealer role. To play against it for fun
- Player: computer takes player role using given policy as strategy. See results generated to learn about optimal strategies


> python blackjack.py --help

usage: blackjack.py [-h] [-r role] [-p policy]

Bot to play blackjack. You can use the bot as dealer (to play against it for
fun) or as player (to learn the best strategy for a given set of rule).

optional arguments:
  -h, --help            show this help message and exit
  -r role, --role role  bot role. Must be one of [player, dealer]
  -p policy, --policy policy
                        strategy file. Default = policy.conf

> python blackjack.py -r dealer
> python blackjack.py -r player -p policy.conf
"""

import argparse
from game import PlayGame, LearnGame
import settings

def run(role, policy):
    """Run Game instance

    Parameters
    ----------
    role : str
        Bot role: 'dealer'|'mentor'
    """
    if role in ['dealer', 'd']:
        """Bot in dealer role"""
        game = PlayGame()
        game.play()
    else:
        """Bot in player role"""
        game = LearnGame(policy)
        game.play()


def main():
    """Init and run game using arguments given by user"""

    # Collect arguments
    parser = argparse.ArgumentParser(prog="blackjack.py", description="Bot to play blackjack.\
            You can use the bot as dealer (to play against it for fun) or as player (to learn the best strategy for a  \
            given set of rule).", epilog="By Concha Labra, April 2014");

    parser.add_argument('-r', '--role', metavar='role', type=str, choices=['player', 'dealer'],
                        help = 'bot role. Must be one of [%(choices)s] ')

    parser.add_argument('-p', '--policy', metavar='policy', type=str, help = 'strategy file. Default = policy.conf')

    args = parser.parse_args();


    if args.role:
        role = args.role
    else:
        role = raw_input("Which role do you want this blackjack bot to play?: \n  player (m): to learn how good is a given policy \n  dealer (d): to play against it for fun\n> Choose role (p/d): ")

    role = role.lower()
    policy = args.policy or 'policy.conf'

    if role in ['p', 'd', 'dealer', 'player']:
        # Let's play!
        run(role, policy);
    else:
        print "Incorrect option"


if __name__ == '__main__':
    main()

