import pyxel as px

import core.constants as c
from core.model import Model
from core.view import View
from core.controller import Controller


class Game:
    def __init__(self):
        px.init(c.WINDOW_WIDTH, c.WINDOW_HEIGHT, title="Zuma TD", fps=c.FPS)
        px.mouse(True)

        self._model = Model()
        self._view = View(self._model)
        self._controller = Controller(self._model, self._view)

    def run(self) -> None:
        px.run(self._update, self._draw)

    def _update(self) -> None:
        self._model.update()
        self._controller.update()

    def _draw(self) -> None:
        self._controller.draw()


if __name__ == "__main__":
    Game().run()