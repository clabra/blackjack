# Game rules
BLACKJACK_VALUE = 21
CHIPS_START = 100
CHIPS_PER_BET = 1
ACTION_HIT = 'h'
ACTION_STAND = 's'
INFINITE_DECK = True # if False, a 52 cards deck is used
# Dealer stands if his hand value is this or more
DEALER_STAND_THRESHOLD = 17
# ace value in soft hands
ACE_SOFT_VALUE = 11
# Payoffs
PAYOFF_BLACKJACK = 2.5
PAYOFF_LOST = 0
PAYOFF_WIN = 2
PAYOFF_PUSH = 1

# Directory for learn results
learn_results = 'learn_results'