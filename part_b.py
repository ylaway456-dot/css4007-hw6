import gymnasium as gym

LEFT, DOWN, RIGHT, UP = 0, 1, 2, 3
MAX_STEPS = 100

FIXED_ACTIONS = {
    0: DOWN,  1: RIGHT,  2: DOWN,  3: LEFT,
    4: DOWN,  6: DOWN,
    8: RIGHT, 9: DOWN,  10: DOWN,
    13: RIGHT, 14: RIGHT,
}


def make_env(slippery, render_mode=None):
    return gym.make(
        "FrozenLake-v1",
        map_name="4x4",
        is_slippery=slippery,
        render_mode=render_mode,
        max_episode_steps=MAX_STEPS,
    )


def fixed_policy(state):
    return FIXED_ACTIONS[state]


def run_episode(env, policy, episode_seed):
    state, _ = env.reset(seed=episode_seed)
    total_reward = 0
    outcome = "time limit"

    for steps in range(1, MAX_STEPS + 1):
        action = policy(state)
        state, reward, terminated, truncated, _ = env.step(action)
        total_reward += reward

        if terminated:
            final_tile = env.unwrapped.desc.ravel()[state]
            outcome = {b"G": "goal", b"H": "hole"}[final_tile]
            break

        if truncated:
            break

    return {
        "steps": steps,
        "total_reward": total_reward,
        "outcome": outcome,
    }
