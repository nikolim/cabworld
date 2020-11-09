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
        # Extract possible moves from state
        possible_moves = [index for index, element in enumerate(state) if element == 1]
        # check if pickup is possible
        if state[3] == 1:
            move = 3
        # check if drop-off is possible
        elif state[4] == 1: 
            move = 4
        else: 
            # if no pick-up or drop-off possible move randomly
            move = random.choice(possible_moves)
        state, reward, is_done, info = env.step(move)
        env.render()
        time.sleep(0.05)
        if is_done: 
            print("Done")