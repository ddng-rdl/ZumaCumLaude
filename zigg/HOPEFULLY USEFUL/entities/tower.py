from abc import ABC, abstractmethod
from enum import Enum, auto
from random import Random

import core.constants as c
import core.common_types as ct


class TowerType(Enum):
    BASIC = auto()


class Tower(ABC):
    def __init__(self, rng: Random, tx: int, ty: int):
        self._rng = rng
        self.tile_x: int = tx
        self.tile_y: int = ty
        self.size_dimensions: tuple[int, int]
        self.direction: ct.Direction = ct.Direction.UP
        self.cooldown: int = 0
        self.color: ct.BasicColors = rng.choice(list(ct.BasicColors))

    @property
    @abstractmethod
    def rate_of_fire_frames(self) -> int: ...

    @abstractmethod
    def draw(self) -> None: ...

    def update(self) -> bool:
        self.cooldown += 1
        if self.cooldown >= self.rate_of_fire_frames:
            self.cooldown -= self.rate_of_fire_frames
            self.color = self._rng.choice(list(ct.BasicColors))
            return True
        return False


class BasicTower(Tower):
    def __init__(self, rng: Random, tx: int, ty: int):
        super().__init__(rng, tx, ty)
        self.size_dimensions = (32, 32)

    @property
    def rate_of_fire_frames(self) -> int:
        return c.TOWER_COOLDOWN

    def draw(self) -> None:
        pass