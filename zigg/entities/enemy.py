from __future__ import annotations
from abc import ABC, abstractmethod
import random

from core.constants import Color


class Enemy(ABC):
    # CONSTANT
    @property
    @abstractmethod
    def square_side_length(self) -> int: ...

    @property
    @abstractmethod
    def tiles_moved_per_move(self) -> int: ...

    @property
    @abstractmethod
    def base_movement_timer(self) -> int: ...

    @property
    @abstractmethod
    def base_hit_points(self) -> int: ...

    @property
    @abstractmethod
    def color(self) -> Color: ...
    
    @property
    @abstractmethod
    def exp_value(self) -> int: ...

    # UPDATING
    @property
    @abstractmethod
    def position_idx(self) -> int: ...

    @property
    @abstractmethod
    def movement_timer(self) -> float: ...

    @property
    @abstractmethod
    def hit_points(self) -> int: ...

    @property
    @abstractmethod
    def is_alive(self) -> bool: ...

    # FUNCS
    @abstractmethod
    def take_hit(self, damage: int) -> None: ...

    @abstractmethod
    def update(self, time_passed: float) -> bool: ...


class BasicEnemy(Enemy):
    def __init__(self, color: Color):
        self._color = color
        self._position_idx = 0
        self._movement_timer = 0.0
        self._hit_points = self.base_hit_points

    # CONSTANT
    @property
    def square_side_length(self) -> int:
        return 15

    @property
    def tiles_moved_per_move(self) -> int:
        return 1

    @property
    def base_movement_timer(self) -> int:
        return 2

    @property
    def base_hit_points(self) -> int: 
        return 1

    @property
    def color(self) -> Color: 
        return self._color
    
    @property
    def exp_value(self) -> int:
        return 1


    # UPDATING
    @property
    def position_idx(self) -> int: 
        return self._position_idx

    @property
    def movement_timer(self) -> float:
        return self._movement_timer

    @property
    def hit_points(self) -> int: 
        return self._hit_points

    @property
    def is_alive(self) -> bool: 
        return self._hit_points > 0

    # FUNCS
    def take_hit(self, damage: int) -> None:
        self._hit_points -= damage

    def update(self, time_passed: float) -> bool:
        self._movement_timer += time_passed
        
        if self._movement_timer >= self.base_movement_timer:
            self._movement_timer -= self.base_movement_timer
            self._position_idx += self.tiles_moved_per_move
            return True
        
        return False
    
class Regenerator(BasicEnemy):
    def __init__(self, color: Color, tiles_needed_to_regen: int = 3):
        super().__init__(color)
        self._tiles_needed_to_regen = tiles_needed_to_regen
        self._tiles_moved_for_regen = 0

    # CONSTANT
    @property
    def tiles_needed_to_regen(self) -> int:
        return self._tiles_needed_to_regen


    # UPDATING
    @property
    def tiles_moved_for_regen(self) -> int:
        return self._tiles_moved_for_regen

    # FUNCS
    def update(self, time_passed: float) -> bool:
        self._movement_timer += time_passed
        
        if self._movement_timer >= self.base_movement_timer:
            self._movement_timer -= self.base_movement_timer
            self._position_idx += self.tiles_moved_per_move

            self._tiles_moved_for_regen += 1
            if self._tiles_moved_for_regen >= self.tiles_needed_to_regen:
                self._hit_points += 1
                self._tiles_moved_for_regen -= self.tiles_needed_to_regen
            
            return True
            
        return False
            
class Chameleon(BasicEnemy):
    def __init__(self, color: Color, colors: list[Color] | None = None, change_color_cooldown: float = 3.0):
        super().__init__(color)
        self._colors = colors if colors is not None else list(Color)
        self._change_color_cooldown = change_color_cooldown
        self._change_color_timer = 0.0

    # CONSTANT
    @property
    def colors(self) -> list[Color]:
        return self._colors
    
    @property
    def change_color_cooldown(self) -> float:
        return self._change_color_cooldown


    # UPDATING
    @property
    def change_color_timer(self) -> float:
        return self._change_color_timer

    # FUNCS
    def update(self, time_passed: float) -> bool:
        self._movement_timer += time_passed
        self._change_color_timer += time_passed
        
        moved = False
        if self._movement_timer >= self.base_movement_timer:
            self._movement_timer -= self.base_movement_timer
            self._position_idx += self.tiles_moved_per_move
            moved = True

        if self._change_color_timer >= self._change_color_cooldown:
            self._change_color_timer -= self._change_color_cooldown
            self._color = random.choice([color for color in self._colors if color != self._color])
        
        return moved