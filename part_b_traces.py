import csv
import re
from contextlib import closing
from pathlib import Path

from gymnasium.wrappers import RenderCollection

from part_b import fixed_policy, make_env, run_episode


def main():
    output = Path("outputs")
    with (output / "frozenlake_episodes.csv").open(encoding="utf-8") as file:
        episodes = [
            row for row in csv.DictReader(file)
            if row["condition"] == "slippery_fixed"
        ]

    for outcome in ("goal", "hole"):
        episode = next(row for row in episodes if row["outcome"] == outcome)
        seed = int(episode["episode_seed"])

        with closing(RenderCollection(make_env(True, render_mode="ansi"))) as env:
            result = run_episode(env, fixed_policy, seed)
            frames = env.render()

        if result["outcome"] != outcome or result["steps"] != int(episode["steps"]):
            raise RuntimeError(f"Replay differs from the CSV for seed {seed}")

        lines = [
            f"Slippery ice | Fixed policy | Seed {seed}",
            f"Outcome: {outcome} | Steps: {result['steps']} | "
            f"Total reward: {result['total_reward']}",
        ]
        for step, frame in enumerate(frames):
            board = re.sub(
                r"\x1b\[[0-9;]*m([SFHG])\x1b\[[0-9;]*m", r"[\1]", frame
            )
            lines.append(f"\nStep {step}\n{board.strip()}")

        path = output / f"frozenlake_{outcome}_trace.txt"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{outcome}: seed {seed}, {result['steps']} steps → {path}")


if __name__ == "__main__":
    main()
