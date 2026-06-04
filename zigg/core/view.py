from __future__ import annotations
import pyxel as px

import core.constants as c
from core.constants import Color
from core.model import Model, GameState


COLOR_MAP: dict[Color, int] = {
    Color.RED:    8,
    Color.ORANGE: 9,
    Color.YELLOW: 10,
    Color.GREEN:  11,
    Color.BLUE:   12,
    Color.VIOLET: 13,
}

PATH_COLOR      = 5   # dark gray
SHOOTER_COLOR   = 7   # white
BG_COLOR        = 0   # black
TEXT_COLOR      = 7   # white
GAMEOVER_COLOR  = 8   # red


class View:
    def __init__(self, model: Model):
        self._model = model

    def draw(self) -> None:
        px.cls(BG_COLOR)
        self._draw_path()
        self._draw_enemies()
        self._draw_projectiles()
        self._draw_shooter()
        self._draw_hud()

        if self._model.state == GameState.GAME_OVER:
            self._draw_game_over()


    # PATH
    def _draw_path(self) -> None:
        for gx, gy in self._model.path:
            px.rect(
                gx * c.TILE_SIZE_PX,
                gy * c.TILE_SIZE_PX,
                c.TILE_SIZE_PX,
                c.TILE_SIZE_PX,
                PATH_COLOR,
            )

    # ENEMIES
    def _draw_enemies(self) -> None:
        path = self._model.path
        for enemy in self._model.enemies:
            idx = enemy.position_idx
            if idx >= len(path):
                continue
            gx, gy = path[idx]
            # Center the enemy square on the tile
            half = enemy.square_side_length // 2
            ex = gx * c.TILE_SIZE_PX + c.TILE_SIZE_PX // 2 - half
            ey = gy * c.TILE_SIZE_PX + c.TILE_SIZE_PX // 2 - half
            col = COLOR_MAP.get(enemy.color, 7)
            px.rect(ex, ey, enemy.square_side_length, enemy.square_side_length, col)


    # PROJECTILES
    def _draw_projectiles(self) -> None:
        for proj in self._model.projectiles:
            x, y = proj.position
            col = COLOR_MAP.get(proj.color, 7)
            px.circ(int(x), int(y), proj.radius, col)


    # SHOOTER
    def _draw_shooter(self) -> None:
        s = self._model.shooter
        sx, sy = int(s.x), int(s.y)
        px.circ(sx, sy, 10, SHOOTER_COLOR)

        dx, dy = s.direction
        ex = int(sx + dx * 16)
        ey = int(sy + dy * 16)
        px.line(sx, sy, ex, ey, COLOR_MAP.get(s.color, 7))


    # HUD
    def _draw_hud(self) -> None:
        px.text(4, 4, f"LIVES: {self._model.lives}", TEXT_COLOR)
        px.text(4, 14, f"EXP:   {self._model.exp}", TEXT_COLOR)


    # GAME OVER
    def _draw_game_over(self) -> None:
        px.rect(100, 200, 312, 80, 1)
        if self._model.lives <= 0:
            msg = "GAME OVER"
        else:
            msg = "YOU WIN!"
        px.text(220, 216, msg, GAMEOVER_COLOR)
        px.text(180, 236, "close the window to exit", TEXT_COLOR)