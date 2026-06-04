from __future__ import annotations
import pyxel as px

from core.model import Model, GameState
from core.view import View


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view

    def update(self) -> None:
        self._model.aim(px.mouse_x, px.mouse_y)

        if self._model.state == GameState.PLAYING:
            if px.btnp(px.MOUSE_BUTTON_LEFT):
                self._model.fire()

    def draw(self) -> None:
        self._view.draw()