from __future__ import annotations
from random import Random

import core.constants as c
import core.utils as u
import core.common_types as ct
from entities.enemy import Enemy
from entities.tower import Tower
from entities.projectile import Projectile
from entities.factory import EntityFactory
from entities.projectile import ProjectileType
from levels.world import World, CampaignWorld, EndlessWorld


class Model:
    def __init__(self, factory: EntityFactory, rng: Random) -> None:
        self.__world: World | None = None
        self.__factory = factory
        self.__rng = rng
        self.__settings = u.read_json(c.SETTINGS_PATH)

    def start_game(self, mode: ct.GameMode) -> None:
        if mode == ct.GameMode.CAMPAIGN:
            self.__world = CampaignWorld(self.__factory, self.__rng, self.__settings)
        elif mode == ct.GameMode.ENDLESS:
            self.__world = EndlessWorld(self.__factory, self.__rng, self.__settings)

        self.reset_states()
    
    def reset_states(self) -> None:
        self.enemies: list[Enemy] = []
        self.towers: list[Tower] = []
        self.projectiles: list[Projectile] = []

        self.current_round: int = 0
        self.between_rounds: bool = True

        self.paths: dict[int, list[tuple[int, int]]] = {}
        self.placeable_tiles: set[tuple[int, int]] = self.__world.placeable_tiles if self.__world else set()
        self.tunnels: set[tuple[int, int]]  = self.__world.tunnels if self.__world else set()

        self.player_lives: int = self.__settings["num_lives"]
        self.player_exp: int = 0

    def start_round(self) -> None:
        self.current_round += 1
        self.between_rounds = False
        if self.__world:
            self.__world.prepare_round(self.current_round)

    def update_states(self) -> None:
        self._update_spawning()
        self._update_enemies()
        self._update_towers()
        self._update_projectiles()
        self._check_collisions()
        self._check_round_end()

    def _update_spawning(self) -> None:
        if self.__world is None:
            return
        
        enemy = self.__world.try_spawn()
        if enemy is not None:
            self.enemies.append(enemy)

    def _update_enemies(self) -> None:
        enemies_reached_end: list[Enemy] = []

        for enemy in self.enemies:
            enemy.update()
            if enemy.path_idx >= len(enemy.path) - 1:
                enemies_reached_end.append(enemy)

        for enemy in enemies_reached_end:
            self.enemies.remove(enemy)
            self.player_lives -= 1

        self.enemies = [e for e in self.enemies if e.is_alive]
    
    def _update_towers(self) -> None:
        for tower in self.towers:
            fired = tower.update()
            if fired:
                dirs = {
                    ct.Direction.UP:    (0, -1),
                    ct.Direction.DOWN:  (0,  1),
                    ct.Direction.LEFT:  (-1, 0),
                    ct.Direction.RIGHT: (1,  0),
                }
                dx, dy = dirs[tower.direction]
                proj = self.__factory.create_projectile(
                    ProjectileType.BULLET,
                    tower.tile_x * c.TILE_SIZE_PX,
                    tower.tile_y * c.TILE_SIZE_PX,
                    dx * c.BULLET_SPEED,
                    dy * c.BULLET_SPEED,
                    tower.color
                )
                self.projectiles.append(proj)

    def _update_projectiles(self) -> None:
        for proj in self.projectiles:
            proj.update()
        
        self.projectiles = [
            p for p in self.projectiles
            if 0 <= p.x <= c.WINDOW_WIDTH and 0 <= p.y <= c.WINDOW_HEIGHT
        ]

    def _check_collisions(self) -> None:
        for proj in self.projectiles:
            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue
                if enemy.is_in_tunnel(list(self.tunnels)):
                    continue
                ex, ey = enemy.px_pos
                dist = u.get_distance(proj.x, proj.y, ex, ey)
                if dist <= enemy.size_dimensions[0] // 2:
                    if proj.color == enemy.color:
                        enemy.take_hit(1)
                        self.projectiles.remove(proj)
                        if not enemy.is_alive:
                            self.player_exp += enemy.exp_value
                        break

    def _check_round_end(self) -> None:
        if self.__world is None:
            return
        if self.__world.is_round_complete and not self.enemies:
            self.between_rounds = True