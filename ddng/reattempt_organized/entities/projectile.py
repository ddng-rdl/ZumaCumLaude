from abc import ABC, abstractmethod
from enum import Enum, auto

# import core.constants as c
import core.common_types as ct


class ProjectileType(Enum):
    BULLET = auto()


class Projectile(ABC):
    def __init__(self, x: float, y: float, dx: float, dy: float, color: ct.BasicColors):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

    def update(self) -> None:
        self.x += self.dx
        self.y += self.dy
        self.apply_effects()

    @abstractmethod
    def apply_effects(self) -> None:
        pass


class Bullet(Projectile):
    def apply_effects(self) -> None:
        pass
