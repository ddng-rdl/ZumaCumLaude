from random import Random

from entities.factory import EntityFactory
import pyxel as px

from core.model import Model
from core.controller import Controller
from core.view import View
import core.constants as c


random = Random()
entity_factory = EntityFactory(random)

if __name__ == "__main__":
    px.init(
        c.WINDOW_WIDTH,
        c.WINDOW_HEIGHT,
        fps=c.FPS,
        quit_key=px.KEY_F1,
        title=c.GAME_TITLE,
    )
    model = Model(entity_factory, random)
    view = View()
    controller = Controller(model, view)
    controller.start_game()
