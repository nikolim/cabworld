from gym.envs.registration import register

register(id='Cabworld', entry_point='gym_cabworld.envs:CustomEnv',
         max_episode_steps=2000)
