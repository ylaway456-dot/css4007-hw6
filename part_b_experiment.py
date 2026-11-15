import csv
from collections import Counter
from contextlib import closing
from pathlib import Path
from random import Random
from statistics import mean

from part_b import fixed_policy, make_env, run_episode

BATCH_SEEDS = (11, 22, 33)
EPISODES_PER_BATCH = 50


def save_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    episode_rows = []
    summaries = []

    for slippery in (False, True):
        surface = "slippery" if slippery else "non_slippery"

        for policy_name in ("random", "fixed"):
            with closing(make_env(slippery)) as env:
                for batch_seed in BATCH_SEEDS:
                    batch = []

                    for i in range(EPISODES_PER_BATCH):
                        episode_seed = 1000 * batch_seed + i
                        policy = fixed_policy

                        if policy_name == "random":
                            rng = Random(episode_seed)

                            def policy(state):
                                return rng.randrange(4)

                        result = run_episode(env, policy, episode_seed)
                        batch.append({
                            "condition": f"{surface}_{policy_name}",
                            "batch_seed": batch_seed,
                            "episode_seed": episode_seed,
                            "policy": policy_name,
                            **result,
                        })

                    episode_rows.extend(batch)
                    outcomes = Counter(row["outcome"] for row in batch)
                    summaries.append({
                        "slippery": slippery,
                        "policy": policy_name,
                        "batch_seed": batch_seed,
                        "goals": outcomes["goal"],
                        "holes": outcomes["hole"],
                        "time_limits": outcomes["time limit"],
                        "success_percent": 100 * outcomes["goal"] / len(batch),
                        "mean_steps": round(mean(row["steps"] for row in batch), 2),
                    })

    output = Path("outputs")
    output.mkdir(exist_ok=True)
    save_csv(output / "frozenlake_episodes.csv", episode_rows)
    save_csv(output / "frozenlake_batches.csv", summaries)
    print(f"Saved {len(episode_rows)} episodes and {len(summaries)} batch summaries.")


if __name__ == "__main__":
    main()
