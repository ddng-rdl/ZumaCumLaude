from functools import partial
import json

import math
import pyxel as pyx
from typing import Any

import core.constants as c
import core.common_types as ct


# CONVERSION FUNCTIONS
def secs_to_frames(seconds: float) -> int:
    return int(seconds * c.FPS)


def px_to_tiles(px: float, tile_width: int) -> int:
    return int(px // tile_width)

def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# PARSING/LOADING FILES FUNCTIONS
# ----- Parsing Pathway Coordinates
def _extract_grid_waypoints(
    tmj_data: dict[str, Any],
) -> dict[int, list[tuple[int, int]]]:
    tile_width = tmj_data["tilewidth"]
    tile_height = tmj_data["tileheight"]

    waypoints_layer = None
    for layer in tmj_data["layers"]:
        if layer["class"] == "waypoints":
            waypoints_layer = layer
            break

    if not waypoints_layer:
        return {}

    paths: dict[int, list[tuple[int, int]]] = {}
    for num, obj in enumerate(waypoints_layer["objects"], 1):
        base_x = obj["x"]
        base_y = obj["y"]

        waypoints: list[tuple[int, int]] = []
        for pt in obj["polyline"]:
            abs_x = base_x + pt["x"]
            abs_y = base_y + pt["y"]

            grid_x = int(abs_x // tile_width)
            grid_y = int(abs_y // tile_height)

            waypoints.append((grid_x, grid_y))
        paths[num] = waypoints

    return paths


def _build_path(waypoints: list[tuple[int, int]]) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    for i in range(len(waypoints) - 1):
        x1, y1 = waypoints[i]
        x2, y2 = waypoints[i + 1]

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

    if not path or path[-1] != waypoints[-1]:
        path.append(waypoints[-1])
    return path


def extract_grid_paths(tmj_data: dict[str, Any]) -> dict[int, list[tuple[int, int]]]:
    waypoints_dict = _extract_grid_waypoints(tmj_data)
    paths_dict = {
        num: _build_path(waypoints) for num, waypoints in waypoints_dict.items()
    }
    return paths_dict


# ----- Handling JSON files
def read_json(file_path: str) -> dict[str, Any]:
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def write_json(file_path: str, data: dict[str, Any]) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f)


# FONT FUNCTIONS
def custom_text(
    x: float,
    y: float,
    text: str,
    color: int = pyx.COLOR_WHITE,
    font_size: int = c.FS_P,
    font_alignment: ct.FontAlign = ct.FontAlign.LEFT,
    font: str = c.F_SANS,
):
    custom_font = pyx.Font(font, font_size)
    alignment = custom_font.text_width(text) * font_alignment.value
    pyx.text(x + alignment, y, text, color, custom_font)


centered_text = partial(custom_text, font_alignment=ct.FontAlign.CENTER)
right_aligned_text = partial(custom_text, font_alignment=ct.FontAlign.RIGHT)
bold_text = partial(custom_text, font=c.F_BOLD)
