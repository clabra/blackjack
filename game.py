from player import HumanPlayer, BotDealer, BotPlayer
import settings
import os
import time

class Game:
    """Abtract class"""
    def __init__(self):
        raise NotImplementedError()

    def play(self):
        """Make bets until user chips are exhausted """

        #############
        # Game loop #
        #############
        number_bets = 0
        print "###############"
        print "# Game starts #"
        print "###############"
        while self.player.chips > 0:
            self.play_hands()
            number_bets += 1
            #wants_exit = raw_input("> Press e for exit ").lower()
            #if wants_exit == 'e':
            #    break
            print "###############"
        print "#########################"
        print "# Game end with %s bets #" % (number_bets)
        print "#########################"

    def play_hands(self):
        """Play until one opponent wins """

        #############
        # First hand
        #############
        # Deal two cards to each opponent
        self.player.cards = self.dealer.deal(2)
        self.dealer.cards = self.dealer.deal(2)

        # Show hand
        self.player.show_hand()
        self.dealer.show_hand(1) # hide second card

        # End if player has blackjack
        if self.player.has_blackjack():
            self.end_bet()
            return

        #################################
        # Hand loop for player and dealer
        #################################
        opponents = [self.player, self.dealer]
        dealer_turn = 0 # 0: is player turn, 1: is dealer turn
        continue_bet = True
        round = 1
        # Bet
        self.player.chips -= self.player.chips_per_bet
        # Repeat until bet end condition
        while continue_bet:
            # Set who plays: player or dealer
            opponent = opponents[dealer_turn]
            continue_hand = True
            while (continue_hand):
                # Ask for action: hit or stand?
                action = opponent.choose_action()
                # If hit, deal cards and show hand
                if action == settings.ACTION_HIT:
                    opponent.cards.extend(self.dealer.deal())
                    opponent.show_hand()
                    # check end conditions
                    if opponent.has_blackjack() or opponent.has_busted():
                        continue_hand = False
                        continue_bet = False
                # If stand, it's dealer's turn
                elif action == settings.ACTION_STAND:
                    dealer_turn = 1 - dealer_turn # pass turn to other opponent
                    round+=1
                    continue_hand = False
                    # Player stands and dealer stands so end bet
                    if round == 4:
                        continue_bet = False
                else:
                    raise Exception("Unknown action: '%s'" % action)
        self.end_bet()

    def end_bet(self):
        """Payoff and print info about who wins and updated chips

        Called when a condition for bet end have been reached
        """
        message, result = self.payoff()
        print
        print "%s - Chips: %s" % (message, self.player.chips)
        # In learn mode, output results to file
        if self.results_file:
            with open(self.results_file, 'a') as f:
                f.write("%s\n" % result)
        return

    def payoff(self):
        """Check game state to set winner and update chips accordingly. Note the order to check conditions is important
        and shouldn't be changed without careful consideration

        Returns end condition message and final state. In learn mode, the last one is written to later processing
        """

        # Calculate hand values only one time
        player_hand_value = self.player.hand_value
        dealer_hand_value = self.dealer.hand_value

        #######################################
        # Check next conditions, in this order
        #######################################

        # If the player has a blackjack he receives 2.5 times his bet (making a profit of 1.5 times)
        if player_hand_value == settings.BLACKJACK_VALUE:
            self.player.update_chips(settings.PAYOFF_BLACKJACK)
            return "Player blackjack!", "BJ"

        # If the player busted, he lost his bet.
        if player_hand_value  > settings.BLACKJACK_VALUE:
            self.player.update_chips(settings.PAYOFF_LOST)
            return "Player busted!", "B"

        # If the dealer busted, he lost and pays to the player double his bet (the player makes a profit equal to his bet)
        if dealer_hand_value > settings.BLACKJACK_VALUE:
            self.player.update_chips(settings.PAYOFF_WIN)
            return "Dealer busted!", "B"

        # If the value of dealer's hand is greater than player's the player loses his bet.
        if dealer_hand_value > player_hand_value and dealer_hand_value != settings.BLACKJACK_VALUE:
            self.player.update_chips(settings.PAYOFF_LOST)
            return "Player loses!", "L"

        # If the value of player's hand is greater than dealer's the player won and dealer pays double her bet.
        if player_hand_value > dealer_hand_value:
            self.player.update_chips(settings.PAYOFF_WIN)
            return "Player wins!", "W"

        # If the dealer has blackjack and the player has non-blackjack, the dealer wins.
        if dealer_hand_value == settings.BLACKJACK_VALUE:
            self.player.update_chips(settings.PAYOFF_LOST)
            return "Dealer blackjack", "DBJ"

        # If the value of the two hands is equal, there is a push and the player gets back her bet money. He has no profit no loss.
        if player_hand_value == dealer_hand_value:
            self.player.update_chips(settings.PAYOFF_PUSH)
            return "Push!", "PU"

        raise Exception("Unknown payoff for current game state")


class PlayGame(Game):
    """Game mode in which user plays against the bot. The bot plays dealer role"""
    def __init__(self):
        # Set player and dealer
        self.player = HumanPlayer() # user is the player
        self.dealer = BotDealer() # program is the dealer


class LearnGame(Game):
    """Game mode in which the bot ask for a hand and advice the user about the best choice to play that hand (stand or hit)

    Bot use a policy calculated using Markov Decision Processes (MDP) theory"""
    def __init__(self, policy):
        # Set player and dealer
        self.dealer = BotDealer()
        self.player = BotPlayer(policy, self.dealer)
        if settings.learn_results:
            # Get unique filename
            self.results_file = os.path.join(settings.learn_results, "learn_" + str(int(time.time())) + ".data")

