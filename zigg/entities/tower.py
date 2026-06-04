from __future__ import annotations
from abc import ABC, abstractmethod
import random

from core.constants import Direction, Color, DIAGONAL

class Tower(ABC):
    # CONSTANT
    @property
    @abstractmethod
    def square_side_length(self) -> int: ...

    @property
    @abstractmethod
    def rate_of_fire(self) -> float: ...

    @property
    @abstractmethod
    def bullet_speed(self) -> float: ...

    @property
    @abstractmethod
    def range(self) -> int: ...

    @property
    @abstractmethod
    def bullet_pierce(self) -> int: ...

    # UPDATING
    @property
    @abstractmethod
    def fire_timer(self) -> float: ...

    @property
    @abstractmethod
    def aim_direction(self) -> Direction: ...

    # FUNCS
    @abstractmethod
    def update(self, time_passed: float) -> bool: ...

    @abstractmethod
    def change_direction(self, direction: Direction) -> None: ...


class BasicTower(Tower):
    def __init__(self, colors: list[Color] | None = None):
        self._colors = colors if colors is not None else list(Color)
        self._color_to_shoot = random.choice(self._colors)
        self._fire_timer = 0.0
        self._aim_direction = Direction.UP
        

    # CONSTANT
    @property
    def square_side_length(self) -> int:
        return 15

    @property
    def rate_of_fire(self) -> float:
        return 0.5

    @property
    def bullet_speed(self) -> float:
        return DIAGONAL / 5

    @property
    def range(self) -> int:
        return 5 # IDK TEST VALUE LANG HAHA

    @property
    def bullet_pierce(self) -> int:
        return 1
    
    @property
    def color_to_shoot(self) -> Color:
        return self._color_to_shoot


    # UPDATING
    @property
    def fire_timer(self) -> float:
        return self._fire_timer

    @property
    def aim_direction(self) -> Direction:
        return self._aim_direction

    def update(self, time_passed: float) -> bool: 
        self._fire_timer += time_passed

        if self._fire_timer >= (1 / self.rate_of_fire):
            self._fire_timer -= (1 / self.rate_of_fire)
            self._color_to_shoot = random.choice(self._colors)
            return True

        return False

    def change_direction(self, direction: Direction) -> None:
        self._aim_direction = direction