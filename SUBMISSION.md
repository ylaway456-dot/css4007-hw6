# HW6 submission

## AI-use declaration

I used ChatGPT to understand the assignment requirements and to learn how the Python code works. It also helped me write and debug the code.

## Setup and reproduction

### Part B setup

Tested in Google Colab with Python 3.13.18, Gymnasium 1.3.0, and NumPy 2.5.4.

```bash
python -m venv --without-pip .venv
python -m pip --python .venv install gymnasium==1.3.0 numpy==2.5.4
.venv/bin/python part_b_experiment.py
.venv/bin/python part_b_traces.py
```
### Part C setup

Part C uses the Python standard library and the provided `data/maps.json`.
Run these commands from the repository root.

```bash
mkdir -p outputs
python part_c.py | tee outputs/gridworld_rule_checks.txt
python part_c_solver.py | tee outputs/gridworld_paper_comparison.txt
python part_c_convergence.py
python part_c_simulation.py
```
## Part A — Paper calculations

[Part A handwritten calculations](part-a.pdf)

## Part B — FrozenLake

### Fixed policy

I chose one action for each nonterminal state before running the experiments.
I used the same policy with and without slipping. The arrows follow short
routes that avoid holes when slipping is off.

| | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Row 1 | 0 ↓ (Start) | 1 → | 2 ↓ | 3 ← |
| Row 2 | 4 ↓ | 5 (Hole) | 6 ↓ | 7 (Hole) |
| Row 3 | 8 → | 9 ↓ | 10 ↓ | 11 (Hole) |
| Row 4 | 12 (Hole) | 13 → | 14 → | 15 (Goal) |

### Results

| Slippery? | Policy | Batch seed | Goals /50 | Holes /50 | Time limits /50 | Success % | Mean steps |
|---|---|---:|---:|---:|---:|---:|---:|
| No | Random | 11 | 0 | 50 | 0 | 0 | 8.14 |
| No | Random | 22 | 1 | 49 | 0 | 2 | 7.56 |
| No | Random | 33 | 0 | 50 | 0 | 0 | 6.88 |
| No | Fixed | 11 | 50 | 0 | 0 | 100 | 6.00 |
| No | Fixed | 22 | 50 | 0 | 0 | 100 | 6.00 |
| No | Fixed | 33 | 50 | 0 | 0 | 100 | 6.00 |
| Yes | Random | 11 | 0 | 50 | 0 | 0 | 8.06 |
| Yes | Random | 22 | 0 | 50 | 0 | 0 | 7.60 |
| Yes | Random | 33 | 0 | 50 | 0 | 0 | 7.98 |
| Yes | Fixed | 11 | 1 | 49 | 0 | 2 | 4.24 |
| Yes | Fixed | 22 | 2 | 48 | 0 | 4 | 5.48 |
| Yes | Fixed | 33 | 1 | 49 | 0 | 2 | 4.44 |

Without slipping, the fixed policy reached the goal in all 150 episodes.
Every run took 6 steps. With slipping, the agent could move sideways into
a hole. The fixed policy reached the goal only 4 times out of 150, with
1, 2, and 1 successes in the three batches. Its mean episode length fell
because many runs ended early in a hole.

The random policy reached the goal once without slipping and zero times
with slipping. None of the 600 episodes reached the time limit. A single
successful run shows that reaching the goal is possible. Repeated runs
show how often it happened under each condition.

These experiments evaluate the two policies. Both keep the same rules
throughout the runs, so there is no training.

- [All 600 episodes](outputs/frozenlake_episodes.csv)
- [All 12 batch summaries](outputs/frozenlake_batches.csv)
- [Successful episode on slippery ice](outputs/frozenlake_goal_trace.txt)
- [Failed episode on slippery ice](outputs/frozenlake_hole_trace.txt)
## Part C — Custom solver

### Compare code with paper

The V1 map gives 10 at (1,3) and −1 at every other nonterminal state.
The requested V2 values are 8.00 at (1,2), 10.00 at (1,3), and 5.21 at (2,3).

For the first update on ice, the action value for Down is
0.8 × (−1) + 0.1 × (−1) + 0.1 × (−10) = −1.90.
The best first-round action is Left, so V1(2,3) = −1.00.

[Full V1 map and V2 comparison](outputs/gridworld_paper_comparison.txt)

### Values, policies and convergence

| Map | Iterations | Final maximum change | Value at start | First action |
|---|---:|---:|---:|---|
| Original | 12 | 2.165e−7 | 1.54 | Right |
| Extended | 11 | 2.406e−7 | 1.50 | Up |

Both maps converged below 0.000001. For equal action values, I choose
the first action in this order: up, right, down, left.

- [Original value and policy maps](outputs/gridworld_original_solution.txt)
- [Extended value and policy maps](outputs/gridworld_extended_solution.txt)

### Simulation results

| Map | Batch seed | Goals /50 | Holes /50 | Time limits /50 | Mean steps | Mean discounted return |
|---|---:|---:|---:|---:|---:|---:|
| Original | 11 | 42 | 8 | 0 | 4.98 | 0.891260 |
| Original | 22 | 46 | 4 | 0 | 5.04 | 1.914776 |
| Original | 33 | 48 | 2 | 0 | 5.04 | 2.492144 |
| Extended | 11 | 50 | 0 | 0 | 5.00 | 1.502000 |
| Extended | 22 | 50 | 0 | 0 | 5.00 | 1.502000 |
| Extended | 33 | 50 | 0 | 0 | 5.00 | 1.502000 |

- [All 300 episodes](outputs/gridworld_episodes.csv)
- [All six batch summaries](outputs/gridworld_batches.csv)

### Explain your results

At two decimal places, only the start value changed, from 1.54 to 1.50.
The only policy arrow that changed was at the start, from Right to Up.
Entering sand costs −2 instead of −1, so the upper route becomes better
from the start. Entering water costs −5, which makes the move into the
bottom-right cell less attractive. The policy already avoided that move.

At the ice cell, both policies choose Up. This action moves toward the
goal with probability 0.8, stays on the ice with probability 0.1 because
of the wall, and slips into the hole with probability 0.1. The original
route from the start reaches the ice. The extended route goes around it,
and all 150 extended-map episodes end at the goal in five steps.

The value at the start estimates the expected discounted return with
no fixed step limit. Each batch average comes from 50 sampled episodes
with a 100-step limit. No episode reached that limit in these runs.
The original-map batch means vary because the number of falls varies.
The extended-map route is deterministic, so every run gives 1.502.

### Rule checks

I checked blocked moves at a wall and a boundary, ice probabilities,
mud, sand and water rewards, and the end of rewards after a terminal state.

[Saved rule checks](outputs/gridworld_rule_checks.txt)
