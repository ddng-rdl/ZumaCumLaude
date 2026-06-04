from __future__ import annotations
from abc import ABC, abstractmethod

from core.constants import Color, DIAGONAL


class Projectile(ABC):
    # CONSTANT
    @property
    @abstractmethod
    def radius(self) -> int: ...

    @property
    @abstractmethod
    def speed(self) -> float: ...

    @property
    @abstractmethod
    def color(self) -> Color: ...

    @property
    @abstractmethod
    def damage(self) -> int: ...

    @property
    @abstractmethod
    def bullet_pierce(self) -> int: ...

    # UPDATING
    @property
    @abstractmethod
    def is_active(self) -> bool: ...

    @property
    @abstractmethod
    def position(self) -> tuple[float, float]: ...

    @property
    @abstractmethod
    def direction(self) -> tuple[float, float]: ...

    # FUNCS
    @abstractmethod
    def update(self, time_passed: float) -> bool: ...

    @abstractmethod
    def hit(self) -> None: ...

    @abstractmethod
    def deactivate(self) -> None: ...


class BasicProjectile(Projectile):
    def __init__(self, position: tuple[float, float], direction: tuple[float, float], color: Color):
        self._position = position
        self._direction = direction
        self._color = color
        self._is_active = True
        self._hits_remaining = self.bullet_pierce
    
    # CONSTANT
    @property
    def radius(self) -> int:
        return 5

    @property
    def speed(self) -> float:
        return DIAGONAL / 5

    @property
    def color(self) -> Color:
        return self._color

    @property
    def damage(self) -> int:
        return 1

    @property
    def bullet_pierce(self) -> int:
        return 1

    # UPDATING
    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def position(self) -> tuple[float, float]:
        return self._position

    @property
    def direction(self) -> tuple[float, float]:
        return self._direction

    # FUNCS
    def update(self, time_passed: float) -> bool:
        if not self._is_active:
            return False
        
        dx, dy = self._direction
        distance_traveled = self.speed * time_passed
        x, y = self._position
        self._position = (x + (dx * distance_traveled), y + (dy * distance_traveled))
        return True

    def hit(self) -> None:
        self._hits_remaining -= 1

        if self._hits_remaining <= 0:
            self._is_active = False

    def deactivate(self) -> None:
        self._is_active = False