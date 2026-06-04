from __future__ import annotations
from enum import Enum, auto
import math

import utils as u

# CLASS ENUMS FOR SORTING LANG
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Color(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    VIOLET = auto()


# GAME DEETS FROM DODONGOAT
FPS = 30
# GAME_TITLE = "tite"

PLAY_AREA_WIDTH_PX = 512
PLAY_AREA_HEIGHT_PX = 512
GRID_TILE_SIZE = 32
TILE_SIZE_PX = 16
# SIDEBAR_WIDTH = 0

SPRITES_PATH = "assets/sprite/"
AUDIO_PATH = "assets/audio/"
FONT_PATH = "assets/font/"

WINDOW_WIDTH = PLAY_AREA_WIDTH_PX # + SIDEBAR_WIDTH
WINDOW_HEIGHT = PLAY_AREA_WIDTH_PX

FONT_CHAR_WIDTH = 24
DIAGONAL = math.sqrt(WINDOW_WIDTH**2 + WINDOW_HEIGHT**2)


# PATHS
PATH_1: list[tuple[int, int]] = u.build_path([
                                             (0,  4),
                                             (8,  4),
                                             (8,  12),
                                             (15, 12),
                                            ])