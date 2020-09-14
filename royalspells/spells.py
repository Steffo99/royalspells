from typing import *
import enum
import random

from .mixins import *
from .formulas import *
from .buffs import *


class Spell(SeededMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.effects: List[Effect] = [...]
        self.cost = ...


class Target(enum.Enum, Selectable):
    """A target for a spell."""

    RANDOM_ENEMY = enum.auto()
    ALL_ENEMIES = enum.auto()
    RANDOM_ALLY = enum.auto()
    ALL_ALLIES = enum.auto()
    RANDOM_CREATURE = enum.auto()
    ALL_CREATURES = enum.auto()
    USELESS_THING = enum.auto()

    @classmethod
    def select(cls, rand: random.Random):
        """Pick a target using the default distribution."""
        result = rand.randrange(1, 101)
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


class Effect(Selectable):
    """A single consequence of a spell."""

    def __init__(self,
                 target: Target,
                 damage: Optional[Formula] = None,
                 healing: Optional[Formula] = None,
                 buffs: Optional[List[Buff]] = None):

        self.target: Target = target
        """The :class:`Target` of the effect."""

        self.damage: Optional[Formula] = damage
        """The :class:`Formula` that calculates the damage of the effect, or :const:`None` if it doesn't do any 
        damage."""

        self.healing: Optional[Formula] = healing
        """The :class:`Formula` that calculates the healing of the effect, or :const:`None` if it doesn't do any 
        damage."""

        self.buffs: List[Buff] = buffs if buffs else []
        """A :class:`list` of :class:`Buff` that will be applied to the target after the damage/healing is applied."""

    @classmethod
    def select(cls, rand: random.Random):
        # noinspection PyDictCreation
        kw = {}

        kw["target"] = Target.select(rand)

        type_ = rand.randrange(1, 101)
        # 70%: Damaging
        if type_ <= 70:
            kw["damage"] = Formula.select(rand)
        # 20%: Healing
        elif type_ <= 90:
            kw["healing"] = Formula.select(rand) if rand.randrange(1, 101) <= 20 else None
        # 10%: Neither

        kw["buffs"] = []

        return cls(**kw)
