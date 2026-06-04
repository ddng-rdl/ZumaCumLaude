import pyxel as px
from collections.abc import Mapping, Sequence
import core.constants as c
from entities.enemy import Enemy
from entities.tower import Tower
from entities.projectile import Bullet


class View:
    def _center_x(self, text: str) -> int:
        return c.SCREEN_CENTER_X - (len(text) * 4) // 2

    def clear_screen(self):
        px.cls(0)

    def show_grid(self):
        for x in range(0, c.SCREEN_SIZE, c.TILE):
            px.line(x, 0, x, c.SCREEN_SIZE, 1)
        for y in range(0, c.SCREEN_SIZE, c.TILE):
            px.line(0, y, c.SCREEN_SIZE, y, 1)

    def start_menu(
        self, state: str, leaderboard: Mapping[str, Sequence[Mapping[str, str | int]]]
    ):
        match state:
            case "START":
                title = "ZUMA: TOWER DEFENSE"
                px.text(self._center_x(title), 80, title, px.frame_count % 16)
                px.text(
                    self._center_x("Press [C] for Campaign"),
                    120,
                    "Press [C] for Campaign",
                    7,
                )
                px.text(
                    self._center_x("Press [E] for Endless"),
                    140,
                    "Press [E] for Endless",
                    7,
                )
                px.text(
                    self._center_x("Press [L] for Leaderboard"),
                    160,
                    "Press [L] for Leaderboard",
                    7,
                )
                return
            case "LEADERBOARD":
                px.text(self._center_x("LEADERBOARD"), 20, "LEADERBOARD", 10)
                px.text(40, 50, "CAMPAIGN", 9)
                for i, entry in enumerate(leaderboard["Campaign"]):
                    px.text(
                        self._center_x(
                            f"{entry['name']} - R:{entry['round']} K:{entry['kills']}"
                        ),
                        70 + i * 10,
                        f"{entry['name']} - R:{entry['round']} K:{entry['kills']}",
                        7,
                    )

                px.text(150, 50, "ENDLESS", 11)
                for i, entry in enumerate(leaderboard["Endless"]):
                    px.text(
                        150,
                        70 + i * 10,
                        f"{entry['name']} - R:{entry['round']} K:{entry['kills']}",
                        7,
                    )

                px.text(
                    self._center_x("Press [ESC] to Return"),
                    220,
                    "Press [ESC] to Return",
                    7,
                )
                return
            case "PAUSE":
                px.text(100, 120, "PAUSED", 10)
                return
            case _:
                return

    def show_temporary_pathway(self, paths: list[list[tuple[int, int]]], color: int):
        for path in paths:
            for i in range(len(path) - 1):
                x1, y1 = (
                    path[i][0] * c.TILE,
                    path[i][1] * c.TILE,
                )
                x2, y2 = (
                    path[i + 1][0] * c.TILE,
                    path[i + 1][1] * c.TILE,
                )
                px.line(x1, y1, x2, y2, color)

    def draw_tunnels(self, tunnels: set[tuple[int, int]]):
        for tx, ty in tunnels:
            px.rect(tx * c.TILE, ty * c.TILE, c.TILE, c.TILE, 4)

    def draw_towers(self, towers: set[Tower], selected_tower: Tower | None):
        for t in towers:
            px.blt(
                t.tx * c.TILE,
                t.ty * c.TILE,
                0,
                3 * c.SPRITE_ATLAS_TILE,
                0,
                c.TOWER_SIZE,
                c.TOWER_SIZE,
                0,
            )

            # Direction Indicator
            cx, cy = t.tx * c.TILE + c.TILE // 2, t.ty * c.TILE + c.TILE // 2
            dirs = [(0, -4), (4, 0), (0, 4), (-4, 0)]
            px.circ(
                cx + dirs[t.direction][0], cy + dirs[t.direction][1], 2, t.next_color
            )

            if t.upgraded:
                px.text(
                    t.tx * c.TILE + (c.TILE - c.FONT_CHAR_WIDTH) // 2,
                    t.ty * c.TILE + (c.TILE - c.FONT_LINE_HEIGHT) // 2,
                    "+",
                    8,
                )
                px.circ(
                    cx + dirs[t.direction][0] * 2,
                    cy + dirs[t.direction][1] * 2,
                    1,
                    t.next_color_2,
                )

            # Selection Highlight
            if t == selected_tower:
                px.rectb(
                    t.tx * c.TILE, t.ty * c.TILE, c.TILE, c.TILE, 10
                )  # Yellow highlight

    def draw_enemies(self, enemies: set[Enemy]):
        for e in enemies:
            if not e.is_in_tunnel():
                img_u = 0
                if e.etype == 1:
                    img_u = c.SPRITE_ATLAS_TILE
                if e.etype == 2:
                    img_u = 2 * c.SPRITE_ATLAS_TILE
                px.blt(
                    e.pixel_x - e.size // 2,
                    e.pixel_y - e.size // 2,
                    0,
                    img_u,
                    0,
                    e.size,
                    e.size,
                    0,
                )
                px.circ(e.pixel_x, e.pixel_y, e.size, e.color)
                px.text(e.pixel_x - 2, e.pixel_y - 12, str(e.hp), 7)

    def draw_projectiles(self, bullets: set[Bullet]):
        for b in bullets:
            px.circ(b.x, b.y, b.radius, b.color)

    def draw_shooter(self, shooter_color: int):
        cx, cy = c.SCREEN_CENTER_X, c.SCREEN_CENTER_Y
        px.circ(cx, cy, c.SHOOTER_OUTER_RADIUS, 13)
        px.circ(cx, cy, c.SHOOTER_INNER_RADIUS, shooter_color)

    def draw_game_stats(self, lives: int, exp: int, round: int, kills: int):
        px.text(5, 5, f"LIVES: {lives}  EXP: {exp}", 15)
        px.text(5, 15, f"ROUND: {round}  KILLS: {kills}", 7)

    def draw_between_rounds(
        self,
        selected_tower: Tower | None,
        between_rounds: bool,
        state: str,
        nickname: str,
        mode: str,
        lives: int,
    ):
        if between_rounds and state == "PLAY":
            px.text(self._center_x("BETWEEN ROUNDS"), 100, "BETWEEN ROUNDS", 10)
            px.text(
                self._center_x("Click empty space to build (5 EXP)"),
                120,
                "Click empty space to build (5 EXP)",
                7,
            )
            px.text(
                self._center_x("Click tower to SELECT it"),
                130,
                "Click tower to SELECT it",
                7,
            )
            if selected_tower:
                px.text(
                    self._center_x("[W A S D] to aim selected tower"),
                    145,
                    "[W A S D] to aim selected tower",
                    10,
                )
                if not selected_tower.upgraded:
                    px.text(
                        self._center_x("[U] to upgrade selected (10 EXP)"),
                        155,
                        "[U] to upgrade selected (10 EXP)",
                        11,
                    )
            px.text(
                self._center_x("Press ENTER to start round"),
                175,
                "Press ENTER to start round",
                8,
            )

        if state == "PAUSE":
            px.text(self._center_x("PAUSED"), 120, "PAUSED", 10)

        if state == "GAMEOVER":
            msg = "YOU WIN!" if lives > 0 and mode == "CAMPAIGN" else "GAME OVER"
            px.text(self._center_x(msg), 100, msg, 8)
            px.text(self._center_x("ENTER NICKNAME:"), 130, "ENTER NICKNAME:", 7)
            px.text(self._center_x(nickname + "_"), 130, nickname + "_", 10)
            px.text(
                self._center_x("Press ENTER to submit"), 150, "Press ENTER to submit", 7
            )
