import pyxel as px
import core.constants as c
import core.utils as u
import math
import random
from core.model import Model
from core.view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view

    def draw(self):
        self.view.clear_screen()
        self.view.show_grid()
        self.view.start_menu(self.model.state, self.model.leaderboard)

        if self.model.state == "PLAY":
            # Game Elements
            self.view.show_temporary_pathway(c.PATHS, 5)  # Light gray paths

            self.view.draw_tunnels(c.TUNNELS)  # Cyan tunnels

            # Towers
            self.view.draw_towers(self.model.towers, self.model.selected_tower)

            # Enemies (Hide if in tunnel)
            self.view.draw_enemies(self.model.enemies)

            # Bullets
            self.view.draw_projectiles(self.model.bullets)

            # Shooter
            self.view.draw_shooter(self.model.shooter_color)

            # UI Overlays
            self.view.draw_game_stats(
                self.model.lives, self.model.exp, self.model.round, self.model.kills
            )
            self.view.draw_between_rounds(
                self.model.selected_tower,
                self.model.between_rounds,
                self.model.state,
                self.model.nickname,
                self.model.mode,
                self.model.lives,
            )

    def update(self):
        if self.model.state == "START":
            if px.btnp(px.KEY_C):
                self.model.mode = "CAMPAIGN"
                self.model.reset_game()
                self.model.state = "PLAY"
                px.playm(0, loop=True)
            elif px.btnp(px.KEY_E):
                self.model.mode = "ENDLESS"
                self.model.reset_game()
                self.model.state = "PLAY"
                px.playm(0, loop=True)
            elif px.btnp(px.KEY_L):
                self.model.state = "LEADERBOARD"

        elif self.model.state == "LEADERBOARD":
            if px.btnp(px.KEY_ESCAPE):
                self.model.state = "START"

        elif self.model.state == "PAUSE":
            if px.btnp(px.KEY_SPACE):
                self.model.state = "PLAY"

        elif self.model.state == "GAMEOVER":
            for key in range(px.KEY_A, px.KEY_Z + 1):
                if px.btnp(key) and len(self.model.nickname) < 5:
                    self.model.nickname += chr(key - px.KEY_A + 65)
            if px.btnp(px.KEY_BACKSPACE) and len(self.model.nickname) > 0:
                self.model.nickname = self.model.nickname[:-1]
            if px.btnp(px.KEY_RETURN) and len(self.model.nickname) > 0:
                lb = self.model.leaderboard
                lb[self.model.mode].append(
                    {
                        "name": self.model.nickname,
                        "round": self.model.round,
                        "kills": self.model.kills,
                    }
                )
                lb[self.model.mode] = sorted(
                    lb[self.model.mode], key=lambda x: x["kills"], reverse=True
                )[:5]
                u.save_leaderboard(lb)
                self.model.state = "START"

        elif self.model.state == "PLAY":
            if px.btnp(px.KEY_SPACE):
                self.model.state = "PAUSE"
                return

            if self.model.between_rounds:
                if px.btnp(px.KEY_RETURN):
                    self.model.start_round()

                # Interactive Selectable Towers
                tx, ty = px.mouse_x // c.TILE, px.mouse_y // c.TILE

                if px.btnp(px.MOUSE_BUTTON_LEFT):
                    clicked_tower = next(
                        (t for t in self.model.towers if t.tx == tx and t.ty == ty),
                        None,
                    )

                    if clicked_tower:
                        self.model.selected_tower = clicked_tower
                    else:
                        self.model.selected_tower = None
                        # Check if empty space and not a path
                        on_path = any((tx, ty) in p for p in c.PATHS)
                        if not on_path and self.model.exp >= c.TOWER_COST:
                            from core.model import Tower

                            new_tower = Tower(tx, ty)
                            self.model.towers.add(new_tower)
                            self.model.selected_tower = new_tower
                            self.model.exp -= c.TOWER_COST

                # Handle Selected Tower Commands
                if self.model.selected_tower:
                    if px.btnp(px.KEY_W):
                        self.model.selected_tower.direction = 0
                    if px.btnp(px.KEY_D):
                        self.model.selected_tower.direction = 1
                    if px.btnp(px.KEY_S):
                        self.model.selected_tower.direction = 2
                    if px.btnp(px.KEY_A):
                        self.model.selected_tower.direction = 3
                    if (
                        px.btnp(px.KEY_U)
                        and not self.model.selected_tower.upgraded
                        and self.model.exp >= c.UPGRADE_COST
                    ):
                        self.model.selected_tower.upgraded = True
                        self.model.exp -= c.UPGRADE_COST

            else:
                # Shooting freely with Mouse
                if px.btn(px.MOUSE_BUTTON_LEFT) and self.model.shooter_cooldown == 0:
                    cx, cy = c.SCREEN_SIZE // 2, c.SCREEN_SIZE // 2
                    angle = math.atan2(px.mouse_y - cy, px.mouse_x - cx)
                    dx = math.cos(angle) * c.BULLET_SPEED
                    dy = math.sin(angle) * c.BULLET_SPEED

                    from core.model import Bullet

                    self.model.bullets.add(
                        Bullet(cx, cy, dx, dy, self.model.shooter_color)
                    )
                    self.model.shooter_color = random.choice(c.COLORS)
                    self.model.shooter_cooldown = c.PLAYER_COOLDOWN
                    px.play(0, 0)

            self.model.update()
