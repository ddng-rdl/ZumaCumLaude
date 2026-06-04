from enum import Enum, StrEnum, auto


class BasicColors(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    VIOLET = auto()


class FontAlign(Enum):
    LEFT = 0
    CENTER = -0.5
    RIGHT = -1


class GameState(StrEnum):
    MAIN_MENU = auto()
    IN_GAME = auto()
    GAME_OVER = auto()


class EnemyState(StrEnum):
    HIT = auto()
    KILLED = auto()
    HIDDEN = auto()


class Direction(StrEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
