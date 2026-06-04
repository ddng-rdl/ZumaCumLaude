import json
import math

import core.constants as c

from typing import Any

# JASON STUFF
def load_json(path: str) -> Any:
    with open(path) as f:
        return json.load(f)

def save_json(path: str, data: Any) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# FOR PATH LOGICS
def build_path(corners: list[tuple[int, int]]) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    for i in range(len(corners) - 1):
        x1, y1 = corners[i]
        x2, y2 = corners[i + 1]

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

    if not path or path[-1] != corners[-1]:
        path.append(corners[-1])
    return path