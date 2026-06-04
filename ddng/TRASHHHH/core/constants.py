import math

# --- CONFIGURATION & CONSTANTS ---
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

FPS = 30
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SCREEN_SIZE = 512
TILE_SIZE = 16
TILE = 16
GRID_COLS = 32
GRID_ROWS = 32
GRID_SIZE = GRID_COLS

SPRITE_ATLAS_TILE = 32
ENEMY_SIZE = 32
TOWER_SIZE = 32
BULLET_RADIUS = 5
SHOOTER_OUTER_RADIUS = 6
SHOOTER_INNER_RADIUS = 3
PATH_THICKNESS = 5
FONT_CHAR_WIDTH = 8
FONT_LINE_HEIGHT = 16

# 6 Colors: Red, Orange, Yellow, Lime, Cyan, Pink
COLORS = [8, 9, 10, 11, 12, 2]

PLAYER_ROF = 0.9
TOWER_ROF = 0.5
BULLET_SPEED_SEC = 5.0
ENEMY_SPEED_SEC = 2.0
TOWER_COST = 5
UPGRADE_COST = 10

DIAGONAL = math.sqrt(SCREEN_SIZE**2 + SCREEN_SIZE**2)
BULLET_SPEED = DIAGONAL / (BULLET_SPEED_SEC * FPS)
PLAYER_COOLDOWN = int(FPS / PLAYER_ROF)
TOWER_COOLDOWN = int(FPS / TOWER_ROF)
ENEMY_MOVE_FRAMES = int(ENEMY_SPEED_SEC * FPS)

SCREEN_CENTER_X = SCREEN_WIDTH // 2
SCREEN_CENTER_Y = SCREEN_HEIGHT // 2


# Path generation (Grid coordinates)
def build_path(corners: list[tuple[int, int]]) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    for i in range(len(corners) - 1):
        x1, y1 = corners[i]
        x2, y2 = corners[i + 1]
        # Skip identical consecutive corners to avoid infinite loops
        if x1 == x2 and y1 == y2:
            if not path or path[-1] != (x1, y1):
                path.append((x1, y1))
            continue

        dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy = 1 if y2 > y1 else -1 if y2 < y1 else 0

        cx, cy = x1, y1
        while (cx, cy) != (x2, y2):
            if not path or path[-1] != (cx, cy):
                path.append((cx, cy))
            cx += dx
            cy += dy
    # Ensure the final corner is included (avoid duplicate)
    if not path or path[-1] != corners[-1]:
        path.append(corners[-1])
    return path


PATHS: list[list[tuple[int, int]]] = [
    build_path([(0, 4), (31, 4), (31, 12), (0, 12)]),  # Path 1
    build_path([(31, 20), (0, 20), (0, 28), (31, 28)]),  # Path 2
]

# Tunnels (grid coordinates: x, y)
TUNNELS: set[tuple[int, int]] = {
    (12, 4),
    (13, 4),
    (14, 4),
    (15, 4),  # Shield on Path 1
    (16, 20),
    (17, 20),
    (18, 20),  # Shield on Path 2
}
