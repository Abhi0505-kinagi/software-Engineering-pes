import unittest
from unittest.mock import patch

from cards import Deck, hand_value
from game import Blackjack


class FixedDeck:
    def __init__(self, cards):
        self.cards = list(cards)

    def draw(self):
        return self.cards.pop(0) if self.cards else None


class HandValueTests(unittest.TestCase):
    def test_ace_stays_eleven_when_hand_does_not_bust(self):
        self.assertEqual(hand_value([("A", "S"), ("9", "H")]), 20)

    def test_ace_becomes_one_when_hand_would_bust(self):
        self.assertEqual(hand_value([("A", "S"), ("9", "H"), ("5", "C")]), 15)

    def test_multiple_aces_are_adjusted_as_needed(self):
        self.assertEqual(hand_value([("A", "S"), ("A", "H"), ("9", "C")]), 21)

    def test_all_aces_can_be_counted_as_one(self):
        self.assertEqual(hand_value([("A", "S"), ("A", "H"), ("A", "C")]), 13)


class BlackjackRoundTests(unittest.TestCase):
    def play_round(self, cards, responses):
        game = Blackjack()
        with patch("game.Deck", return_value=FixedDeck(cards)), \
                patch("builtins.input", side_effect=responses) as mocked_input, \
                patch("builtins.print"):
            result = game.round()
        return game, result, mocked_input

    def test_natural_blackjack_pays_three_to_two(self):
        cards = [("A", "S"), ("K", "H"), ("9", "C"), ("7", "D")]
        game, result, mocked_input = self.play_round(cards, ["10"])
        self.assertTrue(result)
        self.assertEqual(game.chips, 115)
        self.assertEqual(mocked_input.call_count, 1)

    def test_two_naturals_push(self):
        cards = [("A", "S"), ("K", "H"), ("A", "C"), ("Q", "D")]
        game, _, _ = self.play_round(cards, ["10"])
        self.assertEqual(game.chips, 100)

    def test_dealer_natural_beats_non_natural_hand(self):
        cards = [("10", "S"), ("7", "H"), ("A", "C"), ("K", "D")]
        game, _, mocked_input = self.play_round(cards, ["10"])
        self.assertEqual(game.chips, 90)
        self.assertEqual(mocked_input.call_count, 1)

    def test_player_bust_loses_wager(self):
        cards = [("10", "S"), ("8", "H"), ("9", "C"), ("7", "D"), ("5", "S")]
        game, _, mocked_input = self.play_round(cards, ["10", "h"])
        self.assertEqual(game.chips, 90)
        self.assertEqual(mocked_input.call_count, 2)

    def test_dealer_draws_and_busts(self):
        cards = [("10", "S"), ("9", "H"), ("10", "C"), ("6", "D"), ("8", "S")]
        game, _, _ = self.play_round(cards, ["10", "s"])
        self.assertEqual(game.chips, 110)

    def test_equal_totals_push(self):
        cards = [("10", "S"), ("8", "H"), ("10", "C"), ("8", "D")]
        game, _, _ = self.play_round(cards, ["10", "s"])
        self.assertEqual(game.chips, 100)

    def test_invalid_wagers_and_commands_do_not_change_balance(self):
        cards = [("10", "S"), ("8", "H"), ("10", "C"), ("8", "D")]
        game, _, mocked_input = self.play_round(cards, ["0", "101", "10", "invalid", "s"])
        self.assertEqual(game.chips, 100)
        self.assertEqual(mocked_input.call_count, 5)

    def test_settlement_is_applied_only_once(self):
        game = Blackjack()
        game._round_settled = False
        with patch("builtins.print"):
            game._settle(10, "win")
            game._settle(10, "win")
        self.assertEqual(game.chips, 110)

    def test_fractional_balance_below_minimum_wager_stops(self):
        game = Blackjack()
        game.chips = 0.5
        with patch("builtins.input") as mocked_input, patch("builtins.print"):
            game.run()
        mocked_input.assert_not_called()

    def test_empty_deck_before_deal_cancels_without_changing_balance(self):
        game, result, _ = self.play_round([], ["10"])
        self.assertTrue(result)
        self.assertEqual(game.chips, 100)

    def test_empty_deck_on_hit_cancels_without_changing_balance(self):
        cards = [("10", "S"), ("8", "H"), ("9", "C"), ("7", "D")]
        game, result, _ = self.play_round(cards, ["10", "h"])
        self.assertTrue(result)
        self.assertEqual(game.chips, 100)

    def test_empty_deck_during_dealer_turn_cancels_without_changing_balance(self):
        cards = [("10", "S"), ("8", "H"), ("9", "C"), ("7", "D")]
        game, result, _ = self.play_round(cards, ["10", "s"])
        self.assertTrue(result)
        self.assertEqual(game.chips, 100)

    def test_quitting_during_round_does_not_change_balance(self):
        cards = [("10", "S"), ("8", "H"), ("9", "C"), ("7", "D")]
        game, result, _ = self.play_round(cards, ["10", "q"])
        self.assertFalse(result)
        self.assertEqual(game.chips, 100)

    def test_empty_deck_draw_returns_none(self):
        deck = Deck()
        deck.cards.clear()
        self.assertIsNone(deck.draw())


if __name__ == "__main__":
    unittest.main()
