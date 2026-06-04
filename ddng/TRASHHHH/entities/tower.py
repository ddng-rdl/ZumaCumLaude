import random
import core.constants as c


class Tower:
    def __init__(self, tx: int, ty: int):
        self.tx = tx
        self.ty = ty
        self.size = c.TOWER_SIZE
        self.direction = 0  # 0:Up, 1:Right, 2:Down, 3:Left
        self.upgraded = False
        self.cooldown = 0
        self.next_color = random.choice(c.COLORS)
        self.next_color_2 = random.choice(c.COLORS)  # For upgraded shots
