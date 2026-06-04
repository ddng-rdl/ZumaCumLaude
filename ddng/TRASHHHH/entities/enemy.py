import random
import core.constants as c


class Enemy:
    def __init__(
        self, path_idx: int, hp: int, etype: int, regen_rate: int, cham_rate: int
    ):
        self.path_idx = path_idx
        self.path: list[tuple[int, int]] = c.PATHS[path_idx]
        self.node = 0
        self.hp = hp
        self.color = random.choice(c.COLORS)
        self.etype = etype  # 0: Normal, 1: Regen, 2: Chameleon
        self.regen_rate = regen_rate
        self.cham_rate = cham_rate
        self.frames_alive = 0
        self.move_timer = 0
        self.tiles_moved = 0
        self.size = c.ENEMY_SIZE

        self.pixel_x = self.path[self.node][0] * c.TILE
        self.pixel_y = self.path[self.node][1] * c.TILE

    def update(self):
        self.frames_alive += 1
        self.move_timer += 1

        if self.node < len(self.path) - 1:
            next_tx, next_ty = self.path[self.node + 1]

            self.pixel_x = next_tx * c.TILE
            self.pixel_y = next_ty * c.TILE

            if self.move_timer >= c.ENEMY_MOVE_FRAMES:
                self.node += 1
                self.move_timer = 0
                self.tiles_moved += 1

                if self.etype == 1 and self.tiles_moved >= self.regen_rate:
                    self.hp += 1
                    self.tiles_moved = 0

        if self.etype == 2 and self.frames_alive % self.cham_rate == 0:
            self.color = random.choice(c.COLORS)

    def is_in_tunnel(self):
        curr_tx, curr_ty = self.path[self.node]
        return (curr_tx, curr_ty) in c.TUNNELS
