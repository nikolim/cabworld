"""
Demo of the environment with Random Policy
"""

import random
import time
import gym 
import gym_cabworld 

env = gym.make('Cabworld-v0')
env.reset()

# initial random step
state, reward, is_done, info = env.step(0)

while not is_done: 
    possible_moves = [index for index, element in enumerate(state) if element == 1]
    # check if pickup is possible
    if state[3] == 1:
        move = 3
        print("pick up passenger")
    # check if drop-off is possible
    elif state[4] == 1: 
        move = 4
        print("drop off passenger")
    else: 
        move = random.choice(possible_moves)
    state, reward, is_done, info = env.step(move)
    #print(state)
    env.render()
    time.sleep(0.01)
    if is_done: 
        print("Done")
