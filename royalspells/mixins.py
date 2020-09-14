from typing import *
import random


class SeededMixin:
    def __init__(self, seed: Hashable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rand = random.Random(hash(seed))


class RandomMixin:
    def __init__(self, rand: random.Random, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rand = rand
