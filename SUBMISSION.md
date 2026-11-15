# HW6 submission

## AI-use declaration

Which tools did you use, and for what?

## Setup and reproduction

Record dependency versions, installation commands and exact run commands.

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

Show V1 and the requested V2 values. Explain discrepancies.

### Values, policies and convergence

Link both value/policy maps. Record iteration counts, final value changes and tie-breaking rule.

### Simulation results

| Map | Batch seed | Goals /50 | Holes /50 | Time limits /50 | Mean steps | Mean discounted return |
| --- | --- | --- | --- | --- | --- | --- |

### Explain your results

Which values/actions changed with sand and water? Where did cost and risk matter? How do simulations relate to the computed values?

### Rule checks

Show boundary/wall behavior, slip probabilities, floor rewards and terminal handling.

