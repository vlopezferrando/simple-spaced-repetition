# simple-spaced-repetition

Simple spaced repetition scheduler, based on the [classic Anki algorithm](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html) and implemented in under 40 lines of code.

This scheduler is used at [Python.cards](https://python.cards).

[!Test status](https://github.com/vlopezferrando/simple-spaced-repetition/actions/workflows/python-package.yml/badge.svg)
[![Supported Versions](https://img.shields.io/pypi/pyversions/simple_spaced_repetition.svg)](https://pypi.org/project/simple_spaced_repetition)

## Installation

Install with pip:

    pip install simple_spaced_repetition

## Example usage

The `Card` class is what you should use:

```python
>>> from simple_spaced_repetition import Card
>>> Card()
Card(status=learning, step=0, interval=None, ease=2.5)
```

`Card` has a single method `options()` which returns the 4 possible choices for answering a card:

```python
>>> from simple_spaced_repetition import Card
>>> card = Card()
>>> card.options()
[('again', Card(status=learning, step=0, interval=0:01:00, ease=2.5)),
 ('hard', Card(status=learning, step=1, interval=0:06:00, ease=2.5)),
 ('good', Card(status=learning, step=1, interval=0:10:00, ease=2.5)),
 ('easy', Card(status=reviewing, step=0, interval=4 days, 0:00:00, ease=2.5))]
```

Next to each answer is a new `Card` object that represents the card after answering with that option.

The attribute `interval` holds the time that must pass before the card is due again:

```python
>>> from simple_spaced_repetition import Card
>>> card = Card()
>>> for answer, new_card in card.options():
...     print(answer, new_card.interval)
again 0:01:00
hard 0:06:00
good 0:10:00
easy 4 days, 0:00:00
```

## Run tests

Simply run:

    python test_simple_spaced_repetition.py
