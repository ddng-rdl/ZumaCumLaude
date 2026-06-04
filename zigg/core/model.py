from __future__ import annotations

import math
import random
#import json
#import pyxel as px
from enum import Enum, auto

import core.constants as c
#import core.utils as u

from entities.enemy import Enemy, BasicEnemy, Regenerator, Chameleon
from entities.tower import Tower, BasicTower
from entities.projectile import Projectile, BasicProjectile

# CLASS ENUM FOR GAMESTATE
class GameState(Enum):
    PLAYING   = auto()
    GAME_OVER = auto()

class Shooter:
    FIRE_COOLDOWN = 1 / 0.9
 
    def __init__(self):
        self.x = c.WINDOW_WIDTH / 2
        self.y = c.WINDOW_HEIGHT / 2
        self._fire_timer = 0.0
        self.direction: tuple[float, float] = (0.0, -1.0)
        self.color: c.Color = random.choice(list(c.Color)[:1])  # Phase 1: 1 color
 
    def update(self, dt: float) -> None:
        self._fire_timer += dt
 
    def aim_at(self, mx: float, my: float) -> None:
        dx, dy = mx - self.x, my - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.direction = (dx / dist, dy / dist)
 
    def can_fire(self) -> bool:
        return self._fire_timer >= self.FIRE_COOLDOWN
 
    def fire(self) -> BasicProjectile:
        self._fire_timer -= self.FIRE_COOLDOWN
        return BasicProjectile(
            position=(self.x, self.y),
            direction=self.direction,
            color=self.color,
        )
    
class Model:
    ENEMY_COUNT  = 5      
    SPAWN_INTERVAL = 1.5  # ENEMY SPAWN INTERVAL SECONDS
 
    def __init__(self):
        self.state   = GameState.PLAYING
        self.lives   = 2
        self.exp     = 0
 
        self.shooter = Shooter()
 
        # Spawn queue
        color = list(c.Color)[0]  # all enemies same color for now
        self._spawn_queue: list[Enemy] = [BasicEnemy(color) for _ in range(self.ENEMY_COUNT)]
        self._spawn_timer  = 0.0
 
        self.enemies:     list[Enemy]      = []
        self.projectiles: list[Projectile] = []
 
    @property
    def path(self) -> list[tuple[int, int]]:
        return c.PATH_1
    
    def aim(self, mx: float, my: float) -> None:
        self.shooter.aim_at(mx, my)
 
    def fire(self) -> None:
        if self.state != GameState.PLAYING:
            return
        if self.shooter.can_fire():
            self.projectiles.append(self.shooter.fire())

    def update(self) -> None:
        if self.state != GameState.PLAYING:
            return
 
        dt = 1 / c.FPS
 
        self.shooter.update(dt)
        self._update_spawning(dt)
        self._update_enemies(dt)
        self._update_projectiles(dt)
        self._check_collisions()
        self._check_game_over()
 
    def _update_spawning(self, dt: float) -> None:
        self._spawn_timer += dt
        if self._spawn_queue and self._spawn_timer >= self.SPAWN_INTERVAL:
            self._spawn_timer -= self.SPAWN_INTERVAL
            self.enemies.append(self._spawn_queue.pop(0))
 
    def _update_enemies(self, dt: float) -> None:
        reached_end: list[Enemy] = []
        for enemy in self.enemies:
            enemy.update(dt)
            if enemy.position_idx >= len(c.PATH_1):
                reached_end.append(enemy)
 
        for enemy in reached_end:
            self.enemies.remove(enemy)
            self.lives -= 1
 
        self.enemies = [e for e in self.enemies if e.is_alive and e.position_idx < len(c.PATH_1)]
 
    def _update_projectiles(self, dt: float) -> None:
        for proj in self.projectiles:
            proj.update(dt)
            x, y = proj.position
            if x < 0 or x > c.WINDOW_WIDTH or y < 0 or y > c.WINDOW_HEIGHT:
                proj.deactivate()
        self.projectiles = [p for p in self.projectiles if p.is_active]
 
    def _check_collisions(self) -> None:
        for proj in self.projectiles:
            if not proj.is_active:
                continue
            px, py = proj.position
            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue
                if enemy.position_idx >= len(c.PATH_1):
                    continue
                ex, ey = c.PATH_1[enemy.position_idx]
                ex_px = ex * c.GRID_TILE_SIZE + c.GRID_TILE_SIZE // 2
                ey_px = ey * c.GRID_TILE_SIZE + c.GRID_TILE_SIZE // 2
                dist = math.hypot(px - ex_px, py - ey_px)
                if dist <= proj.radius + enemy.square_side_length // 2:
                    if proj.color == enemy.color:
                        enemy.take_hit(proj.damage)
                        proj.hit()
                        if not enemy.is_alive:
                            self.exp += enemy.exp_value
 
    def _check_game_over(self) -> None:
        all_gone = not self._spawn_queue and not self.enemies
        if self.lives <= 0 or all_gone:
            self.state = GameState.GAME_OVER