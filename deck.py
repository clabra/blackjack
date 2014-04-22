from random import choice;
import settings

class Card:
    """All possible cards
    """

    (ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, KING, QUEEN, JACK, ACE) = [1,2,3,4,5,6,7,8,9,10,10,10,10, settings.ACE_SOFT_VALUE];


class Deck:
    """Infinite deck of cards

    Use INFINITE_DECK=False in settings.py to use a finite 52 cards deck.
    Todo: a more versatile option would be create two different subclasses for finite deck and infinite deck and use a
    constant in settings to customize number of decks when INFINITE_DECK=False
    """

    CARDS = [Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX, Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.KING, Card.QUEEN, Card.JACK, Card.ACE];

    def __init__(self):
        self.cards = dict.fromkeys(Deck.CARDS, 4); # 4 suits
        self.size = sum(self.cards.values());

    def draw(self, num_cards=1):
        """Draw cards

        Parameters
        ----------
        num_cards : int
            Number of cards to draw. Default = 1
        """
        cards_left = [c for c in self.cards.keys() if self.cards[c] > 0];
        cards_to_draw = [choice(cards_left) for i in range(num_cards)];

        if not settings.INFINITE_DECK:
            # Play with a finite 52 card deck
            for card in cards_to_draw:
                # remove card from left cards
                self.cards[c] = self.cards[card] - 1;

        return cards_to_draw;

    def __repr__(self):
        return self.cards;

    def __str__(self):
        return str(self.cards);

