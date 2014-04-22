"""Blackjack policy

Strategy used for the program to play the game
"""
import pprint
import settings

class Policy:

    def __init__(self, file):
        self.data = {}
        self._read(file)

    def _read(self, file):
        """Read file config with policy data in format:
        player_hand_value, dealer_faceup_card, action_to_choice
        4,11,'h'
        ...
        and creates a dictionary of dictionaries with those data: {'4': {'9': 'h'}, ...}. Numpy should be useful but I
        want minimize dependencies
        """
        with open (file , 'r') as f:
            policy = {}
            for line in f:
                line = line.strip()
                player_hand_value, dealer_faceup_value, action = line.split(',')
                if player_hand_value in self.data.keys():
                    row = self.data[player_hand_value]
                    row[dealer_faceup_value] = action
                else:
                    self.data[player_hand_value] = {}
                    row = self.data[player_hand_value]
                    row[dealer_faceup_value] = action
                self.data[player_hand_value] = row

    def action(self, player_hand_value, dealer_faceup_value):
        """Action is determined by the player hand value and the dealer face-up card value"""
        row = self.data[str(player_hand_value)]
        try:
            action = row[str(dealer_faceup_value)]
        except:
            # Todo
            action = settings.ACTION_STAND
        return action


