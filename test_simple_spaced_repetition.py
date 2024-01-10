import unittest
from datetime import timedelta

from simple_spaced_repetition import Card

LEARNING, REVIEWING, RELEARNING = "learning", "reviewing", "relearning"

_minutes = lambda m: timedelta(minutes=m)
_days = lambda d: timedelta(days=d)


def check_values(card, attr, again, hard, good, easy):
    op_again, op_hard, op_good, op_easy = card.options()
    assert getattr(op_again[1], attr) == again
    assert getattr(op_hard[1], attr) == hard
    assert getattr(op_good[1], attr) == good
    assert getattr(op_easy[1], attr) == easy


MINIMUM_EASE = 1.3
INITIAL_EASE = 2.5
AGAIN_EASE_DELTA = -0.2
HARD_EASE_DELTA = -0.15
EASY_EASE_DELTA = 0.15
HARD_INTERVAL = 1.2
EASY_INTERVAL_BONUS = 1.5


class TestSimpleSpacedRepetition(unittest.TestCase):
    def test_new_card(self):
        card = Card()
        assert card.status == LEARNING
        assert card.step == 0
        assert card.interval is None
        assert card.ease == INITIAL_EASE

    def test_learning_step_0(self):
        card = Card()
        check_values(card, "status", LEARNING, LEARNING, LEARNING, REVIEWING)
        check_values(card, "step", 0, 1, 1, 0)
        check_values(card, "ease", INITIAL_EASE, INITIAL_EASE, INITIAL_EASE, 2.5)
        check_values(
            card,
            "interval",
            _minutes(1),
            _minutes(6),
            _minutes(10),
            _days(4),
        )

    def test_learning_step_1(self):
        card = Card(step=1)
        check_values(card, "status", LEARNING, LEARNING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, 1, 0, 0)
        check_values(
            card,
            "ease",
            INITIAL_EASE,
            INITIAL_EASE,
            INITIAL_EASE,
            INITIAL_EASE,
        )
        check_values(card, "interval", _minutes(1), _minutes(6), _days(1), _days(4))

    def check_reviewing(self, ease, interval):
        card = Card(status=REVIEWING, ease=ease, interval=interval, step=None)
        check_values(card, "status", RELEARNING, REVIEWING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, 0, 0, 0)
        check_values(
            card,
            "ease",
            max(MINIMUM_EASE, ease + AGAIN_EASE_DELTA),
            max(MINIMUM_EASE, ease + HARD_EASE_DELTA),
            ease,
            ease + EASY_EASE_DELTA,
        )
        hard_ivl = interval * HARD_INTERVAL
        good_ivl = interval * ease
        easy_ivl = interval * ease * EASY_INTERVAL_BONUS
        check_values(
            card,
            "interval",
            _minutes(10),
            hard_ivl,
            good_ivl,
            easy_ivl,
        )

    def test_reviewing(self):
        for ease in [MINIMUM_EASE, 2.5, 3.0, 10.0, 100.0]:
            for interval in [11, 3, 5, 10, 100]:
                self.check_reviewing(ease, _days(interval))

    def test_relearning(self):
        card = Card(status=RELEARNING, ease=3.0, step=0)
        check_values(card, "status", RELEARNING, RELEARNING, REVIEWING, REVIEWING)
        check_values(card, "step", 0, 0, 0, 0)
        check_values(card, "ease", 3.0, 3.0, 3.0, 3.0)
        check_values(card, "interval", _minutes(1), _minutes(6), _days(1), _days(4))


if __name__ == "__main__":
    unittest.main()
