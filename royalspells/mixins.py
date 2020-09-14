from typing import *
import abc
import random


__all__ = [
    "SeededMixin",
    "Selectable",
]


class SeededMixin:
    def __init__(self, seed: Hashable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rand = random.Random(hash(seed))


class Selectable(metaclass=abc.ABCMeta):
    """A class from which an instance can be generated through the :meth:`.select` method."""

    @classmethod
    @abc.abstractmethod
    def select(cls, rand: random.Random):
        raise NotImplementedError()
