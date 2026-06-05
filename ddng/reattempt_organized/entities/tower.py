from abc import ABC
from enum import Enum, auto
from random import Random

# import core.constants as c
import core.common_types as ct


class TowerType(Enum):
    BASIC = auto()


class Tower(ABC):
    def __init__(self, rng: Random, tx: int, ty: int):
        self.tile_x: int = tx
        self.tile_y: int = ty
        self.size_dimensions: tuple[int, int]
        self.direction: ct.Direction = ct.Direction.UP
        self.cooldown = 0
        self.color: ct.BasicColors = rng.choice(list(ct.BasicColors))


class BasicTower(Tower):
    def __init__(self, rng: Random, tx: int, ty: int):
        super().__init__(rng, tx, ty)
        self.size_dimensions = (32, 32)
