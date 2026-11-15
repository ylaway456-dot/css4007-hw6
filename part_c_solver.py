from part_c import ACTIONS, RULES, TILES, transitions

DISCOUNT = RULES["discount"]


def is_nonterminal(tile):
    rule = TILES[tile]
    return rule.get("traversable", True) and not rule.get("terminal", False)


def initial_values(grid):
    return {
        (row, col): RULES["initial_value"]
        for row, tiles in enumerate(grid)
        for col, tile in enumerate(tiles)
        if TILES[tile].get("traversable", True)
    }


def action_value(grid, state, action, values):
    return sum(
        probability * (reward + DISCOUNT * values[next_state])
        for probability, next_state, reward in transitions(grid, state, action)
    )


def update_values(grid, values):
    updated = {}

    for row, col in values:
        state = (row, col)
        if is_nonterminal(grid[row][col]):
            updated[state] = max(
                action_value(grid, state, action, values)
                for action in ACTIONS
            )
        else:
            updated[state] = RULES["terminal_value"]

    return updated


def print_values(grid, values):
    for row, tiles in enumerate(grid):
        print("".join(
            f"{values[row, col]:8.2f}" if (row, col) in values else f"{'#':>8}"
            for col, _ in enumerate(tiles)
        ))


def main():
    grid = RULES["paper_map"]
    v0 = initial_values(grid)
    v1 = update_values(grid, v0)
    v2 = update_values(grid, v1)

    print("V1 — original map")
    print_values(grid, v1)

    print("\nV2 — requested states (row, column)")
    for row, col in RULES["paper_v2_positions"]:
        print(f"V2({row},{col}) = {v2[row - 1, col - 1]:.2f}")

    ice_down = action_value(grid, (1, 2), "down", v0)
    print(f"\nV1 check — ice (2,3), action down: {ice_down:.2f}")


if __name__ == "__main__":
    main()
