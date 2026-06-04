import core.constants as c


class Bullet:
    def __init__(self, x: float, y: float, dx: float, dy: float, color: int):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = c.BULLET_RADIUS
