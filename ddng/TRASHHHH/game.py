import pyxel as px
import core.assets as assets
import core.constants as c
from core.model import Model
from core.controller import Controller
from core.view import View


class Game:
    def __init__(self):
        px.init(c.SCREEN_SIZE, c.SCREEN_SIZE, title="putanginaaaa", fps=c.FPS)
        px.mouse(True)
        assets.init_assets()
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)
        px.run(self.controller.update, self.controller.draw)


if __name__ == "__main__":
    Game()
