import core.constants as c
import core.utils as u
from core.model import Model
from core.view import View
import core.assets_loader as al


class Controller:
    def __init__(self, model: Model, view: View):
        self.__model = model
        self.__view = view

    def start_game(self):
        al.load_assets()
        self.__view.start_game(self, self)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        self.__view.clear_screen()

        self.__view.draw_sprite()
