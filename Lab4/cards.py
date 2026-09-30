import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


def hand_value(hand):

    value = sum(11 if rank == "A" else 10 if rank in {"J", "Q", "K"} else int(rank)
                for rank, _ in hand)
    aces = sum(rank == "A" for rank, _ in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value
