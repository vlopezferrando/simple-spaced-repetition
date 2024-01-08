import unittest
from datetime import timedelta as td

from simple_spaced_repetition import Card

LEARNING, REVIEWING, RELEARNING = (
    Card.LEARNING,
    Card.REVIEWING,
    Card.RELEARNING,
)

def check_values(card, attr, again, hard, good, easy):
    assert getattr(card.again(), attr) == again
    assert getattr(card.hard(), attr) == hard
    assert getattr(card.good(), attr) == good
    assert getattr(card.easy(), attr) == easy

class TestSimpleSpacedRepetition(unittest.TestCase):

    def test_new_card(self):
        card = Card()
        assert card.status == LEARNING
        assert card.step == 0
        assert card.interval is None
        assert card.due is None
        assert card.ease is None

    def test_learning_step_0(self):
        card = Card()
        check_values(card, "status", LEARNING, LEARNING, LEARNING, REVIEWING)
        check_values(card, "step", 0, 1, 1, None)
        check_values(card, "ease", None, None, None, 2.5)
        check_values(card, "interval", None, None, None, 4)
        check_values(
            card, "due", td(minutes=1), td(minutes=6), td(minutes=10), td(days=4)
        )

    def test_learning_step_1(self):
        card = Card(step=1)
        check_values(card, "status", LEARNING, LEARNING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, 1, None, None)
        check_values(card, "ease", None, None, 2.5, 2.5)
        check_values(card, "interval", None, None, 1, 4)
        check_values(card, "due", td(minutes=1), td(minutes=6), td(days=1), td(days=4))

    def check_reviewing(self, ease, interval):
        card = Card(status=REVIEWING, ease=ease, interval=interval, step=None)
        check_values(card, "status", RELEARNING, REVIEWING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, None, None, None)
        check_values(
            card,
            "ease",
            max(Card.MIN_EASE, ease - 0.2),
            max(Card.MIN_EASE, ease - 0.15),
            ease,
            ease + 0.15,
        )
        hard_ivl = interval * Card.HARD_INTERVAL
        good_ivl = interval * ease
        easy_ivl = interval * ease * Card.EASY_BONUS
        check_values(card, "interval", None, hard_ivl, good_ivl, easy_ivl)
        check_values(
            card,
            "due",
            td(minutes=10),
            td(days=hard_ivl),
            td(days=good_ivl),
            td(days=easy_ivl),
        )

    def test_reviewing(self):
        for ease in [Card.MIN_EASE, 2.5, 3.0, 10.0, 100.0]:
            for interval in [11, 3, 5, 10, 100]:
                self.check_reviewing(ease, interval)

    def test_relearning(self):
        card = Card(status=RELEARNING, ease=3.0, step=0)
        check_values(card, "status", RELEARNING, RELEARNING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, 0, None, None)
        check_values(card, "ease", 3.0, 3.0, 3.0, 3.0)
        check_values(card, "interval", None, None, 1, 4)
        check_values(card, "due", td(minutes=1), td(minutes=6), td(days=1), td(days=4))


if __name__ == '__main__':
    unittest.main()
