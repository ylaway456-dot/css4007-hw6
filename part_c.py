import json
from math import isclose
from pathlib import Path

RULES = json.loads(Path("data/maps.json").read_text(encoding="utf-8"))
TILES = RULES["tiles"]
ACTIONS = tuple(RULES["actions"])
DELTAS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def transitions(grid, state, action):
    row, col = state
    tile = TILES[grid[row][col]]

    if tile.get("terminal", False):
        return []

    direction = ACTIONS.index(action)
    moves = [(direction, 1.0)]

    if tile["movement"] == "slippery":
        moves = [
            (direction, tile["intended"]),
            ((direction - 1) % 4, tile["perpendicular_each"]),
            ((direction + 1) % 4, tile["perpendicular_each"]),
        ]

    outcomes = []
    for move, probability in moves:
        dr, dc = DELTAS[move]
        nr, nc = row + dr, col + dc

        if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
            nr, nc = state
        elif not TILES[grid[nr][nc]].get("traversable", True):
            nr, nc = state

        reward = TILES[grid[nr][nc]]["reward"]
        outcomes.append((probability, (nr, nc), reward))

    return outcomes


def check_rules():
    paper = RULES["paper_map"]
    extended = RULES["extended_map"]

    assert transitions(paper, (0, 1), "up") == [(1.0, (0, 1), -3)]
    assert transitions(paper, (0, 1), "down") == [(1.0, (0, 1), -3)]
    print("Boundary and wall: stay in mud, reward -3.")

    ice = transitions(paper, (1, 2), "up")
    assert ice == [(0.8, (0, 2), -1), (0.1, (1, 2), -1), (0.1, (1, 3), -10)]
    for action in ACTIONS:
        assert isclose(sum(p for p, _, _ in transitions(paper, (1, 2), action)), 1.0)
    print("Ice, action up:", ice)
    print("The probabilities sum to 1 for every action on ice.")

    for grid, state, action, reward in [
        (paper, (0, 0), "right", -3),
        (extended, (2, 0), "right", -2),
        (extended, (2, 2), "right", -5),
    ]:
        assert transitions(grid, state, action)[0][2] == reward
    print("Entering mud, sand, and water gives -3, -2, and -5.")

    assert transitions(paper, (0, 2), "right") == [(1.0, (0, 3), 10)]
    for terminal in ((0, 3), (1, 3)):
        for action in ACTIONS:
            assert transitions(paper, terminal, action) == []
    print("Goal entry gives +10. No transitions or rewards after goal or hole.")


if __name__ == "__main__":
    check_rules()
