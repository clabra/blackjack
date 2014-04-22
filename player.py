"""Blackjack dealer bot"""

from deck import Deck, Card
import settings
import math
from policy import Policy

class Opponent(object):
    """Abstract class for which Player and Dealer have in common"""

    def __init__(self):
        self.cards = []

    # Abstract method
    def choose_action(self):
        raise NotImplementedError()

    @property
    def hand_value(self):
        """Ace should count as 11 or 1 following next blackjack rule: the values of the aces in a hand are such that they
        produce the highest value that is 21 or under (if possible). A hand where any ace is counted as 11 is called a
        soft hand
        """
        # Transform aces in 1's until hand value <= 21
        num_cards = len(self.cards)
        while (sum(self.cards) > 21 and Card.ACE in self.cards):
            for i in range(0, num_cards):
                if self.cards[i] == Card.ACE:
                    self.cards[i] = Card.ONE
                    break
        return sum(self.cards)

    def has_blackjack(self):
        if self.hand_value == settings.BLACKJACK_VALUE:
            return True
        return False

    def has_busted(self):
        if self.hand_value > settings.BLACKJACK_VALUE:
            return True
        return False

    def player_name(self):
        raise NotImplementedError()

    def show_hand(self, number_cards=None):
        """Show hand cards"""
        # Note: hand_value is not showed when number_cards arguments is given
        if number_cards:
            hand =  "%s %s" % (self.player_name(), self.cards[:number_cards])
        else:
            hand = self.__str__()
        print hand

    def show_action(self, action):
        """Show chosen action. Used to show dealer's choice"""
        if action == settings.ACTION_HIT:
            print "%s %s" % (self.player_name(), "hits")
        elif action == settings.ACTION_STAND:
            print "%s %s" % (self.player_name(), "stands")
        else:
            raise Exception("Unknown action")

    def __repr__(self):
        return "%s %s" % (self.__class__, self.cards)

    def __str__(self):
        if settings.ACE_SOFT_VALUE in self.cards:
            return "%s %s Soft %s" % (self.player_name(), self.hand_value, self.cards)
        else:
            return "%s %s %s" % (self.player_name(), self.hand_value, self.cards)


class Player(Opponent):
    """Abstract class for Player opponent. Player (human or bot) has chips to bet
    """
    def player_name(self):
        return 'P'

    def __init__(self):
        super(Player, self).__init__()
        self.chips = settings.CHIPS_START
        self.chips_per_bet = settings.CHIPS_PER_BET

    def update_chips(self, add_times_the_bet):
        self.chips += settings.CHIPS_PER_BET * add_times_the_bet

class HumanPlayer(Player):
    """Player when played by user
    """
    def choose_action(self):
        """Ask choice to user: hit or stand"""
        choice = ''
        while choice not in [settings.ACTION_HIT, settings.ACTION_STAND]:
            choice = raw_input("> What is your choice: hit or stand (%s/%s)? " % (settings.ACTION_HIT, settings.ACTION_STAND))

        return choice


class BotPlayer(Player):
    """Player when played by program

    Action to take for a hand is decided according to a policy. At first, the policy is based in MDP
    """
    def __init__(self, policy, dealer):
        super(BotPlayer, self).__init__()
        self.policy = Policy(policy)
        self.dealer = dealer

    def choose_action(self):
        # Policy determines choice
        choice = self.policy.action(self.hand_value, self.dealer.cards[0])
        return choice


class Dealer(Opponent):
    """Abtract class. Dealer, besides be a opponent, has a deck and deal cards"""

    def player_name(self):
        return 'D'

    def __init__(self):
        super(Dealer, self).__init__()
        self.deck = Deck()

    def deal(self):
       raise NotImplementedError()


class BotDealer(Dealer):
    def deal(self, number_cards=1):
        """Return cards dealt to player

        Parameters
        ----------
        number_cards : int
            Number of cards to deal
        """
        cards = self.deck.draw(number_cards)
        return cards


    def choose_action(self):
        """Deterministic policy: the dealer hits until his hand value is 17 or greater
        """
        if self.hand_value < settings.DEALER_STAND_THRESHOLD:
            return settings.ACTION_HIT
        else:
            return settings.ACTION_STAND