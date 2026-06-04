import random
from entities.projectile import Bullet
import pyxel as px
import core.constants as c
import core.utils as u
from entities.enemy import Enemy
from entities.tower import Tower


class Model:
    def __init__(self):
        self.settings = u.load_settings()
        self.leaderboard = u.load_leaderboard()
        self.state: str = "START"
        self.mode: str = "CAMPAIGN"
        self.reset_game()

    def reset_game(self):
        self.lives: int = self.settings["l"]
        self.exp: int = 20  # Start with some EXP to test placing towers
        self.round: int = 1
        self.enemies: set[Enemy] = set()
        self.bullets: set[Bullet] = set()
        self.towers: set[Tower] = set()
        self.selected_tower: Tower | None = None
        self.shooter_cooldown: int = 0
        self.shooter_color: int = random.choice(c.COLORS)
        self.enemies_to_spawn: int = 0
        self.spawn_timer: float = 0
        self.nickname: str = ""
        self.kills: int = 0
        self.between_rounds: bool = True

    def start_round(self):
        self.between_rounds: bool = False
        base_enemies = self.settings["e"]

        # Difficulty scaling
        if self.mode == "CAMPAIGN":
            self.enemies_to_spawn = base_enemies + int(self.round * 2)
        else:
            self.enemies_to_spawn = base_enemies + int(self.round * 3.5)

        self.spawn_timer = 0
        self.selected_tower: Tower | None = None

    def spawn_enemy(self):
        if self.enemies_to_spawn > 0:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                hp = 1 + (self.round // 3)
                etype = (
                    random.choices([0, 1, 2], weights=[70, 15, 15])[0]
                    if self.round > 2
                    else 0
                )
                path_choice = random.randint(0, 1)
                self.enemies.add(
                    Enemy(
                        path_choice, hp, etype, self.settings["h"], self.settings["f"]
                    )
                )
                self.enemies_to_spawn -= 1
                self.spawn_timer = c.FPS * (
                    1.5 - min(0.5, self.round * 0.05)
                )  # Spawns get slightly faster

    def update_shooter_cd(self):
        if self.shooter_cooldown > 0:
            self.shooter_cooldown -= 1

    def update_towers(self):
        for t in self.towers:
            if t.cooldown > 0:
                t.cooldown -= 1
            elif len(self.enemies) > 0:
                t.cooldown = c.TOWER_COOLDOWN
                cx, cy = t.tx * c.TILE + 8, t.ty * c.TILE + 8
                dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                dx, dy = dirs[t.direction]

                # Base bullet
                self.bullets.add(
                    Bullet(
                        cx, cy, dx * c.BULLET_SPEED, dy * c.BULLET_SPEED, t.next_color
                    )
                )
                t.next_color = random.choice(c.COLORS)

                if t.upgraded:
                    # To prevent colors matching on upgraded tower
                    while t.next_color_2 == t.next_color:
                        t.next_color_2 = random.choice(c.COLORS)
                    self.bullets.add(
                        Bullet(
                            cx,
                            cy,
                            dx * c.BULLET_SPEED,
                            dy * c.BULLET_SPEED,
                            t.next_color_2,
                        )
                    )
                    t.next_color_2 = random.choice(c.COLORS)

                px.play(0, 0)

    def update_bullets(self):
        for b in self.bullets.copy():
            b.x += b.dx
            b.y += b.dy

            if (
                b.x < -c.BULLET_RADIUS
                or b.x > c.SCREEN_SIZE + c.BULLET_RADIUS
                or b.y < -c.BULLET_RADIUS
                or b.y > c.SCREEN_SIZE + c.BULLET_RADIUS
            ):
                self.bullets.remove(b)

    def update_entities(self):
        for e in self.enemies.copy():
            e.update()

            if e.node >= len(e.path) - 1:
                self.lives -= 1
                self.enemies.remove(e)
                if self.lives <= 0:
                    self.state = "GAMEOVER"
                continue

            if not e.is_in_tunnel():
                for b in self.bullets.copy():
                    if u.get_distance(e.pixel_x, e.pixel_y, b.x, b.y) < e.size / 2:
                        if b.color == e.color:
                            e.hp -= 1
                            self.bullets.remove(b)
                            px.play(1, 1)
                            if e.hp <= 0:
                                self.exp += 1
                                self.kills += 1
                                if e in self.enemies:
                                    self.enemies.remove(e)
                        break

    def check_round_end(self):
        if self.enemies_to_spawn <= 0 and len(self.enemies) == 0:
            self.between_rounds = True
            if self.mode == "CAMPAIGN" and self.round >= 12:
                self.state = "GAMEOVER"
            else:
                self.round += 1

    def update(self):
        if self.state != "PLAY" or self.between_rounds:
            return

        self.spawn_enemy()
        self.update_shooter_cd()
        self.update_towers()
        self.update_bullets()
        self.update_entities()
        self.check_round_end()
