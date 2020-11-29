from gym.envs.registration import register

register(id='Cabworld-v0',
         entry_point='gym_cabworld.envs:CustomEnv',
         max_episode_steps=3000,)

register(id='Cabworld-v1',
         entry_point='gym_cabworld.envs:CustomEnv1',
         max_episode_steps=3000,)

register(id='Cabworld-v2',
         entry_point='gym_cabworld.envs:CustomEnv2',
         max_episode_steps=3000,)

register(id='Cabworld-v3',
         entry_point='gym_cabworld.envs:MarlEnv',
         max_episode_steps=3000,)
