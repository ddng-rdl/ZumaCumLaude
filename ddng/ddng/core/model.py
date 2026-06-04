from __future__ import annotations
from random import Random

import core.constants as c
import core.utils as u
from entities.enemy import Enemy
from entities.tower import Tower
from entities.projectile import Projectile
from entities.factory import EntityFactory
from levels.world import World


class Model:
    def __init__(
        self,
        factory: EntityFactory,
        rng: Random,
    ) -> None:
        self.__world = World
        self.__rng = rng
        self.__settings = u.read_json(c.SETTINGS_PATH)
        self.reset_states()

    def reset_states(self) -> None:
        self.enemies: list[Enemy] = []
        self.towers: list[Tower] = []
        self.projectiles: list[Projectile] = []

        self.current_round: int = 0
        self.between_rounds: bool = True

        self.paths: dict[int, list[tuple[int, int]]] = {}
        self.player_lives: int = 2
        self.player_exp: int = 0

    def update_states(self) -> None:
        pass

    def start_round(self) -> None:
        self.current_round += 1
