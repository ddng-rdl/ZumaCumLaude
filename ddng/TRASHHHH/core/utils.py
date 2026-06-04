import json
import os
import math
import core.constants as c


def get_distance(x1: float, y1: float, x2: float, y2: float):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_default_settings():
    if not os.path.exists(c.SETTINGS_FILE):
        with open(c.SETTINGS_FILE, "w") as f:
            # e: enemies, l: lives, h: regen tiles, f: chameleon frames
            json.dump({"e": 5, "l": 5, "h": 2, "f": 90}, f)


def load_settings():
    generate_default_settings()
    with open(c.SETTINGS_FILE, "r") as f:
        return json.load(f)


def load_leaderboard() -> dict[str, list[dict[str, str | int]]]:
    if not os.path.exists(c.LEADERBOARD_FILE):
        return {"Campaign": [], "Endless": []}
    with open(c.LEADERBOARD_FILE, "r") as f:
        return json.load(f)


def save_leaderboard(lb: dict[str, list[dict[str, str | int]]]):
    with open(c.LEADERBOARD_FILE, "w") as f:
        json.dump(lb, f)
