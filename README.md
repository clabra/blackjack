Concha Labra, April 2014

This folder contains blackjack.py, a program that can be used as:
- dealer: for user to play against it interactively
- player: to learn optimal strategy for a given rules set

The game is played according to some basic rules. These rules, among others, can be changed in settings.py:
- There are one player and one dealer.
- The dealer hit until his hand value is 17 or greater.
- The player starts with 100 chips and bet 1 chip each hand.


HOW TO USE
----------
> python blackjack.py --help

usage: blackjack.py [-h] [-r role] [-p policy]

Bot to play blackjack. You can use the bot as dealer (to play against it for
fun) or as player (to learn the best strategy for a given set of rule).

optional arguments:
  -h, --help            show this help message and exit
  -r role, --role role  bot role. Must be one of [player, dealer]
  -p policy, --policy policy
                        strategy file. Default = policy.conf

PLAY MODE
---------
> python blackjack.py -r dealer

To play with the program interactively


LEARN MODE
----------
> python blackjack.py -r player -p policy.conf

To learn best strategy for given rules. Results are written to dir set in settings.learn_results dir


MACHINE_LEARNING
----------------
The program in his current state is the base for develop a machine learning system able to generate optimal policies to
play blackjack for a set of given rules using techniques such as Markov Decision Processes


FILES
-----
README.txt      -   this file
blackjack.py	-   main program
game.py         -   the game loop
player.py       -   opponents
deck.py		    -   cards, draw()
policy.py       -   used in learn mode to read policy from file
policy.conf     -   policy file
settings.py     -   configuration: game rules, directory for learn results, etc.
learn_results/  -   directory for result files


TRADE-OFFS
----------
1) For naming conventions PEP 8 - Style Guide is used
2) Code tries to remove as many dependencies as possible, making some trade-offs as:
- not use python's abc module to create abstract classes explicitly. Use it would require python version >= 2.6
- not use numpy for certain data manipulation