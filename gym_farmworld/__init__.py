from gym.envs.registration import register

register(
    id="Farmworld-v0",
    entry_point="gym_farmworld.envs:CustomEnv0",
    max_episode_steps=1000,
)

register(
    id="Farmworld-v1",
    entry_point="gym_farmworld.envs:CustomEnv1",
    max_episode_steps=1000,
)

register(
    id="Farmworld-v2",
    entry_point="gym_farmworld.envs:CustomEnv2",
    max_episode_steps=1000,
)

register(
    id="Farmworld-v3",
    entry_point="gym_farmworld.envs:CustomEnv3",
    max_episode_steps=1000,
)
