from datetime import timedelta


class Card:
    # Statuses
    LEARNING, REVIEWING, RELEARNING = 1, 2, 3

    # Answers
    AGAIN, HARD, GOOD, EASY = 1, 2, 3, 4

    # Config
    HARD_INTERVAL = 1.2
    EASY_BONUS = 1.5
    MIN_EASE = 1.3

    def __init__(self, status=LEARNING, step=0, interval=None, ease=None, due=None):
        self.status = status
        self.step = step
        self.interval = interval
        self.ease = ease
        self.due = due

    def _learning(self, step, minutes):
        return Card(
            status=self.LEARNING,
            step=step,
            due=timedelta(minutes=minutes),
        )

    def _reviewing(self, days, ease):
        return Card(
            status=self.REVIEWING,
            step=None,
            interval=days,
            ease=max(ease, self.MIN_EASE),
            due=timedelta(days=days),
        )

    def _relearning(self, minutes, step=0, ease=None):
        if ease is None:
            ease = self.ease
        return Card(
            status=self.RELEARNING,
            step=step,
            ease=max(ease, self.MIN_EASE),
            due=timedelta(minutes=minutes),
        )

    def _learning_options(self):
        assert self.step is not None
        assert self.interval is None
        assert self.ease is None
        return [
            self._learning(step=0, minutes=1),
            self._learning(step=1, minutes=6),
            self._learning(step=1, minutes=10)
            if self.step == 0
            else self._reviewing(days=1, ease=2.5),
            self._reviewing(days=4, ease=2.5),
        ]

    def _reviewing_options(self):
        assert self.step is None
        assert self.interval is not None
        assert self.ease is not None
        return [
            self._relearning(minutes=10, ease=self.ease - 0.2),
            self._reviewing(self.interval * self.HARD_INTERVAL, self.ease - 0.15),
            self._reviewing(self.interval * self.ease, self.ease),
            self._reviewing(
                self.interval * self.ease * self.EASY_BONUS, self.ease + 0.15
            ),
        ]

    def _relearning_options(self):
        assert self.step is not None
        assert self.interval is None
        assert self.ease is not None
        return [
            self._relearning(minutes=1),
            self._relearning(minutes=6),
            self._reviewing(days=1, ease=self.ease),
            self._reviewing(days=4, ease=self.ease),
        ]

    def _options(self):
        if self.status == self.LEARNING:
            return self._learning_options()
        elif self.status == self.REVIEWING:
            return self._reviewing_options()
        elif self.status == self.RELEARNING:
            return self._relearning_options()
        assert False

    def _answer(self, answer):
        return self._options()[answer - 1]

    # Public methods

    def due_times(self):
        return [o.due for o in self._options()]

    def again(self):
        return self._answer(self.AGAIN)

    def hard(self):
        return self._answer(self.HARD)

    def good(self):
        return self._answer(self.GOOD)

    def easy(self):
        return self._answer(self.EASY)
