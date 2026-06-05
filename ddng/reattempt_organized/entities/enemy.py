from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from random import Random
from typing import Protocol
import pyxel as px

import core.constants as c
import core.common_types as ct
from core import utils as u


# # class EnemySpawnPlan(ABC):
# #     def __init__(self):
# #         self.spawn_queue: list[EnemyType] = []
# #         self.max_spawned_enemies: int
# #         self.spawn_interval: int
# #         self.spawn_timer: int = 0

# #     @abstractmethod
# #     def update_spawn_plan(self) -> None:
# #         pass

# #     @abstractmethod
# #     def spawn_enemy(self, enemy_type: EnemyType, enemy_factory: EnemyFactory) -> None:
# #         pass


# class SimpleEnemySpawn:
#     def __init__(
#         self,
#     ):
#         self.spawn_queue = [EnemyType.BASIC] * 10
#         self.max_spawned_enemies = 5
#         self.spawn_interval = u.secs_to_frames(2)
#         self.spawn_timer = 0
#         self._enemies_to_spawn: list[Enemy] = []

#     def update(self, enemy_type: EnemyType, enemy_factory: EnemyFactory) -> None:
#         if self.spawn_timer > 0:
#             self.spawn_timer -= 1
#         if self.spawn_timer == 0 and len(self.spawn_queue) > 0:
#             if len(self.spawn_queue) > 0:
#                 enemy_type = self.spawn_queue.pop(0)
#                 self._enemies_to_spawn.append(
#                     enemy_factory.create(enemy_type, self._path)
#                 )


class EnemyType(Enum):
    BASIC = auto()
    REGENERATOR = auto()
    CHAMELEON = auto()


class EnemyInfo(Protocol):
    @property
    def health(self) -> int: ...

    @property
    def tile_spd(self) -> float: ...

    @property
    def exp_value(self) -> int: ...

    @property
    def size_dimensions(self) -> tuple[int, int]: ...

    @property
    def color(self) -> ct.BasicColors: ...

    @property
    def path_idx(self) -> int: ...

    @property
    def px_pos(self) -> tuple[float, float]: ...


class Enemy(ABC):
    def __init__(self, rng: Random, path: list[tuple[int, int]], hp: int):
        self._rng = rng
        self._health = hp
        self._tile_spd: float
        self._exp_value: int
        self._size_dimensions: tuple[int, int]
        self._color: ct.BasicColors = self._rng.choice(list(ct.BasicColors))

        self._path = path
        self._path_curr_idx: int = 0
        self._x_pos: float = self._path[self._path_curr_idx][0] * c.TILE_SIZE_PX
        self._y_pos: float = self._path[self._path_curr_idx][1] * c.TILE_SIZE_PX

        self._move_timer: int = 0
        self._sprite_anim_duration: int
        self._spritesheet_idx: int = 0

    @abstractmethod
    def apply_passive(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self, smooth: bool = False):
        self._move_timer += 1
        if self._path_curr_idx < len(self._path) - 1:
            next_tx, next_ty = self._path[self._path_curr_idx + 1]

            t = self._move_timer / c.FPS * self._tile_spd if smooth else 1

            self._x_pos = next_tx * c.TILE_SIZE_PX * t
            self._y_pos = next_ty * c.TILE_SIZE_PX * t

            if self._move_timer >= c.FPS / self._tile_spd:
                self._move_timer = 0
                self._path_curr_idx += 1

    def is_in_tunnel(self, tunnel: list[tuple[int, int]]) -> bool:
        curr_tx, curr_ty = self._path[self._path_curr_idx]
        return (curr_tx, curr_ty) in tunnel

    def update(self) -> None:
        self.apply_passive()
        self.move()

    @property
    def health(self) -> int:
        return self._health

    @property
    def tile_spd(self) -> float:
        return self._tile_spd

    @property
    def exp_value(self) -> int:
        return self._exp_value

    @property
    def size_dimensions(self) -> tuple[int, int]:
        return self._size_dimensions

    @property
    def color(self) -> ct.BasicColors:
        return self._color

    @property
    def path_idx(self) -> int:
        return self._path_curr_idx

    @property
    def px_pos(self) -> tuple[float, float]:
        return (self._x_pos, self._y_pos)


class BasicEnemy(Enemy):
    def __init__(self, rng: Random, path: list[tuple[int, int]], hp: int):
        super().__init__(rng, path, hp)
        self._tile_spd = 2.0
        self._exp_value = 1
        self._size_dimensions = (32, 32)

        self._sprite_anim_duration = u.secs_to_frames(1)

    def apply_passive(self):
        pass

    def draw(self):
        px.circ(self._x_pos, self._y_pos, 16, self._color.value)
