"""
Demo of the environment with Random Policy
"""

import random
import time
import gym 
import gym_cabworld 

env = gym.make('Cabworld-v0')
n_episodes = 10

for episode in range(n_episodes):
    env.reset()
    state, reward, is_done, info = env.step(0)
    while not is_done: 
        move = random.choice(list(range(5)))
        state, reward, is_done, info = env.step(move)
        env.render()
        time.sleep(0.05)
        if is_done: 
            print("Done")
