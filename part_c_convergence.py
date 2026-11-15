from contextlib import redirect_stdout
from pathlib import Path

from part_c import ACTIONS, RULES
from part_c_solver import (
    action_value,
    initial_values,
    is_nonterminal,
    print_values,
    update_values,
)

TOLERANCE = RULES["solver"]["tolerance"]
MAX_ITERATIONS = RULES["solver"]["max_iterations"]
ARROWS = {"up": "↑", "right": "→", "down": "↓", "left": "←"}


def solve(grid):
    values = initial_values(grid)

    for iteration in range(1, MAX_ITERATIONS + 1):
        updated = update_values(grid, values)
        change = max(abs(updated[state] - values[state]) for state in values)
        values = updated

        if change < TOLERANCE:
            return values, iteration, change, True

    return values, iteration, change, False


def extract_policy(grid, values):
    policy = {}

    for row, col in values:
        if is_nonterminal(grid[row][col]):
            state = (row, col)
            policy[state] = max(
                ACTIONS,
                key=lambda action: action_value(grid, state, action, values),
            )

    return policy


def print_solution(grid, name):
    values, iterations, change, converged = solve(grid)
    print(f"Map: {name}")
    print(f"Iterations: {iterations}")
    print(f"Final change: {change:.3e}")

    if not converged:
        print("Did not converge within the iteration limit.")
        return

    print("\nFinal values")
    print_values(grid, values)

    policy = extract_policy(grid, values)
    print("\nPolicy (ties: up, right, down, left)")
    for row, tiles in enumerate(grid):
        print("  ".join(
            ARROWS[policy[row, col]] if (row, col) in policy else tile
            for col, tile in enumerate(tiles)
        ))


def main():
    output = Path("outputs")
    output.mkdir(exist_ok=True)

    for name, map_key in (("original", "paper_map"), ("extended", "extended_map")):
        path = output / f"gridworld_{name}_solution.txt"
        with path.open("w", encoding="utf-8") as file, redirect_stdout(file):
            print_solution(RULES[map_key], name)
        print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
