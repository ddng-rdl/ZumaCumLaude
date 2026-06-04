from __future__ import annotations
import pyxel as px

import core.constants as c
from core.constants import Color
from core.model import Model, GameState

# ---------------------------------------------------------------------------
# Pyxel color palette mapping
# ---------------------------------------------------------------------------
# Pyxel uses a 16-color palette (indices 0-15). Standard mapping:
# 0=black, 1=dark blue, 2=dark purple, 3=dark green, 4=brown, 5=dark gray,
# 6=light gray, 7=white, 8=red, 9=orange, 10=yellow, 11=green,
# 12=blue, 13=indigo/violet, 14=pink, 15=peach

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

    # ------------------------------------------------------------------
    # Path
    # ------------------------------------------------------------------

    def _draw_path(self) -> None:
        for gx, gy in self._model.path:
            px.rect(
                gx * c.GRID_TILE_SIZE,
                gy * c.GRID_TILE_SIZE,
                c.GRID_TILE_SIZE,
                c.GRID_TILE_SIZE,
                PATH_COLOR,
            )

    # ------------------------------------------------------------------
    # Enemies
    # ------------------------------------------------------------------

    def _draw_enemies(self) -> None:
        path = self._model.path
        for enemy in self._model.enemies:
            idx = enemy.position_idx
            if idx >= len(path):
                continue
            gx, gy = path[idx]
            # Center the enemy square on the tile
            half = enemy.square_side_length // 2
            ex = gx * c.GRID_TILE_SIZE + c.GRID_TILE_SIZE // 2 - half
            ey = gy * c.GRID_TILE_SIZE + c.GRID_TILE_SIZE // 2 - half
            col = COLOR_MAP.get(enemy.color, 7)
            px.rect(ex, ey, enemy.square_side_length, enemy.square_side_length, col)

    # ------------------------------------------------------------------
    # Projectiles
    # ------------------------------------------------------------------

    def _draw_projectiles(self) -> None:
        for proj in self._model.projectiles:
            x, y = proj.position
            col = COLOR_MAP.get(proj.color, 7)
            px.circ(int(x), int(y), proj.radius, col)

    # ------------------------------------------------------------------
    # Shooter
    # ------------------------------------------------------------------

    def _draw_shooter(self) -> None:
        s = self._model.shooter
        sx, sy = int(s.x), int(s.y)
        # Body: small white circle
        px.circ(sx, sy, 10, SHOOTER_COLOR)
        # Direction indicator: line pointing in aim direction
        dx, dy = s.direction
        ex = int(sx + dx * 16)
        ey = int(sy + dy * 16)
        px.line(sx, sy, ex, ey, COLOR_MAP.get(s.color, 7))

    # ------------------------------------------------------------------
    # HUD
    # ------------------------------------------------------------------

    def _draw_hud(self) -> None:
        px.text(4, 4, f"LIVES: {self._model.lives}", TEXT_COLOR)
        px.text(4, 14, f"EXP:   {self._model.exp}", TEXT_COLOR)

    # ------------------------------------------------------------------
    # Game over overlay
    # ------------------------------------------------------------------

    def _draw_game_over(self) -> None:
        # Semi-transparent overlay via a dark rect
        px.rect(100, 200, 312, 80, 1)
        if self._model.lives <= 0:
            msg = "GAME OVER"
        else:
            msg = "YOU WIN!"
        px.text(220, 216, msg, GAMEOVER_COLOR)
        px.text(180, 236, "close the window to exit", TEXT_COLOR)