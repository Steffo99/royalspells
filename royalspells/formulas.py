from __future__ import annotations
from typing import *

import abc
import random
import math

from .mixins import *


__all__ = [
    "Formula",
    "RandNonNegativeGaussFormula",
    "RandNonNegativeGaussFormula",
    "FixedFormula",
]


class Formula(Selectable, metaclass=abc.ABCMeta):
    """A int-returning function that will be evaluated at a later time."""

    @abc.abstractmethod
    def calc(self, rand: random.Random) -> int:
        """Calculate the value of the Formula."""
        raise NotImplementedError()

    @classmethod
    def select(cls, rand: random.Random) -> Formula:
        # TODO: I'm not sure if it's a good idea leaving it here
        type_ = rand.randrange(1, 101)
        mean = rand.randrange(1, 80) * 10
        delta = rand.randrange(1, 300)

        if type_ <= 70:
            return RandNonNegativeGaussFormula(mu=mean, sigma=math.sqrt(delta))
        elif type_ <= 90:
            return RandNonNegativeUniformFormula(min_=mean-delta, max_=mean+delta)
        else:
            return FixedFormula(mean)


class RandNonNegativeUniformFormula(Formula):
    """A :class:`Formula` that implements the ``calc`` method using a uniform distribution, setting to 0 the
    result if it is negative and finally ceiling the result."""

    def __init__(self, min_: float, max_: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min: float = min_
        self.max: float = max_

    def calc(self, rand: random.Random) -> int:
        n = rand.uniform(self.min, self.max)
        n = n if n > 0 else 0
        n = math.ceil(n)
        return n


class RandNonNegativeGaussFormula(Formula):
    """A :class:`Formula` that implements the ``calc`` method using a gaussian (normal) distribution, setting to 0 the
    result if it is negative and finally ceiling the result."""

    def __init__(self, mu: float, sigma: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mu: float = mu
        self.sigma: float = sigma

    def calc(self, rand: random.Random) -> int:
        """A mixin that implements the ``calculate`` method using a gaussian (normal) distribution."""
        n = rand.gauss(self.mu, self.sigma)
        n = n if n > 0 else 0
        n = math.ceil(n)
        return n


class FixedFormula(Formula):
    """A :class:`Formula` that implements the ``calc`` method by always returning a fixed value."""

    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def calc(self, rand: random.Random) -> int:
        return self.value
