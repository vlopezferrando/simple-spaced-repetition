from datetime import timedelta


class Card:
    # Statuses
    LEARNING, REVIEWING, RELEARNING = "learning", "reviewing", "relearning"

    # Answers
    ANSWERS = ["again", "hard", "good", "easy"]

    # Interval multipliers
    HARD_INTERVAL = 1.2  # Multiplier for hard answers, used insead of ease
    EASY_BONUS = 1.5

    # Ease values
    INITIAL_EASE = 2.5
    MIN_EASE = 1.3
    AGAIN_EASE_DELTA = -0.2
    HARD_EASE_DELTA = -0.15
    EASY_EASE_DELTA = 0.15

    def __init__(self, status=LEARNING, step=0, interval=None, ease=None, due=None):
        assert step is None or 0 <= step <= 1

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

    def _relearning(self, minutes, ease, step=0):
        return Card(
            status=self.RELEARNING,
            step=step,
            ease=max(ease, self.MIN_EASE),
            due=timedelta(minutes=minutes),
        )

    def _options(self):
        if self.status == self.LEARNING:
            return [
                self._learning(step=0, minutes=1),
                self._learning(step=1, minutes=6),
                self._learning(step=1, minutes=10)
                if self.step == 0
                else self._reviewing(days=1, ease=self.INITIAL_EASE),
                self._reviewing(days=4, ease=self.INITIAL_EASE),
            ]
        elif self.status == self.REVIEWING:
            return [
                self._relearning(minutes=10, ease=self.ease + self.AGAIN_EASE_DELTA),
                self._reviewing(
                    days=self.interval * self.HARD_INTERVAL,
                    ease=self.ease + self.HARD_EASE_DELTA,
                ),
                self._reviewing(days=self.interval * self.ease, ease=self.ease),
                self._reviewing(
                    days=self.interval * self.ease * self.EASY_BONUS,
                    ease=self.ease + self.EASY_EASE_DELTA,
                ),
            ]
        elif self.status == self.RELEARNING:
            return [
                self._relearning(minutes=1, ease=self.ease),
                self._relearning(minutes=6, ease=self.ease),
                self._reviewing(days=1, ease=self.ease),
                self._reviewing(days=4, ease=self.ease),
            ]

    def __repr__(self):
        return (
            f"Card(status={self.status}, step={self.step}, "
            f"interval={self.interval}, ease={self.ease}, due={self.due})"
        )

    # Public methods

    def due_times(self):
        return dict(zip(self.ANSWERS, [o.due for o in self._options()]))

    def answer(self, answer):
        assert answer in self.ANSWERS, f"Invalid answer: {answer}"
        return self._options()[self.ANSWERS.index(answer)]
