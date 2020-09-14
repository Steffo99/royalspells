from typing import *
import math
import enum
import abc

from .mixins import *


class Spell(SeededMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.effects: List[Effect] = [...]
        self.cost = ...


class Effect(RandomMixin):
    """A single consequence of a spell."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.target: Target = Target.select(self.rand)
        """The :class:`Target` of the effect."""

        self.damage: Optional[Damage] = ...
        """The :class:`Damage` of the effect, or :const:`None` if it doesn't do any damage."""

        self.healing = ...
        self.buffs = ...
        self.attributes = ...


class Target(enum.Enum):
    """A target for a spell."""

    RANDOM_ENEMY = enum.auto()
    ALL_ENEMIES = enum.auto()
    RANDOM_ALLY = enum.auto()
    ALL_ALLIES = enum.auto()
    RANDOM_CREATURE = enum.auto()
    ALL_CREATURES = enum.auto()
    USELESS_THING = enum.auto()

    @classmethod
    def select(cls, seed: random.Random):
        """Pick a target using the default distribution."""

        result = seed.randrange(1, 101)
        """A number from 1 to 100, determining the chosen target."""

        # 50%: RANDOM_ENEMY
        if result <= 50:
            return Target.RANDOM_ENEMY
        # 20%: ALL_ENEMIES
        elif result <= 70:
            return Target.ALL_ENEMIES
        # 15%: RANDOM_ALLY
        elif result <= 85:
            return Target.RANDOM_ALLY
        # 5%: ALL_ALLIES
        elif result <= 90:
            return Target.ALL_ALLIES
        # 5%: RANDOM_CREATURE
        elif result <= 95:
            return Target.RANDOM_CREATURE
        # 3%: ALL_CREATURES
        elif result <= 98:
            return Target.ALL_CREATURES
        # 2%: USELESS_THING
        else:
            return Target.USELESS_THING


class Damage(RandomMixin, metaclass=abc.ABCMeta):
    """The damage of a spell effect. Should be extended, implementing its methods.

    Examples:
        See :class:`UniformDamage`, :class:`NormalDamage` and :class:`FixedDamage`."""

    @abc.abstractmethod
    def select(self, rand: random.Random) -> int:
        """Calculate the damage of the spell. It should always return a non-negative :class:`int`.

        Note:
            It uses a separate RNG than the one passed to the damage class!"""
        raise NotImplementedError()


class UniformDamage(Damage):
    """The damage of a spell effect, following a gaussian distribution."""

    def __init__(self, min_: float, max_: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min: float = min_
        self.max: float = max_

    def select(self, rand: random.Random) -> int:
        n = self.rand.uniform(self.min, self.max)
        n = math.ceil(n)
        return n


class NormalDamage(Damage):
    """The damage of a spell effect, following a gaussian distribution."""

    def __init__(self, mu: float, sigma: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mu: float = mu
        self.sigma: float = sigma

    def select(self, rand: random.Random) -> int:
        n = self.rand.gauss(self.mu, self.sigma)
        n = n if n > 0 else 0
        n = math.ceil(n)
        return n


class FixedDamage(Damage):
    """The damage of a spell effect, which is always constant."""

    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value

    def select(self, rand: random.Random) -> int:
        return self.value
