from __future__ import annotations
from abc import ABC, abstractmethod
from random import Random
from typing import Any

import core.utils as u
import core.constants as c
from entities.enemy import Enemy, EnemyType
from entities.factory import EntityFactory

class World(ABC):
    def __init__(self, factory: EntityFactory, rng: Random, settings: dict[str, Any]):
        self._factory = factory
        self._rng = rng
        self._settings = settings

        tmj_data = u.read_json("levels/level.tmj")
        flat_data = self._flatten_layers(tmj_data)
        self.paths: dict[int, list[tuple[int, int]]] = u.extract_grid_paths(flat_data)
        self.tunnels: set[tuple[int, int]] = set()
        self.placeable_tiles: set[tuple[int, int]] = self._get_placeable_tiles()

        self._round_num: int = 0
        self._spawn_queue: list[Enemy] = []
        self._spawn_timer: int = 0
        self._spawn_interval_frames: int = int(1.5 * c.FPS)

    @property
    def is_round_complete(self) -> bool:
        return len(self._spawn_queue) == 0
    
    def _flatten_layers(self, tmj_data: dict[str, Any]) -> dict[str, Any]:
        flat_layers = self._flatten(tmj_data["layers"])
        return {**tmj_data, "layers": flat_layers}

    def _flatten(self, layers: list[dict[str, Any]]) -> list[dict[str, Any]]:
        flat: list[dict[str, Any]] = []
        for layer in layers:
            if layer["type"] == "group":
                flat.extend(self._flatten(layer["layers"]))
            else:
                flat.append(layer)
        return flat

    def _get_placeable_tiles(self) -> set[tuple[int, int]]:
        all_path_tiles: set[tuple[int, int]] = set()
        for path in self.paths.values():
            all_path_tiles.update(path)

        all_tiles = {
            (x, y)
            for x in range(c.GRID_SIZE)
            for y in range(c.GRID_SIZE)
        }

        return all_tiles - all_path_tiles - self.tunnels
    
    def _pick_enemy_type(self, round_num: int) -> EnemyType:
        if round_num <= 2:
            return EnemyType.BASIC
        return self._rng.choices(
            [EnemyType.BASIC, EnemyType.REGENERATOR, EnemyType.CHAMELEON],
            weights=[70, 15, 15]
        )[0]  

    def try_spawn(self) -> Enemy | None:
        if not self._spawn_queue:
            return None

        self._spawn_timer += 1
        if self._spawn_timer >= self._spawn_interval_frames:
            self._spawn_timer -= self._spawn_interval_frames
            return self._spawn_queue.pop(0)

        return None
    
    @abstractmethod
    def prepare_round(self, round_num: int) -> None: ...

class CampaignWorld(World):
    def prepare_round(self, round_num: int) -> None:
        self._spawn_queue.clear()
        self._spawn_timer = 0
        self._round_num = round_num

        base_enemies = self._settings["max_enemies"]
        count = base_enemies + int(round_num)

        for _ in range(count):
            hp = 1 + (round_num // 3)
            etype = self._pick_enemy_type(round_num)
            path_num = self._rng.randint(1, len(self.paths))
            path = self.paths[path_num]
            enemy = self._factory.create_enemy(etype, path, hp)
            self._spawn_queue.append(enemy)

class EndlessWorld(World):
    def prepare_round(self, round_num: int) -> None:
        self._spawn_queue.clear()
        self._spawn_timer = 0
        self._round_num = round_num

        base_enemies = self._settings["max_enemies"]
        count = base_enemies + int(round_num * 3.5) # this just adds nmn pero maybe pwede ung speed ung iadjust

        for _ in range(count):
            hp = 1 + (round_num // 3)
            etype = self._pick_enemy_type(round_num)
            path_num = self._rng.randint(1, len(self.paths))
            path = self.paths[path_num]
            enemy = self._factory.create_enemy(etype, path, hp)
            self._spawn_queue.append(enemy)



