from datetime import timedelta as td


class Card:
    def __init__(self, status="learning", interval=None, ease=2.5, step=0):
        self.status, self.interval, self.step = status, interval, step
        self.ease = max(ease, 1.3)

    def __repr__(self):
        return f"Card(status={self.status}, step={self.step}, interval={self.interval}, ease={self.ease})"

    def options(self):
        if self.status == "learning":
            options = [
                Card("learning", td(minutes=1)),
                Card("learning", td(minutes=6), step=1),
                Card("learning", td(minutes=10), step=1)
                if self.step == 0
                else Card("reviewing", td(days=1)),
                Card("reviewing", td(days=4)),
            ]
        elif self.status == "reviewing":
            options = [
                Card("relearning", td(minutes=10), self.ease - 0.2),
                Card("reviewing", self.interval * 1.2, self.ease - 0.15),
                Card("reviewing", self.interval * self.ease, self.ease),
                Card("reviewing", self.interval * self.ease * 1.5, self.ease + 0.15),
            ]
        elif self.status == "relearning":
            options = [
                Card("relearning", td(minutes=1), self.ease),
                Card("relearning", td(minutes=6), self.ease),
                Card("reviewing", td(days=1), self.ease),
                Card("reviewing", td(days=4), self.ease),
            ]
        return list(zip(["again", "hard", "good", "easy"], options))
