from typing import Protocol

import pyxel as pyx
from . import constants as c
from . import common_types as ct
from . import utils as u


class UpdateHandler(Protocol):
    def update(self) -> None: ...


class DrawHandler(Protocol):
    def draw(self) -> None: ...


class View:
    def start_game(self, update: UpdateHandler, draw: DrawHandler):
        pyx.mouse(True)
        pyx.run(update.update, draw.draw)

    def draw_sprite(self):
        u.bold_text(
            c.WINDOW_CENTER_X,
            0,
            "Hello, Pyxel!",
            font_size=32,
            font_alignment=ct.FontAlign.CENTER,
            color=0,
        )
        print(pyx.colors)
        pyx.rect(100, 100, 32, 32, 31)

    def clear_screen(self):
        pyx.cls(0)
