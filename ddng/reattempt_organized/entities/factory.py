from __future__ import annotations

from random import Random

# import core.constants as c
import core.common_types as ct
from entities.enemy import (
    Enemy,
    EnemyType,
    BasicEnemy,
    # RegeneratorEnemy,
    # ChameleonEnemy,
)
from entities.tower import Tower, TowerType, BasicTower
from entities.projectile import Projectile, ProjectileType, Bullet


class EntityFactory:
    def __init__(self, rng: Random) -> None:
        self._rng = rng
        self._enemy_registry: dict[EnemyType, type[Enemy]] = {
            EnemyType.BASIC: BasicEnemy,
            # EnemyType.REGENERATOR: RegeneratorEnemy,
            # EnemyType.CHAMELEON: ChameleonEnemy,
        }
        self._tower_registry: dict[TowerType, type[Tower]] = {
            TowerType.BASIC: BasicTower,
        }
        self._projectile_registry: dict[ProjectileType, type[Projectile]] = {
            ProjectileType.BULLET: Bullet,
        }

    def create_enemy(
        self, enemy_type: EnemyType, path: list[tuple[int, int]], hp: int
    ) -> Enemy:
        enemy = self._enemy_registry[enemy_type](self._rng, path, hp)
        return enemy

    def create_tower(self, tower_type: TowerType, x: int, y: int) -> Tower:
        tower = self._tower_registry[tower_type](self._rng, x, y)
        return tower

    def create_projectile(
        self,
        projectile_type: ProjectileType,
        x: int,
        y: int,
        dx: float,
        dy: float,
        color: ct.BasicColors,
    ) -> Projectile:
        projectile = self._projectile_registry[projectile_type](x, y, dx, dy, color)
        return projectile
