import csv
from collections import Counter
from pathlib import Path
from random import Random
from statistics import mean

from part_c import RULES, transitions
from part_c_convergence import extract_policy, solve
from part_c_solver import DISCOUNT

SIMULATION = RULES["simulation"]


def run_episode(grid, start, policy, episode_seed):
    rng = Random(episode_seed)
    state = start
    discounted_return = 0.0
    weight = 1.0
    outcome = "time limit"

    for steps in range(1, SIMULATION["max_steps"] + 1):
        outcomes = transitions(grid, state, policy[state])
        probabilities = [probability for probability, _, _ in outcomes]
        _, state, reward = rng.choices(outcomes, weights=probabilities, k=1)[0]

        discounted_return += weight * reward
        weight *= DISCOUNT

        row, col = state
        tile = grid[row][col]
        if tile in ("G", "H"):
            outcome = "goal" if tile == "G" else "hole"
            break

    return {
        "steps": steps,
        "discounted_return": discounted_return,
        "outcome": outcome,
    }


def save_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    output = Path("outputs")
    output.mkdir(exist_ok=True)
    episodes = []
    summaries = []

    for name, key in (("original", "paper_map"), ("extended", "extended_map")):
        grid = RULES[key]
        values, _, _, converged = solve(grid)
        if not converged:
            raise RuntimeError(f"The solver did not converge for the {name} map.")

        policy = extract_policy(grid, values)
        start = next(
            (row, tiles.index("S"))
            for row, tiles in enumerate(grid)
            if "S" in tiles
        )

        for batch_seed in SIMULATION["batch_seeds"]:
            batch = []
            for i in range(SIMULATION["episodes_per_batch"]):
                episode_seed = 1000 * batch_seed + i
                batch.append({
                    "map": name,
                    "batch_seed": batch_seed,
                    "episode_seed": episode_seed,
                    **run_episode(grid, start, policy, episode_seed),
                })

            episodes.extend(batch)
            counts = Counter(episode["outcome"] for episode in batch)
            summaries.append({
                "map": name,
                "batch_seed": batch_seed,
                "goals": counts["goal"],
                "holes": counts["hole"],
                "time_limits": counts["time limit"],
                "mean_steps": round(mean(episode["steps"] for episode in batch), 2),
                "mean_discounted_return": round(
                    mean(episode["discounted_return"] for episode in batch), 6
                ),
            })

    save_csv(output / "gridworld_episodes.csv", episodes)
    save_csv(output / "gridworld_batches.csv", summaries)
    print(f"Saved {len(episodes)} episodes and {len(summaries)} summaries.")


if __name__ == "__main__":
    main()
