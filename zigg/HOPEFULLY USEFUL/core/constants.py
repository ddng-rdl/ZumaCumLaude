from __future__ import annotations
import math

FPS = 30
GAME_TITLE = "ZumaTD (Phase #4)"

PLAY_AREA_WIDTH_PX = 256
PLAY_AREA_HEIGHT_PX = 256
SIDEBAR_WIDTH = 0
GRID_SIZE = 16
TILE_SIZE_PX = 16

SPRITES_PATH = "assets/sprite/"
AUDIO_PATH = "assets/audio/"
FONT_PATH = "assets/font/"
SETTINGS_PATH = "core/settings.json"

WINDOW_WIDTH = PLAY_AREA_WIDTH_PX + SIDEBAR_WIDTH
WINDOW_HEIGHT = PLAY_AREA_HEIGHT_PX

WINDOW_CENTER_X = WINDOW_WIDTH // 2
WINDOW_CENTER_Y = WINDOW_HEIGHT // 2

PLAY_AREA_CENTER_X = PLAY_AREA_WIDTH_PX // 2
PLAY_AREA_CENTER_Y = PLAY_AREA_HEIGHT_PX // 2

F_SANS = FONT_PATH + "PixeloidSans.ttf"
F_BOLD = FONT_PATH + "PixeloidSansBold.ttf"
F_MONO = FONT_PATH + "PixeloidSansMono.ttf"

FS_P = 12
FS_H1 = 24
FS_H2 = 20


DIAGONAL = math.sqrt(WINDOW_WIDTH**2 + WINDOW_HEIGHT**2)


ENEMY_SPEED_SEC = 2.0
TOWER_ROF = 0.5
PLAYER_ROF = 0.9

ENEMY_MOVE_FRAMES = int(ENEMY_SPEED_SEC * FPS)  # 2.0 * 30 = 60 frames
TOWER_COOLDOWN = int(FPS / TOWER_ROF)           # 30 / 0.5 = 60 frames


BULLET_SPEED_SEC = 5.0
BULLET_SPEED = DIAGONAL / (BULLET_SPEED_SEC * FPS)  # pixels per frame