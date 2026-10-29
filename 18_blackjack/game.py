from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100
        self._round_settled = True

    def show(self, player, dealer, hide=True):
        shown_dealer = (["??"] + [f"{r}{s}" for r, s in dealer[1:]]
                        if hide else [f"{r}{s}" for r, s in dealer])
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def _get_wager(self):
        while True:
            entry = input(f"Wager (1-{int(self.chips)}) or [q]uit: ").strip().lower()
            if entry == "q":
                return None
            try:
                wager = int(entry)
            except ValueError:
                print("Enter a whole-number wager.")
                continue
            if wager < 1 or wager > self.chips:
                print("Wager must be between 1 and your chip balance.")
                continue
            return wager

    def _settle(self, wager, result, natural=False):
        if self._round_settled:
            return
        self._round_settled = True
        if result == "win":
            winnings = wager * 1.5 if natural else wager
            self.chips += winnings
            print(f"Player wins{' with blackjack' if natural else ''}. +{winnings:g} chips.")
        elif result == "loss":
            self.chips -= wager
            print(f"Dealer wins. -{wager} chips.")
        else:
            print("Push. Wager returned.")
        print(f"Chip balance: {self.chips:g}")

    def _cancel_round(self):
        self._round_settled = True
        print("Round canceled because the deck is empty. No chips changed.")

    def round(self):
        wager = self._get_wager()
        if wager is None:
            return False

        self._round_settled = False
        deck = Deck()
        player = []
        dealer = []
        for hand in (player, dealer):
            for _ in range(2):
                card = deck.draw()
                if card is None:
                    self._cancel_round()
                    return True
                hand.append(card)
        self.show(player, dealer)

        player_natural = len(player) == 2 and hand_value(player) == 21
        dealer_natural = len(dealer) == 2 and hand_value(dealer) == 21
        if player_natural or dealer_natural:
            self.show(player, dealer, hide=False)
            if player_natural and dealer_natural:
                self._settle(wager, "push")
            elif player_natural:
                self._settle(wager, "win", natural=True)
            else:
                self._settle(wager, "loss")
            return True

        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                self._round_settled = True
                return False
            if key == "s":
                break
            if key == "h":
                card = deck.draw()
                if card is None:
                    self._cancel_round()
                    return True
                player.append(card)
                print(f"Player draws {card[0]}{card[1]}.")
                self.show(player, dealer)
                if hand_value(player) > 21:
                    print("Player busts.")
                    self.show(player, dealer, hide=False)
                    self._settle(wager, "loss")
                    return True
            else:
                print("Invalid command. Enter h, s, or q.")

        while hand_value(dealer) < 17:
            card = deck.draw()
            if card is None:
                self._cancel_round()
                return True
            dealer.append(card)
            print(f"Dealer draws {card[0]}{card[1]}.")

        self.show(player, dealer, hide=False)
        pv, dv = hand_value(player), hand_value(dealer)
        if dv > 21 or pv > dv:
            self._settle(wager, "win")
        elif pv < dv:
            self._settle(wager, "loss")
        else:
            self._settle(wager, "push")
        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips >= 1:
            if not self.round():
                return
            while True:
                answer = input("Play again? [y/n]: ").strip().lower()
                if answer in {"n", "q"}:
                    return
                if answer == "y":
                    break
                print("Enter y or n.")
        if self.chips < 1:
            print("Not enough chips to place a wager.")
