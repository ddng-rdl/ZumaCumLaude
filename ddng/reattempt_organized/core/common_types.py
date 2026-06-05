from enum import Enum, IntEnum, StrEnum, auto


class BasicColors(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    BLUE = auto()
    VIOLET = auto()


class AllColors(IntEnum):
    TRANSPARENT = 0
    BLACK = 1
    WHITE = 2
    RED_DARKEST = 3
    RED_DARK = 4
    RED = 5
    RED_LIGHT = 6
    RED_ORANGE = 7
    ORANGE_DARKEST = 8
    ORANGE_DARK = 9
    ORANGE = 10
    ORANGE_LIGHT = 11
    ORANGE_YELLOW = 12
    YELLOW_DARKEST = 13
    YELLOW_DARK = 14
    YELLOW = 15
    YELLOW_LIGHT = 16
    YELLOW_GREEN = 17
    GREEN_DARKEST = 18
    GREEN_DARK = 19
    GREEN = 20
    GREEN_LIGHT = 21
    GREEN_BLUE = 22
    BLUE_DARKEST = 23
    BLUE_DARK = 24
    BLUE = 25
    BLUE_LIGHT = 26
    BLUE_VIOLET = 27
    VIOLET_DARKEST = 28
    VIOLET_DARK = 29
    VIOLET = 30
    VIOLET_LIGHT = 31
    GRAY_DARKEST = 32
    GRAY_DARK = 33
    GRAY = 34
    GRAY_LIGHT = 35


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
